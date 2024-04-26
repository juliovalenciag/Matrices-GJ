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

        self.images = {}
        self.load_images()

        self.active_frame_name = None
        self.active_frame_function = None
        self.buttons = {}
        self.configure_gui()
        self.configure_sidebar()
        self.create_main_content()
        self.activate_frame(self.show_gauss_jordan, "Gauss-Jordan")

    def configure_gui(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def configure_sidebar(self):
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        text_label = customtkinter.CTkLabel(self.sidebar_frame, text="Matrices",
                                            font=customtkinter.CTkFont(size=20, weight="bold"))
        text_label.grid(row=0, column=0, padx=20, pady=(10, 10))

        self.update_button_images()
        self.add_appearance_controls()

    def add_appearance_controls(self):
        appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Apariencia:", anchor="w")
        appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))

        appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame, values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event)
        appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))
        appearance_mode_optionemenu.set(customtkinter.get_appearance_mode())

        scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Escala:", anchor="w")
        scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))

        scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame,
                                                          values=["80%", "90%", "100%", "110%", "120%"],
                                                          command=self.change_scaling_event)
        scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))
        scaling_optionemenu.set("100%")

    def load_images(self):
        for base_name in ["gj1", "determinante", "operaciones"]:
            for suffix in ["", "LM"]:
                img_name = f"{base_name}{suffix}.png"
                image_path = os.path.join("images", img_name)
                try:
                    pil_image = Image.open(image_path).resize((50, 50))
                    self.images[img_name] = ImageTk.PhotoImage(pil_image)
                except FileNotFoundError:
                    print(f"Error: El archivo {img_name} no se encontró en la carpeta 'images'")

    def update_button_images(self):
        mode_suffix = "LM" if customtkinter.get_appearance_mode() == "Light" else ""
        button_text_color = "#000000" if mode_suffix == "LM" else "#FFFFFF"
        for i, (base_name, text, command) in enumerate([
            ("gj1", "Gauss-Jordan", self.show_gauss_jordan),
            ("determinante", "Determinante", self.show_determinants),
            ("operaciones", "Operaciones", self.show_operations)
        ], start=1):
            img_name = f"{base_name}{mode_suffix}.png"
            image = self.images.get(img_name)
            if image:
                button = customtkinter.CTkButton(
                    self.sidebar_frame, image=image, text=text,
                    command=lambda cmd=command, name=text: self.activate_frame(cmd, name),
                    compound="top", fg_color="transparent", hover_color="gray", text_color=button_text_color
                )
                button.image = image
                button.grid(row=i, column=0, padx=10, pady=10)
                self.buttons[text] = button

    def create_main_content(self):
        self.main_frame = customtkinter.CTkFrame(self)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def activate_frame(self, command, frame_name):
        self.clear_main_frame()
        command()
        self.active_frame_name = frame_name
        self.active_frame_function = command
        self.refresh_active_button()

    def refresh_active_button(self):
        for name, button in self.buttons.items():
            if name == self.active_frame_name:
                button.configure(fg_color="#1F538D")
            else:
                button.configure(fg_color="transparent")
    def show_gauss_jordan(self):
        frame = GaussJordanFrame(self.main_frame)
        frame.pack(fill="both", expand=True)

    def show_determinants(self):
        frame = DeterminantsFrame(self.main_frame)
        frame.pack(fill="both", expand=True)

    def show_operations(self):
        frame = OperationsFrame(self.main_frame)
        frame.pack(fill="both", expand=True)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        self.update_button_images()
        if self.active_frame_name:
            self.activate_frame(self.active_frame_function, self.active_frame_name)

    def change_scaling_event(self, new_scaling: str):
        customtkinter.set_widget_scaling(int(new_scaling.replace("%", "")) / 100)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
