# main.py
from ag.generacion import generar_poblacion
from ag.emparejamiento import emparejamiento
from ag.cruza import cruza
from ag.mutacion import mutacion
from ag.poda import poda
from ag.aptitud import calcular_aptitud
from ag.individuo import decodificar_individuo

def correr_ag(cantidad_individuos, generaciones, prob_cruza, prob_mut_individuo, prob_mut_gen):
    historial_mejor = []
    historial_peor = []
    historial_promedio = []

    poblacion = generar_poblacion(cantidad_individuos)
    mejor_individuo_global = None
    mejor_aptitud_global = None
    top3_global = []

    for gen in range(generaciones):
        parejas = emparejamiento(poblacion, prob_cruza)

        if len(parejas) == 0:
            aptitudes = [calcular_aptitud(ind) for ind in poblacion]
            mejor = max(aptitudes)
            peor = min(aptitudes)
            promedio = sum(aptitudes) / len(aptitudes)
            historial_mejor.append(mejor)
            historial_peor.append(peor)
            historial_promedio.append(promedio)
            continue

        hijos = cruza(poblacion, parejas)
        hijos = mutacion(hijos, prob_mut_individuo, prob_mut_gen)
        poblacion, mejor, peor, promedio, mejor_individuo, top3_gen = poda(
            poblacion, hijos, cantidad_individuos
        )

        historial_mejor.append(mejor)
        historial_peor.append(peor)
        historial_promedio.append(promedio)

        if mejor_aptitud_global is None or mejor > mejor_aptitud_global:
            mejor_aptitud_global = mejor
            mejor_individuo_global = mejor_individuo
            top3_global = top3_gen

    if mejor_individuo_global is None:
        aptitudes = [calcular_aptitud(ind) for ind in poblacion]
        idx_mejor = aptitudes.index(max(aptitudes))
        mejor_individuo_global = poblacion[idx_mejor]
        mejor_aptitud_global = aptitudes[idx_mejor]
        top3_global = []
        for i, ind in enumerate(poblacion[:3]):
            top3_global.append({
                "individuo": ind,
                "aptitud": aptitudes[i]
            })

    programacion = decodificar_individuo(mejor_individuo_global)

    top3_programaciones = []
    for item in top3_global:
        top3_programaciones.append({
            "individuo": item["individuo"],
            "aptitud": item["aptitud"],
            "programacion": decodificar_individuo(item["individuo"])
        })

    return {
        "historial_mejor": historial_mejor,
        "historial_peor": historial_peor,
        "historial_promedio": historial_promedio,
        "mejor_aptitud": mejor_aptitud_global,
        "mejor_programacion": programacion,
        "top3": top3_programaciones
    }

if __name__ == "__main__":
    resultado = correr_ag(
        cantidad_individuos=20,
        generaciones=50,
        prob_cruza=70,
        prob_mut_individuo=20,
        prob_mut_gen=5
    )

    print("\n=== MEJOR PROGRAMACION DE RIEGO ===")
    for parcela in resultado["mejor_programacion"]:
        print(f"{parcela['id']}: hora={parcela['hora']}:00, duracion={parcela['duracion']} min, dias={parcela['dias']}")

    print(f"\nMejor aptitud: {resultado['mejor_aptitud']:.6f}")
    print(f"\nTop 3 individuos:")
    for i, ind in enumerate(resultado["top3"]):
        print(f"  {i+1}. aptitud={ind['aptitud']:.6f}")