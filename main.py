from fractions import Fraction
import os
import tkinter as tk
import tkinter.messagebox
import customtkinter
from PIL import ImageTk, Image
from tkinter import ttk
import numpy as np
import modulos.drop_and_drag.drop_and_drag as TKdnd

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
        
        self.setup_scrollbars()


    def configure_midbar(self):
        midbar_frame = customtkinter.CTkFrame(self, width=120, fg_color=None)
        midbar_frame.grid(row=1, rowspan=4, column=1, sticky="ns")

        functionButtons_info =[("gj1.png", "Gauss-Jordan", self.gauss_jordan),
                               ("determinante.png", "Determinante", self.calculate_determinant),
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

        button_info = [("importar.png", "Importar", self.import_document),
                       ("exportar.png", "Exportar", self.export_document),
                       ("limpiar.png", "Reiniciar", self.eliminate),
                       ("Cambiar.png", "Seleccionar tamaño", self.matrix_size)]

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
        
    def setup_scrollbars(self):
        self.results_canvas = tk.Canvas(self.solution_frame, highlightthickness=0)
        self.v_scroll = ttk.Scrollbar(self.solution_frame, orient="vertical", command=self.results_canvas.yview)
        self.h_scroll = ttk.Scrollbar(self.solution_frame, orient="horizontal", command=self.results_canvas.xview)
        self.results_canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")
        self.results_canvas.pack(side="left", fill="both", expand=True)

        self.results_frame = tk.Frame(self.results_canvas)
        window_id = self.results_canvas.create_window((0, 0), window=self.results_frame, anchor='nw')
        self.results_frame.bind("<Configure>", lambda e: self.update_canvas_window(e, window_id))
        
    def update_canvas_window(self, event, window_id):
        canvas_width = max(self.results_frame.winfo_reqwidth(), event.width)
        self.results_canvas.itemconfig(window_id, width=canvas_width)
        self.results_canvas.configure(scrollregion=self.results_canvas.bbox("all"))

    def toggle_theme(self):
        if customtkinter.get_appearance_mode() == "Dark":
            customtkinter.set_appearance_mode("Light")
        else:
            customtkinter.set_appearance_mode("Dark")

    def toolbar_button_click(self, action):
        print(f"{action} button clicked")

    #cambiar tamaño de matriz:
    def matrix_size(self):
        self.matrix_window = customtkinter.CTkToplevel(self)
        self.matrix_window.title("Adjust Matrix Size")
        self.matrix_window.geometry("800x600")
        self.matrix_window.attributes("-topmost", True)

        bg_color = "#191919" if customtkinter.get_appearance_mode() == "Dark" else "white"
        self.canvas = tk.Canvas(self.matrix_window, bg=bg_color, width=500, height=400)
        self.canvas.pack(pady=20, padx=20)

        self.rows = 3
        self.columns = 4
        self.cell_size = 50
        self.cell_padding = 10

        self.row_box = ttk.Combobox(self.matrix_window, values=list(range(1, 7)), state="readonly", width=10)
        self.row_box.set(self.rows)
        self.row_box.pack(side='left', padx=20, pady=20)
        self.row_box.bind("<<ComboboxSelected>>", self.update_rows_columns)

        self.col_box = ttk.Combobox(self.matrix_window, values=list(range(1, 7)), state="readonly", width=10, height=60)
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

        self.canvas.update_idletasks()

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        total_width = self.columns * (self.cell_size + self.cell_padding)
        total_height = self.rows * (self.cell_size + self.cell_padding)

        start_x = (canvas_width - total_width) // 2
        start_y = (canvas_height - total_height) // 2

        for i in range(self.rows):
            for j in range(self.columns):
                x1 = start_x + j * (self.cell_size + self.cell_padding)
                y1 = start_y + i * (self.cell_size + self.cell_padding)
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.create_rounded_rectangle(x1, y1, x2, y2, radius=10, outline="black", fill="lightgrey")

        bracket_color = "white" if customtkinter.get_appearance_mode() == "Dark" else "black"
        bracket_width = 20

        self.canvas.create_line(start_x - bracket_width, start_y, start_x - bracket_width,
                                start_y + total_height, width=2, fill=bracket_color)
        self.canvas.create_line(start_x + total_width + bracket_width, start_y, start_x + total_width + bracket_width,
                                start_y + total_height, width=2, fill=bracket_color)

        bracket_tab_length = 10
        self.canvas.create_line(start_x - bracket_width, start_y, start_x - bracket_width + bracket_tab_length,
                                start_y, width=2, fill=bracket_color)
        self.canvas.create_line(start_x - bracket_width, start_y + total_height, start_x - bracket_width + bracket_tab_length,
                                start_y + total_height, width=2, fill=bracket_color)

        self.canvas.create_line(start_x + total_width + bracket_width, start_y, start_x + total_width,
                                start_y, width=2, fill=bracket_color)
        self.canvas.create_line(start_x + total_width + bracket_width, start_y + total_height, start_x + total_width,
                                start_y + total_height, width=2, fill=bracket_color)

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

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
                  x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
                  x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
                  x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
                  x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def update_rows_columns(self, event=None):
        self.rows = int(self.row_box.get())
        self.columns = int(self.col_box.get())
        self.draw_matrix()
        self.create_matrix_entries(self.rows, self.columns)

    def accept_size(self):
        rows = int(self.row_box.get())
        columns = int(self.col_box.get())
        self.create_matrix_entries(rows, columns)
        self.matrix_window.destroy()

    def create_matrix_entries(self, rows, columns):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        self.matrix_entries = []
        self.matrix_frame.update_idletasks()

        entry_width = max(60, 600 // max(columns, 10))
        entry_height = max(60, 300 // max(rows, 10))
        padding = 5
        bracket_width = 20
        bracket_depth = 10

        is_square = (rows == columns)
        constant_term_column = columns - 1 if not is_square else None

        if customtkinter.get_appearance_mode() == "Dark":
            bg_color_default = "#2C2F33"
            bg_color_constant = "#60656b" if not is_square else bg_color_default
            bracket_color = "white"
            canvas_bg = "#202020"
        else:
            bg_color_default = "white"
            bg_color_constant = "lightgrey" if not is_square else bg_color_default
            bracket_color = "black"
            canvas_bg = "#e3e3e3"

        total_width = columns * (entry_width + padding)
        total_height = rows * (entry_height + padding)

        start_x = bracket_width + padding
        start_y = padding

        canvas = tk.Canvas(self.matrix_frame, width=total_width + 2 * bracket_width + 2 * padding,
                           height=total_height + 2 * padding, bg=canvas_bg, highlightthickness=0)
        canvas.pack(fill='both', expand=True)

        self.draw_brackets(canvas, start_x, start_y, total_width, total_height, bracket_width, bracket_depth,
                           bracket_color)

        for i in range(rows):
            row_entries = []
            for j in range(columns):
                bg_color = bg_color_constant if j == constant_term_column else bg_color_default
                entry = customtkinter.CTkEntry(canvas, width=entry_width, height=entry_height, corner_radius=5,
                                               fg_color=bg_color, font=('Arial', 24))
                entry.place(x=start_x + j * (entry_width + padding), y=start_y + i * (entry_height + padding))
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

    def draw_brackets(self, canvas, start_x, start_y, total_width, total_height, bracket_width, bracket_depth, bracket_color):
        canvas.create_line(start_x - bracket_width, start_y, start_x, start_y, width=2, fill=bracket_color)
        canvas.create_line(start_x - bracket_width, start_y, start_x - bracket_width, start_y + total_height, width=2,
                           fill=bracket_color)
        canvas.create_line(start_x - bracket_width, start_y + total_height, start_x, start_y + total_height, width=2,
                           fill=bracket_color)

        canvas.create_line(start_x + total_width, start_y, start_x + total_width + bracket_width, start_y, width=2,
                           fill=bracket_color)
        canvas.create_line(start_x + total_width + bracket_width, start_y, start_x + total_width + bracket_width,
                           start_y + total_height, width=2, fill=bracket_color)
        canvas.create_line(start_x + total_width, start_y + total_height, start_x + total_width + bracket_width,
                           start_y + total_height, width=2, fill=bracket_color)
        
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
        
        if size > 6:
            try:
                determinant =np.linalg.det(matrix)
                return
            except np.linalg.LinAlgError:
                tkinter.messagebox.showerror("Error", "Algo salio mal y sepa que fue.")
                return
                
                
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

        self.label_determinant = customtkinter.CTkLabel(self.result_frame, text="Determinante:",
                                                        font=('Arial', 30))
        self.label_determinant.configure(
            text=f"Determinante: {determinant}")
        
    def gauss_jordan(self):
        rows = len(self.matrix_entries)
        columns = len(self.matrix_entries[0])

        matrix = []
        
        if rows > 6 or columns > 6:
            
            try:
                for row_entries in self.matrix_entries:
                    row = []
                    for entry in row_entries:
                        entry_value = entry.get()
                        if entry_value:
                            row.append(Fraction(entry_value))
                        else:
                            row.append(Fraction(0))
                    matrix.append(row)
                matrix = np.array(matrix)
                matrix = np.around(matrix, 5)
                matrix = matrix.astype(float)
                matrix = np.linalg.solve(matrix[:, :-1], matrix[:, -1])
                self.display_result_matrix(matrix)
                self.display_solution(matrix)
                return
            except np.linalg.LinAlgError:
                tkinter.messagebox.showerror("Error",)
                return
        
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

        if rows > 4 or columns > 4:        
            self.display_result_matrix(matrix)
            self.display_solution(matrix)
            
        else:
            self.display_result_matrix(matrix)
            self.display_solution(matrix)
            
    def calculate_inverse(self):
        rows = len(self.matrix_entries)
        columns = len(self.matrix_entries[0])
        print ("inversa")
        if rows != columns:
            tkinter.messagebox.showerror("Error",
                                         "La matriz debe ser cuadrada (sin contar la columna de términos constantes) para calcular la inversa.")
            return

        matrix = []
        if rows > 6:
            inverse_matrix =  np.array(matrix)
            try:
                inverse_matrix = np.linalg.inv(inverse_matrix)
                print(inverse_matrix)
                self.display_result_matrix(inverse_matrix)
                return
            except np.linalg.LinAlgError:
                tkinter.messagebox.showerror("Error",
                                             "La matriz es singular y no tiene inversa.")
                return
            
        print("aqui")    
        for i, row_entries in enumerate(self.matrix_entries):
            row = [Fraction(entry.get() if entry.get() else 0) for entry in
                   row_entries]
            identity = [Fraction(int(i == j)) for j in range(rows)]
            matrix.append(row + identity)

        n = rows
        for i in range(n):
            if matrix[i][i] == 0:
                for j in range(i + 1, n):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    tkinter.messagebox.showerror("Error", "La matriz es singular y no tiene inversa.")
                    return

            pivot = matrix[i][i]
            matrix[i] = [x / pivot for x in matrix[i]]

            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    matrix[j] = [matrix[j][k] - factor * matrix[i][k] for k in range(2 * n)]

        inverse_matrix = [row[n:] for row in matrix]
        print(inverse_matrix)

        self.display_result_matrix(inverse_matrix)
        
    def import_document(self):
        TKdnd.import_document(self, "<GJ>")
    
    def export_document(self):
        TKdnd.export_document(self)
        
    def eliminate(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        for widget in self.matrix_frame.winfo_children():
            widget.destroy()
            
        self.label_determinant.configure(text="Determinante:")

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
