import os
import tkinter as tk
import customtkinter
from PIL import ImageTk, Image

customtkinter.set_appearance_mode("Dark")  # Configura el tema oscuro
customtkinter.set_default_color_theme("dark-blue")  # Configura el tema de color

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Algebra Lineal")
        self.geometry("1280x720")

        self.configure_grid_layout()

        self.configure_topbar()
        self.create_main_content()
        self.configure_midbar()

    def configure_grid_layout(self):
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=0, minsize=120)
        self.grid_columnconfigure(2, weight=2)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=3)
        self.grid_rowconfigure(3, weight=3)
        self.grid_rowconfigure(4, weight=0)

    def create_main_content(self):
        self.matrix_frame = customtkinter.CTkFrame(self, border_width=2, border_color="gray")
        self.matrix_frame.grid(row=1, rowspan=4, column=0, sticky="nsew", padx=20, pady=20)

        self.solution_frame = customtkinter.CTkFrame(self, border_width=2, border_color="gray")
        self.solution_frame.grid(row=1, rowspan=3, column=2, sticky="nsew", padx=20, pady=(20, 0))

        self.result_frame = customtkinter.CTkFrame(self, border_width=2, border_color="gray")
        self.result_frame.grid(row=4, column=2, sticky="nsew", padx=20, pady=20)


    def configure_midbar(self):
        midbar_frame = customtkinter.CTkFrame(self, width=120, fg_color=None)
        midbar_frame.grid(row=1, rowspan=4, column=1, sticky="ns")

        functionButtons_info =[("gj1.png", "Gauss-Jordan", self.toolbar_button_click),
                               ("determinante.png", "Determinante", self.toolbar_button_click),
                               ("inversa.png", "Inversa", self.toolbar_button_click),
        ]

        for i, (img_name, text, cmd) in enumerate(functionButtons_info):
            try:
                image_path = os.path.join("images", img_name)
                pil_image = Image.open(image_path).resize((50, 50))
                tk_image = ImageTk.PhotoImage(pil_image)
                button = customtkinter.CTkButton(midbar_frame, image=tk_image, text=text, command=cmd, compound="top", fg_color=None, hover_color="gray")
                button.image = tk_image
                button.grid(row=i, column=0, padx=10, pady=10)
            except FileNotFoundError:
                print(f"Error: El archivo {img_name} no se encontró en la carpeta 'images'.")

    def configure_topbar(self):
        topbar_frame = customtkinter.CTkFrame(self, height=100, corner_radius=0)
        topbar_frame.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=10)

        button_info = [("importar.png", "Importar", self.toolbar_button_click),
                       ("exportar.png", "Exportar", self.toolbar_button_click),
                       ("limpiar.png", "Reiniciar", self.toolbar_button_click),
                       ("Cambiar.png", "Seleccionar tamaño", self.toolbar_button_click)]

        for i, (img_name, text, cmd) in enumerate(button_info):
            try:
                image_path = os.path.join("images", img_name)
                pil_image = Image.open(image_path).resize((50, 50))
                tk_image = ImageTk.PhotoImage(pil_image)
                button = customtkinter.CTkButton(topbar_frame, image=tk_image, text=text, command=cmd,
                                                 compound="top",
                                                 fg_color=None, hover_color="gray")
                button.image = tk_image
                button.grid(row=0, column=i, padx=10, pady=10)
            except FileNotFoundError:
                print(f"Error: El archivo {img_name} no se encontró en la carpeta 'images'.")

        self.appearance_switch = customtkinter.CTkSwitch(topbar_frame, text="Cambiar tema", command=self.toggle_theme)
        self.appearance_switch.grid(row=0, column=8, padx=10, pady=10, sticky="e")

    def toggle_theme(self):
        if customtkinter.get_appearance_mode() == "Dark":
            customtkinter.set_appearance_mode("Light")
        else:
            customtkinter.set_appearance_mode("Dark")

    def toolbar_button_click(self, action):
        print(f"{action} button clicked")

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
