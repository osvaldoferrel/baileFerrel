from explorador import Laberinto

mapa = [
    "###############",
    "#E....#.......#",
    "#.###.#.#####.#",
    "#...#.#.....#.#",
    "###.#.#####.#.#",
    "#...#...K1#...#",
    "#.#######.###.#",
    "#...K2..D2....#",
    "#.###.#######.#",
    "#...#...K3....#",
    "#.#.#####.###.#",
    "#.#...D3...#..#",
    "#.#####.##.#D4#",
    "#K4....D1....S#",
    "###############"
]

llaves = {
    (5, 8): "K1",
    (7, 4): "K2",
    (9, 8): "K3",
    (13, 1): "K4"

}

puertas = {
    (7, 8): "K2",
    (11, 6): "K3",
    (13, 7): "K4",
    (13, 12): "K1"

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

print("LABERINTO ULTRADIFICIL")
print("Tamaño: 15 x 15")
print("Llaves:", len(llaves))
print("Puertas:", len(puertas))

for nombre, estrategia, usar_heuristica in pruebas:
    print()
    print("-------------------------")
    print(nombre)
    print("-------------------------")
    solucion, explorados = laberinto.resolver(
        estrategia,
        usar_heuristica
    )
    if solucion:
        camino = solucion.getPath()
        print("Movimientos:",
              len(camino) - 1)
        print("Estados explorados:",
              explorados)
        print("Camino:")
        for estado, movimiento, profundidad in camino:
            posicion, llaves_actuales = estado
            print(
                profundidad,
                movimiento,
                posicion,
                list(llaves_actuales)
            )
    else:
        print("No se encontró una solución.")
