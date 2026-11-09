#Proyecto 3
#Proyecto de Pilas | Navegador web
#Diego Gallardo - Emilio Jiménez - Doram Basdemir - Alan López

#Parte Diego
#Cada nodo guarda una pagina y el enlace al siguiente nodo.
class Nodo:

    def __init__(self, pagina, siguiente=None):
        # Guarda la pagina y su enlace
        self.pagina = pagina
        self.siguiente = siguiente


#Parte Emilio
#Pila enlazada: la ultima pagina que entra es la primera que sale.
class Pila:

    def __init__(self):
        # La pila comienza vacia
        self.tope = None

    def esta_vacia(self):
        # Revisa si no hay nodos
        return self.tope is None

    def push(self, pagina):
        # Agrega una pagina en el tope
        self.tope = Nodo(pagina, self.tope)

    def pop(self):
        # Quita y devuelve la pagina del tope
        if self.esta_vacia():
            return None
        pagina = self.tope.pagina
        self.tope = self.tope.siguiente
        return pagina

    def vaciar(self):
        # Elimina el acceso a los nodos de la pila
        self.tope = None

    def mostrar(self):
        # Muestra las paginas desde el tope
        if self.esta_vacia():
            print("  Vacia")
        else:
            actual = self.tope
            while actual is not None:
                print(" ", actual.pagina)
                actual = actual.siguiente


#Parte Doram
#Controla la pagina actual y las dos pilas del historial.
class Navegador:

    def __init__(self):
        # Al iniciar no hay paginas visitadas
        self.pagina_actual = None
        self.pila_atras = Pila()
        self.pila_adelante = Pila()

    def visitar(self, url):
        # Valida la entrada y visita una nueva pagina
        url = url.strip()
        if url == "":
            print("Error: escribe una URL.")
            return
        if not (url.lower().startswith("https://") or url.lower().startswith("http://")):
            print("Error: la URL debe iniciar con http:// o https://.")
            return
        if len(url.split()) != 1:
            print("Error: la URL no debe contener espacios.")
            return
        dominio = url.split("://", 1)[1].split("/", 1)[0]
        if dominio == "":
            print("Error: falta el nombre del sitio.")
            return

        if self.pagina_actual is not None:
            self.pila_atras.push(self.pagina_actual)
        self.pagina_actual = url
        self.pila_adelante.vaciar()
        print("Pagina visitada:", self.pagina_actual)

    def retroceder(self):
        # Pasa la pagina actual a Adelante y recupera la anterior
        if self.pila_atras.esta_vacia():
            print("No hay paginas para retroceder.")
            return
        self.pila_adelante.push(self.pagina_actual)
        self.pagina_actual = self.pila_atras.pop()
        print("Retrocediste a:", self.pagina_actual)

    def avanzar(self):
        # Pasa la pagina actual a Atras y recupera la siguiente
        if self.pila_adelante.esta_vacia():
            print("No hay paginas para avanzar.")
            return
        self.pila_atras.push(self.pagina_actual)
        self.pagina_actual = self.pila_adelante.pop()
        print("Avanzaste a:", self.pagina_actual)

    def mostrar_estado(self):
        # Muestra la pagina actual y ambas pilas
        print("\nPAGINA ACTUAL")
        if self.pagina_actual is None:
            print("Sin paginas visitadas.")
        else:
            print(self.pagina_actual)
        print("Flecha Atras:")
        self.pila_atras.mostrar()
        print("Flecha Adelante:")
        self.pila_adelante.mostrar()


#Parte Alan
#Menu principal del navegador.
def menu():
    navegador = Navegador()
    while True:
        navegador.mostrar_estado()
        print("\nNAVEGADOR WEB")
        print("1. Visitar nueva pagina")
        print("2. Back")
        print("3. Forward ")
        print("4. Exit")
        opcion = input("Elige una opcion: ").strip()

        if opcion == "1":
            url = input("URL de la pagina: ")
            navegador.visitar(url)
        elif opcion == "2":
            navegador.retroceder()
        elif opcion == "3":
            navegador.avanzar()
        elif opcion == "4":
            print("Navegador cerrado. Hasta luego.")
            break
        else:
            print("Opcion no valida. Elige del 1 al 4.")


if __name__ == "__main__":
    menu()
