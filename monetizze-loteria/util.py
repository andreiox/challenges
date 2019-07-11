import random


def get_numeros_aleatorios_ordenados(tuple, quantidade_numeros):
    numeros = random.sample(range(tuple[0], tuple[1]), quantidade_numeros)
    numeros.sort()

    return numeros
