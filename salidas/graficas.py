# graficas.py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

CARPETA_GRAFICAS = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'static', 'graficas')

def asegurar_carpeta():
    os.makedirs(CARPETA_GRAFICAS, exist_ok=True)

def grafica_evolucion_aptitud(historial_mejor, historial_peor, historial_promedio):
    asegurar_carpeta()
    generaciones = range(1, len(historial_mejor) + 1)

    plt.figure(figsize=(10, 5))
    plt.plot(generaciones, historial_mejor, 'g-o', label='Mejor', markersize=4)
    plt.plot(generaciones, historial_promedio, 'y-o', label='Promedio', markersize=4)
    plt.plot(generaciones, historial_peor, 'r-o', label='Peor', markersize=4)
    plt.title('Evolucion de la Aptitud por Generacion')
    plt.xlabel('Generacion')
    plt.ylabel('Aptitud')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    ruta = os.path.join(CARPETA_GRAFICAS, 'evolucion_aptitud.png')
    plt.savefig(ruta, dpi=150)
    plt.close()
    return ruta

def grafica_cobertura(programacion, parcelas):
    asegurar_carpeta()
    from ag.aptitud import calcular_litros_aplicados, calcular_litros_requeridos, calcular_cobertura
    from datos.parcelas import FACTOR_SUELO

    ids = []
    coberturas = []

    for i in range(len(parcelas)):
        parcela = parcelas[i]
        prog = programacion[i]
        num_dias = len(prog["dias"])

        if num_dias == 0 or prog["duracion"] == 0:
            litros_aplicados = 0
        else:
            litros_aplicados = calcular_litros_aplicados(
                parcela["caudal"],
                prog["duracion"],
                num_dias
            )

        litros_requeridos = calcular_litros_requeridos(parcela, 7)
        cobertura = calcular_cobertura(litros_aplicados, litros_requeridos)

        ids.append(parcela["id"])
        coberturas.append(cobertura)

    colores = ['green' if c >= 80 else 'orange' if c >= 50 else 'red' for c in coberturas]

    plt.figure(figsize=(10, 5))
    plt.bar(ids, coberturas, color=colores)
    plt.axhline(y=80, color='green', linestyle='--', label='Umbral optimo 80%')
    plt.title('Cobertura Hidrica por Parcela')
    plt.xlabel('Parcela')
    plt.ylabel('Cobertura (%)')
    plt.ylim(0, 110)
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()

    ruta = os.path.join(CARPETA_GRAFICAS, 'cobertura_hidrica.png')
    plt.savefig(ruta, dpi=150)
    plt.close()
    return ruta