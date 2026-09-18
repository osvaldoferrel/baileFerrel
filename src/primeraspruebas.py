def laberinto_facil():
    mapa = [
        "#########",
        "#E.K.D.S#",
        "#########"
    ]
    llaves = {
        (1,3): "K1"
    }
    puertas = {
        (1,5): "K1"
    }
    return mapa, llaves, puertas


def laberinto_mediano():
    mapa = [
        "#############",
        "#E....#....S#",
        "#.....#.....#",
        "#..K..D.....#",
        "#...........#",
        "#############"
    ]
    llaves = {
        (3,3): "K1"
    }
    puertas = {
        (3,6): "K1"
    }
    return mapa, llaves, puertas
