import os
import re
import platform
import threading
import subprocess

import tkinter as tk

from PIL import Image

BIG_TEXT_FONT_SIZE = 24
MEDIUM_TEXT_FONT_SIZE = 18

YOUTUBE_URL_REGEX = {
    # This link cover all youtube links: vidoes and playlists. It needs for general validation of youtube URL.
    "general": r"http[s]{0,1}:\/\/www\.youtube\.com\/watch\?v=(.*)",

    # You get from this link its ID (where `?v=<ID>` thing)
    "video": r"http[s]{0,1}:\/\/www\.youtube\.com\/watch\?v=(.{11})",

    # You get youtube playlist ID (where `&list=<ID>` thing)
    "playlist": r"http[s]{0,1}:\/\/www\.youtube\.com\/watch\?v=.{11}&list=(.{34})"
}

GIF_PATH = os.path.join(os.path.dirname(__file__), "loading.gif")

OS_SYSTEM_NAME = platform.system()

root = tk.Tk()
root.title("ytmdl GUI")

gif_info = Image.open(GIF_PATH)
count_of_frames = gif_info.n_frames

photoimage_objects = []
for i in range(count_of_frames):
    obj = tk.PhotoImage(file = GIF_PATH, format = f"gif -index {i}")
    photoimage_objects.append(obj)

root.geometry('600x500')
root.minsize(600, 500)
root.maxsize(600, 500)

url: str = ""


def open_music_dir():
    # TODO:
    # Нужно еще сделать тоже самое для Linux, причем нужно взять из $PATH место где скачиваеться музыка из ytmdl
    # Пока сделаю так что бы эта фича была только для Windows.
    if OS_SYSTEM_NAME == "Windows":
        user_system_name = os.getlogin()
        os.system(f"explorer.exe C:\\Users\\{user_system_name}\\Music")


def start_gif(current_frame=0):
    global loop
    
    gif_label.pack()

    image_frame_of_gif = photoimage_objects[current_frame]

    gif_label.config(image=image_frame_of_gif)
    current_frame += 1

    if current_frame == count_of_frames:
        current_frame = 0
    
    loop = root.after(50, lambda: start_gif(current_frame))


def stop_gif():
    root.after_cancel(loop)
    gif_label.pack_forget()

def download_music():
    url = entry.get()

    # General youtube url validaion to exclude any other text and shit.
    if not re.match(YOUTUBE_URL_REGEX["general"], url):
        error_lable = tk.Label(text="Invalid URL", font=("Arial", MEDIUM_TEXT_FONT_SIZE))
        error_lable.pack()
        error_lable.after(2000, error_lable.destroy)
        stop_gif()
        return
    
    lable_download_status = tk.Label(font=("Arial", MEDIUM_TEXT_FONT_SIZE))

    # It is important to check for playlist link first, or otherwise it will not work.
    if re.match(YOUTUBE_URL_REGEX["playlist"], url):
        youtube_playlist_id = re.match(YOUTUBE_URL_REGEX["playlist"], url).group(1)

        start_downloading = subprocess.run(["ytmdl", f"https://www.youtube.com/playlist?list={youtube_playlist_id}", "--skip-meta"], shell=True)
        if start_downloading.returncode == 0:
            lable_download_status.config(text="Download complete")
        else:
            lable_download_status.config(text="Error in downloading")
    else:
        re.match(YOUTUBE_URL_REGEX["video"], url)
        start_downloading = subprocess.run(["ytmdl", "--url", url, "--skip-meta"], shell=True)

        if start_downloading.returncode == 0:
            lable_download_status.config(text="Download complete")
        else:
            lable_download_status.config(text="Download complete")
    
    stop_gif()
    lable_download_status.pack()
    lable_download_status.after(10000, lable_download_status.destroy)
    entry.delete(0, tk.END)
    

tk.Label(text="Download Youtube Music", font=("Arial", BIG_TEXT_FONT_SIZE)).pack()

entry = tk.Entry(root, textvariable="Here", width=50, font=("Arial", 14))  
entry.config(highlightthickness=1.5, highlightbackground="black", highlightcolor="blue")
entry.pack(pady=10)

gif_label = tk.Label(root, image="")

download_button = tk.Button(root, text="Download", font=("Arial", 16), command=lambda: [
    start_gif(current_frame=0),
    threading.Thread(target=download_music).start()
    ])
download_button.pack(pady=10)

open_dir_button = tk.Button(root, text="Open Music Directory", font=("Arial", 16), command=open_music_dir)
open_dir_button.pack(side="bottom", anchor="e", padx=8, pady=8)

root.mainloop()