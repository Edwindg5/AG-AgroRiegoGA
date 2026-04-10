# aptitud.py
import math
from datos.parcelas import PARCELAS, FACTOR_SUELO
from datos.necesidades_hidricas import NECESIDADES_HIDRICAS
from datos.recursos import RECURSOS
from ag.individuo import decodificar_individuo

#  PESOS 
W_COBERTURA = 0.50   # cobertura hídrica tiene mayor peso
W_DEFICIT   = 0.30   # déficit hídrico
W_EQUIDAD   = 0.20   # equidad entre parcelas

#  CONSTANTES DE NORMALIZACIÓN 
# Déficit máximo posible: si ninguna parcela recibe agua en toda la semana
# = suma de litros requeridos de todas las parcelas en 7 días
def _calcular_deficit_maximo():
    total = 0.0
    for parcela in PARCELAS:
        cultivo = parcela["cultivo"]
        etapa   = parcela["etapa"]
        area    = parcela["area"]
        fs      = FACTOR_SUELO[parcela["suelo"]]
        nh      = NECESIDADES_HIDRICAS[cultivo][etapa]
        total  += nh * area * fs * 7
    return total if total > 0 else 1.0

# Equidad máxima posible: cuando una parcela tiene 100% y el resto 0%
# desviación estándar de [100, 0, 0, ..., 0]
def _calcular_equidad_maxima():
    n      = len(PARCELAS)
    vals   = [100.0] + [0.0] * (n - 1)
    media  = 100.0 / n
    var    = sum((v - media) ** 2 for v in vals) / n
    return math.sqrt(var) if var > 0 else 1.0

DEFICIT_MAX = _calcular_deficit_maximo()
EQUIDAD_MAX = _calcular_equidad_maxima()


#  FUNCIONES DE CÁLCULO 

def calcular_litros_aplicados(caudal, duracion, num_dias):
    """
    caudal   → L/hr  (dato fijo del sistema de riego)
    duracion → min   (variable de decisión del individuo)
    num_dias → días que se riega esa parcela en la semana
    """
    litros_por_riego = caudal * (duracion / 60.0)
    return litros_por_riego * num_dias


def calcular_litros_requeridos(parcela, num_dias):
    """
    Lr = Nh × A × fs × días
    Nh  → necesidad hídrica L/m²/día  (tabla INIFAP)
    A   → área m²
    fs  → factor de absorción del suelo
    """
    cultivo = parcela["cultivo"]
    etapa   = parcela["etapa"]
    area    = parcela["area"]
    fs      = FACTOR_SUELO[parcela["suelo"]]
    nh      = NECESIDADES_HIDRICAS[cultivo][etapa]
    return nh * area * fs * num_dias


def calcular_cobertura(litros_aplicados, litros_requeridos):
    """
    Cobertura = (La / Lr) × 100
    Acotada entre 0 y 100 (regar de más no mejora la cobertura).
    """
    if litros_requeridos <= 0:
        return 0.0
    cobertura = (litros_aplicados / litros_requeridos) * 100.0
    return min(cobertura, 100.0)


def calcular_deficit(litros_requeridos, litros_aplicados):
    """
    Déficit = Lr - La
    Solo cuenta el déficit positivo (falta de agua).
    El sobre-riego no penaliza aquí; la cobertura ya lo maneja.
    """
    deficit = litros_requeridos - litros_aplicados
    return max(deficit, 0.0)


def calcular_equidad(coberturas):
    """
    Equidad = desviación estándar de las coberturas entre parcelas.
    Valor bajo = distribución uniforme (bueno).
    """
    n = len(coberturas)
    if n == 0:
        return 0.0
    media   = sum(coberturas) / n
    varianza = sum((c - media) ** 2 for c in coberturas) / n
    return math.sqrt(varianza)


# APTITUD PRINCIPAL 

def calcular_aptitud(individuo):
    """
    Evalúa un individuo y devuelve su aptitud entre 0.0 y 1.0.

    Pasos:
      1. Decodificar el individuo (binario → programación)
      2. Calcular cobertura, déficit y equidad por parcela
      3. Normalizar déficit y equidad entre 0 y 1
      4. Aplicar la fórmula ponderada
    """
    programacion = decodificar_individuo(individuo)

    coberturas    = []
    deficit_total = 0.0

    for i, parcela in enumerate(PARCELAS):
        prog     = programacion[i]
        num_dias = len(prog["dias"])

        # Si no se riega esa parcela → litros aplicados = 0
        if num_dias == 0 or prog["duracion"] == 0:
            litros_aplicados = 0.0
        else:
            litros_aplicados = calcular_litros_aplicados(
                parcela["caudal"],
                prog["duracion"],
                num_dias
            )

        litros_requeridos = calcular_litros_requeridos(parcela, 7)
        cobertura         = calcular_cobertura(litros_aplicados, litros_requeridos)
        deficit           = calcular_deficit(litros_requeridos, litros_aplicados)

        coberturas.append(cobertura)
        deficit_total += deficit

    # Métricas globales
    cobertura_prom = sum(coberturas) / len(coberturas)   # 0 – 100
    equidad        = calcular_equidad(coberturas)         # 0 – EQUIDAD_MAX

    #Normalización (clamp a [0, 1]) 
    cobertura_norm = cobertura_prom / 100.0
    deficit_norm   = min(deficit_total / DEFICIT_MAX, 1.0)
    equidad_norm   = min(equidad / EQUIDAD_MAX, 1.0)

    # Fórmula ponderada 
    aptitud = (
        W_COBERTURA * cobertura_norm        # maximizar cobertura
      + W_DEFICIT   * (1.0 - deficit_norm)  # minimizar déficit
      + W_EQUIDAD   * (1.0 - equidad_norm)  # minimizar inequidad
    )

    # Garantizar rango [0, 1] por seguridad numérica
    return max(0.0, min(aptitud, 1.0))