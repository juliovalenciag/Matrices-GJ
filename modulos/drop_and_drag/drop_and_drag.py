## modulo encargado de desplegar una ventana para el drop and drag
from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter
class Window_drag_and_drop(customtkinter.CTkToplevel, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)