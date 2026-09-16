from SimpleSearch import TreeSearch, node
class Laberinto:
    def __init__(self, mapa, llaves, puertas):
        self.mapa = mapa
        self.llaves = llaves
        self.puertas = puertas

        self.filas = len(mapa)
        self.columnas = len(mapa[0])

        self.inicio = self.buscar("E")
        self.salida = self.buscar("S")

    def buscar(self, simbolo):
        for fila in range(self.filas):
            for columna in range(self.columnas):

                if self.mapa[fila][columna] == simbolo:
                    return (fila, columna)
        return None

    def dentro(self, posicion):
        fila, columna = posicion
        return (
            0 <= fila < self.filas
            and 0 <= columna < self.columnas
        )

    def sucesores(self, actual):
        posicion, llaves = actual.state
        fila, columna = posicion
        movimientos = [
            ("arriba", -1, 0),
            ("abajo", 1, 0),
            ("izquierda", 0, -1),
            ("derecha", 0, 1)
        ]
        hijos = []
        for nombre, cambio_fila, cambio_columna in movimientos:

            nueva_fila = fila + cambio_fila
            nueva_columna = columna + cambio_columna

            nueva_posicion = (nueva_fila, nueva_columna)

            # Fuera del laberinto
            if not self.dentro(nueva_posicion):
                continue
            # Pared
            if self.mapa[nueva_fila][nueva_columna] == "#":
                continue
            # Puerta
            if nueva_posicion in self.puertas:

                llave = self.puertas[nueva_posicion]

                if llave not in llaves:
                    continue

            # Copiamos las llaves actuales
            nuevas_llaves = llaves

            # Si encontramos una llave, la recogemos
            if nueva_posicion in self.llaves:

                llave = self.llaves[nueva_posicion]

                nuevas_llaves = llaves | frozenset([llave])

            nuevo_estado = (
                nueva_posicion,
                nuevas_llaves
            )

            hijo = node(
                nuevo_estado,
                parent=actual,
                depth=actual.depth + 1,
                op=nombre,
                step_cost=1
            )

            hijos.append(hijo)

        return hijos

    def meta(self, actual, objetivo=None):
        posicion, llaves = actual.state
        return posicion == self.salida

    def heuristica(self, actual, objetivo=None):
        posicion, llaves = actual.state
        fila, columna = posicion
        fila_salida, columna_salida = self.salida
        distancia = (
            abs(fila - fila_salida)
            + abs(columna - columna_salida)
        )
        return distancia

    def resolver(self, estrategia):
        estado_inicial = (
            self.inicio,
            frozenset()
        )
        inicial = node(estado_inicial)
        busqueda = TreeSearch(
            inicial,
            self.sucesores,
            self.meta,
            strategy=estrategia,
            goal_state=self.salida,
            heuristic=self.heuristica
        )
        solucion = busqueda.find()
        return solucion, busqueda.iterations


def crear_laberinto():
    mapa = [
        "#########",
        "#E.K.D.S#",
        "#########"
    ]
    llaves = {
        (1, 3): "K1"
    }
    puertas = {
        (1, 5): "K1"
    }
    return Laberinto(
        mapa,
        llaves,
        puertas
    )

if __name__ == "__main__":
    laberinto = crear_laberinto()
    print("Inicio:", laberinto.inicio)
    print("Salida:", laberinto.salida)
    solucion, explorados = laberinto.resolver("bfs")
    if solucion:
        print("\nCamino encontrado:")
        for estado, movimiento, profundidad in solucion.getPath():
            print(
                profundidad,
                movimiento,
                estado
            )
        print("\nEstados explorados:", explorados)

    else:
        print("No se encontró una solución.")
