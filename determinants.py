from fractions import Fraction

from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import os
import modulos.drop_and_drag.drop_and_drag as TKdnd

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
class DeterminantsFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure_mainContent()
        self.configure_topbar()
        self.cell_size = 50
        self.cell_padding = 10
        self.size = 3
        self.create_matrix_entries(self.size)

    def configure_topbar(self):
        topbar_frame = customtkinter.CTkFrame(self, height=100, corner_radius=0)
        topbar_frame.grid(row=0, column=1, columnspan=3, sticky="nsew")

        button_info = [("importar.png", "Importar", self.import_document),
                       ("exportar.png", "Exportar", self.export_document),
                       ("resolver.png", "Resolver", self.calculate_determinant),
                       ("inversa.png", "Inversa", self.calculate_inverse),
                       ("limpiar.png", "Reiniciar",self.clear_all ),
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
        self.mainEntry_frame.grid(row=1, column=1, rowspan=3, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.mainEntry_frame.update_idletasks()

        self.after(100, lambda: self.create_matrix_entries(3))

        self.result_label = customtkinter.CTkLabel(self.mainEntry_frame, text="Determinante:", font=('Arial', 14))
        self.result_label.grid(row=1, column=1, padx=10, pady=10)


        self.mainSolution_frame = customtkinter.CTkFrame(self)
        self.mainSolution_frame.grid(row=1, column=2, rowspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.grid_columnconfigure(2, weight=1)

        self.label_determinant = customtkinter.CTkLabel(self.mainSolution_frame, text="Determinante:",
                                                        font=('Arial', 30))
        self.label_determinant.grid(row=1, column=1, padx=10, pady=10)

        self.mainResults_frame = customtkinter.CTkFrame(self)
        self.mainResults_frame.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.grid_rowconfigure(3, weight=1)


    #A  partir de aqui va lo de formar la matriz (cambiar tamaño):
    def matrix_size(self):
        self.matrix_window = customtkinter.CTkToplevel(self)
        self.matrix_window.title("Adjust Matrix Size")
        self.matrix_window.geometry("800x600")
        self.matrix_window.attributes("-topmost", True)
        self.canvas = tk.Canvas(self.matrix_window, width=500, height=500)
        self.canvas.pack(pady=20, padx=20)
        self.canvas.bind("<B1-Motion>", self.resize_matrix)
        self.size = 3
        self.draw_matrix(self.size)
        self.size_box = ttk.Combobox(self.matrix_window, values=list(range(1, 7)), state="readonly", width=5)
        self.size_box.set(self.size)
        self.size_box.pack(side='left', padx=20, pady=10)
        self.size_box.bind("<<ComboboxSelected>>", self.update_size)
        accept_button = customtkinter.CTkButton(self.matrix_window, text="Aceptar", command=self.accept_size)
        accept_button.pack(side='right', padx=10, pady=10)

    def draw_matrix(self, size):
        self.canvas.delete("all")
        start_x = start_y = 50
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
            self.size_box.set(self.size)

    def update_size(self, event=None):
        new_size = int(self.size_box.get())
        if new_size != self.size:
            self.size = new_size
            self.draw_matrix(self.size)

    def accept_size(self):
        self.create_matrix_entries(self.size)
        self.matrix_window.destroy()

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
        bracket_width = 2
        bracket_spacing = 10
        bg_color_default = "#2C2F33" if customtkinter.get_appearance_mode() == "Dark" else "white"
        frame_bg_color = "#202020" if customtkinter.get_appearance_mode() == "Dark" else "#e3e3e3"
        bracket_color = "white" if customtkinter.get_appearance_mode() == "Dark" else "black"

        self.mainEntry_frame.configure(fg_color=frame_bg_color)

        start_x = bracket_spacing + bracket_width + padding
        start_y = padding

        canvas = tk.Canvas(self.mainEntry_frame, bg=frame_bg_color, highlightthickness=0, bd=0)
        canvas.pack(fill="both", expand=True)

        canvas.create_line(start_x - bracket_spacing, start_y, start_x - bracket_spacing,
                           start_y + size * (entry_height + padding), fill=bracket_color, width=bracket_width)
        canvas.create_line(start_x + size * (entry_width + padding) + bracket_spacing, start_y,
                           start_x + size * (entry_width + padding) + bracket_spacing,
                           start_y + size * (entry_height + padding), fill=bracket_color, width=bracket_width)

        for i in range(size):
            row_entries = []
            for j in range(size):
                entry = customtkinter.CTkEntry(canvas, width=entry_width, height=entry_height, corner_radius=5,
                                               fg_color=bg_color_default)
                entry.place(x=start_x + j * (entry_width + padding), y=start_y + i * (entry_height + padding))
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

        self.mainEntry_frame.configure(
            width=size * (entry_width + padding) + 2 * (bracket_spacing + bracket_width + padding),
            height=size * (entry_height + padding) + 2 * padding)

    def import_document(self):
        TKdnd.import_document(self, "<D>")
    
    def export_document(self):
        TKdnd.export_document(self)
        
    def clear_all(self):
        self.create_matrix_entries(self.size)
        for widget in self.mainResults_frame.winfo_children():
            widget.destroy()
        self.label_determinant.configure(text="Determinante:")

    def calculate_inverse(self):
        rows = len(self.matrix_entries)

        matrix = []
        for i, row_entries in enumerate(self.matrix_entries):
            row = [Fraction(entry.get() if entry.get() else 0) for entry in row_entries]
            identity_row = [Fraction(int(i == j)) for j in range(rows)]
            matrix.append(row + identity_row)

        n = len(matrix)
        for i in range(n):
            pivot = matrix[i][i]
            if pivot == 0:
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    tkinter.messagebox.showerror("Error", "La matriz es singular y no tiene inversa.")
                    return

            matrix[i] = [x / pivot for x in matrix[i]]

            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    matrix[j] = [matrix[j][k] - factor * matrix[i][k] for k in range(2 * n)]

        inverse_matrix = [row[n:] for row in matrix]
        self.display_result_matrix(inverse_matrix)

    def display_result_matrix(self, matrix):
        for widget in self.mainResults_frame.winfo_children():
            widget.destroy()

        rows = len(matrix)
        columns = len(matrix[0]) if matrix else 0
        entry_width = 75
        entry_height = 50

        bg_color = "#2C2F33" if customtkinter.get_appearance_mode() == "Dark" else "white"

        total_width = columns * (entry_width + 10)
        total_height = rows * (entry_height + 10)

        start_x = (self.mainResults_frame.winfo_width() - total_width) // 2
        start_y = (self.mainResults_frame.winfo_height() - total_height) // 2

        start_x = max(start_x, 10)
        start_y = max(start_y, 10)

        for i in range(rows):
            self.mainResults_frame.grid_rowconfigure(i, weight=1, uniform='row')
            for j in range(columns):
                self.mainResults_frame.grid_columnconfigure(j, weight=1, uniform='col')
                value = matrix[i][j]
                label = customtkinter.CTkLabel(self.mainResults_frame, text=str(value),
                                               width=entry_width, height=entry_height,
                                               corner_radius=5, fg_color=bg_color, anchor='center')
                label.grid(row=i, column=j, padx=(5, 5), pady=(5, 5), sticky="nsew")
                label.place(x=start_x + j * (entry_width + 10), y=start_y + i * (entry_height + 10))

    def calculate_determinant(self):
        if not self.matrix_entries:
            tkinter.messagebox.showinfo("Información", "Primero ingresa la matriz.")
            return

        size = len(self.matrix_entries)
        matrix = []
        for row_entries in self.matrix_entries:
            row = [Fraction(entry.get() if entry.get() else '0') for entry in row_entries]
            matrix.append(row)

        determinant = 1
        for i in range(size):
            if matrix[i][i] == 0:  # Buscar un pivot no cero en la columna i
                for k in range(i + 1, size):
                    if matrix[k][i] != 0:
                        matrix[i], matrix[k] = matrix[k], matrix[i]  # Intercambiar filas
                        determinant *= -1  # Cambiar signo del determinante
                        break
                else:
                    determinant = 0  # Si no hay pivote, determinante es 0
                    break
            pivot = matrix[i][i]
            determinant *= pivot  # Multiplicar el determinante por el pivote

            for j in range(i + 1, size):  # Eliminar columnas debajo del pivote
                factor = matrix[j][i] / pivot
                for k in range(size):
                    matrix[j][k] -= factor * matrix[i][k]

        self.label_determinant.configure(
            text=f"Determinante: {determinant}")

if __name__ == "__main__":
    root = customtkinter.CTk()
    gj_frame = DeterminantsFrame(root)
    gj_frame.pack(fill="both", expand=True)
    root.mainloop()
