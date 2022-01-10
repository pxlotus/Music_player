import os
from tkinter.filedialog import askdirectory
import pygame
from mutagen.id3 import ID3
from tkinter import *
from pygame import mixer


root = Tk()
root.minsize(300, 300)

playlist = []
real_names = []

v = StringVar()
song_label = Label(root, textvariable=v, width=35)

index = 0

def file_browse():
    directory = askdirectory()
    os.chdir(directory)

    # to loop over all the files in the directory
    for file in os.listdir(directory):
        # only add files if the end with .mp3
        if file.endswith(".mp3"):
            real_dir = os.path.realpath(file)
            # load the metadata of that song into the audio variable.
            audio = ID3(real_dir)
            real_names.append(audio['title'].text[0])
            playlist.append(file)

    # initialise pygame
    mixer.init()
    # load the first song
    mixer.music.load(playlist[0])
    # play music
    mixer.music.play()

file_browse()

def update_label():
    global index
    global song_name
    v.set(real_names[index])

def nex_song(event):
    global index
    index += 1
    # get the next song from the playlist
    mixer.music.load(playlist[index])
    mixer.music.play()
    # do not forget to update the label
    update_label()

def prev_song(event):
    global index
    index -= 1
    mixer.music.load(playlist[index])
    mixer.music.load(playlist[index])
    mixer.music.play()
    update_label()

def stop_music():
    mixer.music.stop()
    v.set(" ")


label = Label(root, text="Sith Music Player")
label.pack()

playlist_container = Listbox(root)
playlist_container.pack()
# inserting songs in the playlist
real_names.reverse()
for items in real_names:
    playlist_container.insert(0, items)

real_names.reverse()
# next button
nxtBtn = Button(root, text='Next')
nxtBtn.pack()
# previous button
prvBtn = Button(root, text='Prev')
prvBtn.pack()
# stop button
stopBtn = Button(root, text='stop')
stopBtn.pack()

nxtBtn.bind("<Button-1>", nex_song)
prvBtn.bind("<Button-1>", prev_song)
stopBtn.bind("<Button-1>", stop_music)
song_label.pack()

root.mainloop()


