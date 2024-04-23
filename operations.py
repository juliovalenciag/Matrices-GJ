
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter

class OperationsFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure_mainContent()

    def configure_mainContent(self):


if __name__ == "__main__":
    root = customtkinter.CTk()
    gj_frame = OperationsFrame(root)
    gj_frame.pack(fill="both", expand=True)
    root.mainloop()