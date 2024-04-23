import os
import tkinter as tk
from tkinter import ttk
import customtkinter
from PIL import ImageTk, Image
from fractions import Fraction

from gauss_jordan import GaussJordanFrame
from determinants import DeterminantsFrame
from operations import OperationsFrame

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gauss-Jordan")
        self.geometry("1280x720")

        self.configure_gui()
        self.configure_sidebar()
        self.create_main_content()

    def configure_gui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def configure_sidebar(self):
        sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        sidebar_frame.grid_rowconfigure(6, weight=1)

        text_label = customtkinter.CTkLabel(sidebar_frame, text="Matrices",
                                            font=customtkinter.CTkFont(size=20, weight="bold"))
        text_label.grid(row=0, column=0, padx=20, pady=(10, 10))

        buttons_info = [
            ("gj1.png", "Gauss-Jordan", self.show_gauss_jordan),
            ("determinante.png", "Determinante", self.show_determinants),
            ("operaciones.png", "Operaciones", self.show_operations),
        ]

        for i, (img_name, text, command) in enumerate(buttons_info, start=1):
            try:
                image_path = os.path.join("images", img_name)
                pil_image = Image.open(image_path).resize((50, 50))
                tk_image = ImageTk.PhotoImage(pil_image)
                button = customtkinter.CTkButton(sidebar_frame, image=tk_image, text=text, command=command,
                                                 compound="top", fg_color=None, hover_color="gray")
                button.image = tk_image  # Keep a reference to the image to avoid garbage collection
                button.grid(row=i, column=0, padx=10, pady=10)
            except FileNotFoundError:
                print(f"Error: El archivo {img_name} no se encontró en la carpeta 'images'.")

        appearance_mode_label = customtkinter.CTkLabel(sidebar_frame, text="Apariencia:", anchor="w")
        appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        appearance_mode_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"],
                                                                  command=self.change_appearance_mode_event)
        appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))
        scaling_label = customtkinter.CTkLabel(sidebar_frame, text="Escala:", anchor="w")
        scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        scaling_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                          command=self.change_scaling_event)
        scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))
        appearance_mode_optionemenu.set("Dark")
        scaling_optionemenu.set("100%")
    def create_main_content(self):
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.show_gauss_jordan()

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_gauss_jordan(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        gj_frame = GaussJordanFrame(self.main_frame)
        gj_frame.pack(fill="both", expand=True)

    def show_determinants(self):
        self.clear_main_frame()
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        gj_frame = DeterminantsFrame(self.main_frame)
        gj_frame.pack(fill="both", expand=True)

    def show_operations(self):
        self.clear_main_frame()
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        gj_frame = OperationsFrame(self.main_frame)
        gj_frame.pack(fill="both", expand=True)

    def show_configuration(self):
        self.clear_main_frame()
        label = customtkinter.CTkLabel(self.main_frame, text="Configuracion")
        label.pack(pady=20)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        customtkinter.set_widget_scaling(int(new_scaling.replace("%", "")) / 100)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
