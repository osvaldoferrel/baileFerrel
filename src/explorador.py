from SimpleSearch import TreeSearch, node


class Laberinto:

    MOVIMIENTOS = {
        "arriba": (-1, 0),
        "abajo": (1, 0),
        "izquierda": (0, -1),
        "derecha": (0, 1)
    }
#constructor
    def __init__(self, mapa, llaves, puertas):

        self.mapa = [list(fila) for fila in mapa]

        self.filas = len(self.mapa)
        self.columnas = len(self.mapa[0])

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
            0 <= fila < self.filas
            and
            0 <= columna < self.columnas
        )
    def es_pared(self, posicion):
        fila, columna = posicion
        return self.mapa[fila][columna] == "#"
    def sucesores(self, actual):
        posicion, llaves_actuales = actual.state
        hijos = []
        for movimiento, (df, dc) in self.MOVIMIENTOS.items():
            nueva = (
                posicion[0] + df,
                posicion[1] + dc
            )
            if not self.dentro(nueva):
                continue
            if self.es_pared(nueva):
                continue
            # revisar puertas
            if nueva in self.puertas:
                llave_necesaria = self.puertas[nueva]
                if llave_necesaria not in llaves_actuales:
                    continue
            nuevas_llaves = llaves_actuales
            # recoger llave
            if nueva in self.llaves:
                llave = self.llaves[nueva]
                nuevas_llaves = (
                    llaves_actuales |
                    frozenset([llave])
                )
            nuevo_estado = (
                nueva,
                nuevas_llaves
            )
            hijo = node(
                nuevo_estado,
                parent=actual,
                depth=actual.depth + 1,
                op=movimiento,
                step_cost=1
            )
            hijos.append(hijo)
        return hijos
    def meta(self, actual, objetivo=None):
        posicion, llaves = actual.state
        return posicion == self.salida
    def heuristica(self, actual, objetivo=None):
        posicion, llaves = actual.state
        return (
            abs(posicion[0] - self.salida[0])
            +
            abs(posicion[1] - self.salida[1])
        )
    def resolver(
        self,
        estrategia="bfs",
        usar_heuristica=True
    ):
        inicial = node(
            (
                self.inicio,
                frozenset()
            )
        )
        h = None
        if estrategia == "a*" and usar_heuristica:
            h = self.heuristica
        busqueda = TreeSearch(
            inicial,
            self.sucesores,
            self.meta,
            strategy=estrategia,
            goal_state=self.salida,
            heuristic=h
        )
        solucion = busqueda.find()
        return solucion, busqueda.iterations
