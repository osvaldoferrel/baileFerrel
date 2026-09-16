"""Problema de búsqueda: explorador con llaves y puertas.

El estado del problema es:
    (posicion, llaves_recogidas)

La clase Laberinto contiene el mapa y las reglas del problema. El módulo
usa TreeSearch para ejecutar BFS, DFS y A*.
"""

try:
    from .SimpleSearch import TreeSearch, node
except ImportError:
    from SimpleSearch import TreeSearch, node


class Laberinto:
    """Representación de un laberinto de búsqueda."""

    DIRECCIONES = {
        "arriba": (-1, 0),
        "abajo": (1, 0),
        "izquierda": (0, -1),
        "derecha": (0, 1),
    }

    def __init__(self, mapa, llaves=None, puertas=None):
        self.mapa = [list(fila) for fila in mapa]
        self.filas = len(self.mapa)
        self.columnas = len(self.mapa[0])
        self.llaves = llaves or {}
        self.puertas = puertas or {}

        self.inicio = self._buscar("E")
        self.salida = self._buscar("S")

        if self.inicio is None:
            raise ValueError("El laberinto necesita una casilla de inicio E")
        if self.salida is None:
            raise ValueError("El laberinto necesita una casilla de salida S")

    def _buscar(self, simbolo):
        for f in range(self.filas):
            for c in range(self.columnas):
                if self.mapa[f][c] == simbolo:
                    return (f, c)
        return None

    def dentro(self, posicion):
        f, c = posicion
        return 0 <= f < self.filas and 0 <= c < self.columnas

    def es_pared(self, posicion):
        f, c = posicion
        return self.mapa[f][c] == "#"

    def sucesores(self, actual):
        """Genera todos los movimientos legales desde un nodo."""
        posicion, llaves = actual.state
        hijos = []

        for movimiento, (df, dc) in self.DIRECCIONES.items():
            nueva_posicion = (posicion[0] + df, posicion[1] + dc)

            if not self.dentro(nueva_posicion):
                continue
            if self.es_pared(nueva_posicion):
                continue

            # Una puerta solo puede cruzarse si ya se posee su llave.
            if nueva_posicion in self.puertas:
                llave_necesaria = self.puertas[nueva_posicion]
                if llave_necesaria not in llaves:
                    continue

            nuevas_llaves = llaves
            if nueva_posicion in self.llaves:
                nuevas_llaves = llaves | frozenset([self.llaves[nueva_posicion]])

            estado = (nueva_posicion, nuevas_llaves)
            hijos.append(node(
                estado,
                parent=actual,
                depth=actual.depth + 1,
                op=movimiento,
                step_cost=1
            ))

        return hijos

    def es_meta(self, actual, _objetivo=None):
        """La meta se alcanza al llegar a la salida."""
        posicion, _ = actual.state
        return posicion == self.salida

    def heuristica(self, actual, _objetivo=None):
        """Distancia Manhattan a la salida, ignorando obstáculos."""
        posicion, _ = actual.state
        return (
            abs(posicion[0] - self.salida[0])
            + abs(posicion[1] - self.salida[1])
        )

    def resolver(self, estrategia="bfs", max_iter=1000000):
        """Ejecuta una búsqueda y devuelve el nodo solución."""
        estado_inicial = (self.inicio, frozenset())
        inicial = node(estado_inicial)

        busqueda = TreeSearch(
            inicial,
            self.sucesores,
            self.es_meta,
            strategy=estrategia,
            goal_state=self.salida,
            heuristic=self.heuristica if estrategia == "a*" else None,
        )

        solucion = busqueda.find(max_iter=max_iter)
        return solucion, busqueda.iterations

    def mostrar(self):
        """Imprime el mapa usando K para llaves y D para puertas."""
        for f in range(self.filas):
            fila = ""
            for c in range(self.columnas):
                posicion = (f, c)
                if posicion in self.llaves:
                    fila += "K"
                elif posicion in self.puertas:
                    fila += "D"
                else:
                    fila += self.mapa[f][c]
            print(fila)


def crear_laberinto_ejemplo():
    """Laberinto pequeño para probar el modelo antes de usar 15x15."""
    mapa = [
        "#########",
        "#E.K.D.S#",
        "#.#.###.#",
        "#.#.....#",
        "#.#######",
        "#.......#",
        "#########",
    ]

    # Las coordenadas se expresan como (fila, columna).
    llaves = {
        (1, 3): "K1",
    }

    puertas = {
        (1, 5): "K1",
    }

    return Laberinto(mapa, llaves, puertas)


def resolver_ejemplo(estrategia="bfs"):
    """Atajo para probar BFS, DFS o A* con el ejemplo."""
    laberinto = crear_laberinto_ejemplo()
    return laberinto.resolver(estrategia)
