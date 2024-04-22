from fractions import Fraction

from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import os


class GaussJordanFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure_mainContent()
        self.configure_topbar()

        self.after(100, lambda: self.create_matrix_entries(3, 4))

    def configure_topbar(self):
        topbar_frame = customtkinter.CTkFrame(self, height=100, corner_radius=0)
        topbar_frame.grid(row=0, column=1, columnspan=3, sticky="nsew")

        button_info = [("importar.png", "Importar", self.toolbar_button_click),
                       ("exportar.png", "Exportar", self.toolbar_button_click),
                       ("resolver.png", "Resolver", self.gauss_jordan),
                       ("inversa.png", "Inversa", self.calculate_inverse),
                       ("limpiar.png", "Reiniciar", self.clear_all),
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

    def configure_mainContent(self):
        self.mainEntry_frame = customtkinter.CTkFrame(self)
        self.mainEntry_frame.grid(row=1, column=1, rowspan=3, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.grid_columnconfigure(1, weight=1)
        self.mainEntry_frame.update_idletasks()

        self.mainSolution_frame = customtkinter.CTkFrame(self)
        self.mainSolution_frame.grid(row=1, column=2, rowspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.grid_columnconfigure(2, weight=1)

        self.mainResults_frame = customtkinter.CTkFrame(self)
        self.mainResults_frame.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        self.grid_rowconfigure(3, weight=1)


    def create_matrix_entries(self, rows, columns):
        for widget in self.mainEntry_frame.winfo_children():
            widget.destroy()

        self.matrix_entries = []
        self.mainEntry_frame.update_idletasks()

        entry_width = 60
        entry_height = 60
        padding = 5
        bracket_width = 20

        if customtkinter.get_appearance_mode() == "Dark":
            bg_color_default = "#2C2F33"
            bg_color_constant = "#60656b"
            bracket_color = "white"
        else:
            bg_color_default = "white"
            bg_color_constant = "lightgrey"
            bracket_color = "black"

        total_width = columns * (entry_width + padding)
        total_height = rows * (entry_height + padding)

        start_x = (self.mainEntry_frame.winfo_width() - total_width) // 2
        start_y = (self.mainEntry_frame.winfo_height() - total_height) // 2

        canvas = tk.Canvas(self.mainEntry_frame, width=self.mainEntry_frame.winfo_width(),
                           height=self.mainEntry_frame.winfo_height(), highlightthickness=0)
        canvas.pack(fill='both', expand=True)

        canvas.create_line(start_x - bracket_width, start_y, start_x - bracket_width,
                           start_y + total_height, width=2, fill=bracket_color)
        canvas.create_line(start_x + total_width + bracket_width, start_y, start_x + total_width + bracket_width,
                           start_y + total_height, width=2, fill=bracket_color)

        for i in range(rows):
            row_entries = []
            for j in range(columns):
                bg_color = bg_color_constant if j == columns - 1 else bg_color_default
                entry = customtkinter.CTkEntry(self.mainEntry_frame, width=entry_width, height=entry_height,
                                               corner_radius=5, fg_color=bg_color)

                entry.place(x=start_x + j * (entry_width + padding), y=start_y + i * (entry_height + padding))
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
                  x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
                  x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
                  x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
                  x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def resize_matrix(self, event):
        start_x = (self.canvas.winfo_width() - self.columns * (self.cell_size + self.cell_padding)) // 2
        start_y = (self.canvas.winfo_height() - self.rows * (self.cell_size + self.cell_padding)) // 2

        cursor_x = max(self.canvas.canvasx(event.x) - start_x, 0)
        cursor_y = max(self.canvas.canvasy(event.y) - start_y, 0)

        new_columns = max(int(cursor_x / (self.cell_size + self.cell_padding)) + 1, 1)
        new_rows = max(int(cursor_y / (self.cell_size + self.cell_padding)) + 1, 1)

        if new_columns != self.columns or new_rows != self.rows:
            self.columns = min(new_columns, 10)
            self.rows = min(new_rows, 10)
            self.row_box.set(self.rows)
            self.col_box.set(self.columns)
            self.draw_matrix()

    def gauss_jordan(self):
        rows = len(self.matrix_entries)
        columns = len(self.matrix_entries[0])

        matrix = []
        for row_entries in self.matrix_entries:
            row = []
            for entry in row_entries:
                entry_value = entry.get()
                if entry_value:
                    row.append(Fraction(entry_value))
                else:
                    row.append(Fraction(0))
            matrix.append(row)

        for i in range(min(rows, columns)):
            if matrix[i][i] == 0:
                for k in range(i + 1, rows):
                    if matrix[k][i] != 0:
                        matrix[i], matrix[k] = matrix[k], matrix[i]
                        break

            pivot = matrix[i][i]
            if pivot == 0:
                continue

            for k in range(columns):
                matrix[i][k] /= pivot

            for j in range(rows):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(columns):
                        matrix[j][k] -= factor * matrix[i][k]

        self.display_result_matrix(matrix)
        self.display_solution(matrix)

    def display_result_matrix(self, matrix):
        for widget in self.mainResults_frame.winfo_children():
            widget.destroy()

        rows = len(matrix)
        columns = max(len(row) for row in matrix) if matrix else 0
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

    def display_solution(self, matrix):
        for widget in self.mainSolution_frame.winfo_children():
            widget.destroy()

        rows = len(matrix)
        columns = len(matrix[0])
        solution_texts = []

        rank = sum(1 for i in range(rows) if any(matrix[i][j] != 0 for j in range(columns - 1)))
        if rank < rows:
            solution_texts.append("El sistema tiene infinitas soluciones debido a las filas cero.")

        for i in range(rows):
            if all(matrix[i][j] == 0 for j in range(columns - 1)):
                if matrix[i][-1] != 0:
                    solution_texts = ["Sistema inconsistente. No hay solución."]
                    break
                else:
                    continue
            else:
                terms = []
                for j in range(columns - 1):
                    if matrix[i][j] != 0:
                        coefficient = f"{matrix[i][j]:.2f}" if isinstance(matrix[i][j], float) else str(matrix[i][j])
                        terms.append(f"{coefficient}x_{j + 1}")
                constant = matrix[i][-1]
                equation = " + ".join(terms) + f" = {constant}"
                solution_texts.append(equation)

        solution_text = "\n".join(solution_texts)
        if not solution_texts:
            solution_text = "El sistema tiene infinitas soluciones (sistema indeterminado)."

        label = customtkinter.CTkLabel(self.mainSolution_frame, text=solution_text, anchor="w", justify=tk.LEFT)
        label.grid(sticky="nsew", padx=20, pady=20)

    def calculate_inverse(self):
        # Obtener las dimensiones de la matriz de la GUI, excluyendo la columna de términos constantes
        rows = len(self.matrix_entries)
        columns = len(self.matrix_entries[0]) - 1  # Excluir la última columna (términos constantes)

        if rows != columns:
            tkinter.messagebox.showerror("Error",
                                         "La matriz debe ser cuadrada (sin contar la columna de términos constantes) para calcular la inversa.")
            return

        # Crear la matriz aumentada sin incluir la columna de términos constantes
        matrix = []
        for i, row_entries in enumerate(self.matrix_entries):
            row = [Fraction(entry.get() if entry.get() else 0) for entry in
                   row_entries[:-1]]  # Excluir el último elemento de cada fila
            identity = [Fraction(int(i == j)) for j in range(rows)]
            matrix.append(row + identity)

        # Aplicar el método Gauss-Jordan para obtener la inversa
        n = rows
        for i in range(n):
            if matrix[i][i] == 0:  # Buscar un pivote no nulo
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    tkinter.messagebox.showerror("Error", "La matriz es singular y no tiene inversa.")
                    return

            # Normalizar la fila del pivote
            pivot = matrix[i][i]
            matrix[i] = [x / pivot for x in matrix[i]]

            # Eliminar todos los otros elementos en la columna actual
            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    matrix[j] = [matrix[j][k] - factor * matrix[i][k] for k in range(2 * n)]

        # Extraer la matriz inversa de la parte derecha de la matriz aumentada
        inverse_matrix = [row[n:] for row in matrix]

        # Mostrar solo la matriz inversa
        self.display_result_matrix(inverse_matrix)

    def matrix_size(self):
        self.matrix_window = customtkinter.CTkToplevel(self)
        self.matrix_window.title("Adjust Matrix Size")
        self.matrix_window.geometry("600x500")

        bg_color = "#191919" if customtkinter.get_appearance_mode() == "Dark" else "white"
        self.canvas = tk.Canvas(self.matrix_window, bg=bg_color, width=500, height=400)
        self.canvas.pack(pady=20, padx=20)

        self.rows = 3
        self.columns = 4
        self.cell_size = 50
        self.cell_padding = 10


        combobox_style = ttk.Style()
        combobox_style.theme_use('alt')
        combobox_style.configure("TCombobox", fieldbackground=bg_color, background=bg_color,
                                 foreground='black' if customtkinter.get_appearance_mode() == "Light" else 'white')

        self.row_box = ttk.Combobox(self.matrix_window, values=list(range(1, 11)), state="readonly", width=5,
                                    style="TCombobox")
        self.row_box.set(self.rows)
        self.row_box.pack(side='left', padx=20, pady=20)
        self.row_box.bind("<<ComboboxSelected>>", self.update_rows_columns)

        self.col_box = ttk.Combobox(self.matrix_window, values=list(range(1, 11)), state="readonly", width=5,
                                    style="TCombobox")
        self.col_box.set(self.columns)
        self.col_box.pack(side='left', padx=20, pady=20)
        self.col_box.bind("<<ComboboxSelected>>", self.update_rows_columns)

        self.accept_button = customtkinter.CTkButton(self.matrix_window, text="Aceptar", command=self.accept_size)
        self.accept_button.pack(side='right', padx=10, pady=10)

        self.canvas.update()
        self.draw_matrix()
        self.canvas.bind("<B1-Motion>", self.resize_matrix)

    def draw_matrix(self):
        self.canvas.delete("all")
        start_x = (self.canvas.winfo_width() - (self.columns * (self.cell_size + self.cell_padding))) // 2
        start_y = (self.canvas.winfo_height() - (self.rows * (self.cell_size + self.cell_padding))) // 2

        for i in range(self.rows):
            for j in range(self.columns):
                x1 = start_x + j * (self.cell_size + self.cell_padding)
                y1 = start_y + i * (self.cell_size + self.cell_padding)
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.create_rounded_rectangle(x1, y1, x2, y2, radius=10, outline="black", fill="lightgrey")

        bracket_width = 20
        start_x = (self.canvas.winfo_width() - self.columns * (self.cell_size + self.cell_padding)) // 2
        start_y = (self.canvas.winfo_height() - self.rows * (self.cell_size + self.cell_padding)) // 2

        if customtkinter.get_appearance_mode() == "Dark":
            bracket_color = "white"
        else:
            bracket_color = "black"

        self.canvas.create_line(start_x - bracket_width, start_y, start_x - bracket_width,
                                start_y + self.rows * (self.cell_size + self.cell_padding),
                                width=2, fill=bracket_color)
        self.canvas.create_line(start_x + self.columns * (self.cell_size + self.cell_padding) + bracket_width, start_y,
                                start_x + self.columns * (self.cell_size + self.cell_padding) + bracket_width,
                                start_y + self.rows * (self.cell_size + self.cell_padding),
                                width=2, fill=bracket_color)

        self.canvas.create_rectangle(
            start_x + self.columns * (self.cell_size + self.cell_padding) - self.cell_padding,
            start_y + self.rows * (self.cell_size + self.cell_padding) - self.cell_padding,
            start_x + self.columns * (self.cell_size + self.cell_padding),
            start_y + self.rows * (self.cell_size + self.cell_padding),
            fill="red", outline="black", width=2
        )

    def resize_matrix(self, event):
        start_x = (self.canvas.winfo_width() - self.columns * (self.cell_size + self.cell_padding)) // 2
        start_y = (self.canvas.winfo_height() - self.rows * (self.cell_size + self.cell_padding)) // 2

        cursor_x = max(self.canvas.canvasx(event.x) - start_x, 0)
        cursor_y = max(self.canvas.canvasy(event.y) - start_y, 0)

        new_columns = max(int(cursor_x / (self.cell_size + self.cell_padding)) + 1, 1)
        new_rows = max(int(cursor_y / (self.cell_size + self.cell_padding)) + 1, 1)

        if new_columns != self.columns or new_rows != self.rows:
            self.columns = min(new_columns, 10)
            self.rows = min(new_rows, 10)
            self.row_box.set(self.rows)
            self.col_box.set(self.columns)
            self.draw_matrix()

    def accept_size(self):
        rows = int(self.row_box.get())
        columns = int(self.col_box.get())
        self.create_matrix_entries(rows, columns)
        self.matrix_window.destroy()

    def clear_all(self):
        self.create_matrix_entries(3, 4)

        for widget in self.mainResults_frame.winfo_children():
            widget.destroy()

        for widget in self.mainSolution_frame.winfo_children():
            widget.destroy()

    def update_rows_columns(self, event=None):
        self.rows = int(self.row_box.get())
        self.columns = int(self.col_box.get())
        self.draw_matrix()
        self.create_matrix_entries(self.rows, self.columns)

    def toolbar_button_click(self):
        print("Toolbar button clicked")



if __name__ == "__main__":
    root = customtkinter.CTk()
    gj_frame = GaussJordanFrame(root)
    gj_frame.pack(fill="both", expand=True)
    root.mainloop()
