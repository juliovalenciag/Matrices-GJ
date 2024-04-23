
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import customtkinter
import os

class OperationsFrame(customtkinter.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure_mainContent()
        self.configure_toolbar()

        #self.add_matrix_operations(self.firstTool_frame)
        #self.add_matrix_operations(self.secondTool_frame)

        self.create_matrix_entries(self.firstEntry_frame, 3, 3)
        self.create_matrix_entries(self.secondEntry_frame, 3, 3)

    def configure_toolbar(self):
        toolbar_frame = customtkinter.CTkFrame(self, width=150, corner_radius=0)
        toolbar_frame.grid(row=0, column=1, rowspan=5, sticky="nsew")
        toolbar_frame.grid_propagate(False)

        button_info = [
            ("suma.png", "Suma", self.sum_matrices),
            ("resta.png", "Resta", self.subtract_matrices),
            ("multiplicacion.png", "Multiplicación", self.multiply_matrices),
            ("limpiarOp.png", "Reiniciar", self.reset_matrices),
            ("cambiarOp.png", "Tamaño", self.matrix_size),
        ]

        for i, (img_name, text, cmd) in enumerate(button_info):
            image_path = os.path.join("images", img_name)
            try:
                pil_image = Image.open(image_path).resize((80, 30))
                tk_image = ImageTk.PhotoImage(pil_image)
                button = customtkinter.CTkButton(toolbar_frame, image=tk_image, text=text,
                                                 command=cmd, compound="top", fg_color=None, hover_color="gray")
                button.image = tk_image
                button.grid(row=i, column=0, padx=5, pady=5)
            except FileNotFoundError:
                print(f"Error: El archivo {img_name} no se encontró en la carpeta 'images'.")


    def configure_mainContent(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(2, weight=3)
        self.grid_columnconfigure(3, weight=1)

        self.firstEntry_frame = customtkinter.CTkFrame(self)
        self.firstEntry_frame.grid(row=0, rowspan=2, column=0, padx=5, pady=5, sticky="nsew")
        self.first_matrix_entries = self.create_matrix_entries(self.firstEntry_frame, 3, 3)

        self.firstTool_frame = customtkinter.CTkFrame(self)
        self.firstTool_frame.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")

        self.firstResult_frame = customtkinter.CTkFrame(self)
        self.firstResult_frame.grid(row=3, rowspan=2, column=0, padx=5, pady=5, sticky="nsew")

        self.secondEntry_frame = customtkinter.CTkFrame(self)
        self.secondEntry_frame.grid(row=0, rowspan=2, column=2, padx=5, pady=5, sticky="nsew")
        self.second_matrix_entries = self.create_matrix_entries(self.secondEntry_frame, 3, 3)

        self.secondTool_frame = customtkinter.CTkFrame(self)
        self.secondTool_frame.grid(row=2, column=2, padx=5, pady=5, sticky="nsew")

        self.secondResult_frame = customtkinter.CTkFrame(self)
        self.secondResult_frame.grid(row=4, rowspan=2, column=2, padx=5, pady=5, sticky="nsew")

        self.mainResults_frame = customtkinter.CTkFrame(self)
        self.mainResults_frame.grid(row=0,column=3, rowspan=5, padx=5, pady=5, sticky="nsew")

        #self.add_matrix_operations(self.firstTool_frame)
        #self.add_matrix_operations(self.secondTool_frame)

    """
    def add_matrix_operations(self, tool_frame):
        operation_labels = ["Determinantes", "Matriz inversa", "Matriz transpuesta",
                            "Matriz multiplicada por:", "Matriz elevada a:"]
        operation_commands = [self.calculate_determinant, self.calculate_inverse,
                              self.transpose_matrix, self.multiply_matrix, self.power_matrix]

        for i, (label, command) in enumerate(zip(operation_labels, operation_commands)):
            row = customtkinter.CTkFrame(tool_frame)
            row.grid(row=i, column=0, padx=5, pady=2, sticky="ew")

            if "multiplicada por" in label or "elevada a" in label:
                entry = customtkinter.CTkEntry(row, width=50)
                entry.grid(row=0, column=1, sticky="e")
                button = customtkinter.CTkButton(row, text=label.split(':')[0],
                                                 command=lambda e=entry, c=command: c(e.get()),
                                                 fg_color="transparent", hover_color="gray")
            else:
                button = customtkinter.CTkButton(row, text=label, command=command,
                                                 fg_color="transparent", hover_color="gray")
            button.grid(row=0, column=0, sticky="ew")
    """

    def create_matrix_entries(self, frame, rows, columns):
        for widget in frame.winfo_children():
            widget.destroy()

        matrix_entries = []
        frame.update_idletasks()

        for i in range(rows):
            row_entries = []
            for j in range(columns):
                entry = customtkinter.CTkEntry(frame, width=40, height=40)
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            matrix_entries.append(row_entries)

        return matrix_entries

    def matrix_size(self):
        self.matrix_window = customtkinter.CTkToplevel(self)
        self.matrix_window.title("Ajustar el tamaño de matriz para las operaciones")
        self.matrix_window.geometry("800x600")
        bg_color = "#191919" if customtkinter.get_appearance_mode() == "Dark" else "white"

        self.canvas = tk.Canvas(self.matrix_window, bg=bg_color, width=500, height=400)
        self.canvas.pack(pady=20, padx=20)

        self.rows = 3
        self.columns = 3
        self.cell_size = 50
        self.cell_padding = 10

        self.row_box = ttk.Combobox(self.matrix_window, values=list(range(1, 7)), state="readonly", width=5)
        self.row_box.set(self.rows)
        self.row_box.pack(side='left', padx=20, pady=20)
        self.row_box.bind("<<ComboboxSelected>>", self.update_rows_columns)

        self.col_box = ttk.Combobox(self.matrix_window, values=list(range(1, 7)), state="readonly", width=5)
        self.col_box.set(self.columns)
        self.col_box.pack(side='left', padx=20, pady=20)
        self.col_box.bind("<<ComboboxSelected>>", self.update_rows_columns)

        self.accept_button = customtkinter.CTkButton(self.matrix_window, text="Aceptar", command=self.accept_size)
        self.accept_button.pack(side='right', padx=10, pady=10)

        self.after_idle(self.draw_matrix)
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
        bracket_color = "white" if customtkinter.get_appearance_mode() == "Dark" else "black"
        start_x = (self.canvas.winfo_width() - self.columns * (self.cell_size + self.cell_padding)) // 2
        start_y = (self.canvas.winfo_height() - self.rows * (self.cell_size + self.cell_padding)) // 2

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
            fill="red", outline="black", width=2)

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
        self.create_matrix_entries(self.firstEntry_frame, rows, columns)
        self.create_matrix_entries(self.secondEntry_frame, rows, columns)
        self.matrix_window.destroy()

    def update_rows_columns(self, event=None):
        new_rows = int(self.row_box.get())
        new_columns = int(self.col_box.get())

        self.create_matrix_entries(self.firstEntry_frame, new_rows, new_columns)
        self.create_matrix_entries(self.secondEntry_frame, new_rows, new_columns)

    def create_rounded_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1,
                  x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius,
                  x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2,
                  x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius,
                  x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def calculate_determinant(self):
        print("Calculating determinant...")

    def calculate_inverse(self):
        print("Calculating inverse...")

    def transpose_matrix(self):
        print("Transposing matrix...")

    def multiply_matrix(self, value):
        print(f"Multiplying matrix by {value}...")

    def power_matrix(self, power):
        print(f"Raising matrix to the power of {power}...")

    def sum_matrices(self):
        try:
            if not all(entry.winfo_exists() for row in self.first_matrix_entries for entry in row):
                tkinter.messagebox.showerror("Error", "Intento de ejecutar una accion sin entradas.")
                return

            rows = len(self.first_matrix_entries)
            columns = len(self.first_matrix_entries[0])
            if rows != len(self.second_matrix_entries) or any(
                    len(row) != columns for row in self.second_matrix_entries):
                tkinter.messagebox.showerror("Error", "Matrices deben tener la misma dimension.")
                return

            result_matrix = []
            for i in range(rows):
                result_row = []
                for j in range(columns):
                    entry_a = self.first_matrix_entries[i][j].get() or "0"
                    entry_b = self.second_matrix_entries[i][j].get() or "0"
                    result_row.append(int(entry_a) + int(entry_b))
                result_matrix.append(result_row)

            self.display_matrix(result_matrix, self.mainResults_frame)
        except Exception as e:
            tkinter.messagebox.showerror("Error", str(e))

    def subtract_matrices(self):
        try:
            # Obtener el tamaño de las matrices
            rows = len(self.first_matrix_entries)
            columns = len(self.first_matrix_entries[0])
            # Verificar que ambas matrices tienen el mismo tamaño
            if rows != len(self.second_matrix_entries) or any(
                    len(row) != columns for row in self.second_matrix_entries):
                tkinter.messagebox.showerror("Error", "Las matrices deben ser del mismo tamaño para restarlas.")
                return

            result_matrix = []
            for i in range(rows):
                result_row = []
                for j in range(columns):
                    # Convertir los valores de las entradas a enteros y restar
                    entry_a = int(self.first_matrix_entries[i][j].get())
                    entry_b = int(self.second_matrix_entries[i][j].get())
                    result_row.append(entry_a - entry_b)
                result_matrix.append(result_row)

            # Mostrar el resultado en mainResults_frame
            self.display_matrix(result_matrix, self.mainResults_frame)

        except ValueError:
            # Manejar el caso en que las entradas no son números enteros
            tkinter.messagebox.showerror("Error", "Todos los campos deben contener valores numéricos válidos.")
        except Exception as e:
            # Cualquier otro error no anticipado
            tkinter.messagebox.showerror("Error", str(e))

    def multiply_matrices(self):
        try:
            # Asegurarse de que las dimensiones son compatibles para la multiplicación
            a_rows = len(self.first_matrix_entries)
            a_cols = len(self.first_matrix_entries[0])
            b_rows = len(self.second_matrix_entries)
            b_cols = len(self.second_matrix_entries[0])

            if a_cols != b_rows:
                tkinter.messagebox.showerror("Error de multiplicación",
                                             "El número de columnas de la primera matriz debe ser igual al número de filas de la segunda matriz.")
                return

            # Inicializar la matriz de resultado con ceros
            result_matrix = [[0 for _ in range(b_cols)] for _ in range(a_rows)]

            # Realizar la multiplicación de matrices
            for i in range(a_rows):
                for j in range(b_cols):
                    for k in range(a_cols):  # o b_rows, ya que a_cols == b_rows
                        result_matrix[i][j] += int(self.first_matrix_entries[i][k].get()) * int(
                            self.second_matrix_entries[k][j].get())

            # Mostrar el resultado en mainResults_frame
            self.display_matrix(result_matrix, self.mainResults_frame)

        except ValueError:
            # Manejar el caso en que las entradas no son números enteros
            tkinter.messagebox.showerror("Error", "Todos los campos deben contener valores numéricos válidos.")
        except Exception as e:
            # Cualquier otro error no anticipado
            tkinter.messagebox.showerror("Error", str(e))

    def reset_matrices(self):
        self.clear_matrix_entries(self.first_matrix_entries)
        self.clear_matrix_entries(self.second_matrix_entries)

        for widget in self.mainResults_frame.winfo_children():
            widget.destroy()

    def clear_matrix_entries(self, matrix_entries):
        for row in matrix_entries:
            for entry in row:
                entry.delete(0, tk.END)

    def display_matrix(self, matrix, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        for i, row in enumerate(matrix):
            for j, value in enumerate(row):
                label = customtkinter.CTkLabel(frame, text=str(value))
                label.grid(row=i, column=j, padx=5, pady=5)


if __name__ == "__main__":
    root = customtkinter.CTk()
    operations_frame = OperationsFrame(root)
    operations_frame.pack(fill="both", expand=True)
    root.mainloop()