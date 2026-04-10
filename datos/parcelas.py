#parcelas.py
FACTOR_SUELO = {
    "arenoso": 1.3,
    "franco": 1.0,
    "arcilloso": 0.8
}

PARCELAS = [
    {"id": "P1", "area": 50,  "suelo": "arenoso",  "cultivo": "maiz",     "etapa": "floracion",   "caudal": 400},
    {"id": "P2", "area": 30,  "suelo": "franco",    "cultivo": "frijol",   "etapa": "vegetativo",  "caudal": 250},
    {"id": "P3", "area": 45,  "suelo": "arcilloso", "cultivo": "calabaza", "etapa": "germinacion", "caudal": 300},
    {"id": "P4", "area": 60,  "suelo": "franco",    "cultivo": "maiz",     "etapa": "vegetativo",  "caudal": 500},
    {"id": "P5", "area": 35,  "suelo": "arenoso",   "cultivo": "frijol",   "etapa": "maduracion",  "caudal": 200},
    {"id": "P6", "area": 40,  "suelo": "arcilloso", "cultivo": "calabaza", "etapa": "floracion",   "caudal": 350},
    {"id": "P7", "area": 55,  "suelo": "franco",    "cultivo": "maiz",     "etapa": "germinacion", "caudal": 450}
]