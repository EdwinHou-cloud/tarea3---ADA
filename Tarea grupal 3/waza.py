"""
Integrantes:
Hou, Edwin	        8-1021-1916
Arosemena, Miguel	8-1016-2330
Corrales, Diego		8-1001-1890
Camaño, Edward		8-1010-515
Pino, Josué		    8-1012-688
"""

import tkinter as tk # Librería para crear interfaces gráficas para el usuario
from tkinter import messagebox # Librería para mostrar cuadros de dialogo
from PIL import Image, ImageTk # Librería para manipular y mostrar imágenes

# Crear ventana principal
root = tk.Tk() #Inicializar ventana principal
root.title("Hamburguesería Hou") #Titulo de ventana principal

# Título de bienvenida
titulo_label = tk.Label(root, text="BIENVENIDO A HAMBURGUESERÍA HOU", font=("Arial", 18, "bold")) #Tipo de letra del título
titulo_label.pack(pady=10)  # Añadir el título a la ventana principal

# Variables globales para el subtotal, descuento y total de la compra
subtotal = 0
descuento = 0.0
total = 0
detallesHamburguesa = [] #Lista que guarda los detalles de cada hamburguesa añadida
combo_precio = 1.50  # Precio adicional por combo

# Función para actualizar factura
def agregar_hamburguesa():
    global subtotal, total, descuento #Variables globales para modificar dentro de la funcion
    cantidad = int(cantidad_var.get()) #Obtener la cantidad de hamburguesas seleccionadas
    
    # Validar que la cantidad sea mayor que 0
    if cantidad <= 0:
        messagebox.showerror("Error", "La cantidad de hamburguesas debe ser mayor a 0.")
        return  # No continuar si la cantidad es negativa o cero
    
    # Contar ingredientes seleccionados (solo se permiten hasta 3)
    ingredientes_seleccionados = sum(1 for var in ingredientes_vars.values() if var.get())
    
    # Validar que se haya seleccionado al menos un ingrediente
    if ingredientes_seleccionados == 0:
        messagebox.showerror("Error", "Debe seleccionar al menos un ingrediente.")
        return  # No continuar si no se ha seleccionado al menos un ingrediente
    
    # Validar que el usuario no haya seleccionado mas de 3 ingredientes
    if ingredientes_seleccionados > 3:
        messagebox.showerror("Error", "Solo se pueden seleccionar hasta 3 ingredientes.")
        return  # No continuar si hay más de 3 ingredientes seleccionados
    
    # Obtener el precio del tamaño seleccionado
    precio_tamano = precios_tamano[opcion_tamano.get()]
    # Calcular el precio de los ingredientes seleccionados
    precio_ingredientes = sum([precios_ingredientes[ingrediente] for ingrediente, var in ingredientes_vars.items() if var.get()])
    
    # Si el combo está marcado, agregar $1.50
    if combo_var.get():
        precio_tamano += combo_precio
    
    # Calcular el precio total de la hamburguesa (incluye tamaño y los ingredientes)
    precio_hamburguesa = (precio_tamano + precio_ingredientes) * cantidad
    subtotal += precio_hamburguesa #Actualiza el subtotal
    
    # Aplicar descuento si el combo está marcado
    if combo_var.get():
        if subtotal > 30.00:
            descuento = subtotal * 0.05  # Descuento del 5% si el subtotal es mayor a $30
        elif 20.00 <= subtotal <= 30.00:
            descuento = subtotal * 0.02  # Descuento del 2% si esta entre $20 y #30
        else:
            descuento = 0  # No hay descuento si no se cumplen los requisitos de monto
    else:
        descuento = 0  # No hay descuento si no es combo
    
    # Calcular el total final después del descuento
    total = subtotal - descuento
    
    # Actualizar el texto de la factura
    factura_label.config(text=f"SubTotal: ${subtotal:.2f}\nDescuento: ${descuento:.2f}\nTotal: ${total:.2f}")
    
    #Detallar la hamburguesa en la factura
    detalle = f"Hamburguesa Nº {len(detallesHamburguesa) + 1}: {opcion_tamano.get()}, Cantidad: {cantidad}, Precio: ${precio_hamburguesa:.2f}"
    
    #Agregar los ingredientes si han sido seleccionados
    if ingredientes_seleccionados > 0:
        detalle += f"\n  Ingredientes: {', '.join([ing for ing, var in ingredientes_vars.items() if var.get()])}"
    
    detallesHamburguesa.append(detalle) # Agregar el detalle de la hamburguesa a la lista de detalles
    
    #Actualizar el historial de detalles de la factura
    detalle_texto = "\n".join(detallesHamburguesa)
    detalle_factura.config(state=tk.NORMAL)  # Permitir edición temporal
    detalle_factura.delete(1.0, tk.END)  # Borrar texto anterior
    detalle_factura.insert(tk.END, detalle_texto)  # Insertar nuevo historial
    detalle_factura.config(state=tk.DISABLED)  # Volver a deshabilitar la edición
    
    # Mostrar un mensaje de confirmación de que la hamburguesa se agregó correctamente
    messagebox.showinfo("Confirmación", "¡Hamburguesa agregada con éxito!")
    
# Precios de las hamburguesas por tamaño
precios_tamano = {
    "Pequeña": 5.00,
    "Mediana": 7.50,
    "Grande": 10.00,
    "Doble": 12.50
}

# Precios de ingredientes
precios_ingredientes = {
    "Queso": 1.00,
    "Bacon": 1.25,
    "Pepinillos": 0.85,
    "Lechuga": 0.75,
    "Tomate": 1.00,
    "Cebolla en tiras": 0.75,
    "Salsa de la casa": 1.00,
    "Ketchup/Mayonesa": 0.50
}

# Crear frames para organizar mejor los elementos

# Frame para mostrar la fractura
frame_izquierda = tk.Frame(root, bd=2, relief="sunken")
frame_izquierda.pack(side=tk.LEFT, padx=10, pady=10, anchor="n")

# Frame para mostrar la imagen y controles de cantidad/combo
frame_central = tk.Frame(root, bd=2, relief="sunken")
frame_central.pack(side=tk.LEFT, padx=10, pady=10, anchor="n")

# Frame para las opciones de tamaño e ingredientes adicionales
frame_derecha = tk.Frame(root, bd=2, relief="sunken")
frame_derecha.pack(side=tk.LEFT, padx=10, pady=10)

# Frame Izquierda (Factura)
tk.Label(frame_izquierda, text="Factura: ").pack(anchor="w")
# Crear un widget Text para mostrar el historial de pedidos
detalle_factura = tk.Text(frame_izquierda, height=10, width=30, state=tk.DISABLED)  # Inicialmente deshabilitado
detalle_factura.pack()
# Mostrar subtotal, descuento y total
factura_label = tk.Label(frame_izquierda, text=f"SubTotal: ${subtotal:.2f}\nDescuento: ${descuento:.2f}\nTotal: ${total:.2f}", anchor="w", justify="left")
factura_label.pack()

# Frame Central (Imagen)
try:
    # Buscar la imagen "Combo_Hamburguesa.png"
    imagen = Image.open("Combo_Hamburguesa.png")
    
    # Redimensiona la imagen a 200x200 píxeles
    # Image.Resampling.LANCZOS es un método de alta calidad para redimensionar imágenes
    imagen = imagen.resize((200, 200), Image.Resampling.LANCZOS)
    
    # Convierte la imagen de PIL a un formato que Tkinter pueda usar
    imagen_tk = ImageTk.PhotoImage(imagen)
    
    # Crea un widget Label para mostrar la imagen
    imagen_label = tk.Label(frame_central, image=imagen_tk)
    
    # Coloca la imagen en el frame central con un poco de espacio vertical (pady)
    imagen_label.pack(pady=10)
except Exception as e:
    print(f"Error al cargar la imagen: {e}")

# Entrada de cantidad de hamburguesas
tk.Label(frame_central, text="Cantidad:").pack(anchor="w")
cantidad_var = tk.StringVar(value="1")
cantidad_entry = tk.Entry(frame_central, textvariable=cantidad_var)
cantidad_entry.pack()

# Opción de Combo (agrega +$1.50)
combo_var = tk.BooleanVar()
combo_check = tk.Checkbutton(frame_central, text=f"Combo (+${combo_precio})", variable=combo_var)
combo_check.pack()

# Botón para agregar hamburguesa a la factura
agregar_button = tk.Button(frame_central, text="AGREGAR", command=agregar_hamburguesa)
agregar_button.pack(pady=5)

# Frame Derecha (Tamaños e Ingredientes extras)
# Sub-Frame para separar tamaño e ingredientes
frame_tamano = tk.Frame(frame_derecha, bd=2, relief="sunken")
frame_tamano.pack(side=tk.TOP, padx=5, pady=5)

frame_ingredientes = tk.Frame(frame_derecha, bd=2, relief="sunken")
frame_ingredientes.pack(side=tk.TOP, padx=5, pady=5)

# Opciones de tamaño de hamburguesa
tk.Label(frame_tamano, text="Tamaño de la hamburguesa").pack(anchor="w")
opcion_tamano = tk.StringVar(value="Pequeña")
for tamano, precio in precios_tamano.items():
    tk.Radiobutton(frame_tamano, text=f"{tamano} - ${precio}", variable=opcion_tamano, value=tamano).pack(anchor="w")

# Ingredientes adicionales (máximo 3)
tk.Label(frame_ingredientes, text="Ingredientes").pack(anchor="w")
ingredientes_vars = {}
for ingrediente, precio in precios_ingredientes.items():
    var = tk.BooleanVar()
    ingredientes_vars[ingrediente] = var
    tk.Checkbutton(frame_ingredientes, text=f"{ingrediente} - ${precio}", variable=var).pack(anchor="w")

# Ejecutar la aplicación
root.mainloop() # Iniciar el bucle principal de la aplicación