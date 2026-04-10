#generacion.py
from ag.individuo import generar_individuo

def generar_poblacion(cantidad_individuos):
    poblacion = []
    for i in range(cantidad_individuos):
        individuo = generar_individuo()
        poblacion.append(individuo)
    return poblacion