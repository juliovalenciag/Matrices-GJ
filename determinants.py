from fractions import Fraction

from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import os


class DeterminantsFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure_mainContent()

        self.configure_topbar()

        self.cell_size = 50
        self.cell_padding = 10

        self.size = 3


    def configure_topbar(self):
        topbar_frame = customtkinter.CTkFrame(self, height=100, corner_radius=0)
        topbar_frame.grid(row=0, column=1, columnspan=3, sticky="nsew")

        button_info = [("importar.png", "Importar", self.toolbar_button_click),
                       ("exportar.png", "Exportar", self.toolbar_button_click),
                       ("resolver.png", "Resolver", self.toolbar_button_click),
                       ("inversa.png", "Inversa", self.toolbar_button_click),
                       ("limpiar.png", "Reiniciar",self.toolbar_button_click ),
                       ("Cambiar.png", "Seleccionar tamaño", self.matrix_size), ]

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

    def toolbar_button_click(self):
        print("Toolbar button clicked")

    def configure_mainContent(self):
        self.mainEntry_frame = customtkinter.CTkFrame(self)
        self.mainEntry_frame.grid(row=1, column=1, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.grid_columnconfigure(1, weight=1)

        self.create_matrix_entries(3)

        self.result_label = customtkinter.CTkLabel(self.mainEntry_frame, text="Determinante:", font=('Arial', 14))
        self.result_label.grid(row=1, column=1, padx=10, pady=10)

        self.mainSolution_frame = customtkinter.CTkFrame(self)
        self.mainSolution_frame.grid(row=1, column=2, rowspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.grid_columnconfigure(2, weight=1)

        self.mainResults_frame = customtkinter.CTkFrame(self)
        self.mainResults_frame.grid(row=3, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.grid_rowconfigure(3, weight=1)

        self.clear_content_button = customtkinter.CTkButton(self, text="Limpiar contenido", fg_color="transparent",
                                                            border_width=1, text_color=("gray10", "#DCE4EE"),
                                                            command=self.clear_matrix_content)
        self.clear_content_button.grid(row=4, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.label_determinant = customtkinter.CTkLabel(self, text="Determinante de matriz")
        self.label_determinant.grid(row=4, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

    #A  partir de aqui va lo de formar la matriz:
    def matrix_size(self):
        self.matrix_window = customtkinter.CTkToplevel(self)
        self.matrix_window.title("Adjust Matrix Size")
        self.matrix_window.geometry("600x500")

        self.canvas = tk.Canvas(self.matrix_window, width=500, height=400)
        self.canvas.pack(pady=20, padx=20)
        self.canvas.bind("<B1-Motion>", self.resize_matrix)
        self.draw_matrix(self.size)


    def draw_matrix(self, size):
        self.canvas.delete("all")
        start_x = start_y = 50  # Start position for the grid.

        for i in range(size):
            for j in range(size):
                x1 = start_x + j * (self.cell_size + self.cell_padding)
                y1 = start_y + i * (self.cell_size + self.cell_padding)
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.create_rounded_rectangle(x1, y1, x2, y2, outline="black", fill="lightgrey")

        self.canvas.create_rectangle(start_x + size * (self.cell_size + self.cell_padding) - self.cell_padding,
                                     start_y + size * (self.cell_size + self.cell_padding) - self.cell_padding,
                                     start_x + size * (self.cell_size + self.cell_padding),
                                     start_y + size * (self.cell_size + self.cell_padding),
                                     fill="red", outline="black", width=2)
    def resize_matrix(self, event):
        new_size = int((max(event.x, event.y) - 50) / (self.cell_size + self.cell_padding)) + 1
        if new_size != self.size and 1 <= new_size <= 10:
            self.size = new_size
            self.draw_matrix(self.size)

    def accept_size(self):
        self.create_matrix_entries(self.size)
        self.matrix_window.destroy()



    def update_rows_columns(self, event=None):
        self.rows = int(self.row_box.get())
        self.columns = int(self.col_box.get())
        self.draw_matrix()
        self.create_matrix_entries(self.rows, self.columns)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=10, **kwargs):
        points = [x1 + radius, y1,
                  x1 + radius, y1, x2 - radius, y1, x2 - radius, y1,
                  x2, y1, x2, y1 + radius, x2, y1 + radius, x2, y2 - radius,
                  x2, y2 - radius, x2, y2, x2 - radius, y2, x2 - radius, y2,
                  x1 + radius, y2, x1 + radius, y2, x1, y2, x1, y2 - radius,
                  x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1, y1]
        self.canvas.create_polygon(points, **kwargs, smooth=True)

    def create_matrix_entries(self, size):
        for widget in self.mainEntry_frame.winfo_children():
            widget.destroy()

        self.matrix_entries = []
        entry_width = 60
        entry_height = 60
        padding = 5
        bg_color_default = "#2C2F33" if customtkinter.get_appearance_mode() == "Dark" else "white"

        start_x = (self.mainEntry_frame.winfo_width() - size * (entry_width + padding)) // 2
        start_y = (self.mainEntry_frame.winfo_height() - size * (entry_height + padding)) // 2

        for i in range(size):
            row_entries = []
            for j in range(size):
                entry = customtkinter.CTkEntry(self.mainEntry_frame, width=entry_width, height=entry_height,
                                               corner_radius=5, fg_color=bg_color_default)
                entry.place(x=start_x + j * (entry_width + padding), y=start_y + i * (entry_height + padding))
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

    def clear_matrix_content(self):
        self.create_matrix_entries(3)




if __name__ == "__main__":
    root = customtkinter.CTk()
    gj_frame = DeterminantsFrame(root)
    gj_frame.pack(fill="both", expand=True)
    root.mainloop()
