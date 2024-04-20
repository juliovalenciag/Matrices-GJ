## modulo encargado de desplegar una ventana para el drop and drag
from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter
import os
from PIL import ImageTk, Image


class Window_drag_and_drop(customtkinter.CTkToplevel, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)
        self.title("Coloca aqui tu matriz")
        self.geometry("400x400")
        self.resizable(False, False)
        try:
                image_path = os.path.join("images", img_name)
                pil_image = Image.open(image_path).resize((50, 50))
                tk_image = ImageTk.PhotoImage(pil_image)
                button = customtkinter.CTkButton(topbar_frame, image=tk_image, text=text, command=cmd, compound="top",
                                                 fg_color=None, hover_color="gray")
                button.image = tk_image
                button.grid(row=0, column=i, padx=10, pady=10)
        except FileNotFoundError:
            print(f"Error: El archivo {img_name} no se encontró en la carpeta 'images'.")
