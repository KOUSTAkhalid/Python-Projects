from tkinter import *
from tkinter import messagebox
import tkinter
import os
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

class MyApp(object):
    def __init__(self, parent):
        self.root = parent
        self.root.title("Youtube video Downloader")



        def down():
                try:
                    yt = YouTube(user_input.get())
                    if messagebox.askokcancel("Confirmation", "Do you want to download : "+yt.title):
                        Directiry = os.getcwd()
                        Folder = '\\PythonMusic'
                        path = Directiry + Folder
                        
                        if not os.path.isdir(path):
                            os.mkdir(path)
                            print("Directory Created")
                        yt.streams.filter(only_audio=True).first().download(path)
                        print("Download COMPLETED")
                except:
                    messagebox.showinfo("Connection problem", "Please  Try again")#####

    
                

        user_input = tkinter.StringVar(self.root)        
        Label(parent,text = "Link :").pack(side = TOP, fill=None, expand=False)
        e1 = Entry(parent, textvariable=user_input)
        e1.pack(side = TOP,fill=X, expand=True)
        if pyperclip.paste():
            e1.insert(0, pyperclip.paste())
            
        Button(parent, text = "Download", command = down).pack(side = BOTTOM)  


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        os._exit(0)


if __name__ == "__main__":
    # Create the tkinter window
    sim_window = Tk()
    sim_window.protocol("WM_DELETE_WINDOW", on_closing)
    sim_window.geometry("400x100")
    sim_window.resizable(False, False)
    app = MyApp(sim_window)
    # Loop
    sim_window.mainloop()

