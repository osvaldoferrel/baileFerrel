from explorador import Laberinto

mapa = [
    "###############",
    "#E............#",
    "#####.#######.#",
    "#############.#",
    "#.............#",
    "#.#######.#####",
    "#.#############",
    "#.............#",
    "#####.#######.#",
    "#############.#",
    "#.............#",
    "#.#######.#####",
    "#.#############",
    "#............S#",
    "###############"
]

llaves = {
    (2, 5): "K1",
    (5, 9): "K2",
    (8, 5): "K3",
    (11, 9): "K4"
}

puertas = {
    (2, 13): "K1",
    (5, 1): "K2",
    (8, 13): "K3",
    (11, 1): "K4"
}

laberinto = Laberinto(
    mapa,
    llaves,
    puertas
)

pruebas = [
    ("BFS", "bfs", False),
    ("DFS", "dfs", False),
    ("A* h=0", "a*", False),
    ("A* Manhattan", "a*", True)
]

for nombre, estrategia, heuristica in pruebas:
    solucion, explorados = laberinto.resolver(
        estrategia,
        heuristica
    )
    print()
    print(nombre)

    if solucion:
        camino = solucion.getPath()
        print("Movimientos:",
              len(camino) - 1)
        print("Estados explorados:",
              explorados)
    else:

        print("No hay solución")
