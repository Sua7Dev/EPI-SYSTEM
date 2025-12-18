# 01_Morbilidad_Preparacion_Geografica.py
import random
from datetime import date, timedelta
import sys
import codecs

# Configurar la salida estándar para UTF-8
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
# --- Datos Fijos de Ubicación ---
# Asumimos que ID_CIUDAD = 1 (El Tigre) ya existe.
ID_CIUDAD = 1 

MUNICIPIOS_DATA = {
    "Simón Rodríguez": ["Edmundo Barrios", "Miguel Otero Silva", "Atapirire"],
    "Guanipa": ["San José de Guanipa", "El Chaparro", "San José de Anaco"],
    "Independencia": ["Ciudad Orinoco", "Mamo", "Soledad"],
    "Miranda": ["Clarines", "Boca de Uchire", "San Pablo"],
    "José Gregorio Monagas": ["Mapire", "Piar", "Santa Cruz del Orinoco"]
}

# ----------------------------------------------------
# 1. GENERACIÓN DE SENTENCIAS SQL
# ----------------------------------------------------
sql_statements = []

# --- 1. Crear Municipios Faltantes ---
sql_statements.append("-- 1. INSERTAR MUNICIPIOS (usando autoincremento)")
# Insertamos los municipios que no sean "Simón Rodríguez" (asumimos que ya existe con ID 1)
for nombre_muni in MUNICIPIOS_DATA.keys():
    if nombre_muni != "Simón Rodríguez":
        sql_statements.append(
            f"INSERT INTO municipio (nombre, id_ciudad) VALUES ('{nombre_muni}', {ID_CIUDAD});"
        )

# --- 2. Crear las Parroquias ---
sql_statements.append("\n-- 2. INSERTAR PARROQUIAS (usando subconsulta para obtener id_municipio)")
# La tabla parroquia tiene (id_parroquia, nombre, id_municipio)
for nombre_muni, parroquias in MUNICIPIOS_DATA.items():
    
    for nombre_parroquia in parroquias:
        # Excluimos 'Edmundo Barrios' (asumida ID 1 inicial)
        if nombre_parroquia != "Edmundo Barrios":
            # Usamos subquery para encontrar el id_municipio correcto por nombre
            sql_statements.append(
                f"INSERT INTO parroquia (nombre, id_municipio) VALUES ('{nombre_parroquia}', (SELECT id_municipio FROM municipio WHERE nombre = '{nombre_muni}'));"
            )

# ----------------------------------------------------
# 2. IMPRESIÓN DEL SCRIPT SQL FINAL
# ----------------------------------------------------
print("BEGIN TRANSACTION;")
print("-- --------------------------------------------------------------------------------------")
print("-- SCRIPT 01: PREPARACIÓN GEOGRÁFICA (Morbilidad)")
print("-- --------------------------------------------------------------------------------------")
print("PRAGMA foreign_keys = OFF;") # Deshabilitar FKs temporalmente si hay problemas de orden

for sql in sql_statements:
    print(sql)

print("PRAGMA foreign_keys = ON;")
print("COMMIT;")