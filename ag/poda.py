#poda.py
from ag.aptitud import calcular_aptitud

def poda(poblacion, hijos, cantidad_individuos):
    poblacion_temporal = poblacion + hijos

    individuos_con_aptitud = []
    for individuo in poblacion_temporal:
        aptitud = calcular_aptitud(individuo)
        individuos_con_aptitud.append({
            "individuo": individuo,
            "aptitud": aptitud
        })

    individuos_ordenados = sorted(
        individuos_con_aptitud,
        key=lambda x: x["aptitud"],
        reverse=True
    )

    nueva_poblacion = []
    for i in range(cantidad_individuos):
        nueva_poblacion.append(individuos_ordenados[i]["individuo"])

    mejor = individuos_ordenados[0]["aptitud"]
    peor = individuos_ordenados[cantidad_individuos - 1]["aptitud"]
    suma = 0
    for i in range(cantidad_individuos):
        suma += individuos_ordenados[i]["aptitud"]
    promedio = suma / cantidad_individuos

    top3_individuos = []
    for i in range(min(3, len(individuos_ordenados))):
        top3_individuos.append({
            "individuo": individuos_ordenados[i]["individuo"],
            "aptitud": individuos_ordenados[i]["aptitud"]
        })

    return nueva_poblacion, mejor, peor, promedio, individuos_ordenados[0]["individuo"], top3_individuos