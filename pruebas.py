import customtkinter as ctk

root = ctk.CTk()

# Crear un frame para la sombra
shadow_frame = ctk.CTkFrame(
    root,
    fg_color="grey",  # Color de la sombra
    corner_radius=15,
    width=210,
    height=60
)
shadow_frame.place(x=20, y=20)

# Crear el frame principal para la etiqueta
main_frame = ctk.CTkFrame(
    root,
    fg_color="white",
    corner_radius=15,
    width=200,
    height=50
)
main_frame.place(x=10, y=10)

# Crear la etiqueta en el frame principal
label = ctk.CTkLabel(
    main_frame,
    text="Con profundidad",
    fg_color="white",
    corner_radius=15,
    text_color="black",
    width=200,
    height=50
)
label.pack()

root.geometry("300x200")  # Configurar el tamaño de la ventana principal
root.mainloop()
