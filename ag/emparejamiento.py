#emparejamiento.py
import random

def emparejamiento(poblacion, probabilidad_cruza):
    parejas = []
    for i in range(len(poblacion)):
        for j in range(i + 1, len(poblacion)):
            numero = random.randint(0, 100)
            if numero <= probabilidad_cruza:
                parejas.append([i, j])
    return parejas