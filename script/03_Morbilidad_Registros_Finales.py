# 03_Morbilidad_Registros_Finales.py > 03_Morbilidad_Registros_Finales.sql
import json
import sys
import codecs

# Configurar la salida estándar para UTF-8
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
# --- Configuración de IDs de inicio (debe coincidir con el SCRIPT 02) ---
# Si persona_paciente se limpió, el primer ID será 1.
ID_INICIO_PACIENTE = 1 
# Si direccion se limpió y el ID 1 es el hospital, el primer ID nuevo será 2.
ID_INICIO_DIRECCION = 2 

# ----------------------------------------------------
# 1. CARGAR MAPPING DE DATOS
# ----------------------------------------------------
try:
    with open("morbilidad_data_mapping.json", "r") as f:
        ID_MAPPING = json.load(f)
except FileNotFoundError:
    print("\n-- ERROR: No se encontró el archivo 'morbilidad_data_mapping.json'.")
    print("-- Por favor, ejecuta el SCRIPT 02 primero.")
    exit()

# ----------------------------------------------------
# 2. GENERACIÓN DE SENTENCIAS SQL
# ----------------------------------------------------
sql_statements_morbilidad = []

TABLA_MORBILIDAD = "morbilidad"

for i, registro in enumerate(ID_MAPPING):
    
    # Asignación de IDs basada en la secuencia del Script 02
    id_paciente_fk = ID_INICIO_PACIENTE + i
    id_direccion_fk = ID_INICIO_DIRECCION + i

    # Datos
    nombres = registro['nombres_apellidos']
    diagnostico = registro['diagnostico']
    fecha_reg = registro['fecha_reg']
    
    # Generar INSERT final
    insert_sql = (
        f"INSERT INTO {TABLA_MORBILIDAD} (id_paciente, id_direccion_hogar, nombres_apellidos, diagnostico, fecha_registro_formulario) VALUES ("
        f"{id_paciente_fk}, "
        f"{id_direccion_fk}, "
        f"'{nombres}', "
        f"'{diagnostico}', "
        f"'{fecha_reg}'"
        f");"
    )

    sql_statements_morbilidad.append(insert_sql)

# ----------------------------------------------------
# 3. IMPRESIÓN DEL SCRIPT SQL FINAL
# ----------------------------------------------------
print("BEGIN TRANSACTION;")
print("-- --------------------------------------------------------------------------------------")
print("-- SCRIPT 03: REGISTROS FINALES DE MORBILIDAD")
print("-- Inserta 300 registros en morbilidad usando la secuencia de IDs generada en el SCRIPT 02.")
print("-- --------------------------------------------------------------------------------------")
print(f"DELETE FROM {TABLA_MORBILIDAD};")

for sql in sql_statements_morbilidad:
    print(sql)

print("COMMIT;")
print(f"\n-- TOTAL DE REGISTROS DE MORBILIDAD GENERADOS: {len(sql_statements_morbilidad)}")