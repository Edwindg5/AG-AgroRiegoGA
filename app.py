# app.py
from flask import Flask, render_template, request, jsonify
from main import correr_ag
from salidas.reporte import generar_reporte
from salidas.graficas import grafica_evolucion_aptitud, grafica_cobertura
from datos.parcelas import PARCELAS

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')

# Almacén en memoria para los resultados del AG
_resultados_cache = None


# ─── PÁGINAS ────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html', parcelas=PARCELAS)


@app.route('/resultados')
def resultados():
    return render_template('resultados.html')


@app.route('/calendario')
def calendario():
    return render_template('calendario.html')


# ─── API DE DATOS ────────────────────────────────────────────────────────────

@app.route('/api/parcelas')
def api_parcelas():
    """Devuelve la lista de parcelas para que el frontend la muestre."""
    return jsonify(PARCELAS)


@app.route('/api/resultados')
def api_resultados():
    """
    Devuelve los resultados del último AG ejecutado.
    Formato esperado por el frontend:
    {
        "top3": [ { aptitud, cobertura_prom, deficit_total, equidad, programacion: [...] } ],
        "historico": [ { mejor, promedio, peor, cobertura, equidad, deficit_norm } ],
        "comparativa": { ag_litros, manual_litros, ahorro_litros,
                         ag_cobertura, manual_cobertura,
                         ag_equidad,  manual_equidad }
    }
    """
    global _resultados_cache
    if _resultados_cache is None:
        return jsonify({"error": "No hay resultados aún. Ejecuta el AG primero."}), 404
    return jsonify(_resultados_cache)


# ─── EJECUCIÓN DEL AG ────────────────────────────────────────────────────────

@app.route('/ejecutar', methods=['POST'])
def ejecutar():
    global _resultados_cache

    try:
        datos = request.get_json()

        cantidad_individuos = int(datos.get('npob', 50))
        generaciones = int(datos.get('ngen', 100))
        prob_cruza = float(datos.get('pc', 0.85)) * 100
        prob_mut_individuo = float(datos.get('pm', 0.01)) * 100
        prob_mut_gen = float(datos.get('pmg', 0.05)) * 100

        resultado = correr_ag(
            cantidad_individuos=cantidad_individuos,
            generaciones=generaciones,
            prob_cruza=prob_cruza,
            prob_mut_individuo=prob_mut_individuo,
            prob_mut_gen=prob_mut_gen
        )

        grafica_evolucion_aptitud(
            resultado["historial_mejor"],
            resultado["historial_peor"],
            resultado["historial_promedio"]
        )
        grafica_cobertura(resultado["mejor_programacion"], PARCELAS)

        reporte = generar_reporte(
            resultado["top3"],
            resultado["historial_mejor"],
            resultado["historial_peor"],
            resultado["historial_promedio"]
        )

        _resultados_cache = reporte
        return jsonify(reporte)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─── MAIN ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True)