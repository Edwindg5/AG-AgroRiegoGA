#individuo.py
import random
from datos.parcelas import PARCELAS

BITS_HORA = 5
BITS_DURACION = 8
BITS_DIAS = 7
BITS_POR_PARCELA = BITS_HORA + BITS_DURACION + BITS_DIAS
NUM_PARCELAS = len(PARCELAS)
TOTAL_BITS = BITS_POR_PARCELA * NUM_PARCELAS

def generar_individuo():
    individuo = []
    for i in range(TOTAL_BITS):
        individuo.append(random.randint(0, 1))
    return individuo

def decodificar_individuo(individuo):
    parcelas_decodificadas = []
    for i in range(NUM_PARCELAS):
        inicio = i * BITS_POR_PARCELA

        bits_hora = individuo[inicio: inicio + BITS_HORA]
        decimal_hora = 0
        for j in range(BITS_HORA):
            decimal_hora += bits_hora[j] * (2 ** (BITS_HORA - 1 - j))
        hora = decimal_hora % 24

        bits_duracion = individuo[inicio + BITS_HORA: inicio + BITS_HORA + BITS_DURACION]
        decimal_duracion = 0
        for j in range(BITS_DURACION):
            decimal_duracion += bits_duracion[j] * (2 ** (BITS_DURACION - 1 - j))
        duracion = decimal_duracion % 181

        bits_dias = individuo[inicio + BITS_HORA + BITS_DURACION: inicio + BITS_POR_PARCELA]
        dias = []
        nombres_dias = ["lun", "mar", "mie", "jue", "vie", "sab", "dom"]
        for j in range(BITS_DIAS):
            if bits_dias[j] == 1:
                dias.append(nombres_dias[j])

        parcelas_decodificadas.append({
            "id": PARCELAS[i]["id"],
            "hora": hora,
            "duracion": duracion,
            "dias": dias
        })

    return parcelas_decodificadas