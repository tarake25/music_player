import tkinter as tk
import os
from pygame import mixer
from functools import partial

# the music player functios for the buttom events
mixer.init()

def next():
    pass
def prev():
    pass
def puse():
    mixer.music.pause()
def play():
    mixer.music.play()
def add_v():
    mixer.music.set_volume(mixer.music.get_volume()+0.1)
def del_v():
    mixer.music.set_volume(mixer.music.get_volume()-0.1)
def play_song(i):
    mixer.music.load(f"MUSIC\{i}")
    mixer.music.set_volume(0.5)
    mixer.music.play()



root = tk.Tk()
root.geometry('600x600')
root.title('Music Player')

# Create a Frame to hold the the butoms
frame = tk.Frame(root)
frame.grid()

# Create a Frame to hold the the labels names of the music
frame_2 = tk.Frame(root)
frame_2.grid()

# List to store all label references
labels = []

# Function to update wraplength of all labels when the window resizes
def update_wrap(event):
    for lbl in labels:
        lbl.config(wraplength=min(event.width, 400))

# Load music file names
music_files = os.listdir("MUSIC")

# Create a label for each file
for filename in music_files:
    label = tk.Label(
        frame,
        text=filename,
        justify="left",
        anchor="nw"
    )

    label.pack()
    butun=tk.Button(frame,text='Play music',command=partial(play_song,filename))
    butun.pack()
    labels.append(label)

pus = tk.Button(root,text='puse',command= partial(puse))
pus.grid(column=0, row=1)

add = tk.Button(root,text='+++++',command= partial(add_v))
add.grid(column=1, row=1)

nex = tk.Button(root,text='Next',command= partial(next))
nex.grid(column=2, row=1)
# Bind resize event to the frame
frame.bind("<Configure>", update_wrap)

root.mainloop()
