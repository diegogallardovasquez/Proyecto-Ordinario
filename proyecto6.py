#Proyecto 6
#Proyecto de Grafos | Ruta Mágica
#Diego Gallardo - Emilio Jiménez - Doram Basdemir - Alan López


#Parte Diego
#Clase para guardar los datos de un Pueblo Magico.
class Pueblo:

    def __init__(self, numero, nombre, clave):
        self.numero = numero
        self.nombre = nombre
        self.clave = clave


#Parte Emilio
#Clase que guarda el grafo y calcula la ruta mas corta.
class Grafo:

    def __init__(self):
        self.pueblos = []
        self.caminos = {}

    def agregar_pueblo(self, numero, nombre, clave):
        pueblo = Pueblo(numero, nombre, clave)
        self.pueblos.append(pueblo)
        self.caminos[clave] = []

    def agregar_carretera(self, origen, destino, distancia):
        # El grafo no dirigido guarda los dos sentidos.
        self.caminos[origen].append([destino, distancia])
        self.caminos[destino].append([origen, distancia])

    def buscar_pueblo(self, clave):
        for pueblo in self.pueblos:
            if pueblo.clave == clave:
                return pueblo
        return None

    def dijkstra(self, origen, destino):
        # Calcula las distancias mas cortas desde el origen.
        distancias = {}
        anteriores = {}
        pendientes = []

        for pueblo in self.pueblos:
            distancias[pueblo.clave] = 999999
            anteriores[pueblo.clave] = ""
            pendientes.append(pueblo.clave)

        distancias[origen] = 0

        while len(pendientes) > 0:
            actual = pendientes[0]

            for clave in pendientes:
                if distancias[clave] < distancias[actual]:
                    actual = clave

            pendientes.remove(actual)

            if distancias[actual] == 999999:
                break

            for carretera in self.caminos[actual]:
                vecino = carretera[0]
                nueva_distancia = distancias[actual] + carretera[1]

                if vecino in pendientes and nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = actual

        if distancias[destino] == 999999:
            return [], 0

        ruta = []
        actual = destino

        while actual != "":
            ruta.insert(0, actual)
            actual = anteriores[actual]

        return ruta, distancias[destino]

    def distancia(self, origen, destino):
        for carretera in self.caminos[origen]:
            if carretera[0] == destino:
                return carretera[1]
        return 0


#Parte Doram
#Datos de Puebla usados en el ejemplo del proyecto.
def cargar_grafo():
    grafo = Grafo()

    pueblos = [
        ["Zacatlan de las Manzanas", "ZAC"],
        ["Chignahuapan", "CHI"],
        ["Tetela de Ocampo", "TET"],
        ["Cuetzalan del Progreso", "CUE"],
        ["Tlatlauquitepec", "TLA"],
        ["Xicotepec de Juarez", "XIC"],
        ["Pahuatlan", "PAH"]
    ]

    for indice in range(len(pueblos)):
        grafo.agregar_pueblo(indice + 1, pueblos[indice][0], pueblos[indice][1])

    carreteras = [
        ["ZAC", "CHI", 22], ["ZAC", "TET", 48],
        ["CHI", "TET", 42], ["TET", "CUE", 68],
        ["CUE", "TLA", 38], ["CHI", "TLA", 90],
        ["ZAC", "XIC", 55], ["XIC", "PAH", 32],
        ["PAH", "ZAC", 60], ["XIC", "CUE", 115]
    ]

    for carretera in carreteras:
        grafo.agregar_carretera(carretera[0], carretera[1], carretera[2])

    return grafo


#Parte Alan
#Pide una opcion valida y muestra el resultado.
def pedir_pueblo(mensaje):
    while True:
        dato = input(mensaje).strip()

        if dato.isdigit():
            numero = int(dato)
            if numero >= 1 and numero <= 7:
                return numero

        print("Opcion no valida. Elige un numero del 1 al 7.")


def mostrar_ruta(grafo, ruta, total):
    print("\nRUTA ENCONTRADA\n")

    for indice in range(len(ruta) - 1):
        origen = grafo.buscar_pueblo(ruta[indice])
        destino = grafo.buscar_pueblo(ruta[indice + 1])
        distancia = grafo.distancia(ruta[indice], ruta[indice + 1])

        print("{} --({} km)--> {}".format(
            origen.nombre, distancia, destino.nombre))

    nombres = []
    for clave in ruta:
        nombres.append(grafo.buscar_pueblo(clave).nombre)

    print("\nRuta completa:")
    print(" -> ".join(nombres))
    print("Distancia total: {} km".format(total))


def menu():
    grafo = cargar_grafo()
    continuar = "s"

    print("RUTA MAGICA -- PUEBLA")
    print("Algoritmo utilizado: Dijkstra")

    while continuar == "s":
        print("\nPueblos Magicos disponibles:")
        for pueblo in grafo.pueblos:
            print("{}. {}".format(pueblo.numero, pueblo.nombre))

        numero_origen = pedir_pueblo("\nSeleccione pueblo de ORIGEN (1-7): ")
        numero_destino = pedir_pueblo("Seleccione pueblo de DESTINO (1-7): ")

        while numero_origen == numero_destino:
            print("El origen y el destino no pueden ser iguales.")
            numero_destino = pedir_pueblo("Seleccione pueblo de DESTINO (1-7): ")

        origen = grafo.pueblos[numero_origen - 1]
        destino = grafo.pueblos[numero_destino - 1]
        ruta, total = grafo.dijkstra(origen.clave, destino.clave)

        mostrar_ruta(grafo, ruta, total)

        continuar = input("\nDesea consultar otra ruta? (s/n): ").strip().lower()

        while continuar != "s" and continuar != "n":
            continuar = input("Escribe s o n: ").strip().lower()

    print("Gracias por usar Ruta Magica.")


if __name__ == "__main__":
    menu()