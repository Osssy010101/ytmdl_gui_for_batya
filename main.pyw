import tkinter as tk
import subprocess
import re
import os
import platform

# TODO:
# Нужно сделать что-то вроде анимации, или .. крч показывать процесс загрузки, что что-то происходит

# TODO:
# После успешной загрузки тексn "Download Complete" нужно убрать.

# TODO:
# После каждого ввода очищать поле ввода (ну убирать ссылку)

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

os_system_name = platform.system()

root = tk.Tk()
root.title("ytmdl GUI")

root.geometry('600x200')
root.minsize(600, 200)
root.maxsize(600, 200)

url: str = ""

def open_music_dir():
    # TODO:
    # Нужно еще сделать тоже самое для Linux, причем нужно взять из $PATH место где скачиваеться музыка из ytmdl
    # Пока сделаю так что бы эта фича была только для Windows.
    if os_system_name == "Windows":
        user_system_name = os.getlogin()
        os.system(f"explorer.exe C:\\Users\\{user_system_name}\\Music")

def download_music():
    url = entry.get()

    # General youtube url validaion to exclude any other text and shit.
    if not re.match(YOUTUBE_URL_REGEX["general"], url):
        error_lable = tk.Label(text="Invalid URL", font=("Arial", MEDIUM_TEXT_FONT_SIZE))
        error_lable.pack()
        error_lable.after(2000, error_lable.destroy)
        return

    # It is important to check for playlist link first, or otherwise it will not work.
    if re.match(YOUTUBE_URL_REGEX["playlist"], url):
        youtube_playlist_id = re.match(YOUTUBE_URL_REGEX["playlist"], url).group(1)

        start_ytmdl = subprocess.run(["ytmdl", f"https://www.youtube.com/playlist?list={youtube_playlist_id}", "--skip-meta"], shell=True)
        if start_ytmdl.returncode == 0:
            tk.Label(text="Download Complete", font=("Arial", MEDIUM_TEXT_FONT_SIZE)).pack()
        else:
            tk.Label(text="Download Failed", font=("Arial", MEDIUM_TEXT_FONT_SIZE)).pack()
    elif re.match(YOUTUBE_URL_REGEX["video"], url):
        start_ytmdl = subprocess.run(["ytmdl", "--url", url, "--skip-meta"], shell=True)

        if start_ytmdl.returncode == 0:
            tk.Label(text="Download Complete", font=("Arial", MEDIUM_TEXT_FONT_SIZE)).pack()
        else:
            tk.Label(text="Download Failed", font=("Arial", MEDIUM_TEXT_FONT_SIZE)).pack()
    else:
        error_lable = tk.Label(text="Invalid URL", font=("Arial", MEDIUM_TEXT_FONT_SIZE))
        error_lable.pack()
        error_lable.after(2000, error_lable.destroy)
        return

tk.Label(text="Download Youtube Music", font=("Arial", BIG_TEXT_FONT_SIZE)).pack()

entry = tk.Entry(root, textvariable="Here", width=50, font=("Arial", 14))  
entry.config(highlightthickness=1.5, highlightbackground="black", highlightcolor="blue")
entry.pack(pady=10)

download_button = tk.Button(root, text="Download", font=("Arial", 16), command=download_music)
download_button.pack(pady=10)

open_dir_button = tk.Button(root, text="Open Music Directory", font=("Arial", 16), command=open_music_dir)
open_dir_button.pack(side="bottom", anchor="e", padx=8, pady=8)

root.mainloop()