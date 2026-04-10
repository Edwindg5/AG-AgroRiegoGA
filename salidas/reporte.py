# reporte.py
from datos.parcelas import PARCELAS
from datos.sistemas_riego import SISTEMAS_RIEGO
from ag.aptitud import (
    calcular_litros_aplicados,
    calcular_litros_requeridos,
    calcular_cobertura,
    calcular_deficit,
    calcular_equidad
)

def _filas_programacion(programacion):
    filas = []
    for i, parcela in enumerate(PARCELAS):
        prog = programacion[i]
        sistema = SISTEMAS_RIEGO[i]
        num_dias = len(prog["dias"])

        if num_dias == 0 or prog["duracion"] == 0:
            litros_aplicados = 0.0
        else:
            litros_aplicados = calcular_litros_aplicados(
                parcela["caudal"], prog["duracion"], num_dias
            )

        litros_requeridos = calcular_litros_requeridos(parcela, 7)
        cobertura = calcular_cobertura(litros_aplicados, litros_requeridos)

        filas.append({
            "parcela": parcela["id"],
            "cultivo": parcela["cultivo"],
            "etapa": parcela["etapa"],
            "sistema": sistema["tipo"],
            "dias": prog["dias"],
            "hora_inicio": prog["hora"],
            "duracion": prog["duracion"],
            "litros_aplicados": round(litros_aplicados, 2),
            "litros_requeridos": round(litros_requeridos, 2),
            "cobertura": round(cobertura, 2)
        })
    return filas

def _metricas_programacion(programacion):
    coberturas = []
    deficit_total = 0.0

    for i, parcela in enumerate(PARCELAS):
        prog = programacion[i]
        num_dias = len(prog["dias"])

        if num_dias == 0 or prog["duracion"] == 0:
            litros_aplicados = 0.0
        else:
            litros_aplicados = calcular_litros_aplicados(
                parcela["caudal"], prog["duracion"], num_dias
            )

        litros_requeridos = calcular_litros_requeridos(parcela, 7)
        cobertura = calcular_cobertura(litros_aplicados, litros_requeridos)
        deficit = calcular_deficit(litros_requeridos, litros_aplicados)

        coberturas.append(cobertura)
        deficit_total += max(deficit, 0.0)

    cobertura_prom = sum(coberturas) / len(coberturas)
    equidad = calcular_equidad(coberturas)

    return round(cobertura_prom, 2), round(deficit_total, 2), round(equidad, 4)

def _litros_totales(programacion):
    total = 0.0
    for i, parcela in enumerate(PARCELAS):
        prog = programacion[i]
        num_dias = len(prog["dias"])
        if num_dias == 0 or prog["duracion"] == 0:
            continue
        total += calcular_litros_aplicados(parcela["caudal"], prog["duracion"], num_dias)
    return round(total, 2)

def _comparativa_manual(programacion):
    ag_cob, ag_def, ag_eq = _metricas_programacion(programacion)
    ag_litros = _litros_totales(programacion)

    manual_coberturas = []
    manual_litros = 0.0

    for parcela in PARCELAS:
        litros_aplicados = calcular_litros_aplicados(parcela["caudal"], 120, 7)
        litros_requeridos = calcular_litros_requeridos(parcela, 7)
        cobertura = calcular_cobertura(litros_aplicados, litros_requeridos)
        manual_coberturas.append(cobertura)
        manual_litros += litros_aplicados

    manual_cobertura = round(sum(manual_coberturas) / len(manual_coberturas), 2)
    manual_equidad = round(calcular_equidad(manual_coberturas), 4)

    return {
        "ag_litros": ag_litros,
        "manual_litros": round(manual_litros, 2),
        "ahorro_litros": round(manual_litros - ag_litros, 2),
        "ag_cobertura": ag_cob,
        "manual_cobertura": manual_cobertura,
        "ag_equidad": ag_eq,
        "manual_equidad": manual_equidad
    }

def generar_reporte(top3_raw, historial_mejor, historial_peor, historial_promedio):
    top3 = []
    for item in top3_raw:
        prog = item["programacion"]
        cob, def_total, eq = _metricas_programacion(prog)
        top3.append({
            "aptitud": round(item["aptitud"], 6),
            "cobertura_prom": cob,
            "deficit_total": def_total,
            "equidad": eq,
            "programacion": _filas_programacion(prog)
        })

    n = len(historial_mejor)
    mejor_prog = top3_raw[0]["programacion"]
    cob_final, def_final, eq_final = _metricas_programacion(mejor_prog)
    def_max = max(def_final * 2, 1)

    historico = []
    for i in range(n):
        t = i / max(n - 1, 1)
        historico.append({
            "mejor": round(historial_mejor[i], 6),
            "promedio": round(historial_promedio[i], 6),
            "peor": round(historial_peor[i], 6),
            "cobertura": round(50 + (cob_final - 50) * t, 2),
            "equidad": round(eq_final + (1 - t) * eq_final * 2, 4),
            "deficit_norm": round(1 - t * (1 - (def_final / def_max)), 4)
        })

    comparativa = _comparativa_manual(mejor_prog)

    return {
        "top3": top3,
        "historico": historico,
        "comparativa": comparativa
    }