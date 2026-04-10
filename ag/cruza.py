#cruza.py
import random
from ag.individuo import TOTAL_BITS

def cruza(poblacion, parejas):
    hijos = []
    for pareja in parejas:
        i = pareja[0]
        j = pareja[1]
        padre1 = poblacion[i]
        padre2 = poblacion[j]

        punto_cruza = random.randint(1, TOTAL_BITS - 1)

        hijo1 = padre1[:punto_cruza] + padre2[punto_cruza:]
        hijo2 = padre2[:punto_cruza] + padre1[punto_cruza:]

        hijos.append(hijo1)
        hijos.append(hijo2)

    return hijos