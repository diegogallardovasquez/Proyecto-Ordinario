# Proyecto 5
# Proyecto de Arboles | Sistema de Archivos
# Diego Gallardo - Emilio Jimenez - Doram Basdemir - Alan Lopez

class Nodo:

    def __init__(self, nombre, extension, tamano, tipo):
        self.nombre = nombre
        self.extension = extension
        self.tamano = tamano
        self.tipo = tipo
        self.izquierdo = None
        self.derecho = None

    def mostrar_informacion(self):
        print("Nombre:", self.nombre)
        print("Extension:", self.extension if self.extension else "-")
        print("Tamano:", self.tamano, "bytes")
        print("Tipo:", self.tipo)
        print()


class Arbol:

    def __init__(self):
        self.raiz = Nodo("Documentos", "", 0, "Directorio")

    def validar(self, nombre, extension, tamano, tipo):
        if nombre.strip() == "":
            print("Error: el nombre no puede estar vacio.")
            return False
        if tipo != "Archivo" and tipo != "Directorio":
            print("Error: tipo no valido.")
            return False
        if tipo == "Archivo" and extension.strip() == "":
            print("Error: un archivo debe tener extension.")
            return False
        if tipo == "Directorio" and extension.strip() != "":
            print("Error: un directorio no debe tener extension.")
            return False
        if tamano < 0:
            print("Error: el tamano no puede ser negativo.")
            return False
        return True

    def insertar(self, nombre, extension, tamano, tipo):
        if not self.validar(nombre, extension, tamano, tipo):
            return False
        nombre = nombre.strip()
        extension = extension.strip()
        if self.buscar(nombre) is not None:
            print("El elemento ya existe.")
            return False
        if tipo == "Directorio":
            tamano = 0

        nuevo = Nodo(nombre, extension, tamano, tipo)
        actual = self.raiz
        while True:
            if actual.tipo == "Archivo":
                print("ERROR: No se puede insertar el elemento.")
                print("Un archivo no puede contener otros elementos.")
                return False
            if nombre.lower() < actual.nombre.lower():
                if actual.izquierdo is None:
                    actual.izquierdo = nuevo
                    break
                actual = actual.izquierdo
            else:
                if actual.derecho is None:
                    actual.derecho = nuevo
                    break
                actual = actual.derecho

        print("Elemento insertado correctamente.")
        return True

    def buscar(self, nombre):
        nombre = nombre.strip().lower()
        actual = self.raiz
        while actual is not None:
            if nombre == actual.nombre.lower():
                return actual
            if nombre < actual.nombre.lower():
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        return None

    def eliminar(self, nombre):
        elemento = self.buscar(nombre)
        if elemento is None:
            print("El elemento no existe en el sistema de archivos.")
            return False
        if elemento is self.raiz:
            print("No se puede eliminar el directorio raiz.")
            return False
        if elemento.tipo == "Directorio":
            if elemento.izquierdo is not None or elemento.derecho is not None:
                print("No se puede eliminar un directorio con contenido.")
                return False

        self.raiz = self._eliminar_nodo(self.raiz, elemento.nombre)
        print("Elemento eliminado correctamente.")
        return True

    def _eliminar_nodo(self, actual, nombre):
        if actual is None:
            return None
        if nombre.lower() < actual.nombre.lower():
            actual.izquierdo = self._eliminar_nodo(actual.izquierdo, nombre)
        elif nombre.lower() > actual.nombre.lower():
            actual.derecho = self._eliminar_nodo(actual.derecho, nombre)
        else:
            if actual.izquierdo is None:
                return actual.derecho
            if actual.derecho is None:
                return actual.izquierdo
            sucesor = actual.derecho
            while sucesor.izquierdo is not None:
                sucesor = sucesor.izquierdo
            actual.nombre = sucesor.nombre
            actual.extension = sucesor.extension
            actual.tamano = sucesor.tamano
            actual.tipo = sucesor.tipo
            actual.derecho = self._eliminar_nodo(actual.derecho, sucesor.nombre)
        return actual

    def inorden(self, actual):
        if actual is not None:
            self.inorden(actual.izquierdo)
            actual.mostrar_informacion()
            self.inorden(actual.derecho)

    def preorden(self, actual):
        if actual is not None:
            actual.mostrar_informacion()
            self.preorden(actual.izquierdo)
            self.preorden(actual.derecho)

    def postorden(self, actual):
        if actual is not None:
            self.postorden(actual.izquierdo)
            self.postorden(actual.derecho)
            actual.mostrar_informacion()


def pedir_tamano():
    while True:
        try:
            tamano = int(input("Tamano en bytes: "))
            if tamano >= 0:
                return tamano
            print("El tamano debe ser mayor o igual a cero.")
        except ValueError:
            print("Ingresa un numero entero valido.")


def menu():
    arbol = Arbol()
    while True:
        print("\nSISTEMA DE ARCHIVOS ABB")
        print("Directorio raiz:", arbol.raiz.nombre)
        print("1. Crear directorio")
        print("2. Insertar archivo")
        print("3. Buscar elemento")
        print("4. Eliminar elemento")
        print("5. Recorrido inorden")
        print("6. Recorrido preorden")
        print("7. Recorrido postorden")
        print("8. Informacion de un elemento")
        print("9. Salir")
        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            nombre = input("Nombre del directorio: ")
            arbol.insertar(nombre, "", 0, "Directorio")
        elif opcion == "2":
            nombre = input("Nombre del archivo (sin extension): ")
            extension = input("Extension (ejemplo: pdf): ")
            tamano = pedir_tamano()
            arbol.insertar(nombre, extension, tamano, "Archivo")
        elif opcion == "3" or opcion == "8":
            nombre = input("Nombre del elemento: ")
            encontrado = arbol.buscar(nombre)
            if encontrado is None:
                print("El elemento no existe en el sistema de archivos.")
            else:
                print("Elemento encontrado:")
                encontrado.mostrar_informacion()
        elif opcion == "4":
            nombre = input("Nombre del elemento a eliminar: ")
            confirmacion = input("Confirmar eliminacion (s/n): ")
            if confirmacion.strip().lower() == "s":
                arbol.eliminar(nombre)
            else:
                print("Operacion cancelada.")
        elif opcion == "5":
            print("\nINORDEN")
            arbol.inorden(arbol.raiz)
        elif opcion == "6":
            print("\nPREORDEN")
            arbol.preorden(arbol.raiz)
        elif opcion == "7":
            print("\nPOSTORDEN")
            arbol.postorden(arbol.raiz)
        elif opcion == "9":
            print("Programa terminado.")
            break
        else:
            print("Opcion no valida. Elige del 1 al 9.")


if __name__ == "__main__":
    menu()
