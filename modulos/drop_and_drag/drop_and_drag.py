# modulo encargado de desplegar una ventana para el drop and drag
from fractions import Fraction
import os
from turtle import onclick
from PIL import ImageTk, Image
from tkinter import BOTTOM, END, StringVar, filedialog, TOP
import tkinter.messagebox
from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter


class Window_drag_and_drop(customtkinter.CTkToplevel, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


def import_document(secondary_window, page:str = ""):
    def get_path(event):
        nameVarString.set(event.data)
        file_name = os.path.normpath(event.data)
        if file_name and nameVarString.get().endswith(".txt"):  # Verifica si se seleccionó un archivo
            try:
                with open(file_name, 'r') as file:  # Abre el archivo en modo lectura
                    matriz = []
                    for line in file:  # Itera sobre cada línea del archivo
                        # Convierte cada elemento de la línea en un float y crea una lista
                        fila = [Fraction(x) for x in line.split()]
                        matriz.append(fila)  # Agrega la fila a la matriz

                # Elimina todas las entradas existentes en la interfaz gráfica
                secondary_window.clear_all()

                #crear matriz para gauss-jordan 
                if page == "<GJ>":
                # Crea nuevas entradas en la interfaz gráfica para la nueva matriz importada
                    filas_importadas = len(matriz)
                    columnas_importadas = len(matriz[0])
                    secondary_window.create_matrix_entries(
                        filas_importadas, columnas_importadas)
                    
                #crear matriz para determinar
                elif page == "<D>":
                    filas_importadas = len(matriz)
                    columnas_importadas = len(matriz)
                    secondary_window.create_matrix_entries(
                        len(matriz))
                    
                # Muestra la matriz importada en las nuevas entradas creadas
                for i in range(filas_importadas):
                    for j in range(columnas_importadas):
                        # Borra el contenido actual de la entrada
                        secondary_window.matrix_entries[i][j].delete(0, END)
                        # Inserta el valor de la matriz en la entrada
                        secondary_window.matrix_entries[i][j].insert(
                            END, Fraction(str(matriz[i][j])))

                root.destroy()  # Cierra la ventana de selección de archivo

            except FileNotFoundError:
                # Muestra un mensaje de error si el archivo no se encuentra
                tkinter.messagebox.showerror(
                    "Error", "El archivo no fue encontrado.")
            except ValueError:
                # Muestra un mensaje de error si hay valores no válidos en el archivo
                tkinter.messagebox.showerror(
                    "Error", "El archivo contiene valores no válidos.")
            except Exception as e:
                # Muestra un mensaje de error genérico si ocurre cualquier otra excepción
                tkinter.messagebox.showerror(
                    "Error", f"No se pudo abrir el archivo: {e}")
        else:
            # Muestra un mensaje de error si no se seleccionó un archivo o si el archivo no es un archivo de texto
            tkinter.messagebox.showerror(
                "Error", "Por favor, seleccione un archivo de texto (.txt)")

    root = Window_drag_and_drop()
    root.geometry("500x500")
    root.title("Get file path")
    root.attributes("-topmost", True)
    root.wm_attributes("-topmost", 1)
    try:
        image_path = os.path.join("images", "drop_and_drag.png")
        pil_image = Image.open(image_path).resize((350, 180))
        image_tk_t = customtkinter.CTkImage(pil_image, size=(350, 180))
    except FileNotFoundError:
        print(
            f"Error: El archivo drop_and_drag.png no se encontró en la carpeta 'images'.")
    except Exception as e:
        print(f"Error: {e}")

    nameVarString = StringVar()

    entryWidget = customtkinter.CTkEntry(
        root, width=550, height=550, bg_color="white", fg_color="white", border_color="black",)
    entryWidget.pack(side=TOP, padx=5, pady=5)

    background_Label = customtkinter.CTkLabel(
        root, text="Pon tu archivo en al zona azul")
    background_Label.place(x=170, y=400)

    button1 = customtkinter.CTkButton(root, width=80, height=30, text="Explorar archivos", command=lambda: import_explore(
        secondary_window, root), bg_color="blue", fg_color="white", text_color="black", hover_color="grey")
    button1.place(x=200, y=330)

    entryWidget.drop_target_register(DND_ALL)
    entryWidget.dnd_bind("<<Drop>>", get_path)

    print("Import document")


def export_document(secondary_window):
    # Abrir una ventana del explorador de archivos para que el usuario seleccione la ubicación y el nombre del archivo
    filepath = filedialog.asksaveasfilename(defaultextension=".txt")

    if filepath:  # Verifica si se seleccionó un archivo para guardar
        try:
            # Abrir el archivo en modo escritura y escribir los datos de la matriz en él
            with open(filepath, 'w') as file:
                for fila in secondary_window.matrix_entries:  # Itera sobre cada fila en la matriz de entradas
                    for entry in fila:  # Itera sobre cada entrada en la fila actual
                        valor = entry.get()  # Obtiene el valor de la entrada actual
                        if valor:  # Verifica si hay un valor en la entrada
                            # Escribe el valor seguido de un espacio en el archivo
                            file.write(str(Fraction(valor)) + " ")
                        else:
                            # Escribe "0.0" seguido de un espacio si no hay valor en la entrada
                            file.write("0")
                # Agrega un salto de línea al final de cada fila en el archivo
                    file.write("\n")

        # Muestra un mensaje de éxito después de exportar la matriz
            tkinter.messagebox.showinfo(
                "Éxito", "La matriz ha sido exportada exitosamente.")
        except Exception as e:
            # Manejar cualquier error que pueda ocurrir al escribir en el archivo
            # Muestra un mensaje de error si no se puede exportar la matriz
            tkinter.messagebox.showerror(
                "Error", f"No se pudo exportar la matriz: {e}")


def import_explore(secondary_window, root: customtkinter.CTkToplevel):

    root.withdraw()  # Oculta la ventana principal para que la ventana de selección de archivo sea la ventana principal
    file_name = filedialog.askopenfilename(
        parent=root, filetypes=[("Text files", "*.txt")])
    # Abrir una ventana del explorador de archivos para que el usuario seleccione un archivo
    if file_name:  # Verifica si se seleccionó un archivo
        try:
            with open(file_name, 'r') as file:  # Abre el archivo en modo lectura
                matriz = []
                for line in file:  # Itera sobre cada línea del archivo
                    # Convierte cada elemento de la línea en un float y crea una lista
                    fila = [Fraction(x) for x in line.split()]
                    matriz.append(fila)  # Agrega la fila a la matriz

            # Elimina todas las entradas existentes en la interfaz gráfica
            secondary_window.clear_all()

            # Crea nuevas entradas en la interfaz gráfica para la nueva matriz importada
            filas_importadas = len(matriz)
            columnas_importadas = len(matriz[0])

            secondary_window.create_matrix_entries(
                filas_importadas, columnas_importadas)

            # Muestra la matriz importada en las nuevas entradas creadas
            for i in range(filas_importadas):
                for j in range(columnas_importadas):
                    # Borra el contenido actual de la entrada
                    secondary_window.matrix_entries[i][j].delete(0, END)
                    # Inserta el valor de la matriz en la entrada
                    secondary_window.matrix_entries[i][j].insert(
                        END, Fraction(str(matriz[i][j])))

            root.destroy()  # Cierra la ventana de selección de archivo

        except FileNotFoundError:
            # Muestra un mensaje de error si el archivo no se encuentra
            tkinter.messagebox.showerror(
                "Error", "El archivo no fue encontrado.")
        except ValueError:
            # Muestra un mensaje de error si hay valores no válidos en el archivo
            tkinter.messagebox.showerror(
                "Error", "El archivo contiene valores no válidos.")
        except Exception as e:
            # Muestra un mensaje de error genérico si ocurre cualquier otra excepción
            tkinter.messagebox.showerror(
                "Error", f"No se pudo abrir el archivo: {e}")
    else:
        # Muestra un mensaje de error si no se seleccionó un archivo o si el archivo no es un archivo de texto
        tkinter.messagebox.showerror(
            "Error", "Por favor, seleccione un archivo de texto (.txt)")
