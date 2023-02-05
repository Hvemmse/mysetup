import tkinter as tk
import random
import hashlib

def get_random_words(filename, num_words):
    """Get a list of random words from a file

    Args:
        filename (str): The name of the file to read the words from
        num_words (int): The number of words to get from the file

    Returns:
        list: A list of random words from the file
    """
    with open(filename) as f:
        words = f.read().splitlines()
    return random.sample(words, num_words)

def hash_password(password):
    """Hash a password using SHA-256

    Args:
        password (str): The password to hash

    Returns:
        str: The hexadecimal representation of the password hash
    """
    return hashlib.sha256(password.encode()).hexdigest()

def generate_password():
    """Generate a random password

    The function generates a password by concatenating 4 random words from a file, each word's first 4 characters and a random number between 0 and 9. It also randomly capitalizes a letter in the password.
    """
    filename = "passwords.txt"
    num_words = 4
    words = get_random_words(filename, num_words)
    password = "".join([word[:4] + str(random.randint(0,9)) for word in words])
    password_list = list(password)
    password_list[random.randint(0, len(password_list) - 1)] = password_list[random.randint(0, len(password_list) - 1)].upper()
    password = "".join(password_list)
    password_hash = hash_password(password)
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    hash_entry.delete(0, tk.END)
    hash_entry.insert(0, password_hash)

def copy_password():
    """Copy the password to the clipboard"""
    password = password_entry.get()
    root.clipboard_clear()
    root.clipboard_append(password)

def copy_hash():
    """Copy the password hash to the clipboard"""
    password_hash = hash_entry.get()
    root.clipboard_clear()
    root.clipboard_append(password_hash)

root = tk.Tk()
root.title("Password Generator")

frame1 = tk.Frame(root)
frame1.pack()

password_label = tk.Label(frame1, text="Password:")
password_label.grid(row=0, column=0, sticky="W")

password_entry = tk.Entry(frame1)
password_entry.grid(row=0, column=1)

generate_button = tk.Button(frame1, text="Generate", command=generate_password)
generate_button.grid(row=0, column=2, padx=5)

copy_password_button = tk.Button(frame1, text="Copy", command=copy_password)
copy_password_button.grid(row=0, column=3, padx=5)

frame2 = tk.Frame(root)
frame2.pack()

hash_label = tk.Label(frame2, text="Hash:")
hash_label.grid(row=1, column=0, sticky="W")

hash_entry = tk.Entry(frame2)
hash_entry.grid(row=1, column=1)

copy_hash_button = tk.Button(frame2, text="Copy", command=copy_hash)
copy_hash_button.grid(row=1, column=3, padx=5)

root.mainloop()
