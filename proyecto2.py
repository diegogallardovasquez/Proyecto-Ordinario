#Proyecto 2
#Proyecto de Listas | Carrito de compras
#Diego Gallardo - Emilio Jiménez - Doram Basdemir - Alan López

class Producto:

    def __init__(self, id_producto, nombre, categoria, precio):
        self.id = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio


class ItemCarrito:
#Esto es un producto quwe ya fue agregado al carrito.

    def __init__(self, producto, cantidad):
        self.producto = producto
        self.cantidad = cantidad

    def calcular_subtotal(self):
        return self.producto.precio * self.cantidad


# LISTAS PRINCIPALES (catalogo y carrito) | Parte Diego

# Catalogo de productos
catalogo = [
    Producto(5055, "Teclado", "Accesorios", 450),
    Producto(3208, "Mouse", "Accesorios", 250),
    Producto(3450, "Monitor", "Electronica", 3200),
    Producto(4070, "Audifonos", "Audio", 800),
    Producto(5892, "Memoria USB", "Almacenamiento", 180),
]

# Carrito de compras
carrito = []


# FUNCIONES DE APOYO PARA BUSCAR PRODUCTOS | Parte Emilio


def buscar_en_catalogo_por_id(id_producto):
 
    for producto in catalogo:
        if producto.id == id_producto:
            return producto
    return None


def buscar_en_catalogo_por_nombre(nombre):

    for producto in catalogo:
        if producto.nombre.lower() == nombre.lower():
            return producto
    return None


def buscar_en_carrito_por_id(id_producto):
 
    for item in carrito:
        if item.producto.id == id_producto:
            return item
    return None


def buscar_en_carrito_por_nombre(nombre):
    for item in carrito:
        if item.producto.nombre.lower() == nombre.lower():
            return item
    return None
 

# Funciones para datos del usuario | Parte Doram


def pedir_numero_entero(mensaje):
    
    while True:
        entrada = input(mensaje)
        try:
            numero = int(entrada)
            return numero
        except ValueError:
            print("Error: debes ingresar un numero entero valido.\n")


def pedir_cantidad_valida(mensaje):
    while True:
        cantidad = pedir_numero_entero(mensaje)
        if cantidad <= 0:
            print("Error: la cantidad debe ser mayor a 0.\n")
        else:
            return cantidad

# Opciones del Menu | Emilio y Alan

def mostrar_catalogo():
    print("\nCATALOGO DE PRODUCTOS")
    print("ID | Producto     | Categoria       | Precio")
    print("-" * 50)
    for producto in catalogo:
        print(f"{producto.id:<3} | {producto.nombre:<12} | "
              f"{producto.categoria:<15} | ${producto.precio}")
    print()


def buscar_producto():
    print("\nBUSCAR PRODUCTO")
    print("1. Buscar por ID")
    print("2. Buscar por nombre")
    opcion = input("Seleccione una opcion: ")

    producto_encontrado = None

    if opcion == "1":
        id_producto = pedir_numero_entero("ID del producto: ")
        producto_encontrado = buscar_en_catalogo_por_id(id_producto)
    elif opcion == "2":
        nombre = input("Nombre del producto: ")
        producto_encontrado = buscar_en_catalogo_por_nombre(nombre)
    else:
        print("Opcion no valida.\n")
        return

    if producto_encontrado is None:
        print("El producto no existe en el catalogo.\n")
    else:
        print("\nProducto encontrado:")
        print(f"ID: {producto_encontrado.id}")
        print(f"Nombre: {producto_encontrado.nombre}")
        print(f"Categoria: {producto_encontrado.categoria}")
        print(f"Precio: ${producto_encontrado.precio}\n")


def agregar_producto_al_carrito():
    print("\nAGREGAR PRODUCTO AL CARRITO")
    id_producto = pedir_numero_entero("ID del producto: ")
    producto = buscar_en_catalogo_por_id(id_producto)

    if producto is None:
        print("Error: no existe un producto con ese ID.\n")
        return

    print(f"Producto: {producto.nombre}")
    print(f"Precio unitario: ${producto.precio}")

    cantidad = pedir_cantidad_valida("Cantidad: ")

    # Si el producto ya esta en el carrito, solo pongan para sumar la cantidad
    item_existente = buscar_en_carrito_por_id(id_producto)
    if item_existente is not None:
        item_existente.cantidad += cantidad
    else:
        nuevo_item = ItemCarrito(producto, cantidad)
        carrito.append(nuevo_item)

    print("\nProducto agregado al carrito\n")


def ver_carrito():
    print("\nCARRITO DE COMPRAS")

    if len(carrito) == 0:
        print("El carrito esta vacio.\n")
        return

    print("ID  | Producto     | Precio  | Cant. | Subtotal")
    print("-" * 50)

    total = 0
    for item in carrito:
        subtotal = item.calcular_subtotal()
        total += subtotal
        print(f"{item.producto.id:<3} | {item.producto.nombre:<12} | "
              f"${item.producto.precio:<6} | {item.cantidad:<5} | ${subtotal}")

    print("-" * 50)
    print(f"TOTAL: ${total}\n")


def modificar_cantidad():
    print("\nMODIFICAR CANTIDAD")

    if len(carrito) == 0:
        print("El carrito esta vacio.\n")
        return

    id_producto = pedir_numero_entero("ID del producto a modificar: ")
    item = buscar_en_carrito_por_id(id_producto)

    if item is None:
        print("Error: ese producto no esta en el carrito.\n")
        return

    print(f"Producto: {item.producto.nombre}")
    print(f"Cantidad actual: {item.cantidad}")

    nueva_cantidad = pedir_cantidad_valida("Nueva cantidad: ")
    item.cantidad = nueva_cantidad

    print("\nCantidad actualizada")
    print(f"Nuevo subtotal: ${item.calcular_subtotal()}\n")


def eliminar_producto():
    print("\nELIMINAR PRODUCTO")

    if len(carrito) == 0:
        print("El carrito esta vacio.\n")
        return

    print("1. Eliminar por ID")
    print("2. Eliminar por nombre")
    opcion = input("Seleccione una opcion: ")

    item = None

    if opcion == "1":
        id_producto = pedir_numero_entero("ID del producto a eliminar: ")
        item = buscar_en_carrito_por_id(id_producto)
    elif opcion == "2":
        nombre = input("Nombre del producto a eliminar: ")
        item = buscar_en_carrito_por_nombre(nombre)
    else:
        print("Opcion no valida.\n")
        return

    if item is None:
        print("Error: ese producto no esta en el carrito.\n")
        return

    print(f"Producto: {item.producto.nombre}")
    confirmacion = input("¿Esta seguro que desea eliminar este producto? (s/n): ")

    if confirmacion.lower() == "s":
        carrito.remove(item)
        print("\nProducto eliminado del carrito\n")
    else:
        print("\nOperacion cancelada.\n")


def vaciar_carrito():
    print("\nVACIAR CARRITO")

    if len(carrito) == 0:
        print("El carrito ya esta vacio.\n")
        return

    confirmacion = input("¿Esta seguro que desea vaciar el carrito? (s/n): ")

    if confirmacion.lower() == "s":
        carrito.clear()
        print("\nCarrito vaciado\n")
    else:
        print("\nOperacion cancelada.\n")


def finalizar_compra():
    print("\nRESUMEN DE COMPRA")

    if len(carrito) == 0:
        print("No hay productos en el carrito.\n")
        return

    print("ID  | Producto     | Cant. | Subtotal")
    print("-" * 40)

    total_articulos = 0
    total_pagar = 0

    for item in carrito:
        subtotal = item.calcular_subtotal()
        total_articulos += item.cantidad
        total_pagar += subtotal
        print(f"{item.producto.id:<3} | {item.producto.nombre:<12} | "
              f"{item.cantidad:<5} | ${subtotal}")

    print("-" * 40)
    print(f"Productos distintos: {len(carrito)}")
    print(f"Articulos totales: {total_articulos}")
    print(f"Total a pagar: ${total_pagar}")
    print("\nGracias por su compra\n")

    # Al finalizar la compra se reinicia el carrito
    carrito.clear()



# MENU PRINCIPAL | Parte Diego

def mostrar_menu():
    print("CARRITO DE COMPRAS")
    print("1. Mostrar catalogo")
    print("2. Buscar producto")
    print("3. Agregar producto al carrito")
    print("4. Ver carrito")
    print("5. Modificar cantidad")
    print("6. Eliminar producto")
    print("7. Vaciar carrito")
    print("8. Finalizar compra")
    print("9. Salir")


def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opcion: ")

        if opcion == "1":
            mostrar_catalogo()
        elif opcion == "2":
            buscar_producto()
        elif opcion == "3":
            agregar_producto_al_carrito()
        elif opcion == "4":
            ver_carrito()
        elif opcion == "5":
            modificar_cantidad()
        elif opcion == "6":
            eliminar_producto()
        elif opcion == "7":
            vaciar_carrito()
        elif opcion == "8":
            finalizar_compra()
        elif opcion == "9":
            print("\nGracias por usar el carrito de compras.")
            break
        else:
            print("\nOpcion no valida.\n")

        input("Presione ENTER para continuar.")
        print()


if __name__ == "__main__":
    main()
