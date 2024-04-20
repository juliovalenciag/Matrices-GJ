## modulo encargado de desplegar una ventana para el drop and drag
from tkinterdnd2 import TkinterDnD
import customtkinter


class Window_drag_and_drop(customtkinter.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)