"""
Algebra Lineal
main file for the Algebra Lineal project

This file contains the main class that will be used to run the application.
"""

# libreria encargada de las fracciones
from fractions import Fraction

# libreria encargada del sistema de archivos
import os

# librerias encargada de la interfaz grafica
import tkinter as tk
import tkinter.messagebox
import customtkinter
from tkinter import ttk
import tkinter.font as tkfont


# libreria encargada de las imagenes
from PIL import ImageTk, Image

# libreria encargada de las matrices
import matplotlib
import matplotlib.pyplot
import numpy as np

# modulos externos
import modulos.drop_and_drag.drop_and_drag as TKdnd
from modulos.verificador_variables.verificador import verificador_de_variables

# define los temas de la interfaz grafica
customtkinter.set_appearance_mode("Light")  # Configura el tema oscuro
customtkinter.set_default_color_theme(
    "dark-blue")  # Configura el tema de color


class App(customtkinter.CTk):

    """
    #Clase principal de la aplicacion
    #hereda de customtkinter.CTk
    #contiene los metodos necesarios para la interfaz grafica

    #metodos:
        contructores:
    # - __init__(self) -> None

        esqueleto
    # - configure_grid_layout(self) -> None
    # - create_main_content(self) -> None
    # - configure_midbar(self) -> None
    # - configure_topbar(self) -> None
    # - setup_scrollbars(self) -> None
    # - update_canvas_window(self, event, window_id) -> None
    # - toggle_theme(self) -> None

        funciones de la barra de herramientas
    # - toolbar_button_click(self, action) -> None #se usa para probar los botones de la barra de herramientas
    # - import_document(self) -> None
    # - export_document(self) -> None
    # - eliminate(self) -> None
    # - calculate_determinant(self) -> None
    # - gauss_jordan(self) -> None
    # - calculate_inverse(self) -> None

        funciones para el dibujo de las matrices
    # - matrix_size(self) -> None
    # - draw_matrix(self) -> None
    # - resize_matrix(self, event) -> None
    # - create_rounded_rectangle(self, x1, y1, x2, y2, type_e, radius=25, **kwargs) -> None
    # - update_rows_columns(self, event=None) -> None
    # - accept_size(self) -> None
    # - create_matrix_entries(self, rows, columns) -> None
    # - display_result_matrix(self, matrix) -> None
    # - display_solution(self, matrix) -> None
    # - run(self) -> None


    """

#################### _____________esqueleto_inicio______________#########################
    def __init__(self):
        super().__init__()

        self.title("Algebra Lineal")
        self.geometry("1280x720")

        self.configure_grid_layout()

        self.configure_topbar()
        self.create_main_content()
        self.configure_midbar()
        self.matrix_result = None

    def configure_grid_layout(self):
        """
        funcion que configura el layout grid
        """
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=0, minsize=120)
        self.grid_columnconfigure(2, weight=2)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=3)
        self.grid_rowconfigure(3, weight=3)
        self.grid_rowconfigure(4, weight=0)

    def create_main_content(self):
        """
        crea los frame directores de las zonas de la matriz de entrada,
        zona resultado de texto y zona de resultado de matriz
        """
        self.matrix_frame_container = customtkinter.CTkFrame(self)
        self.matrix_frame_container.grid(row=1, rowspan=4, column=0, sticky="nsew", padx=20, pady=20)

        # Configurar canvas y scrollbars
        self.matrix_canvas = tk.Canvas(self.matrix_frame_container, bg="#f0f0f0", highlightthickness=0)
        self.v_scroll = ttk.Scrollbar(self.matrix_frame_container, orient="vertical", command=self.matrix_canvas.yview)
        self.h_scroll = ttk.Scrollbar(self.matrix_frame_container, orient="horizontal",
                                      command=self.matrix_canvas.xview)
        self.matrix_canvas.configure(yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        self.matrix_canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")

        self.matrix_frame_container.grid_rowconfigure(0, weight=1)
        self.matrix_frame_container.grid_columnconfigure(0, weight=1)

        # Crear un frame interno para la matriz dentro del canvas
        self.matrix_frame = customtkinter.CTkFrame(self.matrix_canvas)
        self.matrix_window_id = self.matrix_canvas.create_window((0, 0), window=self.matrix_frame, anchor="nw")

        self.solution_frame = customtkinter.CTkFrame(self, border_width=2, border_color="gray")
        self.solution_frame.grid(row=1, rowspan=3, column=2, sticky="nsew", padx=20, pady=(20, 0))

        self.result_frame = customtkinter.CTkFrame(self, border_width=2, border_color="gray")
        self.result_frame.grid(row=4, column=2, sticky="nsew", padx=20, pady=20)

        self.setup_scrollbars()
        self.eliminate()

        # Actualizar la región de scroll del canvas
        self.matrix_frame.bind("<Configure>", self.update_matrix_canvas)

    def update_matrix_canvas(self, event):
        self.matrix_canvas.configure(scrollregion=self.matrix_canvas.bbox("all"))

    def configure_midbar(self):
        """
        configura la pestaña intermedia de operaciones a matrices
        """
        midbar_frame = customtkinter.CTkFrame(self, width=120, fg_color=None)
        midbar_frame.grid(row=1, rowspan=4, column=1, sticky="ns")

        functionButtons_info = [("gj1.png", "Gauss-Jordan", self.gauss_jordan),
                                ("determinante.png", "Determinante",
                                self.calculate_determinant),
                                ("inversa.png", "Inversa", self.calculate_inverse),
                                ]

        for i, (img_name, text, cmd) in enumerate(functionButtons_info):
            try:
                image_path = os.path.join("images", img_name)
                pil_image = Image.open(image_path).resize((50, 50))
                tk_image = ImageTk.PhotoImage(pil_image)
                button = customtkinter.CTkButton(midbar_frame, image=tk_image, text=text, command=cmd,
                                                 compound="top", fg_color="#0D87BF", hover_color="gray", font=('Arial', 24))
                button.image = tk_image
                button.grid(row=i, column=0, padx=10, pady=10)
            except FileNotFoundError:
                print(
                    f"Error: El archivo {img_name} no se encontró en la carpeta 'images'.")

    def configure_topbar(self):
        """
        configura la pestaña superior de herramientas
        """
        topbar_frame = customtkinter.CTkFrame(
            self, height=100, corner_radius=0)
        topbar_frame.grid(row=0, column=0, columnspan=3,
                          sticky="nsew", pady=10)

        button_info = [("importar.png", "Importar", self.import_document),
                       ("Cambiar.png", "Seleccionar tamaño", self.matrix_size),
                       ("exportar.png", "Exportar", self.export_document),
                       ("limpiar.png", "Reiniciar", self.eliminate),
                       ("exportarSalida.png", "Exportar resultado",
                        self.export_document_result)
                       ]

        for i, (img_name, text, cmd) in enumerate(button_info):
            try:
                image_path = os.path.join("images", img_name)
                pil_image = Image.open(image_path).resize((50, 50))
                tk_image = ImageTk.PhotoImage(pil_image)
                button = customtkinter.CTkButton(topbar_frame, image=tk_image, text=text, command=cmd,
                                                 compound="top",
                                                 fg_color="#0D87BF", hover_color="gray", font=('Arial', 24))
                button.image = tk_image
                button.grid(row=0, column=i, padx=10, pady=10)
            except FileNotFoundError:
                print(
                    f"Error: El archivo {img_name} no se encontró en la carpeta 'images'.")

        # self.appearance_switch = customtkinter.CTkSwitch(
           # topbar_frame, text="Cambiar tema", command=self.toggle_theme, font=('Arial', 24))
        # self.appearance_switch.grid(
           # row=0, column=8, padx=10, pady=10, sticky="e")

    def setup_scrollbars(self):
        """
        Configura sobre la zona de resultado de la matriz, un canvas que permite
        un área de trabajo más amplia con posibilidad de consulta con scrollbar
        """
        bg_co = "#ececec" if customtkinter.get_appearance_mode() == "Light" else "#202020"

        # Elimina cualquier scrollbar existente antes de agregar nuevos
        for widget in self.solution_frame.winfo_children():
            widget.destroy()

        self.results_canvas = tk.Canvas(
            self.solution_frame, highlightthickness=0, bg=bg_co)
        self.v_scroll = ttk.Scrollbar(
            self.solution_frame, orient="vertical", command=self.results_canvas.yview)
        self.h_scroll = ttk.Scrollbar(
            self.solution_frame, orient="horizontal", command=self.results_canvas.xview)
        self.results_canvas.configure(
            yscrollcommand=self.v_scroll.set, xscrollcommand=self.h_scroll.set)

        self.results_canvas.grid(row=0, column=0, sticky="nsew")
        self.v_scroll.grid(row=0, column=1, sticky="ns")
        self.h_scroll.grid(row=1, column=0, sticky="ew")

        # Configura las filas y columnas de la cuadrícula
        self.solution_frame.grid_rowconfigure(0, weight=1)
        self.solution_frame.grid_columnconfigure(0, weight=1)

        # Crear un marco desplazable dentro del canvas
        self.results_scroll = tk.Frame(self.results_canvas)
        self.results_scroll_id = self.results_canvas.create_window(
            (0, 0), window=self.results_scroll, anchor='nw')

        self.results_scroll.bind("<Configure>", self.update_canvas_window)
        self.results_canvas.bind("<Configure>", self.update_scroll_region)

    def update_canvas_window(self, event):
        """
        Función que actualiza las propiedades del scrollbar en ejecución
        """
        self.results_canvas.configure(
            scrollregion=self.results_canvas.bbox("all"))

    def update_scroll_region(self, event):
        """
        Función que actualiza las propiedades del scrollbar en ejecución
        """
        self.results_canvas.configure(
            scrollregion=self.results_canvas.bbox("all"))

    def toggle_theme(self):
        """
        cambia el tema de la interfaz
        """
        if customtkinter.get_appearance_mode() == "Dark":
            customtkinter.set_appearance_mode("Light")

        else:
            customtkinter.set_appearance_mode("Dark")

    def toolbar_button_click(self, action):
        """
        función relleno para puerbas
        """
        print(f"{action} button clicked")

    # cambiar tamaño de matriz:
    def matrix_size(self):
        """
        gestiona una ventana emergente que permite el elegir una ventana 

        """
        self.eliminate()
        self.matrix_window = customtkinter.CTkToplevel(self)
        self.matrix_window.title("Adjust Matrix Size")
        self.matrix_window.geometry("1200x800")
        self.matrix_window.attributes("-topmost", True)

        bg_color = "#191919" if customtkinter.get_appearance_mode() == "Dark" else "white"
        self.canvas = tk.Canvas(self.matrix_window, bg=bg_color, width=800, height=650)
        self.canvas.pack(pady=20, padx=20)

        self.rows = 3
        self.columns = 4
        self.cell_size = 50
        self.cell_padding = 10

        self.row_box = ttk.Combobox(self.matrix_window, values=list(
            range(1, 10)), state="readonly", width=10)
        self.row_box.set(self.rows)
        self.row_box.pack(side='left', padx=20, pady=20)
        self.row_box.bind("<<ComboboxSelected>>", self.update_rows_columns)

        self.col_box = ttk.Combobox(self.matrix_window, values=list(
            range(1, 10)), state="readonly", width=10, height=60)
        self.col_box.set(self.columns)
        self.col_box.pack(side='left', padx=20, pady=20)
        self.col_box.bind("<<ComboboxSelected>>", self.update_rows_columns)

        self.accept_button = customtkinter.CTkButton(
            self.matrix_window, text="Aceptar", command=self.accept_size)
        self.accept_button.pack(side='right', padx=10, pady=10)

        self.canvas.update()
        self.draw_matrix()
        self.canvas.bind("<B1-Motion>", self.resize_matrix)

    def draw_matrix(self):
        """
        dibuja la matriz en redimensionar la matriz
        """
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
                self.create_rounded_rectangle(
                    x1, y1, x2, y2, radius=10, outline="black", type_e=self.canvas, fill="lightgrey")

        bracket_color = "white" if customtkinter.get_appearance_mode() == "Dark" else "black"
        bracket_width = 20

        self.canvas.create_line(start_x - bracket_width, start_y, start_x - bracket_width,
                                start_y + total_height, width=2, fill=bracket_color)
        self.canvas.create_line(start_x + total_width + bracket_width, start_y, start_x + total_width + bracket_width,
                                start_y + total_height, width=2, fill=bracket_color)

        bracket_tab_length = 20
        self.canvas.create_line(start_x - bracket_width, start_y, start_x - bracket_width + bracket_tab_length,
                                start_y, width=2, fill=bracket_color)
        self.canvas.create_line(start_x - bracket_width, start_y + total_height, start_x - bracket_width + bracket_tab_length,
                                start_y + total_height, width=2, fill=bracket_color)

        self.canvas.create_line(start_x + total_width + bracket_width, start_y, start_x + total_width,
                                start_y, width=2, fill=bracket_color)
        self.canvas.create_line(start_x + total_width + bracket_width, start_y + total_height, start_x + total_width,
                                start_y + total_height, width=2, fill=bracket_color)

        self.canvas.create_rectangle(
            start_x + self.columns *
            (self.cell_size + self.cell_padding) - self.cell_padding,
            start_y + self.rows *
            (self.cell_size + self.cell_padding) - self.cell_padding,
            start_x + self.columns * (self.cell_size + self.cell_padding),
            start_y + self.rows * (self.cell_size + self.cell_padding),
            fill="red", outline="black", width=2
        )

    def resize_matrix(self, event):
        """
        funciona para redimensionar la matriz en la ventana emergente de redimensionar matriz
        """
        start_x = (self.canvas.winfo_width() - self.columns *
                   (self.cell_size + self.cell_padding)) // 2
        start_y = (self.canvas.winfo_height() - self.rows *
                   (self.cell_size + self.cell_padding)) // 2

        cursor_x = max(self.canvas.canvasx(event.x) - start_x, 0)
        cursor_y = max(self.canvas.canvasy(event.y) - start_y, 0)

        new_columns = max(
            int(cursor_x / (self.cell_size + self.cell_padding)) + 1, 1)
        new_rows = max(
            int(cursor_y / (self.cell_size + self.cell_padding)) + 1, 1)

        if new_columns != self.columns or new_rows != self.rows:
            self.columns = min(new_columns, 10)
            self.rows = min(new_rows, 10)
            self.row_box.set(self.rows)
            self.col_box.set(self.columns)
            self.draw_matrix()

    def create_rounded_rectangle(self, x1, y1, x2, y2, type_e, radius=25, **kwargs):
        """
        crea un rectagulo de arrastre rojo de la ventana emergente
        """
        points = [x1+radius, y1,
                  x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
                  x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
                  x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
                  x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
                  x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return type_e.create_polygon(points, **kwargs, smooth=True)

    def update_rows_columns(self, event=None):
        """
        crea mas columnas o filas en la ventana emergente de redimensionar matriz
        """
        self.rows = int(self.row_box.get())
        self.columns = int(self.col_box.get())
        self.draw_matrix()
        self.create_matrix_entries(self.rows, self.columns)

    def accept_size(self):
        """
        funcionalidad del boton de aceptar tamaño de matriz
        """
        rows = int(self.row_box.get())
        columns = int(self.col_box.get())
        self.create_matrix_entries(rows, columns)
        self.matrix_window.destroy()

    def create_matrix_entries(self, rows, columns):
        """
        dibuja la matriz una vez se importa o se redimensiona la matriz
        """
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
            canvas_bg = "#ececec"

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
                entry.place(x=start_x + j * (entry_width + padding),
                            y=start_y + i * (entry_height + padding))
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

        # Actualizar la región de scroll del canvas
        self.matrix_frame.update_idletasks()
        self.update_matrix_canvas(None)

    def draw_brackets(self, canvas, start_x, start_y, total_width, total_height, bracket_width, bracket_depth,
                      bracket_color):
        """
        Dibuja los corchetes de las matrices en el canvas
        """
        # Corchete izquierdo
        canvas.create_line(start_x - bracket_width, start_y,
                           start_x, start_y, width=2, fill=bracket_color)
        canvas.create_line(start_x - bracket_width, start_y, start_x - bracket_width, start_y + total_height, width=2,
                           fill=bracket_color)
        canvas.create_line(start_x - bracket_width, start_y + total_height, start_x, start_y + total_height, width=2,
                           fill=bracket_color)

        # Corchete derecho
        canvas.create_line(start_x + total_width, start_y, start_x + total_width + bracket_width, start_y, width=2,
                           fill=bracket_color)
        canvas.create_line(start_x + total_width + bracket_width, start_y, start_x + total_width + bracket_width,
                           start_y + total_height, width=2, fill=bracket_color)
        canvas.create_line(start_x + total_width, start_y + total_height, start_x + total_width + bracket_width,
                           start_y + total_height, width=2, fill=bracket_color)

    def calculate_determinant(self):
        """
        función que calcula el determinante
        """
        if self.results_scroll.winfo_exists():
            for widget in self.results_scroll.winfo_children():
                widget.destroy()

        if self.result_frame.winfo_exists():
            for widget in self.result_frame.winfo_children():
                widget.destroy()

        if customtkinter.get_appearance_mode() == "Dark":
            color_te = "white"
        else:
            color_te = "black"

        if not self.matrix_entries:
            tkinter.messagebox.showinfo(
                "Información", "Primero ingresa la matriz.")
            return

        size = len(self.matrix_entries)
        columns = len(self.matrix_entries[0])
        if size != columns:
            tkinter.messagebox.showerror("Error",
                                         "La matriz debe ser cuadrada (sin contar la columna de términos constantes) para calcular el determinante.")
            return

        matrix = []

        if size > 6:
            try:
                for row_entries in self.matrix_entries:
                    row = [float(Fraction(entry.get() if entry.get() else '0'))
                           for entry in row_entries]
                    matrix.append(row)

                matrix = np.array(matrix, dtype=np.float64)
                determinant = np.linalg.det(matrix)
                label = customtkinter.CTkLabel(
                    self.result_frame, text=f"Determinante: {determinant}", anchor="w", justify=tk.LEFT, font=('Arial', 20), text_color=color_te)
                label.grid(sticky="nsew", padx=20, pady=20)
                return

            except np.linalg.LinAlgError:
                tkinter.messagebox.showerror(
                    "Error", "Algo salio mal y sepa que fue.")
                return

        for row_entries in self.matrix_entries:
            row = [Fraction(entry.get() if entry.get() else '0')
                   for entry in row_entries]
            matrix.append(row)

        determinant = 1
        for i in range(size):
            if matrix[i][i] == 0:  # Buscar un pivot no cero en la columna i
                for k in range(i + 1, size):
                    if matrix[k][i] != 0:
                        # Intercambiar filas
                        matrix[i], matrix[k] = matrix[k], matrix[i]
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

        label = customtkinter.CTkLabel(
            self.result_frame, text=f"Determinante: {determinant}", anchor="w", justify=tk.LEFT, font=('Arial', 20), text_color=color_te)
        label.grid(sticky="nsew", padx=20, pady=20)

    def gauss_jordan(self):
        """
        función que culcula el sistemas de ecuaciones por gauss-jordan
        """
        self.matrix_result = None
        rows = len(self.matrix_entries)
        columns = len(self.matrix_entries[0])

        matrix = []

        # if rows > 5 or columns > 5:

        #     try:
        #         for row_entries in self.matrix_entries:
        #             row = []
        #             for entry in row_entries:
        #                 entry_value = entry.get()
        #                 if entry_value:
        #                     row.append(float(Fraction(entry_value)))
        #                 else:
        #                     row.append(0.0)
        #             matrix.append(row)

        #         matrix = np.array(matrix, dtype=np.float64)
        #         matrix = np.around(matrix, 5)
        #         matrix = matrix.astype(float)
        #         matrix = np.linalg.solve(matrix[:, :-1], matrix[:, -1])
        #         self.display_result_matrix(matrix)
        #         self.display_solution(matrix)
        #         return
        #     except np.linalg.LinAlgError:
        #         tkinter.messagebox.showerror(
        #             "Error", "No se puede resolver el sistema de ecuaciones.")
        #         return

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
        """
        función que culcula la inversa
        """
        self.matrix_result = None
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        rows = len(self.matrix_entries)
        columns = len(self.matrix_entries[0])
        if rows != columns:
            tkinter.messagebox.showerror("Error",
                                         "La matriz debe ser cuadrada (sin contar la columna de términos constantes) para calcular la inversa.")
            return

        matrix = []
        if rows > 5:
            for row_entries in self.matrix_entries:
                row = []
                for entry in row_entries:
                    entry_value = entry.get()
                    if entry_value:
                        row.append(float(entry_value))
                    else:
                        row.append(0.0)
                matrix.append(row)
            inverse_matrix = np.array(matrix)
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
                    tkinter.messagebox.showerror(
                        "Error", "La matriz es singular y no tiene inversa.")
                    return

            pivot = matrix[i][i]
            matrix[i] = [x / pivot for x in matrix[i]]

            for j in range(n):
                if i != j:
                    factor = matrix[j][i]
                    matrix[j] = [matrix[j][k] - factor * matrix[i][k]
                                 for k in range(2 * n)]

        inverse_matrix = [row[n:] for row in matrix]
        print(inverse_matrix)

        self.display_result_matrix(inverse_matrix)

    def display_result_matrix(self, matrix):
        """
        Función que se encarga de mostrar la matriz de resultado
        """
        # Verifica que los scrollbars estén configurados
        if not hasattr(self, 'results_scroll') or not self.results_scroll.winfo_exists():
            self.setup_scrollbars()

        # Limpia el canvas antes de dibujar
        self.results_canvas.delete("all")
        for widget in self.results_scroll.winfo_children():
            widget.destroy()

        if isinstance(matrix, np.ndarray):
            new_matrix = []
            for row in matrix:
                new_matrix.append([Fraction(x).limit_denominator(100000) for x in row])

            matrix = new_matrix
            columns = max(len(row) for row in matrix) if np.size(matrix) > 0 else 0
            
        else:
            columns = max(len(row) for row in matrix) if matrix else 0
            
        rows = len(matrix)
        print(matrix)
        entry_width = max(len(max((str(max(int(s.denominator), int(s.numerator)))
                                   for row in matrix for s in row), key=len))*14, 40)
        entry_height = max(30, 300 // max(rows, 10))
        # entry_width = max(80, 800 // max(columns, 10))
        padding = 15  # Ajuste del padding
        bracket_width = 20
        bracket_depth = 10
        control = False
        
        for row in matrix:
            for s in row:
                print(s.denominator, s.denominator != 1, '\n')
        array = [s.denominator == 1 for row in matrix for s in row]
        print(array)
        if (array.count(False) != 0):
            control = True
            total_height = rows * (entry_height + padding) * 2
        else:
            total_height = rows * (entry_height + padding)

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
            canvas_bg = "#ececec"

        start_x = bracket_width
        start_y = padding
        total_width = columns * (entry_width + padding)

        for i in range(rows):
            for j in range(columns):
                value = matrix[i][j]
                bg_color = bg_color_constant if j == constant_term_column else bg_color_default
                # entry = customtkinter.CTkEntry(self.results_canvas, width=entry_width, height=entry_height,
                #                               corner_radius=5, fg_color=bg_color, font=('Arial', 24), state="disabled")
                # entry_2 = customtkinter.CTkEntry(self.results_canvas, width=entry_width, height=entry_height,
                #                               corner_radius=5, fg_color=bg_color, font=('Arial', 24), state="disabled")
                # entry_2.insert(0, str(Fraction(value).denominator))
                if control and value.denominator != 1:
                    entry = customtkinter.CTkLabel(self.results_canvas, width=entry_width, height=entry_height,
                                                   corner_radius=5, fg_color=bg_color, font=('Arial', 24), justify="center", text="0")
                    entry_2 = customtkinter.CTkLabel(self.results_canvas, width=entry_width, height=entry_height,
                                                     corner_radius=5, fg_color=bg_color, font=('Arial', 24), justify="center", text="1")
                    entry = customtkinter.CTkLabel(self.results_canvas, width=entry_width, height=entry_height,
                                                   corner_radius=5, fg_color=bg_color, font=('Arial', 24), justify="center", text=str(Fraction(value).numerator))
                    entry_2 = customtkinter.CTkLabel(self.results_canvas, width=entry_width, height=entry_height,
                                                     corner_radius=5, fg_color=bg_color, font=('Arial', 24), justify="center", text=str(Fraction(value).denominator))
                    self.results_canvas.create_window((start_x + 10 + entry_width/2) + j * (entry_width + padding),
                                                      (start_y + 30) + i * (entry_height + padding)*2, window=entry)
                    self.results_canvas.create_line((start_x + 10) + j * (entry_width + padding) - 5,
                                                    (start_y + 30) + i * (entry_height +
                                                                          padding)*2 + entry_height/2 + 2,
                                                    (start_x + 10) + j * (entry_width +
                                                                          padding) + entry_width + 5,
                                                    (start_y + 30) + i * (entry_height + padding)*2 + entry_height/2 + 2)
                    self.results_canvas.create_window((start_x + 10 + entry_width/2) + j * (entry_width + padding),
                                                      (start_y + 30) + i * (entry_height + padding)*2 + entry_height + 5, window=entry_2)

                elif control:
                    entry = customtkinter.CTkLabel(self.results_canvas, width=entry_width, height=entry_height*2,
                                                   corner_radius=5, fg_color=bg_color, font=('Arial', 24), justify="center", text=str(value))
                    self.results_canvas.create_window((start_x + 10 + entry_width/2) + j * (entry_width + padding),
                                                      (start_y + 30) + i * (entry_height + padding)*2 + entry_height/2, window=entry)
                else:
                    entry = customtkinter.CTkLabel(self.results_canvas, width=entry_width, height=entry_height,
                                                   corner_radius=5, fg_color=bg_color, font=('Arial', 24), justify="center", text=str(value))
                    self.results_canvas.create_window((start_x + 10 + entry_width/2) + j * (entry_width + padding),
                                                      (start_y + 30) + i * (entry_height + padding), window=entry)

        self.draw_brackets(self.results_canvas, start_x, start_y, total_width, total_height, bracket_width,
                           bracket_depth, bracket_color)

        self.results_scroll.update_idletasks()
        self.results_canvas.configure(
            scrollregion=self.results_canvas.bbox("all"))
        self.matrix_result = matrix

    def display_solution(self, matrix):
        """
        función que se encarga de mostrar el texto de solución
        """
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        rows = len(matrix)
        columns = len(matrix[0])
        solution_texts = []
        error_message = ""

        rank = sum(1 for i in range(rows) if any(
            matrix[i][j] != 0 for j in range(columns - 1)))
        if rank < rows:
            error_message = "El sistema tiene infinitas soluciones debido a las filas cero.\n"

        terminos_sin = []
        for i in range(rows):
            if all(matrix[i][j] == 0 for j in range(columns - 1)):
                if matrix[i][-1] != 0:
                    error_message = "Sistema inconsistente. No hay solución.\n"
                    break
                else:
                    continue
            else:
                if len(terminos_sin) <= i:
                    terminos_sin.append([])
                terms = []
                for j in range(columns - 1):
                    if matrix[i][j] != 0:
                        coefficient = str(matrix[i][j])
                        if coefficient == "1":
                            terms.append(f"x{self.subscript(j + 1)}")
                            terminos_sin[i].append(f"x{self.subscript(j + 1)}")
                            continue

                        terms.append(f"{coefficient}x{self.subscript(j + 1)}")
                constant = matrix[i][-1]
                equation = terms[0] + " = " + " - ".join(terms[1:]) + (f"{constant}" if len(terms) == 1 else (
                    " + " + str(constant) if constant > 0 else ("" if constant == 0 else str(constant))))
                solution_texts.append(equation)

        if error_message == "Sistema inconsistente. No hay solución.\n":
            print(error_message)
            self.matrix_frame.update_idletasks()
            label = customtkinter.CTkLabel(
                self.result_frame, text=error_message, anchor="w", justify=tk.LEFT, font=('Arial', 20))
            label.grid(sticky="nsew", padx=10, pady=10)
            return

        soluciones_infinitas, variables = verificador_de_variables(
            terminos_sin)
        solution_text = error_message
        variables.sort()
        solution_text += "{ " + "( " + ",".join(variables) + " ) |" + "\n"
        solution_text += "\n".join(solution_texts)

        if not solution_texts:
            solution_text = "El sistema tiene infinitas soluciones (sistema indeterminado)."

        if soluciones_infinitas:
            if len(soluciones_infinitas) == 1:
                solution_text += "\n & " + soluciones_infinitas[0] + " }"
            elif len(soluciones_infinitas) == 2:
                solution_text += ",\n" + \
                                 soluciones_infinitas[0] + " & " + \
                                 soluciones_infinitas[1] + " }"
            else:
                solution_text += ",\n" + \
                                 ", ".join(soluciones_infinitas[0:-2]) + \
                                 "&" + soluciones_infinitas[-1] + " }"
        else:
            solution_text += " }\n"

        print(solution_text)
        self.matrix_frame.update_idletasks()
        label = customtkinter.CTkLabel(
            self.result_frame, text=solution_text, anchor="w", justify=tk.LEFT, font=('Arial', 20))
        label.grid(sticky="nsew", padx=20, pady=20)

    def subscript(self, n):
        subscript_map = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        return str(n).translate(subscript_map)

    def import_document(self):
        """
        función que importa matrices
        """
        self.eliminate()
        TKdnd.import_document(self, "<GJ>")
        self.matrix_frame.update_idletasks()

    def export_document(self):
        """
        función que exporta la matriz
        """
        TKdnd.export_document(self)
        self.matrix_frame.update_idletasks()

    def export_document_result(self):
        """
        función que exporta_result la matriz
        """
        TKdnd.export_document_result(self)
        self.matrix_frame.update_idletasks()

    def eliminate(self):
        """
        Función que elimina todas las entradas y limpia todos los frames
        """
        # Limpiar matrix_frame
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        # Limpiar results_scroll
        if hasattr(self, 'results_scroll'):
            for widget in self.results_scroll.winfo_children():
                widget.destroy()

        # Limpiar result_frame
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        # Limpiar results_canvas
        if hasattr(self, 'results_canvas'):
            self.results_canvas.delete("all")

        if customtkinter.get_appearance_mode() == "Dark":
            fg_co = "#202020"
            text_co = "white"
        else:
            fg_co = "#e3e3e3"
            text_co = "black"

        # Mensaje por defecto en matrix_frame
        message_label = customtkinter.CTkLabel(
            self.matrix_frame,
            text="Importa una matriz o selecciona\n un tamaño de matriz",
            corner_radius=5,
            fg_color=fg_co,
            text_color=text_co,
            anchor='center',
            font=('Arial', 24)
        )
        message_label.pack(fill='both', expand=True, padx=20, pady=20)
        self.matrix_result = None
        self.update_matrix_canvas(None)

    def run(self):
        """
        función de arranque de la aplicación
        """
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()
