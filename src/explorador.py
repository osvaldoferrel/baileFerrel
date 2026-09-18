"""
Proyecto IA
Explorador con llaves y puertas

Estado:
(posicion, llaves_recogidas)
"""
from SimpleSearch import TreeSearch, node

class Laberinto:
    def __init__(self, mapa, llaves, puertas):
        self.mapa = [list(fila) for fila in mapa]
        self.filas = len(mapa)
        self.columnas = len(mapa[0])
        self.llaves = llaves
        self.puertas = puertas
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
            0 <= fila < self.filas and
            0 <= columna < self.columnas
        )
    def pared(self, posicion):
        fila, columna = posicion
        return self.mapa[fila][columna] == "#"
    def sucesores(self, actual):
        posicion, llaves_actuales = actual.state
        fila, columna = posicion
        movimientos = [
            ("arriba", -1, 0),
            ("abajo", 1, 0),
            ("izquierda", 0, -1),
            ("derecha", 0, 1)
        ]
        hijos = []
        for nombre, df, dc in movimientos:

            nueva_fila = fila + df
            nueva_columna = columna + dc
            nueva_posicion = (
                nueva_fila,
                nueva_columna
            )
            if not self.dentro(nueva_posicion):
                continue
            if self.pared(nueva_posicion):
                continue
            # Revisar puerta
            if nueva_posicion in self.puertas:
                llave_necesaria = self.puertas[nueva_posicion]
                if llave_necesaria not in llaves_actuales:
                    continue
            nuevas_llaves = llaves_actuales
            # Recoger llave
            if nueva_posicion in self.llaves:
                llave = self.llaves[nueva_posicion]
                nuevas_llaves = (
                    llaves_actuales |
                    frozenset([llave])
                )
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
        return (
            abs(fila - fila_salida)
            +
            abs(columna - columna_salida)
        )
    def resolver(self, estrategia="bfs", usar_heuristica=True):
        estado_inicial = (
            self.inicio,
            frozenset()
        )
        inicial = node(estado_inicial)
        heuristica = None
        if estrategia == "a*" and usar_heuristica:
            heuristica = self.heuristica
        busqueda = TreeSearch(
            inicial,
            self.sucesores,
            self.meta,
            strategy=estrategia,
            goal_state=self.salida,
            heuristic=heuristica
        )
        solucion = busqueda.find()
        return solucion, busqueda.iterations
def crear_laberinto():
    mapa = [
        "#############",
        "#E....#....S#",
        "#.....#.....#",
        "#..K..D.....#",
        "#...........#",
        "#############"
    ]
    llaves = {
        (3, 3): "K1"
    }
    puertas = {
        (3, 6): "K1"
    }
    return Laberinto(
        mapa,
        llaves,
        puertas
    )
def imprimir_camino(solucion):
    if solucion is None:
        print("No hay solución")
        return
    camino = solucion.getPath()
    print("Movimientos:")
    for estado, movimiento, profundidad in camino:
        posicion, llaves = estado
        print(
            profundidad,
            movimiento,
            posicion,
            list(llaves)
        )

    print()
    print("Pasos:", len(camino) - 1)

def probar():
    laberinto = crear_laberinto()
    pruebas = [

        ("BFS", "bfs", False),
        ("DFS", "dfs", False),
        ("A* h=0", "a*", False),
        ("A* Manhattan", "a*", True)

    ]
    print()
    print("RESULTADOS")
    print()
    for nombre, estrategia, heuristica in pruebas:
        solucion, explorados = laberinto.resolver(
            estrategia,
            heuristica
        )
        print("--------------------")
        print(nombre)
        if solucion:
            pasos = len(solucion.getPath()) - 1
            print("Pasos:", pasos)
            print("Estados explorados:", explorados)
        else:
            print("Sin solución")

        print()

if __name__ == "__main__":
    probar()
