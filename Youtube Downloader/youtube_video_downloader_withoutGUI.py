from tkinter import messagebox
import tkinter
import os
import os.path
from pytube import YouTube
import pyperclip
    
print("""
    _______        ____     |    __  __                _                   _                  
   / _____ \      /___ \    |   |  \/  | ___  ___ __ _| |_ _ __ ___  _ __ (_) __ _ _   _  ___ 
  / /     \ \         \ \   |   | |\/| |/ _ \/ __/ _` | __| '__/ _ \| '_ \| |/ _` | | | |/ _ \ 
 / /       \ \         \ \  |   | |  | |  __/ (_| (_| | |_| | | (_) | | | | | (_| | |_| |  __/
 | |        \ \        | |  |   |_|  |_|\___|\___\__,_|\__|_|  \___/|_| |_|_|\__, |\__,_|\___|
 \ \         \ \       / /  |                                                   |_|           
  \ \____     \ \_____/ /   |  
   \____/      \_______/    |             Mechatronics CLUB <<ENSET MOHAMMEDIA>>
   

    thia script was made by KOUSTA KHALID for the Python Training
    Gmail : kousta90@gmail.com
    date : 08/01/2021

""")     


def download():
    try:
        yt = YouTube(pyperclip.paste())
        if messagebox.askokcancel("Confirmation", "Do you want to download : "+yt.title):
            Directiry = os.getcwd()
            Folder = '\\PythonVideos'
            path = Directiry + Folder
            
            if not os.path.isdir(path):
                os.mkdir(path)
            yt.streams.first().download(path)
    except:
        messagebox.showinfo("Connection problem", "Please  Try again")##

root = tkinter.Tk()
root.withdraw()
download()
