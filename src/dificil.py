from explorador import Laberinto


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

        print("Ruta:")

        for estado, operacion, profundidad in camino:

            posicion, llaves = estado

            print(
                profundidad,
                operacion,
                posicion,
                list(llaves)
            )

    else:

        print("No hay solución")
