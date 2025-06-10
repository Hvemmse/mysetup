#!/usr/bin/env python3
# pystrsmer.py - GUI-baseret radioafspiller med mpv og sanginfo
# Frank @ simens.dk

import tkinter as tk
from tkinter import messagebox
import subprocess
import signal
import os
import sys
import json
import threading
import time
import socket
import select

# Liste over radiostationer
stations = {
    "NDR 2": "https://www.ndr.de/resources/metadaten/audio/m3u/ndr2_sh.m3u",
    "P4 Østjylland": "http://live-icy.gss.dr.dk:8000/A/A14L.mp3",
    "Radio Soft": "https://live-bauerdk.sharp-stream.com/radiosoft_dk_mp3",
    "GoFM": "http://stream1.webfm.dk/Webfm",
    "Eins Live": "http://www.wdr.de/wdrlive/media/einslive.m3u",
    "Radio 100": "https://live-bauerdk.sharp-stream.com/radio100_dk_mp3",
}

# Globale variabler
current_process = None
mpv_ipc_socket_path = "/tmp/mpv-radio-ipc"
mpv_ipc_thread = None
mpv_stdout_thread = None
ipc_thread_running = False

current_playing_text = None
current_song_info_text = None
ipc_request_id_counter = 0

# --- Helper function for GUI updates (must be on main thread) ---
def update_song_info_on_gui(text):
    """Updates the song info Tkinter StringVar on the main thread."""
    global current_song_info_text
    if current_song_info_text:
        current_song_info_text.set(text)

# --- Funktioner til mpv-kontrol ---

def stop_mpv():
    """Stopper den nuværende mpv-proces og rydder op."""
    global current_process, mpv_ipc_thread, mpv_stdout_thread, ipc_thread_running
    
    # Signalér IPC- og stdout-trådene om at stoppe og vent på dem
    if ipc_thread_running:
        ipc_thread_running = False
        if mpv_ipc_thread and mpv_ipc_thread.is_alive():
            # print("[Stop] Venter på IPC-tråd lukker...") # DEBUG
            mpv_ipc_thread.join(timeout=1) 
            # if mpv_ipc_thread.is_alive():
            #     print("[Stop] IPC-tråd svarede ikke, fortsætter...") # DEBUG
        mpv_ipc_thread = None

        if mpv_stdout_thread and mpv_stdout_thread.is_alive():
            # print("[Stop] Venter på stdout-tråd lukker...") # DEBUG
            mpv_stdout_thread.join(timeout=1)
            # if mpv_stdout_thread.is_alive():
            #     print("[Stop] Stdout-tråd svarede ikke, fortsætter...") # DEBUG
        mpv_stdout_thread = None

    if current_process and current_process.poll() is None:
        try:
            # print("[Stop] Stopper mpv...") # DEBUG
            # Send SIGTERM til procesgruppen for at stoppe mpv og dets underprocesser
            if current_process.pid:
                os.killpg(os.getpgid(current_process.pid), signal.SIGTERM)
            current_process.wait(timeout=2)
            # print("[Stop] mpv er stoppet.") # DEBUG
        except subprocess.TimeoutExpired:
            # print("[Stop] mpv svarer ikke, dræder proces...") # DEBUG
            if current_process.pid:
                os.killpg(os.getpgid(current_process.pid), signal.SIGKILL)
            current_process.wait()
            # print("[Stop] mpv er dræbt.") # DEBUG
        except Exception as e:
            print(f"Fejl ved stop af mpv: {e}") # Keep critical errors

    current_process = None
    
    # Ryd displayet
    if current_playing_text:
        current_playing_text.set("Ingen station afspiller")
    root.after(0, update_song_info_on_gui, "") # Clear song info

    # Ryd IPC socket-filen, hvis den findes
    if os.path.exists(mpv_ipc_socket_path):
        try:
            os.remove(mpv_ipc_socket_path)
            # print(f"[Stop] Slettet IPC socket fil: {mpv_ipc_socket_path}") # DEBUG
        except OSError as e:
            print(f"Fejl ved sletning af IPC socket fil: {e}") # Keep critical errors

# Funktion til at læse mpv's standard output for sanginfo
def read_mpv_stdout():
    """Læser mpv's standard output for sanginfo."""
    global current_process
    
    last_song_info_stdout = "" 

    # print("[Stdout Debug] mpv stdout læse-tråd startet.") # DEBUG
    while ipc_thread_running and current_process and current_process.poll() is None:
        try:
            line = current_process.stdout.readline().decode('utf-8').strip()
            if line:
                # print(f"[Stdout Debug] Rå mpv linje: {line}") # DEBUG (very verbose)

                new_song_info_from_this_line = ""

                if "icy-title:" in line:
                    try:
                        song_info_part = line.split("icy-title: ", 1)[1].strip()
                        new_song_info_from_this_line = f"Sang: {song_info_part}"
                        # print(f"[Stdout Debug] Fundet 'icy-title': {new_song_info_from_this_line}") # DEBUG
                    except IndexError:
                        # print("[Stdout Debug] Kunne ikke parse 'icy-title' fra linje.") # DEBUG
                        pass
                elif "media-title:" in line:
                    try:
                        song_info_part = line.split("media-title: ", 1)[1].strip()
                        new_song_info_from_this_line = f"Titel: {song_info_part}"
                        # print(f"[Stdout Debug] Fundet 'media-title': {new_song_info_from_this_line}") # DEBUG
                    except IndexError:
                        # print("[Stdout Debug] Kunne ikke parse 'media-title' fra linje.") # DEBUG
                        pass
                
                if new_song_info_from_this_line and new_song_info_from_this_line != last_song_info_stdout:
                    root.after(0, update_song_info_on_gui, new_song_info_from_this_line)
                    last_song_info_stdout = new_song_info_from_this_line
                    # print(f"[Stdout Debug] GUI opdatering SKEDULET fra stdout: {new_song_info_from_this_line}") # DEBUG

            else:
                time.sleep(0.05) 
        except ValueError: 
            # print("[Stdout Debug] mpv stdout er lukket.") # DEBUG
            break
        except Exception as e:
            print(f"Fejl ved læsning af mpv stdout: {e}") # Keep critical errors
            break
    # print("[Stdout Debug] mpv stdout læse-tråd afsluttet.") # DEBUG


# Funktion til at læse fra mpv's IPC socket (simplified, no longer for song info)
def read_mpv_ipc():
    """Læser JSON-data fra mpv's IPC socket i en separat tråd."""
    global current_song_info_text, ipc_thread_running, ipc_request_id_counter

    # print("[IPC Debug] IPC læse-tråd startet.") # DEBUG

    mpv_socket = None
    max_socket_connect_retries = 20 
    socket_connect_delay = 0.2 
    
    for i in range(max_socket_connect_retries):
        if not ipc_thread_running:
            # print("[IPC Debug] IPC læse-tråd stoppet under opstart (retry loop).") # DEBUG
            return
        
        try:
            mpv_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            mpv_socket.settimeout(0.5) 
            mpv_socket.connect(mpv_ipc_socket_path)
            # print(f"[IPC Debug] IPC socket fundet og forbundet efter {i+1} forsøg.") # DEBUG
            break 
        except (socket.error, FileNotFoundError) as e:
            mpv_socket = None 
            # print(f"[IPC Debug] Venter på mpv IPC socket... Forsøg {i+1}/{max_socket_connect_retries} ({e})") # DEBUG
            time.sleep(socket_connect_delay)
    else: 
        print(f"FEJL: mpv IPC socket blev ikke fundet eller forbundet inden for tidsfristen: {mpv_ipc_socket_path}") # Keep critical errors
        root.after(0, update_song_info_on_gui, "FEJL: IPC fejl (ingen kontrol)") 
        ipc_thread_running = False
        return 
    
    mpv_socket.setblocking(False) 
    
    # print("[IPC Debug] IPC Connected. Now idling, stdout thread handles song info.") # DEBUG
    while ipc_thread_running and mpv_socket:
        try:
            readable, _, _ = select.select([mpv_socket], [], [], 0.1) 
            if readable:
                data = mpv_socket.recv(4096)
                if not data: 
                    # print("[IPC Debug] mpv lukkede IPC socket.") # DEBUG
                    break
            else:
                time.sleep(0.5) 

        except (socket.timeout, BlockingIOError) as e: 
            # print(f"[IPC Debug] Socket timeout/BlockingIOError (forventet): {e}") # DEBUG (very verbose)
            pass 
        except socket.error as e:
            print(f"Kritisk IPC socket fejl: {e}, stopper læsning.") # Keep critical errors
            ipc_thread_running = False
            break
        except Exception as e:
            print(f"Generel fejl i read_mpv_ipc: {e}") # Keep critical errors
            time.sleep(3) 
            
    if mpv_socket:
        mpv_socket.close() 
    # print("[IPC Debug] IPC læse-tråd afsluttet.") # DEBUG


# --- Funktion til at starte mpv ---

def start_mpv(name, url):
    """Starter mpv-processen og en IPC-læse-tråd."""
    global current_process, mpv_ipc_thread, mpv_stdout_thread, ipc_thread_running
    
    stop_mpv() 
    
    if os.path.exists(mpv_ipc_socket_path):
        try:
            os.remove(mpv_ipc_socket_path)
            # print(f"[Start] Rydde op i gammel socket fil: {mpv_ipc_socket_path}") # DEBUG
        except OSError as e:
            print(f"Kunne ikke slette gammel IPC socket fil: {e}") # Keep critical errors

    if current_playing_text:
        current_playing_text.set(f"Afspiller: {name}")
    root.after(0, update_song_info_on_gui, "Indlæser sanginfo...")

    mpv_command = [
        'mpv', 
        '--no-video', 
        f'--title={name}', 
        f'--input-ipc-server={mpv_ipc_socket_path}', 
        '--idle=once', 
        url
    ] 
    
    # print(f"\n--- Starter mpv (verbose) ---") # DEBUG
    # print(f"Kommando: {' '.join(mpv_command)}") # DEBUG
    
    try:
        current_process = subprocess.Popen(
            mpv_command,
            preexec_fn=os.setsid,
            stdout=subprocess.PIPE,  
            stderr=subprocess.STDOUT 
        )
        # print(f"mpv proces startet med PID: {current_process.pid}") # DEBUG

        ipc_thread_running = True
        mpv_ipc_thread = threading.Thread(target=read_mpv_ipc, daemon=True)
        mpv_ipc_thread.start()
        # print(f"IPC-tråd startet. Overvåger: {mpv_ipc_socket_path}") # DEBUG

        mpv_stdout_thread = threading.Thread(target=read_mpv_stdout, daemon=True)
        mpv_stdout_thread.start()
        # print(f"mpv stdout læse-tråd startet.") # DEBUG

    except FileNotFoundError:
        messagebox.showerror("Fejl", "mpv blev ikke fundet. Sørg for, at mpv er installeret og tilgængeligt i din PATH.")
        if current_playing_text:
            current_playing_text.set("FEJL: mpv ikke fundet!")
        root.after(0, update_song_info_on_gui, "") 
    except Exception as e:
        messagebox.showerror("Fejl", f"Kunne ikke starte mpv:\n{e}")
        if current_playing_text:
            current_playing_text.set("FEJL ved start af mpv!")
        root.after(0, update_song_info_on_gui, "") 

# --- GUI-callbacks ---

def on_station_click(name):
    """Callback funktion når en radiostationsknap klikkes."""
    url = stations[name]
    start_mpv(name, url)

def on_close():
    """Lukker applikationen og rydder op."""
    print("Lukker applikationen...")
    stop_mpv()
    root.destroy()

# --- GUI Opsætning ---

root = tk.Tk()
root.title("Radioafspiller")
root.geometry("300x450")
root.configure(bg="black")

tk.Label(root, text="Vælg en station:", fg="lime", bg="black", font=("Helvetica", 14)).pack(pady=10)

current_playing_text = tk.StringVar()
current_playing_text.set("Ingen station afspiller")

playing_display_label = tk.Label(
    root, 
    textvariable=current_playing_text,
    fg="cyan",
    bg="gray10",
    font=("Helvetica", 12, "italic"),
    width=35,
    height=2,
    wraplength=250,
    relief="sunken",
    bd=2
)
playing_display_label.pack(pady=5)

current_song_info_text = tk.StringVar()
current_song_info_text.set("")

song_info_display_label = tk.Label(
    root,
    textvariable=current_song_info_text,
    fg="yellow",
    bg="gray15",
    font=("Helvetica", 11),
    width=35,
    height=2,
    wraplength=250,
    relief="flat",
    bd=1
)
song_info_display_label.pack(pady=5)

for name in stations:
    btn = tk.Button(
        root,
        text=name,
        width=25,
        command=lambda n=name: on_station_click(n),
        bg="gray20",
        fg="lime",
        font=("Helvetica", 12),
        activebackground="gray30",
        relief="flat"
    )
    btn.pack(pady=4)

exit_btn = tk.Button(
    root,
    text="Afslut",
    command=on_close,
    bg="darkred",
    fg="white",
    font=("Helvetica", 12, "bold"),
    activebackground="red",
    relief="raised"
)
exit_btn.pack(pady=20)

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
