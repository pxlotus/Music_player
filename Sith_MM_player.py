import tkinter
import tkinter.ttk
import os
import threading
import pygame
import time
from tkinter import filedialog, messagebox, Menu, ttk
from tkinter import *
from pygame import mixer
from PIL import ImageTk, Image

# creating windows
root = tkinter.Tk()

# created a status bar
statusbar = ttk.Label(root, text="Sith Music, Media Player", anchor=W, font='Arial 8 italic')
statusbar.pack(side=BOTTOM, fill=X)
statusbar1 = ttk.Label(root, text="Sith Music, Media Player", anchor=W, font='Arial 8 italic')
statusbar1.pack(side=TOP, fill=X)

# create menun bar
menu_Bar = Menu(root)
root.config(menu=menu_Bar)
root["bg"] = "#FCE205"
sub_menu = Menu(menu_Bar, tearoff=0)

# music functions and tools

playlist = []
# real_names = []
filename_path = ''
v = StringVar()
song_label = Label(root, textvariable=v, width=35)

# function for adding songs to the playlist
def file_browse():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)
    mixer.music.queue(filename_path)

    # to loop over all the files in the directory

def add_to_playlist(filename):
    global index
    filename = os.path.basename(filename)
    index = 0
    # audio = ID3(playlist_container)
    # real_names.append(audio['title'].text[0])
    playlist_container.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1


# filename = os.path.basename(filename)
"""for file in os.listdir(directory):
    # add files
    real_dir = os.path.realpath(file)
    # load the metadata of that song into the audio variable
    audio = ID3(real_dir)
    real_names.append(audio['title'].text[0])
    playlist.append(file)"""

mixer.init()

def remove_song():
    sel_song = playlist_container.curselection()
    sel_song = int(sel_song[0])
    playlist_container.delete(sel_song)
    playlist.pop(sel_song)

def show_details(play_song):
    file_data = os.path.splitext(play_song)
    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    time_format = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel["text"] = "Total Time " + " - " + time_format
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()

# song count down
def start_count(t):
    global paused
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            current_time_label['text'] = "Current_time " + " - " + time_format
            time.sleep(1)
            current_time += 1


def play_music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            sel_song = playlist_container.curselection()
            sel_song = int(sel_song[0])
            play = playlist[sel_song]
            mixer.music.load(play)
            mixer.music.play()
            statusbar['text'] = "playing music " + " - " + os.path.basename(play)
        except :
            tkinter.messagebox.showerror("File not Found", "Sith MM player could not find the given file"
                                                           "please select again.")

def update_label():
    global index
    global song_name
    v.set(filename_path[index])


def nex_song():
    global index
    index += 1
    mixer.music.load(playlist_container[index])
    mixer.music.play()
    update_label()

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "music Paused"

def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"
paused = FALSE

def rewind_music():
    play_music()
    statusbar['text'] = "Music Repeat"

def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
muted = FALSE

def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.8)
        volumeBtn.configure(text="Mute")
        scale.set(70)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        volumeBtn.configure(text="Volume")
        scale.set(0)
        muted = TRUE

# menu options
sub_menu.add_command(label="New")
sub_menu.add_separator()
sub_menu.add_command(label="Open", command=file_browse)
sub_menu.add_separator()
menu_Bar.add_cascade(label="File", menu=sub_menu)
"""
image1 = Image.open("deck.jpg")
image1.resize((20, 20))
test = ImageTk.PhotoImage(image1)
img = Label(root, image=test)
img.place(x=100, y=100)
label1 = tkinter.Label(image=test)
label1.image = test"""


# mixer theme
root.title("Sith Media Player")
lt_frame = Frame(root, bg="#FFFFFF")
lt_frame.pack(side=LEFT, pady=100, padx=60)

# playlist tools
playlist_container = Listbox(lt_frame, selectmode=SINGLE, fg="gold")
playlist_container["bg"] = "#364C69"
playlist_container.pack(pady=100, padx=50)

root.style = ttk.Style()
root.style.theme_use("clam")
# add songs button
addBtn = ttk.Button(lt_frame, text='+Add', command=file_browse)
addBtn.pack(side=LEFT)
remBtn = ttk.Button(lt_frame, text='-Del', command=remove_song)
remBtn.pack(side=RIGHT)
volumeBtn = ttk.Button(lt_frame, text="Mute", command=mute_music)
volumeBtn.pack()

root.style.configure('TButton', bg='#000')
rt_frame = Frame(root, bg='#364C69')
rt_frame.pack(pady=30, padx=20)

top_frame = Frame(rt_frame, bg='#000')
top_frame.pack()
root.style = ttk.Style()

# status bar
root.style.theme_use("clam")
root.style.configure('TLabel', background="#364C69")

# time labels
lengthlabel = ttk.Label(top_frame, text='Total Time :--:--')
lengthlabel.pack(pady=5)
current_time_label = ttk.Label(top_frame, text='Current Time :--:--')
current_time_label.pack()


# control theme box
middle_frame = Frame(rt_frame, bg="#364C69")
middle_frame.pack(pady=45, padx=30)
playBtn = ttk.Button(middle_frame, text="Play", command=play_music)
playBtn.grid(row=0, column=0, padx=10)
pauseBtn = ttk.Button(middle_frame, text="Pause", command=pause_music)
pauseBtn.grid(row=0, column=1, padx=10)
nextBtn = ttk.Button(middle_frame, text="Next", command=nex_song)
nextBtn.grid(row=0, column=2, padx=10)
stopBtn = ttk.Button(middle_frame, text="Stop", command=stop_music)
stopBtn.grid(row=2, column=2, padx=10)
rewindBtn = ttk.Button(middle_frame, text="Rewind", command=rewind_music)
rewindBtn.grid(row=2, column=0, padx=10)


bottom_frame = Frame(rt_frame, bg="#345")
bottom_frame.pack(pady=10, padx=5)
volumeBtn = ttk.Button(bottom_frame, text="Mute", command=mute_music)
volumeBtn.grid(row=0, column=1)
scale = ttk.Scale(bottom_frame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70) # implement the default value of scale when the music player starts
mixer.music.set_volume(0.9)
scale.grid(row=0, column=2, pady=15, padx=30)
"""
canvas = Canvas(root, width=300, height=300)
canvas.pack()"""

# closing the player windows
def _quit():
    root.quit()
    root.destroy()
    exit()
root.protocol("Sith_Delete_window", _quit)
sub_menu.add_command(label="Exit", command=_quit)

root.mainloop()

