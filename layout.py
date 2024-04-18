from fractions import Fraction

from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import os

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Gauss-Jordan")
        self.geometry(f"{1280}x{720}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure((1, 2, 3), weight=1)

        self.configure_topbar()
        self.configure_sidebar()
        self.configure_mainContent()

    def configure_topbar(self):
        topbar_frame = customtkinter.CTkFrame(self, height=100, corner_radius=0)
        topbar_frame.grid(row=0, column=1, columnspan=3, sticky="nsew")

        button_info = [("importar.png", "Importar", self.toolbar_button_click),
                       ("exportar.png", "Exportar", self.toolbar_button_click),
                       ("resolver.png", "Resolver", self.gauss_jordan),
                       ("inversa.png", "Inversa", self.toolbar_button_click),
                       ("limpiar.png", "Limpiar", self.toolbar_button_click),
                       ("Cambiar.png", "Cambiar tamaño", self.matrix_size),]

        for i, (img_name, text, cmd) in enumerate(button_info):
            try:
                image_path = os.path.join("images", img_name)
                pil_image = Image.open(image_path).resize((50, 50))
                tk_image = ImageTk.PhotoImage(pil_image)
                button = customtkinter.CTkButton(topbar_frame, image=tk_image, text=text, command=cmd, compound="top",
                                                 fg_color=None, hover_color="gray")
                button.image = tk_image
                button.grid(row=0, column=i, padx=10, pady=10)
            except FileNotFoundError:
                print(f"Error: El archivo {img_name} no se encontró en la carpeta 'images'.")

    def toolbar_button_click(self):
        print("Toolbar button clicked")

    def configure_sidebar(self):
        sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        sidebar_frame.grid(row=0, column=0, rowspan=6, sticky="nsew")
        sidebar_frame.grid_rowconfigure(6, weight=1)

        text_label = customtkinter.CTkLabel(sidebar_frame, text="Algebra Lineal",
                                            font=customtkinter.CTkFont(size=20, weight="bold"))
        text_label.grid(row=0, column=0, padx=20, pady=(10, 10))

        buttons_info = [("Gauss-Jordan", self.gauss_jordan), ("Determinantes", self.Determinantes),
                        ("Suma", self.Suma), ("Multiplicacion", self.Multiplicacion),
                        ("Configuración", self.Configuracion)]

        for i, (text, command) in enumerate(buttons_info, start=1):
            button = customtkinter.CTkButton(sidebar_frame, text=text, command=command)
            button.grid(row=i, column=0, padx=20, pady=10)

        appearance_mode_label = customtkinter.CTkLabel(sidebar_frame, text="Appearance Mode:", anchor="w")
        appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        appearance_mode_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        appearance_mode_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 10))
        scaling_label = customtkinter.CTkLabel(sidebar_frame, text="UI Scaling:", anchor="w")
        scaling_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        scaling_optionemenu = customtkinter.CTkOptionMenu(sidebar_frame,
                                                                   values=["80%", "90%", "100%", "110%", "120%"],
                                                                   command=self.change_scaling_event)
        scaling_optionemenu.grid(row=10, column=0, padx=20, pady=(10, 20))
        appearance_mode_optionemenu.set("Dark")
        scaling_optionemenu.set("100%")

    def configure_mainContent(self):
        self.mainEntry_frame = customtkinter.CTkFrame(self)
        self.mainEntry_frame.grid(row=1, column=1, rowspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # Configura todos los espacios de columnas para una expansión uniforme
        for i in range(10):  # Asume un número máximo de columnas, ajusta según sea necesario
            self.mainEntry_frame.grid_columnconfigure(i, weight=1)

        self.mainResults_frame = customtkinter.CTkFrame(self)
        self.mainResults_frame.grid(row=1, column=2, rowspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        for i in range(10):
            self.mainResults_frame.grid_columnconfigure(i, weight=1)

        self.mainSolution_frame = customtkinter.CTkFrame(self)
        self.mainSolution_frame.grid(row=3, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.mainSolution_frame.grid_columnconfigure(0, weight=1)

        # Barra inferior
        self.bottomBar_frame = customtkinter.CTkEntry(self, placeholder_text="Texto de prueba")
        self.bottomBar_frame.grid(row=4, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.bottomBar_frame_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.bottomBar_frame_button_1.grid(row=4, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def create_matrix_entries(self, rows, columns):
        for widget in self.mainEntry_frame.winfo_children():
            widget.destroy()

        total_width = columns * (self.cell_size + self.cell_padding)
        total_height = rows * (self.cell_size + self.cell_padding)

        start_x = max(0, (self.mainEntry_frame.winfo_width() - total_width) // 2)
        start_y = max(0, (self.mainEntry_frame.winfo_height() - total_height) // 2)

        self.matrix_entries = []
        for i in range(rows):
            row_entries = []
            for j in range(columns):
                entry = customtkinter.CTkEntry(self.mainEntry_frame, width=60, height=60, corner_radius=5)
                entry.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")
                self.mainEntry_frame.grid_rowconfigure(i, weight=1)
                self.mainEntry_frame.grid_columnconfigure(j, weight=1)

                entry.place(x=start_x + j * (self.cell_size + self.cell_padding),
                            y=start_y + i * (self.cell_size + self.cell_padding))
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

        self.mainEntry_frame.bind("<Configure>", lambda e: self.update_matrix_layout(rows, columns))

    def update_matrix_layout(self, rows, columns):
        total_width = columns * (self.cell_size + self.cell_padding)
        total_height = rows * (self.cell_size + self.cell_padding)

        start_x = max(0, (self.mainEntry_frame.winfo_width() - total_width) // 2)
        start_y = max(0, (self.mainEntry_frame.winfo_height() - total_height) // 2)

        for i in range(len(self.matrix_entries)):
            for j in range(len(self.matrix_entries[i])):
                entry = self.matrix_entries[i][j]
                entry.place(x=start_x + j * (self.cell_size + self.cell_padding),
                            y=start_y + i * (self.cell_size + self.cell_padding))

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

        self.mainResults_frame.grid_columnconfigure(0, weight=1)
        for i in range(len(matrix)):
            self.mainResults_frame.grid_rowconfigure(i, weight=1)
            for j in range(len(matrix[i])):
                self.mainResults_frame.grid_columnconfigure(j, weight=1)
                value = matrix[i][j]
                label = customtkinter.CTkLabel(self.mainResults_frame, text=str(value), width=100, height=40,
                                               corner_radius=0)
                label.grid(row=i, column=j, padx=(1, 1), pady=(1, 1), sticky="nsew")

    def display_solution(self, matrix):
        for widget in self.mainSolution_frame.winfo_children():
            widget.destroy()

        solution_texts = []
        for i, row in enumerate(matrix):
            if row[i] != 0:
                solution_texts.append(f"x{i + 1} = {row[-1]}")
            else:
                if row[-1] != 0:
                    solution_texts.append("No hay solución.")
                    break

        solution_text = "\n".join(solution_texts)
        label = customtkinter.CTkLabel(self.mainSolution_frame, text=solution_text, width=300, height=200)
        label.grid(row=0, column=0, padx=20, pady=20)

    def Determinantes(self):
        print("Determinantes")

    def Suma(self):
        print("Suma")

    def Multiplicacion(self):
        print("Multiplicacion")

    def Configuracion(self):
        print("Configuracion")

    def sidebar_button_event(self):
        print("Sidebar button clicked")

    def toolbar_button_click(self):
        print("Toolbar button clicked")

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
                  x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
                  x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
                  x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
                  x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def matrix_size(self):
        self.matrix_window = customtkinter.CTkToplevel(self)
        self.matrix_window.title("Adjust Matrix Size")
        self.matrix_window.geometry("600x500")

        self.canvas = tk.Canvas(self.matrix_window, bg='white', width=500, height=400)
        self.canvas.pack(pady=20, padx=20)

        self.rows = 3
        self.columns = 4
        self.cell_size = 50
        self.cell_padding = 10

        self.row_box = ttk.Combobox(self.matrix_window, values=list(range(1, 11)), state="readonly", width=5)
        self.row_box.set(self.rows)
        self.row_box.pack(side='left', padx=10)
        self.row_box.bind("<<ComboboxSelected>>", self.update_rows_columns)

        self.col_box = ttk.Combobox(self.matrix_window, values=list(range(1, 11)), state="readonly", width=5)
        self.col_box.set(self.columns)
        self.col_box.pack(side='left', padx=10)
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

        # Dibujar corchetes alrededor de la matriz
        bracket_width = 20
        self.canvas.create_line(start_x - bracket_width, start_y, start_x - bracket_width,
                                start_y + self.rows * (self.cell_size + self.cell_padding), width=2)
        self.canvas.create_line(start_x + self.columns * (self.cell_size + self.cell_padding) + bracket_width, start_y,
                                start_x + self.columns * (self.cell_size + self.cell_padding) + bracket_width,
                                start_y + self.rows * (self.cell_size + self.cell_padding), width=2)

        # Dibujar el controlador de tamaño
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

    def update_rows_columns(self, event=None):
        self.rows = int(self.row_box.get())
        self.columns = int(self.col_box.get())
        self.draw_matrix()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        customtkinter.set_widget_scaling(int(new_scaling.replace("%", "")) / 100)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
