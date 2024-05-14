"""


# modulo encargado de desplegar una ventana para el drop and drag
#funciones:
#   -import_document(secondary_window, page:str = "") -> None
#   -export_document(secondary_window) -> None
#   -import_explore(secondary_window, root: customtkinter.CTkToplevel) -> None


"""

#libreria para manejar fracciones
from fractions import Fraction

#libreria para manejar archivos
import os
import traceback

#libreria para manejar imagenes
from PIL import ImageTk, Image

#libreria para manejar tkinter customtkinter
from tkinter import BOTTOM, END, StringVar, filedialog, TOP
import tkinter.messagebox
from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter

#protototipo de la clase para una ventana emergente
class Window_drag_and_drop(customtkinter.CTkToplevel, TkinterDnD.DnDWrapper):
    """
    Clase que hereda de la clase CTkToplevel y DnDWrapper para crear una ventana emergente con soporte para arrastrar y soltar archivos.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

#funcion para importar un documento
def import_document(secondary_window, page:str = "") -> None:
    """
    Abre una ventana para seleccionar y arrastrar un archivo de texto (.txt) y lo importa en la interfaz gráfica.
    """
    
    #función interna para obtener la ruta del archivo y crear la matriz de importación
    def get_path(event):
        nameVarString.set(event.data)
        file_name = None  # Inicializa la variable del nombre del archivo
        if event.data.endswith(".txt"): 
            file_name = os.path.normpath(event.data)
            
        else:
            file_name = os.path.normpath(event.data[1:-1])
            
        print(file_name)
        print(nameVarString.get()[1:-1])
        print(nameVarString.get())
        if file_name and (nameVarString.get().endswith(".txt") or nameVarString.get().endswith(".txt}")):  # Verifica si se seleccionó un archivo
            try:
                with open(file_name, 'r') as file:  # Abre el archivo en modo lectura
                    matriz = []
                    for line in file:  # Itera sobre cada línea del archivo
                        # Convierte cada elemento de la línea en un float y crea una lista
                        fila = [Fraction(x) for x in line.split()]
                        matriz.append(fila)  # Agrega la fila a la matriz

                # Elimina todas las entradas existentes en la interfaz gráfica
                secondary_window.eliminate()

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

    # Crea un widget de entrada para el DND
    entryWidget = customtkinter.CTkEntry(
        root, width=550, height=550, bg_color="white", fg_color="white", border_color="black",)
    entryWidget.pack(side=TOP, padx=5, pady=5)

    # Crea un widget de etiqueta para indicar lo que se debe hacer
    background_Label = customtkinter.CTkLabel(
        root, text="Pon tu archivo en al zona blanca")
    background_Label.place(x=170, y=400)

    # Crea un widget para habilitar la busquedad de archivo en el sistema
    button1 = customtkinter.CTkButton(root, width=80, height=30, text="Explorar archivos", command=lambda: import_explore(
        secondary_window, root), bg_color="blue", fg_color="white", text_color="black", hover_color="grey")
    button1.place(x=200, y=330)

    #habilitar el drop and drag
    entryWidget.drop_target_register(DND_ALL)
    entryWidget.dnd_bind("<<Drop>>", get_path)

    print("Import document")

###############################################
#funcion para exportar un documento
def export_document(secondary_window) -> None:
    """
    Exporta la matriz de entradas en la interfaz gráfica a un archivo de texto (.txt).
    """
    # Abrir una ventana del explorador de archivos para que el usuario seleccione la ubicación y el nombre del archivo
    filepath = filedialog.asksaveasfilename(defaultextension=".txt")

    if filepath:  # Verifica si se seleccionó un archivo para guardar
        try:
            if secondary_window.matrix_entries:
            # Abrir el archivo en modo escritura y escribir los datos de la matriz en él
                with open(filepath, 'w') as file:
                    for fila in secondary_window.matrix_entries:  # Itera sobre cada fila en la matriz de entradas
                        for entry in fila:  # Itera sobre cada entrada en la fila actual
                            valor = entry  # Obtiene el valor de la entrada actual
                            if valor:  # Verifica si hay un valor en la entrada
                                # Escribe el valor seguido de un espacio en el archivo
                                file.write(str(Fraction(valor)) + " ")
                            else:
                                # Escribe "0.0" seguido de un espacio si no hay valor en la entrada
                                file.write("0")
                    # Agrega un salto de línea al final de cada fila en el archivo
                        file.write("\n")
            
            else:
                tkinter.messagebox.showerror(
                    "Error", "NO HAY RESULTADO")        
            

        # Muestra un mensaje de éxito después de exportar la matriz
                tkinter.messagebox.showinfo(
                    "Éxito", "La matriz ha sido exportada exitosamente.")
        except Exception as e:
            # Manejar cualquier error que pueda ocurrir al escribir en el archivo
            # Muestra un mensaje de error si no se puede exportar la matriz
            tkinter.messagebox.showerror(
                "Error", f"No se pudo exportar la matriz: {e}")
            

def export_document_result(secondary_window) -> None:
    """
    Exporta la matriz de salidas en la interfaz gráfica a un archivo de texto (.txt).
    """
    if (secondary_window.matrix_result != None):
    # Abrir una ventana del explorador de archivos para que el usuario seleccione la ubicación y el nombre del archivo
        filepath = filedialog.asksaveasfilename(defaultextension=".txt")

        if filepath:  # Verifica si se seleccionó un archivo para guardar
            try:
                # Abrir el archivo en modo escritura y escribir los datos de la matriz en él
                with open(filepath, 'w') as file:
                    for fila in secondary_window.matrix_result:  # Itera sobre cada fila en la matriz de entradas
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
                
    else:     
        tkinter.messagebox.showerror(
            "Error", "NO HAY NINGUN RESULTADO QUE EXPORTAR")

#funcion para importar un archivo explorando el sistema
def import_explore(secondary_window, root: customtkinter.CTkToplevel) -> None:
    """
    Abre un explorador de archivos para seleccionar un archivo de texto (.txt) y lo importa en la interfaz gráfica.
    """
    root.withdraw()  # Oculta la ventana principal para que la ventana de selección de archivo sea la ventana principal
    file_name = filedialog.askopenfilename(
        parent=root, filetypes=[("Text files", "*.txt")])
    # Abrir una ventana del explorador de archivos para que el usuario seleccione un archivo
    file_name = os.path.normpath(file_name)
    print(file_name)
    if file_name:  # Verifica si se seleccionó un archivo
        try:
            with open(file_name, 'r') as file:  # Abre el archivo en modo lectura
                matriz = []
                for line in file:  # Itera sobre cada línea del archivo
                    # Convierte cada elemento de la línea en un float y crea una lista
                    fila = [Fraction(x) for x in line.split()]
                    matriz.append(fila)  # Agrega la fila a la matriz

            # Elimina todas las entradas existentes en la interfaz gráfica
            secondary_window.eliminate()

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
            traceback.print_exc()
    else:
        # Muestra un mensaje de error si no se seleccionó un archivo o si el archivo no es un archivo de texto
        tkinter.messagebox.showerror(
            "Error", "Por favor, seleccione un archivo de texto (.txt)")
