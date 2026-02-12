import sqlite3
from faker import Faker
import random
from datetime import date, timedelta
import sys
import codecs

# Configurar la salida estándar para UTF-8
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
# 1. Configuración y Claves Foráneas
# ------------------------------------
ID_DOCTOR_INICIAL = 1 
NUM_REGISTROS = 52
fake = Faker('es_ES')

# Definición de la tabla y sus campos
TABLA_NATALIDAD = "natalidad"
CAMPOS_NATALIDAD = [
    "id_doctor", "fecha", "partos", "cesareas", "varones", 
    "hembras", "gemelar", "mto", "partos_extrahospitalarios", 
    "fecha_registro_formulario"
]

# Definición de rango de fechas
START_DATE = date(2024, 1, 1)
END_DATE = date(2025, 12, 31)

def generar_fecha_aleatoria(start_date, end_date):
    """Genera una fecha aleatoria dentro del rango especificado."""
    random_days = random.randint(0, (end_date - start_date).days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

def generar_datos_natalidad(doctor_id):
    """Genera una fila de datos coherentes para la tabla natalidad."""
    
    # Ambas fechas serán aleatorias entre 2024 y 2025
    fecha_evento = generar_fecha_aleatoria(START_DATE, END_DATE)
    
    # Para mayor realismo, la fecha de registro puede ser el mismo día o un poco después
    fecha_registro = generar_fecha_aleatoria(START_DATE, END_DATE)

    # 1. Generar el total de nacimientos
    total_nacidos_vivos = random.randint(5, 20)
    
    # 2. Distribución coherente
    mto = random.randint(0, int(total_nacidos_vivos * 0.1)) # Mortinatos (0-10% del total)
    partos_extra = random.randint(0, 3) # Partos fuera del hospital
    
    total_nacimientos = total_nacidos_vivos + mto
    
    # Distribuir entre partos y cesáreas
    cesareas = random.randint(int(total_nacimientos * 0.1), int(total_nacimientos * 0.4))
    partos = total_nacimientos - cesareas 
    if partos < 0: partos = 0
    
    # Distribución por sexo
    varones = random.randint(int(total_nacidos_vivos * 0.4), int(total_nacidos_vivos * 0.6))
    hembras = total_nacidos_vivos - varones
    
    # Partos gemelares
    gemelar_pares = random.randint(0, int(total_nacimientos * 0.1))

    # Creamos la tupla de datos
    return (
        doctor_id, 
        fecha_evento,
        partos, 
        cesareas, 
        varones, 
        hembras, 
        gemelar_pares, 
        mto, 
        partos_extra, 
        fecha_registro # fecha_registro_formulario (aleatoria 2024-2025)
    )

# 2. Generación del Script SQL
# -----------------------------
sql_inserts = []
for i in range(NUM_REGISTROS):
    datos = generar_datos_natalidad(ID_DOCTOR_INICIAL)
    
    # Formato de la sentencia SQL (usando formato f-string para insertar valores directamente)
    # Importante: Las fechas y el ID del doctor deben ir sin comillas para SQLite
    insert_sql = (
        f"INSERT INTO {TABLA_NATALIDAD} "
        f"({', '.join(CAMPOS_NATALIDAD)}) VALUES ("
        f"{datos[0]}, '{datos[1]}', {datos[2]}, {datos[3]}, {datos[4]}, "
        f"{datos[5]}, {datos[6]}, {datos[7]}, {datos[8]}, '{datos[9]}'"
        f");"
    )

    sql_inserts.append(insert_sql)

# 3. Impresión del Script
# -----------------------
print("BEGIN TRANSACTION;")
print(f"-- Script de inserción para {NUM_REGISTROS} registros en la tabla natalidad")
print(f"-- Rango de fechas para 'fecha' y 'fecha_registro_formulario': 2024-01-01 a 2025-12-31")
print(f"DELETE FROM {TABLA_NATALIDAD}; -- Opcional: Limpiar la tabla antes de insertar")

for sql in sql_inserts:
    print(sql)

print("COMMIT;")

# python script_nata.py > script_nata.sql