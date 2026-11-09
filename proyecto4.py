# Proyecto 4
# Proyecto de colas | Cola de impresion
# Diego Gallardo - Emilio Jimenez - Doram Basdemir - Alan Lopez

import random


# Parte Diego: estructura de la cola
class ColaImpresion:

    def __init__(self, capacidad=6):
        self.capacidad = capacidad
        self.trabajos = []

    # Parte Emilio: revisar si la cola esta vacia o llena
    def esta_vacia(self):
        return len(self.trabajos) == 0

    def esta_llena(self):
        return len(self.trabajos) == self.capacidad

    # Parte Emilio: agregar un trabajo al final de la cola
    def agregar_trabajo(self):
        if self.esta_llena():
            print("La cola de impresión está LLENA")
            return

        numero_pc = random.randint(1, 5)
        pc = "PC" + str(numero_pc)
        self.trabajos.append(pc)
        print("Se agregó un trabajo desde", pc)
        self.mostrar_cola()

    # Parte Doram: imprimir el primer trabajo de la cola
    def imprimir_documento(self):
        if self.esta_vacia():
            print("La cola de impresión está VACÍA")
            return

        pc = self.trabajos.pop(0)
        print("Imprimiendo el documento de", pc)
        self.mostrar_cola()

    # Parte Doram: mostrar los trabajos en orden de impresion
    def mostrar_cola(self):
        print("\nCola de impresión:")

        if self.esta_vacia():
            print("La cola está vacía.")
        else:
            for posicion in range(len(self.trabajos)):
                print(str(posicion + 1) + ". " + self.trabajos[posicion])
        print()


# Parte Alan: menu principal
def menu():
    cola = ColaImpresion()

    while True:
        print("COLA DE IMPRESIÓN")
        print("1. Agregar trabajo de impresión")
        print("2. Imprimir documento")
        print("3. Mostrar cola")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            cola.agregar_trabajo()
        elif opcion == "2":
            cola.imprimir_documento()
        elif opcion == "3":
            cola.mostrar_cola()
        elif opcion == "4":
            print("Programa terminado.")
            break
        else:
            print("Opción no válida.")

        input("Presione ENTER para continuar.")
        print()


if __name__ == "__main__":
    menu()
