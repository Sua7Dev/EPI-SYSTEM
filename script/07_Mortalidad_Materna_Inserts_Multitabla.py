# 07_Mortalidad_Materna_Inserts_Multitabla.py
import random
from datetime import date, timedelta
from faker import Faker
import json
import sys
import codecs

# Configurar la salida estándar para UTF-8
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)

fake = Faker('es_ES')
NUM_REGISTROS = 37 # Generaremos 100 registros de Mortalidad Materna

# --- Listas de Datos (Reutilizadas y Adaptadas) ---
NOMBRES_MUJER = [
    "María", "Ana", "Carmen", "Isabel", "Rosa", "Luisa", "Teresa", "Andrea", 
    "Carolina", "Patricia", "Laura", "Gabriela", "Camila", "Valentina", "Sofía", 
    "Daniela", "Mariana", "Victoria", "Fernanda", "Natalia", "Adriana", "Alejandra", 
    "Génesis", "Valeria", "Gabriela", "Antonieta", "Xiomara", "Yosmary", "Yulimar", 
    "Yusmary", "Mariángel", "Luisana", "Mayerling", "Lismar", "Oriana", "Ninoska", 
    "Lilian", "Yolanda", "Mercedes", "Diana", "Clara", "Elena", "Beatriz", "Rocío", 
    "Silvia", "Alicia", "Irma", "Margarita", "Gladys", "Marta", "Susana", "Julia", 
    "Esther", "Ruth", "Raquel", "Verónica", "Olivia", "Noelia", "Jimena", "Paula", 
    "Eva", "Inés", "Claudia", "Nora", "Elisa", "Miriam", "Lidia", "Cecilia", 
    "Rosa María", "Ángela", "Consuelo", "Dolores", "Catalina", "Bernarda", "Gloria", 
    "Milagros", "Esperanza", "Pilar", "Concepción", "Juana", "Petra", "Manuela", 
    "Francisca", "Josefina", "Lourdes", "Soledad", "Amparo", "Lucía", "Rita", 
    "Edith", "Matilde", "Emma", "Alba", "Berta", "Elvira", "Irene", "Olga", 
    "Nelly", "Wilmer", "Yajaira", "Yusbely", "Zulay", "Zulimar"
]

APELLIDOS = [
    "González", "Rodríguez", "Pérez", "García", "Martínez", "López", "Hernández", 
    "Gómez", "Díaz", "Vásquez", "Rojas", "Morales", "Castillo", "Ramírez", "Ramos", 
    "Suárez", "Romero", "Torres", "Flores", "Rivera", "Álvarez", "Mendoza", "Vargas", 
    "Medina", "Guerrero", "Reyes", "Castro", "Ortiz", "Silva", "Núñez", "Jiménez", 
    "Molina", "Delgado", "Peña", "Cruz", "Acosta", "Herrera", "Fernández", "Vega", 
    "Chávez", "Cabrera", "Briceño", "Barrios", "Aguilar", "Paredes", "Salazar", 
    "Mejía", "Quintana", "Contreras", "Arias", "Parra", "Sandoval", "Bravo", "Miranda", 
    "Zambrano", "Montes", "Escobar", "Cárdenas", "Campos", "León", "Fuentes", "Márquez", 
    "Valera", "Figueroa", "Rivas", "Padilla", "Calderón", "Bermúdez", "Sánchez", 
    "Méndez", "Rangel", "Duarte", "Brito", "Cordero", "Moreno", "Pinto", "Urdaneta", 
    "Marín", "Villalobos", "Peraza", "Quintero", "Velásquez", "Navarro", "Rincón", 
    "Marcano", "Barreto", "Salas", "Lara", "Zambrano", "Arroyo", "Carrillo", "Carvajal", 
    "Guerra", "Ibarra", "Serrano", "Valdez", "Galindo", "Véliz", "Yánez", "Zapata", 
    "Arévalo", "Bautista", "Bernal", "Blanco", "Bustamante", "Cano", "Cantillo", 
    "Caraballo", "Cedeno", "Colina", "Correa", "Cortez", "Del Castillo", "Estrada", 
    "Fajardo", "Gallegos", "Gil", "Granados", "Guevara", "Gutiérrez", "Henríquez", 
    "Izquierdo", "Jaimes", "Lozano", "Lucena", "Maldonado", "Marques", "Mora", 
    "Murillo", "Naranjo", "Navia", "Olivo", "Ortega", "Ospina", "Palma", "Palacios", 
    "Paz", "Pereira", "Prieto", "Pulido", "Quiñones", "Quiroz", "Redondo", "Restrepo", 
    "Roldán", "Rosales", "Ruiz", "Salcedo", "Salinas", "Santana", "Sierra", "Soto", 
    "Téllez", "Toro", "Trejo", "Trujillo", "Uribe", "Valencia", "Valenzuela", 
    "Varela", "Vera", "Vidal", "Villegas", "Yépez", "Zabala", "Zambrano", "Zambrano", 
    "Abreu", "Alvarado", "Amaya", "Aranda", "Arcila", "Arguello", "Arismendi", 
    "Arjona", "Arrate", "Arteaga", "Asuaje", "Aular", "Avila", "Azocar", "Báez", 
    "Bandres", "Barboza", "Baron", "Barros", "Bello", "Benitez", "Betancourt", 
    "Bohorquez", "Bolivar", "Borjas", "Briceño", "Burgos", "Caballero", "Cadenas", 
    "Calles", "Campo", "Cardona", "Carreño", "Carvajal", "Casas", "Castañeda", 
    "Causado", "Celis", "Cerrada", "Cicero", "Cisneros", "Colmenares", "Consalvi"
]

# Datos Geográficos (Reutilizados de Morbilidad)
MUNICIPIOS_DATA = {
    "Simón Rodríguez": ["Edmundo Barrios", "Miguel Otero Silva", "Atapirire"],
    "Guanipa": ["San José de Guanipa", "El Chaparro", "San José de Anaco"],
    "Independencia": ["Ciudad Orinoco", "Mamo", "Soledad"],
    "Miranda": ["Clarines", "Boca de Uchire", "San Pablo"],
    "José Gregorio Monagas": ["Mapire", "Piar", "Santa Cruz del Orinoco"]
}
PARROQUIAS_LISTA = [p for subs in MUNICIPIOS_DATA.values() for p in subs]


# [Se asume que las listas de Nombres (Mujer), Apellidos y Datos Geográficos existen aquí, copiadas de scripts anteriores]

# Diccionario de causas/sintomas para Mortalidad Materna
CAUSAS_SINTOMAS_MATERNA = {
    "Hemorragia posparto": "sangrado vaginal abundante, palidez, taquicardia, hipotensión, mareo, debilidad.",
    "Preeclampsia": "hipertensión, proteinuria, edema en cara y manos, cefalea, visión borrosa.",
    "Eclampsia": "convulsiones, pérdida de conciencia, hipertensión severa, dolor epigástrico.",
    "Infección puerperal": "fiebre >38°C, loquios fétidos, dolor abdominal, taquicardia.",
    "Sepsis": "fiebre alta, hipotensión, confusión, taquicardia, escalofríos.",
    "Ruptura uterina": "dolor abdominal súbito, sangrado vaginal, pérdida de tono uterino, sufrimiento fetal.",
    "Aborto inseguro": "sangrado vaginal, dolor pélvico, fiebre, secreción vaginal fétida.",
    "Embolia de líquido amniótico": "disnea súbita, hipotensión, cianosis, convulsiones, paro cardíaco.",
    "Embarazo ectópico roto": "dolor abdominal agudo, sangrado vaginal, mareo, síncope.",
    "Trastornos hipertensivos del embarazo": "presión elevada, proteinuria, edema, visión borrosa.",
    "Desprendimiento prematuro de placenta": "dolor abdominal intenso, sangrado vaginal, útero duro, sufrimiento fetal.",
    "Embolia pulmonar": "disnea súbita, dolor torácico, taquicardia, hemoptisis.",
    "Cardiopatía preexistente agravada": "disnea, fatiga, palpitaciones, edema periférico.",
    "Síndrome HELLP": "hemólisis, enzimas hepáticas elevadas, plaquetas bajas, dolor epigástrico.",
    "Falta de atención prenatal": "ausencia de control, detección tardía de complicaciones.",
    "Retraso en la atención obstétrica": "progresión de síntomas sin intervención, complicaciones evitables.",
}

# --- Funciones Auxiliares ---
START_DATE_DEF = date(2024, 1, 1)
END_DATE_DEF = date(2025, 12, 31)
MIN_EDAD_AÑOS = 18
MAX_EDAD_AÑOS = 40

def generar_nombre_completo(es_mujer=True):
    """Genera nombres y apellidos solo femeninos para Mortalidad Materna."""
    if es_mujer:
        nombre = random.choice(NOMBRES_MUJER)
    else:
        # Fallback, aunque no se usa en este script
        nombre = random.choice(NOMBRES_MUJER) 

    apellido1 = random.choice(APELLIDOS)
    apellido2 = random.choice(APELLIDOS)
    return f"{nombre} {apellido1} {apellido2}"

def generar_direccion_exacta(municipio):
    # [Función copiada de SCRIPT 06]
    sectores = {
        "Simón Rodríguez": ["Pueblo Nuevo Sur", "Campo Alegre", "Casco Central", "Vía San Tomé"],
        "Guanipa": ["Barrio Simón Bolívar", "Los Olivos", "Centro", "El Palomar"],
        "Independencia": ["El Centro", "La Esperanza", "Km 55"],
        "Miranda": ["Las Malvinas", "El Casco", "Vía Clarines"],
        "José Gregorio Monagas": ["Sector Las Vegas", "El Centro", "Punta de Mata"]
    }
    tipo_via = random.choice(["Calle", "Carrera", "Avenida"])
    num_via = random.randint(1, 100)
    sector = random.choice(sectores.get(municipio, ["Sector Genérico"]))
    return f"{tipo_via} {num_via}, Sector {sector}, cerca del CDI. ({municipio})"

def generar_datos_ingreso_defuncion():
    """Genera la relación idx_defuncion (clave) : idx_ingreso (valor)"""
    idx_defuncion = random.choice(list(CAUSAS_SINTOMAS_MATERNA.keys()))
    idx_ingreso = CAUSAS_SINTOMAS_MATERNA[idx_defuncion]
    return idx_defuncion.replace("'", "''"), idx_ingreso.replace("'", "''")


def generar_fecha_y_edad_materna():
    """Genera fecha de nacimiento y defunción coherente (18 a 40 años)."""
    
    # 1. Definir la fecha de defunción (entre 2024 y 2025)
    random_days_def = random.randint(0, (END_DATE_DEF - START_DATE_DEF).days)
    fecha_defuncion = START_DATE_DEF + timedelta(days=random_days_def)
    
    # 2. Definir la edad
    edad_años = random.randint(MIN_EDAD_AÑOS, MAX_EDAD_AÑOS)
    edad_junto = f"{edad_años} Años"
    
    # 3. Calcular la fecha de nacimiento (defunción - edad_años)
    dias_para_restar = edad_años * 365 + random.randint(0, 364) # Asegura que la edad sea exacta en algún momento
    fecha_nacimiento = fecha_defuncion - timedelta(days=dias_para_restar)
    
    # 4. Fecha y Hora de ingreso (puede ser el mismo día o unos días antes)
    fecha_ingreso = fecha_defuncion - timedelta(days=random.randint(0, 5)) # Ingresa 0 a 5 días antes
    hora_aleatoria_ingreso = f"{random.randint(0, 23):02}:{random.randint(0, 59):02}:00"
    
    # 5. Hora de defunción
    hora_aleatoria_defuncion = f"{random.randint(0, 23):02}:{random.randint(0, 59):02}:00"

    # Formato DD/MM/YYYY
    return {
        "fecha_nacimiento": fecha_nacimiento.strftime("%d/%m/%Y"),
        "fecha_ingreso": fecha_ingreso.strftime("%d/%m/%Y"),
        "hora_ingreso": hora_aleatoria_ingreso,
        "fecha_defuncion": fecha_defuncion.strftime("%d/%m/%Y"),
        "hora_defuncion": hora_aleatoria_defuncion,
        "edad_junto": edad_junto,
        "edad_solo": edad_años
    }

# --- Configuración de IDs Fijos ---
ID_FIJO_DOCTOR = 1
ID_FIJO_ADMIN = 1

# ----------------------------------------------------
# 1. GENERACIÓN DE DATOS Y SENTENCIAS SQL EN ORDEN
# ----------------------------------------------------

sql_statements_paciente = []
sql_statements_direccion = []
sql_statements_mortalidad = []
sql_statements_materna = []
ID_MAPPING = [] 

# Contadores de secuencia para el diccionario
start_idx_defuncion = 50000
start_idx_ingreso = 60000


for i in range(NUM_REGISTROS):
    
    # IDs de texto solicitados (Clave : Valor)
    idx_defuncion_key = start_idx_defuncion + i
    idx_ingreso_val = start_idx_ingreso + i

    # Datos temporales
    historia_clinica = random.randint(11111111, 99999999)
    # Nombre debe ser femenino
    nombres_apellidos = generar_nombre_completo(es_mujer=True).replace("'", "''")
    
    fechas = generar_fecha_y_edad_materna()
    idx_def_txt, idx_ing_txt = generar_datos_ingreso_defuncion()
    
    # Datos Geográficos
    parroquia_random = random.choice(PARROQUIAS_LISTA)
    municipio_random = next(k for k, v in MUNICIPIOS_DATA.items() if parroquia_random in v)
    direccion_exacta = generar_direccion_exacta(municipio_random).replace("'", "''") 
    
    
    # --- PASO 1: Insertar en persona_paciente (para obtener ID_PACIENTE) ---
    sql_statements_paciente.append(
        f"INSERT INTO persona_paciente (edad) VALUES ({fechas['edad_solo']});"
    )

    # --- PASO 2: Insertar en direccion (para obtener ID_DIRECCION) ---
    sql_statements_direccion.append(
        f"INSERT INTO direccion (descripcion, id_parroquia) VALUES ('{direccion_exacta}', (SELECT id_parroquia FROM parroquia WHERE nombre = '{parroquia_random}'));"
    )

    # --- 3. Generar Mapeo para el SCRIPT FINAL (usando IDs de búsqueda) ---
    ID_MAPPING.append({
        "nombres_apellidos": nombres_apellidos,
        "direccion_exacta": direccion_exacta, 
        "historia_clinica": historia_clinica,
        "idx_defuncion_key": idx_defuncion_key, 
        "idx_ingreso_val": idx_ingreso_val,
        # Datos para Mortalidad (Tabla Principal)
        "idx_ingreso_txt": idx_ing_txt,
        "idx_defuncion_txt": idx_def_txt,
        "fecha_nacimiento": fechas["fecha_nacimiento"],
        "fecha_ingreso": fechas["fecha_ingreso"],
        "hora_ingreso": fechas["hora_ingreso"],
        "fecha_defuncion": fechas["fecha_defuncion"],
        "hora_defuncion": fechas["hora_defuncion"],
        # Datos de relleno
        "edad_junto": fechas["edad_junto"],
        "id_doctor": ID_FIJO_DOCTOR,
        "id_administrador": ID_FIJO_ADMIN
    })


# ----------------------------------------------------
# 2. IMPRESIÓN DEL SCRIPT SQL (3 INSERTS EN CASCADA)
# ----------------------------------------------------

print("BEGIN TRANSACTION;")
print("-- --------------------------------------------------------------------------------------")
print("-- SCRIPT 07: INSERCIÓN EN MORTALIDAD MATERNA (3 Tablas en Cascada)")
print("-- --------------------------------------------------------------------------------------")

# --- 1. Insertar Pacientes ---
print("\n-- 1. INSERTAR ENTIDADES PACIENTE (Para obtener id_paciente, clave para mortalidad)")
for sql in sql_statements_paciente:
    print(sql)

# --- 2. Insertar Direcciones ---
print("\n-- 2. INSERTAR ENTIDADES DIRECCIÓN (Para obtener id_direccion, clave para mortalidad)")
for sql in sql_statements_direccion:
    print(sql)

# --- 3. Insertar Mortalidad (Principal) y Materna (Detalle) ---
print("\n-- 3. INSERTAR MORTALIDAD (Principal) y MORTALIDAD_MATERNA (Detalle)")

# Lookups
paciente_lookup = "(SELECT MAX(id_paciente) FROM persona_paciente)" 
direccion_lookup_template = "(SELECT id_direccion FROM direccion WHERE descripcion = '{desc}' LIMIT 1)"

print("DELETE FROM mortalidad_materna;") 
# print("DELETE FROM mortalidad;") # No limpiamos 'mortalidad' ya que ya contiene Neonatal e Infantil.

for i, registro in enumerate(ID_MAPPING):
    
    # A) INSERT en la tabla 'mortalidad' (Tabla Principal)
    paciente_id_calc = f"{paciente_lookup} - {NUM_REGISTROS - (i+1)}"
    
    sql_mortalidad = (
        f"INSERT INTO mortalidad ("
        f"id_paciente, historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, "
        f"hora_ingreso, fecha_defuncion, hora_defuncion, id_direccion, idx_ingreso, "
        f"idx_defuncion, fecha_registro_formulario"
        f") VALUES ("
        f"{paciente_id_calc}, " 
        f"'{registro['historia_clinica']}', '{registro['nombres_apellidos']}', "
        f"'{registro['fecha_nacimiento']}', '{registro['fecha_ingreso']}', "
        f"'{registro['hora_ingreso']}', '{registro['fecha_defuncion']}', "
        f"'{registro['hora_defuncion']}', "
        f"{direccion_lookup_template.format(desc=registro['direccion_exacta'])}, "
        f"'{registro['idx_ingreso_txt']}', '{registro['idx_defuncion_txt']}', "
        f"'{date.today().strftime('%Y-%m-%d')}'"
        f");"
    )
    sql_statements_mortalidad.append(sql_mortalidad)
    print(sql_mortalidad)
    
    # B) INSERT en la tabla 'mortalidad_materna' (Tabla Detalle)
    
    sql_materna = (
        f"INSERT INTO mortalidad_materna ("
        f"id_m"
        f") VALUES ("
        f"LAST_INSERT_ROWID()" # Usa el ID de la mortalidad recién insertada
        f");"
    )
    sql_statements_materna.append(sql_materna)
    print(sql_materna)
    
    # Imprimir el diccionario solicitado por el usuario
    print(f"-- IDx Materna: {registro['idx_defuncion_key']} : {registro['idx_ingreso_val']}")

print("COMMIT;")
print(f"\n-- TOTAL DE REGISTROS DE MORTALIDAD MATERNA GENERADOS: {NUM_REGISTROS}")
print("-- RECUERDA: Este script asume que la secuencia de IDs de persona_paciente e ID de direccion continúa a partir de los registros anteriores.")

# python 07_Mortalidad_Materna_Inserts_Multitabla.py > 07_materna_inserts.sql