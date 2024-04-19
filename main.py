
from tkinter import *
from tkinter import filedialog, messagebox
#para obtener imagenes
from PIL import ImageTk, Image

from fractions import Fraction

import numpy as np
import os

def on_enter(event):
    event.widget.config(bg="#cccccc")

def on_leave(event):
    event.widget.config(bg='white')

# --------------------------------------------definicionBotones--------------------------------------------------- #

def cambiar_tamano():
    def aceptar():
        # Función interna para obtener las dimensiones ingresadas por el usuario y actualizar la matriz en la interfaz.
        filas = int(entry_filas.get())  # Obtiene el número de filas ingresado por el usuario.
        columnas = int(entry_columnas.get())  # Obtiene el número de columnas ingresado por el usuario.

        # Elimina las entradas de la matriz existente.
        for fila in matriz_entries:
            for entry in fila:
                entry.grid_forget()

        matriz_entries.clear()  # Limpia la lista de entradas de la matriz.

        # Crea y muestra las nuevas entradas de la matriz con las dimensiones ingresadas por el usuario.
        for i in range(filas):
            fila_entries = []
            for j in range(columnas):
                entry = Entry(entradaDeMatriz, width=8, font=("Century Gothic", 13), highlightthickness=1, highlightbackground="black")
                entry.grid(row=i, column=j, padx=5, pady=5, ipady=8)  # Posiciona la entrada en la interfaz.
                fila_entries.append(entry)
            matriz_entries.append(fila_entries)  # Agrega la fila de entradas a la lista de entradas de la matriz.

        ventana_tamano.destroy()  # Cierra la ventana secundaria después de aceptar los cambios.

    # Crear y configurar la ventana secundaria para cambiar el tamaño de la matriz.
    ventana_tamano = Toplevel(GaussJordan)
    ventana_tamano.title("Cambiar Tamaño de la Matriz")
    ventana_tamano.geometry("300x150")
    ventana_tamano.resizable(False, False)  # Evita que el usuario cambie el tamaño de la ventana.

    # Etiqueta y entrada para ingresar el número de filas.
    label_filas = Label(ventana_tamano, text="Filas:")
    label_filas.grid(row=0, column=0, padx=10, pady=10)  # Posiciona la etiqueta en la ventana.

    entry_filas = Entry(ventana_tamano)  # Crea una entrada para que el usuario ingrese el número de filas.
    entry_filas.grid(row=0, column=1, padx=10, pady=10)  # Posiciona la entrada en la ventana.

    # Etiqueta y entrada para ingresar el número de columnas.
    label_columnas = Label(ventana_tamano, text="Columnas:")
    label_columnas.grid(row=1, column=0, padx=10, pady=10)  # Posiciona la etiqueta en la ventana.

    entry_columnas = Entry(ventana_tamano)  # Crea una entrada para que el usuario ingrese el número de columnas.
    entry_columnas.grid(row=1, column=1, padx=10, pady=10)  # Posiciona la entrada en la ventana.

    # Botón para aceptar los cambios y llamar a la función `aceptar`.
    boton_aceptar = Button(ventana_tamano, text="Aceptar", command=aceptar)
    boton_aceptar.grid(row=2, column=0, columnspan=2, pady=10)  # Posiciona el botón en la ventana.

def resolver_matriz():
    # Obtener la matriz ingresada por el usuario desde la interfaz gráfica
    matriz = []
    for fila in matriz_entries:
        fila_valores = []
        for entry in fila:
            valor = entry.get()
            if valor:
                fila_valores.append(Fraction(valor))  # Convertir el valor a un objeto Fraction si está presente
            else:
                fila_valores.append(0.0)  # Agregar 0.0 si la entrada está vacía
        matriz.append(fila_valores)

    # Imprimir la matriz ingresada por el usuario
    print("Matriz ingresada:")
    for fila in matriz:
        print(fila)

    # Resolver la matriz utilizando el método de eliminación de Gauss-Jordan
    matriz_resuelta = gauss_jordan(matriz)

    # Imprimir la matriz resuelta
    print("Matriz resuelta:")
    for fila in matriz_resuelta:
        print(fila)

    # Limpiar la ventana de salidaDeMatriz eliminando todos los widgets hijos
    for widget in salidaDeMatriz.winfo_children():
        widget.destroy()

    # Mostrar el título de la matriz resuelta en la ventana de salida
    titulo_label = Label(salidaDeMatriz, text="Matriz Resuelta\n", font=("Century Gothic", 15))
    titulo_label.place(relx=0.5, rely=0.05, anchor="n")

    # Mostrar los valores de la matriz resuelta en la ventana de salida
    for i, fila in enumerate(matriz_resuelta):
        for j, valor in enumerate(fila):
            label = Label(salidaDeMatriz, text=str(valor), font=("Century Gothic", 13))
            label.place(relx=(j + 0.5) * (1 / (len(fila) + 1)), rely=(i + 1) * (1 / (len(matriz_resuelta) + 1)), anchor="center")

    # Verificar si la matriz tiene solución
    tiene_solucion = True
    for fila in matriz_resuelta:
        if all(valor == 0 for valor in fila[:-1]) and fila[-1] != 0:
            tiene_solucion = False
            break

    # Limpiar la ventana de conjuntoSolucion eliminando todos los widgets hijos
    for widget in conjuntoSolucion.winfo_children():
        widget.destroy()

    # Mostrar el conjunto de soluciones o un mensaje de que no hay solución en la ventana de conjuntoSolucion
    if tiene_solucion:
        conjunto_label = Label(conjuntoSolucion, text="Conjunto de soluciones:", font=("Century Gothic", 15), bg="#ffffff")
        conjunto_label.place(relx=0.5, rely=0.05, anchor="n")

        soluciones = []
        for i, fila in enumerate(matriz_resuelta):
            soluciones.append(f"x{i+1} = {fila[-1]}")

        soluciones_text = "; ".join(soluciones)
        label = Label(conjuntoSolucion, text=soluciones_text, font=("Century Gothic", 13), bg="#ffffff")
        label.place(relx=0.5, rely=0.5, anchor="center")
    else:
        no_solucion_label = Label(conjuntoSolucion, text="No hay conjunto de solución.", font=("Century Gothic", 13), bg="#ffffff")
        no_solucion_label.place(relx=0.5, rely=0.5, anchor="center")

def obtener_matriz_inversa():
    # Obtener la matriz ingresada por el usuario desde la interfaz gráfica
    matriz = []
    for fila in matriz_entries:
        fila_valores = []
        for entry in fila:
            valor = entry.get()
            if valor:
                fila_valores.append(float(valor))  # Convertir el valor a tipo float si está presente
            else:
                fila_valores.append(0.0)  # Agregar 0.0 si la entrada está vacía
        matriz.append(fila_valores)

    n_filas = len(matriz)
    n_columnas = len(matriz[0])

    # Verificar si la matriz es cuadrada y tiene una columna adicional para las constantes
    if n_filas == n_columnas:
        matriz_cuadrada = True
        for fila in matriz:
            if len(fila) != n_columnas:
                matriz_cuadrada = False
                break

        if matriz_cuadrada:
            matriz_sin_constantes = [fila[:-1] for fila in matriz]
            try:
                # Calcular la inversa de la matriz utilizando NumPy
                matriz_inversa = np.linalg.inv(matriz_sin_constantes)

                # Limpiar la ventana de salidaDeMatriz eliminando todos los widgets hijos
                for widget in conjuntoSolucion.winfo_children():
                    widget.destroy()

                for widget in salidaDeMatriz.winfo_children():
                    widget.destroy()

                # Mostrar el título de la matriz inversa en la ventana de salida
                titulo_label = Label(salidaDeMatriz, text="Matriz Inversa\n", font=("Century Gothic", 15))
                titulo_label.place(relx=0.5, rely=0.05, anchor="n")

                # Mostrar los valores de la matriz inversa en la ventana de salida
                for i, fila in enumerate(matriz_inversa):
                    for j, valor in enumerate(fila):
                        # Convertir el valor a fracción y mostrarlo en la ventana de salida
                        valor_fraccion = Fraction(valor).limit_denominator()
                        label = Label(salidaDeMatriz, text=str(valor_fraccion), font=("Century Gothic", 13))
                        label.place(relx=(j + 0.5) * (1 / (len(fila) + 1)), rely=(i + 1) * (1 / (len(matriz_inversa) + 1)), anchor="center")

            except np.linalg.LinAlgError:
                # En caso de que no se pueda calcular la inversa, limpiar la ventana de salidaDeMatriz y mostrar un mensaje
                for widget in salidaDeMatriz.winfo_children():
                    widget.destroy()
                no_solucion_label = Label(conjuntoSolucion, text="No existe matriz inversa.", font=("Century Gothic", 13), bg="#ffffff")
                no_solucion_label.place(relx=0.5, rely=0.5, anchor="center")
        else:
            # Si la matriz no es cuadrada, limpiar la ventana de salidaDeMatriz y mostrar un mensaje
            for widget in salidaDeMatriz.winfo_children():
                widget.destroy()
            no_solucion_label = Label(conjuntoSolucion, text="No existe matriz inversa.", font=("Century Gothic", 13), bg="#ffffff")
            no_solucion_label.place(relx=0.5, rely=0.5, anchor="center")
    else:
        # Si la matriz no tiene una columna adicional para las constantes, limpiar la ventana de salidaDeMatriz y mostrar un mensaje
        for widget in salidaDeMatriz.winfo_children():
            widget.destroy()
        no_solucion_label = Label(conjuntoSolucion, text="No existe matriz inversa.", font=("Century Gothic", 13), bg="#ffffff")
        no_solucion_label.place(relx=0.5, rely=0.5, anchor="center")

def limpiar_matriz():
    # Limpiar la matriz ingresada por el usuario
    for fila in matriz_entries:
        for entry in fila:
            entry.delete(0, END)  # Borrar el contenido de cada entrada

    # Limpiar la ventana de salida donde se muestran los resultados de la matriz
    for widget in salidaDeMatriz.winfo_children():
        widget.destroy()  # Eliminar todos los widgets hijos de la ventana de salida

    # Limpiar la ventana donde se muestra el conjunto de soluciones
    for widget in conjuntoSolucion.winfo_children():
        widget.destroy()  # Eliminar todos los widgets hijos de la ventana del conjunto de soluciones

def importar_matriz():
    filepath = filedialog.askopenfilename()  # Abre una ventana para que el usuario seleccione un archivo

    if filepath:  # Verifica si se seleccionó un archivo
        try:
            with open(filepath, 'r') as file:  # Abre el archivo en modo lectura
                matriz = []
                for line in file:  # Itera sobre cada línea del archivo
                    fila = [float(x) for x in line.split()]  # Convierte cada elemento de la línea en un float y crea una lista
                    matriz.append(fila)  # Agrega la fila a la matriz

            # Elimina todas las entradas existentes en la interfaz gráfica
            for fila in matriz_entries:
                for entry in fila:
                    entry.grid_forget()  # Quita cada entrada de la vista
            matriz_entries.clear()  # Borra todas las entradas de la matriz

            # Crea nuevas entradas en la interfaz gráfica para la nueva matriz importada
            filas_importadas = len(matriz)
            columnas_importadas = len(matriz[0])

            for i in range(filas_importadas):
                fila_entries = []
                for j in range(columnas_importadas):
                    entry = Entry(entradaDeMatriz, width=8, font=("Century Gothic", 13),
                                  highlightthickness=1, highlightbackground="black")
                    entry.grid(row=i, column=j, padx=5, pady=5, ipady=8)  # Ajusta la posición de la entrada en la interfaz gráfica
                    fila_entries.append(entry)
                matriz_entries.append(fila_entries)  # Agrega la fila de entradas a la matriz de entradas

            # Muestra la matriz importada en las nuevas entradas creadas
            for i in range(filas_importadas):
                for j in range(columnas_importadas):
                    matriz_entries[i][j].delete(0, END)  # Borra el contenido actual de la entrada
                    matriz_entries[i][j].insert(END, str(matriz[i][j]))  # Inserta el valor de la matriz en la entrada

        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo no fue encontrado.")  # Muestra un mensaje de error si el archivo no se encuentra
        except ValueError:
            messagebox.showerror("Error", "El archivo contiene valores no válidos.")  # Muestra un mensaje de error si hay valores no válidos en el archivo
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo: {e}")  # Muestra un mensaje de error genérico si ocurre cualquier otra excepción

def exportar_matriz():
    # Abrir una ventana del explorador de archivos para que el usuario seleccione la ubicación y el nombre del archivo
    filepath = filedialog.asksaveasfilename(defaultextension=".txt")

    if filepath:  # Verifica si se seleccionó un archivo para guardar
        try:
            # Abrir el archivo en modo escritura y escribir los datos de la matriz en él
            with open(filepath, 'w') as file:
                for fila in matriz_entries:  # Itera sobre cada fila en la matriz de entradas
                    for entry in fila:  # Itera sobre cada entrada en la fila actual
                        valor = entry.get()  # Obtiene el valor de la entrada actual
                        if valor:  # Verifica si hay un valor en la entrada
                            file.write(valor + " ")  # Escribe el valor seguido de un espacio en el archivo
                        else:
                            file.write("0.0 ")  # Escribe "0.0" seguido de un espacio si no hay valor en la entrada
                    file.write("\n")  # Agrega un salto de línea al final de cada fila en el archivo

            messagebox.showinfo("Éxito", "La matriz ha sido exportada exitosamente.")  # Muestra un mensaje de éxito después de exportar la matriz
        except Exception as e:
            # Manejar cualquier error que pueda ocurrir al escribir en el archivo
            messagebox.showerror("Error", f"No se pudo exportar la matriz: {e}")  # Muestra un mensaje de error si no se puede exportar la matriz


# --------------------------------------------definicionBotones--------------------------------------------------- #
# --------------------------------------------gaussJordan--------------------------------------------------------- #

def gauss_jordan(matriz):
    n = len(matriz)  # Obtiene el tamaño de la matriz
    for i in range(n):
        # Si el elemento en la diagonal principal es cero, busca una fila debajo con un valor no cero en la misma columna
        if matriz[i][i] == 0:
            for k in range(i + 1, n):
                if matriz[k][i] != 0:
                    matriz[i], matriz[k] = matriz[k], matriz[i]  # Intercambia las filas
                    break
            else:
                continue  # Si no se encuentra una fila adecuada, continúa con la siguiente columna
        # Hace ceros por debajo del pivote
        for j in range(i + 1, n):
            factor = matriz[j][i] / matriz[i][i]
            for k in range(i, n):
                matriz[j][k] -= factor * matriz[i][k]
            matriz[j][-1] -= factor * matriz[i][-1]  # Actualiza los resultados en el lado derecho
        # Hace ceros por encima del pivote
        for j in range(i):
            factor = matriz[j][i] / matriz[i][i]
            for k in range(i, n):
                matriz[j][k] -= factor * matriz[i][k]
            matriz[j][-1] -= factor * matriz[i][-1]  # Actualiza los resultados en el lado derecho
        # Normaliza el pivote y el resultado correspondiente
        pivot = matriz[i][i]
        for k in range(n):
            matriz[i][k] /= pivot
        matriz[i][-1] /= pivot
    return matriz



# --------------------------------------------gaussJordan--------------------------------------------------------- #

# --------------------------------------------ventanaPrincipal--------------------------------------------------- #
GaussJordan = Tk()  # Crea la ventana principal de la aplicación
GaussJordan.title("Gauss - Jordan")  # Establece el título de la ventana
GaussJordan.geometry("1280x720")  # Establece las dimensiones de la ventana
GaussJordan.configure(bg="#dddddd")  # Configura el color de fondo de la ventana

# Carga y establece el icono de la ventana
icono = Image.open(os.path.join("images", "logogj_mesa_de_trabajo.png"))
icono_tk = ImageTk.PhotoImage(icono)
GaussJordan.iconphoto(True, icono_tk)

# Carga y establece el fondo de la ventana
fondo_ventana = Image.open(os.path.join("images", "fondo.png")).convert("RGBA")
fondo_ventana = ImageTk.PhotoImage(fondo_ventana)

fondo_ventana_label = Label(GaussJordan, image=fondo_ventana)  # Crea una etiqueta para mostrar el fondo
fondo_ventana_label.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)  # Posiciona el fondo en la ventana


# --------------------------------------------ventanaPrincipal--------------------------------------------------- #

# --------------------------------------------barraDeHerramientas------------------------------------------------#

barraDeHerramientas = Frame(GaussJordan)  # Crea un marco para la barra de herramientas
barraDeHerramientas.place(relx=0, rely=0, relwidth=1, relheight=0.2)  # Coloca la barra de herramientas en la parte superior de la ventana

# Carga la imagen de la barra de herramientas y la muestra en un Label
bhpng = Image.open(os.path.join("images", "barraHerramientas.png")).convert("RGBA")
bhtk = ImageTk.PhotoImage(bhpng)

lbbh = Label(barraDeHerramientas, image=bhtk)
lbbh.place(x=0, y=0, relwidth=1, relheight=1)
lbbh.bhpng = bhtk

botones = []  # Lista para almacenar los botones creados dinámicamente

# Función para crear un botón con una imagen, texto y comando asociado
def crear_boton(imagen, texto, command):
    imagen_path = os.path.join("images", imagen)  # Ruta de la imagen del botón
    imagen_pil = Image.open(imagen_path).convert("RGBA")  # Abre y convierte la imagen a formato RGBA
    imagen_pil = imagen_pil.resize((55, 50))  # Redimensiona la imagen
    imagen_tk = ImageTk.PhotoImage(imagen_pil)  # Convierte la imagen en formato que puede ser usado en Tkinter

    # Crea un botón con la imagen, texto y comando asociado
    boton = Button(barraDeHerramientas, image=imagen_tk, text=texto, compound="top", bg="white", bd=0,
                   font=("Century Gothic", 12), command=command)
    boton.grid(row=0, column=len(botones), padx=30, pady=30)  # Coloca el botón en la barra de herramientas

    boton.imagen = imagen_tk  # Asigna la imagen al botón

    botones.append(boton)  # Agrega el botón a la lista de botones

    boton.bind("<Enter>", on_enter)  # Asocia la función on_enter al evento de pasar el ratón sobre el botón
    boton.bind("<Leave>", on_leave)  # Asocia la función on_leave al evento de retirar el ratón del botón

# Crea los botones de la barra de herramientas llamando a la función crear_boton con las respectivas imágenes, textos y comandos
crear_boton("importar.png", "\nImportar", importar_matriz)
crear_boton("exportar.png", "\nExportar", exportar_matriz)
crear_boton("resolver.png", "\nResolver", resolver_matriz)
crear_boton("inversa.png", "Obtener matriz\ninversa", obtener_matriz_inversa)
crear_boton("limpiar.png", "\nLimpiar", limpiar_matriz)
crear_boton("cambiar.png", "Cambiar\n tamaño", cambiar_tamano)


# --------------------------------------------barraDeHerramientas------------------------------------------------#

# ------------------------------------------------entradaDeMatriz------------------------------------------------#
entradaDeMatriz = Frame(GaussJordan)  # Crea un marco para la entrada de la matriz
entradaDeMatriz.place(relx=0.015, rely=0.225, relwidth=0.47, relheight=0.755)  # Coloca el marco en una posición específica dentro de la ventana principal

matriz_entries = []  # Lista para almacenar las entradas de la matriz

# Bucle para crear las entradas de la matriz, con 3 filas y 4 columnas en este caso
for i in range(3):
    fila_entries = []  # Lista para almacenar las entradas de cada fila
    for j in range(4):
        # Crea una entrada con un ancho específico, fuente y decoraciones visuales
        entry = Entry(entradaDeMatriz, width=8, font=("Century Gothic", 13), highlightthickness=1, highlightbackground="black")
        entry.grid(row=i, column=j, padx=5, pady=5, ipady=8)  # Coloca la entrada en una posición específica dentro del marco
        fila_entries.append(entry)  # Agrega la entrada a la lista de entradas de la fila actual
    matriz_entries.append(fila_entries)  # Agrega la lista de entradas de la fila a la lista de entradas de la matriz


# ------------------------------------------------entradaDeMatriz------------------------------------------------#

# ------------------------------------------------salidaDeMatriz------------------------------------------------#

salidaDeMatriz = Frame(GaussJordan)  # Crea un marco para mostrar la matriz resuelta
salidaDeMatriz.place(relx=0.505, rely=0.225, relwidth=0.47, relheight=0.505)  # Coloca el marco en una posición específica dentro de la ventana principal

label_salida_de_matriz = Label(salidaDeMatriz, text="Matriz Resuelta:", font=("Century Gothic", 15))  # Crea una etiqueta para indicar que se trata de la matriz resuelta
label_salida_de_matriz.place(relx=0.5, rely=0.05, anchor="n")  # Coloca la etiqueta en el centro superior del marco


# ------------------------------------------------salidaDeMatriz------------------------------------------------#
# ------------------------------------------------conjuntoSolucion----------------------------------------------#

conjuntoSolucion = Frame(GaussJordan, bg="#ffffff")  # Crea un marco para mostrar el conjunto de soluciones, con un fondo blanco
conjuntoSolucion.place(relx=0.505, rely=0.755, relwidth=0.47, relheight=0.225)  # Coloca el marco en una posición específica dentro de la ventana principal

label_conjunto_solucion = Label(conjuntoSolucion, text="Conjunto Solución:", font=("Century Gothic", 15), bg="#ffffff")  # Crea una etiqueta para indicar que se trata del conjunto de soluciones
label_conjunto_solucion.place(relx=0.5, rely=0.05, anchor="n")  # Coloca la etiqueta en el centro superior del marco

label_conjunto_solucion_value = Label(conjuntoSolucion, text="", font=("Century Gothic", 13), bg="#ffffff")  # Crea una etiqueta vacía para mostrar el conjunto de soluciones calculado
label_conjunto_solucion_value.place(relx=0.5, rely=0.5, anchor="center")  # Coloca la etiqueta en el centro del marco para mostrar el conjunto de soluciones


# ------------------------------------------------conjuntoSolucion----------------------------------------------#

GaussJordan.mainloop()
