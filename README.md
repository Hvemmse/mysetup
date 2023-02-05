# mysetup


In this repository, will there be some dotfiles from my config.

hent og kør ./radio eller ./radiodk for engelsk eller dansk. lavet i til arch

radio.py

is a gui version for the radio player done in python and pygame vlc must be installed

from tkinter import *
from PIL import ImageTk,Image
import vlc
import time

easyaur is a tool to get the comopiling automated- use it as easyaur url

aur is the same tool but use only det pakage name usage is aur pkgname

passwordgen.py

feat: Generate and hash random passwords

This code generates 4 random passwords by concatenating 4 random words from a file, each word's first 4 characters and a random number between 0 and 9. It also randomly capitalizes a letter in each password. The password and its hash are then printed.

Functions and variables are well documented, making the code easier to understand and maintain. The code uses the SHA-256 hash function to hash the passwords.

# password_generator.py

This script generates a random password and displays the password and its hash in a GUI created with tkinter. The user can copy the password or its hash to the clipboard by clicking the "Copy" buttons. you need a wordile as passwords.txt
