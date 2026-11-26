#Proyecto 1
#Proyecto de arreglos | Resistencias
#Diego Gallardo - Emilio Jiménez - Doram Basdemir - Alan López

import numpy as np

#Emilio:
class CalculadoraResistencia:

    def __init__(self):
        # Arreglo con los nombres de color
        self.colores = np.array([
            "Negro", "Marrón", "Rojo", "Naranja", "Amarillo",
            "Verde", "Azul", "Violeta", "Gris", "Blanco",
            "Dorado", "Plateado"
        ])
        # Multiplicadores en el mismo orden que los colores
        self.multiplicadores = np.array([
            1, 10, 100, 1000, 10000, 100000, 1000000,
            10000000, 100000000, 1000000000, 0.1, 0.01
        ])

    def obtener_colores(self, valor):
        # Para buscar los dos dígitos y el multiplicador
        for i in range(len(self.multiplicadores)):
            for numero in range(10, 100):
                # Esto es para redondear el cálculo para evitar errores con decimales
                resultado = round(numero * self.multiplicadores[i], 2)
                if resultado == valor:
                    d1 = numero // 10
                    d2 = numero % 10
                    return np.array([
                        self.colores[d1], self.colores[d2], self.colores[i]
                    ])

        # Si no se encuentra la combinaión
        return None

#Parte Doram
    def resistencia_serie(self, n):
        #Para generar resistencias aleatorias y calcula el total en serie
        resistores = np.random.randint(10, 1000000001, size=n)
        # Usa 64 bits para que quepan las sumas grandes
        total = np.sum(resistores, dtype=np.int64)
        return resistores, total

    def resistencia_paralelo(self, n):
        #Genera resistencias aleatorias y calcula el total en paralelo
        resistores = np.random.randint(10, 1000000001, size=n)
        total = 1 / np.sum(1 / resistores)
        return resistores, total

#Parte Diego y Alan: Menu
def menu():
    # Menú principal
    calc = CalculadoraResistencia()

    while True:
        print("\n1. Ver colores de una resistencia")
        print("2. Resistencia total en serie")
        print("3. Resistencia total en paralelo")
        print("4. Salir")
        opcion = input("Elige una opción: ").strip()

        try:
            if opcion == "1":
                valor = float(input("Valor de la resistencia en ohmios: "))
                colores = calc.obtener_colores(valor)
                if colores is None:
                    print("Ese valor no se puede representar exactamente con tres bandas.")
                    print("Ejemplos válidos: 160, 5800, 4.7 y 0.47 ohmios.")
                else:
                    print("Colores:", colores[0], "-", colores[1], "-", colores[2])

            elif opcion == "2":
                n = int(input("Cantidad de resistencias: "))
                if n <= 0:
                    print("La cantidad debe ser mayor que cero.")
                else:
                    resistores, total = calc.resistencia_serie(n)
                    print("Resistencias:", resistores)
                    print("Total:", total, "ohmios")

            elif opcion == "3":
                n = int(input("Cantidad de resistencias: "))
                if n <= 0:
                    print("La cantidad debe ser mayor que cero.")
                else:
                    resistores, total = calc.resistencia_paralelo(n)
                    print("Resistencias:", resistores)
                    print("Total:", round(total, 4), "ohmios")

            elif opcion == "4":
                print("Adiós")
                break

            else:
                print("Opción no válida")

        except ValueError:
            print("Debes escribir un número válido. La cantidad debe ser entera.")


menu()
