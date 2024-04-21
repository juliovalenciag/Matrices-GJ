from ast import Import
from os import name, path
import modulos.drop_and_drag.drop_and_drag as TKdnd
from tkinter import BOTTOM, StringVar, TOP
import customtkinter as ctk

root = TKdnd.Window_drag_and_drop()
root.geometry("350x100")
root.title("Get file path")

def get_path(event):
    pathLabel.configure(text=event.data)
    nameVarString.set(event.data)
    
    
nameVarString = StringVar()

entryWidget = ctk.CTkEntry(root)
entryWidget.pack(side=TOP, padx=5, pady=5)

pathLabel = ctk.CTkLabel(root, text="Drag and drop file in the entry box")
pathLabel.pack(side=TOP)

entryWidget.drop_target_register(TKdnd.DND_ALL)
entryWidget.dnd_bind("<<Drop>>", get_path)

button1 = ctk.CTkButton(root, text="Get path", command=lambda: print(nameVarString.get()))
button1.pack(side=BOTTOM, padx=5, pady=5)

pathLabel.destroy()
entryWidget.destroy()

root.mainloop()