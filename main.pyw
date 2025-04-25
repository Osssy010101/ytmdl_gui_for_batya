import tkinter as tk
import subprocess
import re

BIG_TEXT_FONT_SIZE = 24
MEDIUM_TEXT_FONT_SIZE = 18

# Examples of regex:
# https://www.youtube.com/watch?v=P-jXyi9bxEk
# http://www.youtube.com/watch?v=P-jXyi9bxEk
# https://www.youtube.com/watch?v=00xprBmokcI&list=PLHWoCotuxs61cuC0OQShmUoR0mP_8YXFx
# 
# It gets even youtube playlist links
YOUTUBE_URL_REGEX = r"http[s]{0,1}:\/\/www.youtube.com\/watch\?v=(.*)"

root = tk.Tk()
root.title("ytmdl GUI")

root.geometry('600x200')
root.minsize(600, 200)
root.maxsize(600, 200)

url: str = ""

def get_url_link_from_entry():
    url = entry.get()

    if not re.match(YOUTUBE_URL_REGEX, url):
        error_lable = tk.Label(text="Invalid URL", font=("Arial", MEDIUM_TEXT_FONT_SIZE))
        error_lable.pack()
        error_lable.after(2000, error_lable.destroy)
        return

    start_ytmdl = subprocess.run(["ytmdl", "--url", url, "--skip-meta"], shell=True)

    if start_ytmdl.returncode == 0:
        tk.Label(text="Download Complete", font=("Arial", MEDIUM_TEXT_FONT_SIZE)).pack()
    else:
        tk.Label(text="Download Failed", font=("Arial", MEDIUM_TEXT_FONT_SIZE)).pack()

tk.Label(text="Download Youtube Music", font=("Arial", BIG_TEXT_FONT_SIZE)).pack()

entry = tk.Entry(root, textvariable="Here", width=50, font=("Arial", 14))  
entry.config(highlightthickness=1.5, highlightbackground="black", highlightcolor="blue")
entry.pack(pady=10)

download_button = tk.Button(root, text="Download", font=("Arial", 16), command=get_url_link_from_entry)
download_button.pack(side="bottom", pady=10)

root.mainloop()