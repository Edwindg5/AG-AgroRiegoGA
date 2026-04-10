#mutacion.py
import random

def mutacion(hijos, prob_individuo, prob_gen):
    for i in range(len(hijos)):
        individuo = hijos[i]
        numero = random.randint(0, 100)
        if numero <= prob_individuo:
            for j in range(len(individuo)):
                numero_gen = random.randint(0, 100)
                if numero_gen <= prob_gen:
                    individuo[j] = 1 - individuo[j]
        hijos[i] = individuo
    return hijos