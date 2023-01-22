# radiopexample.py
from tkinter import *
from PIL import ImageTk,Image
import vlc
import time

root = Tk()
root.title('Radio Application')

r = IntVar()
r.set("2")

MODES = [
    ("Ndr 2","http://icecast.ndr.de/ndr/ndr2/schleswigholstein/mp3/128/stream.mp3"),
    ("P4 Østjyland","http://live-icy.gss.dr.dk:8000/A/A14L.mp3"),
    ("Hits 2022","https://streams.ilovemusic.de/iloveradio109.mp3"),
    ("goFM","http://stream1.webfm.dk/Webfm"),
]

pizz = StringVar()
pizz.set(MODES[1][0])

for text, mode in MODES:
    Radiobutton(root, text=text, variable=pizz, value=mode).pack(anchor=W)

instance = vlc.Instance()
player = instance.media_player_new()

def clicked():
    url = pizz.get()
    media = instance.media_new(url)
    if player.get_media() != media:
        if player.get_state() == vlc.State.Playing:
            player.stop()
        player.set_media(media)
        player.play()

MyButton = Button(root, text="Play", command=clicked)
MyButton.pack()
root.mainloop()
