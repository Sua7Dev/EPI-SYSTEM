# 06_Mortalidad_Infantil_Inserts_Multitabla.py > 06_Mortalidad_Infantil_Inserts_Multitabla.sql
import random
from datetime import date, timedelta
from faker import Faker
import json
import sys
import codecs

# Configurar la salida estándar para UTF-8
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
fake = Faker('es_ES')
NUM_REGISTROS = 65 # Generaremos 65 registros infantiles

# --- Listas de Datos (Reutilizadas) ---
NOMBRES_HOMBRE = [
    "José", "Juan", "Carlos", "Luis", "Miguel", "Alejandro", "Daniel", "Manuel", 
    "Jesús", "Antonio", "Francisco", "David", "Ángel", "Pedro", "Jorge", "Andrés", 
    "Fernando", "Rafael", "Gabriel", "Diego", "Roberto", "Javier", "Mario", "Ricardo", 
    "Eduardo", "Alberto", "Victor", "Mauricio", "Héctor", "Raúl", "Oscar", "Pablo", 
    "Santiago", "Gustavo", "Felipe", "Ronaldo", "Samuel", "Guillermo", "Emilio", 
    "Hugo", "Iván", "Rubén", "Julio", "César", "Marco", "Esteban", "Enrique", 
    "Ramón", "Simón", "Tomás", "Nicolás", "Adrián", "Víctor", "Leonardo", "Óscar", 
    "Walter", "Rodrigo", "Salvador", "Ramiro", "Armando", "René", "Gerardo", 
    "Rigoberto", "Martín", "Saúl", "Alonso", "Isaac", "Erick", "Gregorio", "Ismael", 
    "Fidel", "Fausto", "Ulises", "Bernardo", "Teodoro", "Aarón", "Damián", "Jacobo", 
    "Noé", "Cristian", "Patricio", "Baltazar", "Mateo", "Elias", "Emanuel", 
    "Cristóbal", "Joaquín", "Gonzalo", "Julian", "Eugenio", "Lorenzo", "Ignacio", 
    "Fermín", "Lucas", "Maximiliano", "Agustín", "Valentín", "Benjamín", "Sebastián"
]

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

# Diccionario de causas/sintomas
CAUSAS_SINTOMAS_NEONATAL = {
    "Prematuridad": "dificultad para respirar, succión débil, hipotermia, apnea, bajo peso, inmadurez pulmonar.",
    "Bajo peso al nacer": "hipotermia, hipoglucemia, dificultad para alimentarse, debilidad, ictericia.",
    "Asfixia perinatal": "cianosis, respiración irregular o ausente, tono muscular bajo, reflejos débiles, convulsiones.",
    "Sepsis neonatal": "fiebre o hipotermia, letargo, rechazo al alimento, dificultad respiratoria, ictericia.",
    "Infección del cordón umbilical (onfalitis)": "enrojecimiento, secreción purulenta, mal olor, fiebre, distensión abdominal.",
    "Neumonía neonatal": "fiebre, taquipnea, quejido respiratorio, retracciones, cianosis.",
    "Meningitis neonatal": "fiebre, irritabilidad, fontanela abombada, convulsiones, rechazo al alimento.",
    "Malformaciones congénitas mayores": "signos variables según el órgano afectado (cianosis, dificultad respiratoria, vómitos, abdomen distendido).",
    "Cardiopatías congénitas": "cianosis, soplo cardíaco, taquipnea, sudoración al alimentarse, fatiga.",
    "Enfermedad de membrana hialina": "dificultad respiratoria progresiva, quejido espiratorio, retracciones, cianosis.",
    "Hipoglucemia neonatal": "temblores, irritabilidad, apnea, convulsiones, letargo.",
    "Hipotermia": "piel fría, letargo, apnea, hipoglucemia, dificultad para alimentarse.",
    "Ictericia severa": "coloración amarilla de piel y ojos, somnolencia, succión débil, llanto agudo.",
    "Hemorragia intracraneal": "convulsiones, fontanela abombada, apnea, palidez, alteración del tono muscular.",
    "Síndrome de aspiración meconial": "dificultad respiratoria, cianosis, taquipnea, quejido, retracciones.",
    "Enterocolitis necrotizante": "distensión abdominal, sangre en heces, vómitos biliosos, letargo, fiebre.",
    "Infección por estreptococo del grupo B": "fiebre, dificultad respiratoria, letargo, convulsiones, shock.",
    "Infección por Listeria": "fiebre, dificultad respiratoria, ictericia, convulsiones, sepsis.",
    "Infección por citomegalovirus": "ictericia, hepatoesplenomegalia, microcefalia, convulsiones, petequias.",
    "Infección por toxoplasmosis": "hidrocefalia, convulsiones, coriorretinitis, ictericia, hepatoesplenomegalia.",
    "Infección por herpes neonatal": "lesiones vesiculares, fiebre, letargo, convulsiones, hepatitis.",
    "Infección por VIH congénito": "fiebre persistente, infecciones recurrentes, hepatoesplenomegalia, retraso del crecimiento.",
    "Infección por sífilis congénita": "lesiones cutáneas, rinorrea sanguinolenta, hepatoesplenomegalia, ictericia, anemia.",
    "Infección por rubéola congénita": "cataratas, sordera, cardiopatías, púrpura, retraso del crecimiento.",
    "Infección por Zika congénito": "microcefalia, hipertonía, convulsiones, retraso del desarrollo, calcificaciones intracraneales.",
    "Infección por hepatitis B": "ictericia, hepatomegalia, letargo, vómitos, fiebre.",
    "Hipoxia isquémica": "apnea, tono muscular bajo, convulsiones, acidosis, encefalopatía.",
    "Trastornos metabólicos congénitos": "vómitos, letargo, hipoglucemia, convulsiones, olor corporal inusual.",
    "Atresia esofágica": "salivación excesiva, tos al alimentarse, dificultad para tragar, distensión abdominal.",
    "Hernia diafragmática congénita": "dificultad respiratoria, abdomen hundido, cianosis, sonidos respiratorios disminuidos.",
    "Gastrosquisis": "asas intestinales expuestas al nacer, riesgo de sepsis, dificultad para alimentarse.",
    "Onfalocele": "masa abdominal cubierta por membrana, dificultad respiratoria si es grande.",
    "Hidrocefalia": "fontanela abombada, macrocefalia, vómitos, irritabilidad, mirada en sol poniente.",
    "Anencefalia": "ausencia de bóveda craneana, exposición del tejido cerebral, letalidad inmediata.",
    "Espina bífida": "masa en región lumbar, parálisis de miembros inferiores, hidrocefalia, incontinencia.",
    "Síndrome de Down con complicaciones": "hipotonía, cardiopatías congénitas, retraso del desarrollo, infecciones frecuentes.",
    "Trastornos de la coagulación": "sangrado umbilical persistente, hematomas, hemorragias internas, petequias.",
    "Hemorragia pulmonar": "dificultad respiratoria, hemoptisis, cianosis, taquicardia, shock.",
    "Hipertensión pulmonar persistente": "cianosis, taquipnea, soplo cardíaco, dificultad respiratoria.",
    "Cardiomiopatía neonatal": "taquicardia, hepatomegalia, dificultad para alimentarse, cianosis.",
    "Taquicardia supraventricular": "palpitaciones, taquicardia >220 lpm, palidez, dificultad para alimentarse.",
    "Arritmias congénitas": "bradicardia o taquicardia, síncope, cianosis, letargo.",
    "Shock séptico": "hipotensión, taquicardia, piel moteada, letargo, oliguria.",
    "Trauma obstétrico": "hematomas, fracturas, parálisis braquial, convulsiones si hay hemorragia intracraneal.",
    "Lesión cerebral hipóxica": "convulsiones, hipotonía, apnea, reflejos ausentes, encefalopatía.",
    "Retraso en el inicio de la lactancia": "hipoglucemia, pérdida de peso, ictericia, deshidratación.",
    "Alimentación inadecuada": "hipoglucemia, deshidratación, pérdida de peso, letargo.",
    "Falta de atención neonatal inmediata": "hipotermia, hipoglucemia, dificultad respiratoria no tratada.",
    "Nacimiento en domicilio sin asistencia": "riesgo de asfixia, sepsis, hipotermia, hemorragia.",
    "Falta de acceso a cuidados intensivos neonatales": "evolución de patologías graves sin soporte vital.",
}

# Datos Geográficos (Reutilizados de Morbilidad)
MUNICIPIOS_DATA = {
    "Simón Rodríguez": ["Edmundo Barrios", "Miguel Otero Silva"],
    "Guanipa": ["San José de Guanipa"],
}
PARROQUIAS_LISTA = [p for subs in MUNICIPIOS_DATA.values() for p in subs]


# [Se asume que las listas de Nombres, Apellidos y Datos Geográficos existen aquí, copiadas de scripts anteriores]

# Diccionario de causas/sintomas para Mortalidad Infantil
CAUSAS_SINTOMAS_INFANTIL = {
    "Neumonía": "fiebre, tos, dificultad respiratoria, aleteo nasal, retracciones intercostales, cianosis.",
    "Diarrea aguda": "deposiciones líquidas frecuentes, deshidratación, ojos hundidos, boca seca, letargo.",
    "Malaria": "fiebre intermitente, escalofríos, sudoración, vómitos, palidez, convulsiones en casos graves.",
    "Sarampión": "fiebre alta, exantema maculopapular, tos, conjuntivitis, manchas de Koplik.",
    "VIH/SIDA": "pérdida de peso, infecciones recurrentes, fiebre persistente, candidiasis oral, retraso del crecimiento.",
    "Sepsis": "fiebre o hipotermia, letargo, rechazo al alimento, dificultad respiratoria, palidez, taquicardia.",
    "Meningitis": "fiebre alta, rigidez de nuca, vómitos, irritabilidad, fontanela abombada, convulsiones.",
    "Tuberculosis": "tos crónica, fiebre vespertina, pérdida de peso, sudoración nocturna, linfadenopatías.",
    "Desnutrición aguda severa": "emaciación, edema en piernas (kwashiorkor), apatía, piel seca, cabello quebradizo.",
    "Asfixia por alimentos": "dificultad respiratoria súbita, cianosis, tos intensa, pérdida de conciencia.",
    "Ahogamiento": "pérdida de conciencia, cianosis, dificultad respiratoria, tos con espuma, paro cardiorrespiratorio.",
    "Quemaduras": "dolor intenso, ampollas, enrojecimiento o carbonización, fiebre si hay infección.",
    "Accidentes de tránsito": "politraumatismos, fracturas, pérdida de conciencia, hemorragias internas.",
    "Caídas graves": "hematomas, fracturas, vómitos, somnolencia, convulsiones si hay trauma craneal.",
    "Intoxicaciones accidentales": "vómitos, somnolencia, convulsiones, dificultad respiratoria, pupilas dilatadas o contraídas.",
    "Malformaciones congénitas": "signos variables según el órgano afectado (cianosis, dificultad para alimentarse, retraso del desarrollo).",
    "Cardiopatías congénitas": "cianosis, disnea, sudoración al alimentarse, soplo cardíaco, retraso ponderal.",
    "Cáncer infantil": "palidez, fiebre persistente, pérdida de peso, masas palpables, sangrados.",
    "Asma severa": "dificultad respiratoria, sibilancias, tos nocturna, uso de músculos accesorios.",
    "Dengue grave": "fiebre alta, sangrado, dolor abdominal, vómitos persistentes, shock.",
    "Violencia doméstica": "hematomas, fracturas, retraimiento, miedo, cambios de comportamiento.",
    "Abuso infantil": "lesiones inexplicables, miedo a adultos, retraso en el desarrollo, retraimiento.",
    "Negligencia": "desnutrición, falta de higiene, infecciones frecuentes, retraso en el crecimiento.",
}

# --- Funciones Auxiliares ---
START_DATE_DEF = date(2024, 1, 1)
END_DATE_DEF = date(2025, 12, 31)
MIN_EDAD_AÑOS = 2
MAX_EDAD_AÑOS = 5

def generar_nombre_completo(es_bebe=True):
    # [Función copiada de SCRIPT 05]
    if es_bebe:
        nombre = random.choice(NOMBRES_HOMBRE + NOMBRES_MUJER)
    else: # Madre (solo nombres femeninos)
        nombre = random.choice(NOMBRES_MUJER)

    apellido1 = random.choice(APELLIDOS)
    apellido2 = random.choice(APELLIDOS)
    return f"{nombre} {apellido1} {apellido2}"

def generar_direccion_exacta(municipio):
    # [Función copiada de SCRIPT 05]
    sectores = {
        "Simón Rodríguez": ["Pueblo Nuevo Sur", "Campo Alegre", "Casco Central", "Las Villas", "Pedro Camejo", "Los Ángeles", "San José", "Paraíso 1", "Paraíso 2", "Campo Oficina"],
        "Guanipa": ["Barrio Blanco", "Las Malvinas", "Bicentenario", "19 de Marzo", "Central", "Colinas", "Cementerio", "Simón Bolívar", "La Floresta", "Valmore Rodríguez"],
    }
    tipo_via = random.choice(["Calle", "Carrera", "Avenida"])
    num_via = random.randint(1, 100)
    sector = random.choice(sectores.get(municipio, ["Sector Genérico"]))
    return f"{tipo_via} {num_via}, Sector {sector}."

def generar_datos_ingreso_defuncion():
    """Genera la relación idx_defuncion (clave) : idx_ingreso (valor)"""
    idx_defuncion = random.choice(list(CAUSAS_SINTOMAS_INFANTIL.keys()))
    idx_ingreso = CAUSAS_SINTOMAS_INFANTIL[idx_defuncion]
    return idx_defuncion.replace("'", "''"), idx_ingreso.replace("'", "''")


def generar_fecha_y_edad_infantil():
    """Genera fecha de nacimiento y defunción coherente (2 a 5 años)."""
    
    # 1. Definir la fecha de defunción (entre 2024 y 2025)
    random_days_def = random.randint(0, (END_DATE_DEF - START_DATE_DEF).days)
    fecha_defuncion = START_DATE_DEF + timedelta(days=random_days_def)
    
    # 2. Definir la edad
    edad_años = random.randint(MIN_EDAD_AÑOS, MAX_EDAD_AÑOS)
    edad_junto = f"{edad_años} Años"
    
    # 3. Calcular la fecha de nacimiento (defunción - edad_años)
    # Para simplificar y mantener el día/mes consistente, usamos relativedelta mental
    # Restamos el número de días para la edad en años + un desplazamiento de 0 a 364 días
    dias_para_restar = edad_años * 365 + random.randint(0, 364)
    fecha_nacimiento = fecha_defuncion - timedelta(days=dias_para_restar)
    
    # 4. Fecha de ingreso (puede ser el mismo día o un día antes)
    fecha_ingreso = fecha_defuncion - timedelta(days=random.choice([0, 1]))
        
    # 5. Horas
    hora_aleatoria = f"{random.randint(0, 23):02}:{random.randint(0, 59):02}:00"

    # Formato DD/MM/YYYY
    return {
        "fecha_nacimiento": fecha_nacimiento.strftime("%d/%m/%Y"),
        "fecha_ingreso": fecha_ingreso.strftime("%d/%m/%Y"),
        "hora_ingreso": hora_aleatoria,
        "fecha_defuncion": fecha_defuncion.strftime("%d/%m/%Y"),
        "hora_defuncion": hora_aleatoria,
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
sql_statements_infantil = []
ID_MAPPING = [] 

# Contadores de secuencia para el diccionario
start_idx_defuncion = 30000
start_idx_ingreso = 40000


for i in range(NUM_REGISTROS):
    
    # IDs de texto solicitados (Clave : Valor)
    idx_defuncion_key = start_idx_defuncion + i
    idx_ingreso_val = start_idx_ingreso + i

    # Datos temporales
    historia_clinica = random.randint(11111111, 99999999)
    nombres_apellidos = generar_nombre_completo(es_bebe=True).replace("'", "''")
    nombre_madre = generar_nombre_completo(es_bebe=False).replace("'", "''")
    
    fechas = generar_fecha_y_edad_infantil()
    idx_def_txt, idx_ing_txt = generar_datos_ingreso_defuncion()
    
    # Datos Geográficos
    parroquia_random = random.choice(PARROQUIAS_LISTA)
    municipio_random = next(k for k, v in MUNICIPIOS_DATA.items() if parroquia_random in v)
    direccion_exacta = generar_direccion_exacta(municipio_random).replace("'", "''") 
    
    
    # --- PASO 1: Insertar en persona_paciente (para obtener ID_PACIENTE) ---
    sql_statements_paciente.append(
        f"INSERT INTO persona_paciente (edad) VALUES ('{fechas['edad_junto']}');"
    )

    # --- PASO 2: Insertar en direccion (para obtener ID_DIRECCION) ---
    sql_statements_direccion.append(
        f"INSERT INTO direccion (descripcion, id_parroquia) VALUES ('{direccion_exacta}', (SELECT id_parroquia FROM parroquia WHERE nombre = '{parroquia_random}'));"
    )

    # --- 3. Generar Mapeo para el SCRIPT FINAL (usando IDs de búsqueda) ---
    ID_MAPPING.append({
        "nombres_apellidos": nombres_apellidos,
        "direccion_exacta": direccion_exacta, # Clave de búsqueda de la FK de Direccion
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
        # Datos para Mortalidad Infantil (Tabla Detalle)
        "nombre_madre": nombre_madre,
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
print("-- SCRIPT 06: INSERCIÓN EN MORTALIDAD INFANTIL (3 Tablas en Cascada)")
print("-- --------------------------------------------------------------------------------------")

# --- 1. Insertar Pacientes ---
print("\n-- 1. INSERTAR ENTIDADES PACIENTE (Para obtener id_paciente, clave para mortalidad)")
for sql in sql_statements_paciente:
    print(sql)

# --- 2. Insertar Direcciones ---
print("\n-- 2. INSERTAR ENTIDADES DIRECCIÓN (Para obtener id_direccion, clave para mortalidad)")
for sql in sql_statements_direccion:
    print(sql)

# --- 3. Insertar Mortalidad (Principal) e Infantil (Detalle) ---
print("\n-- 3. INSERTAR MORTALIDAD (Principal) y MORTALIDAD_INFANTIL (Detalle)")

# Lookups
paciente_lookup = "(SELECT MAX(id_paciente) FROM persona_paciente)" 
direccion_lookup_template = "(SELECT id_direccion FROM direccion WHERE descripcion = '{desc}' LIMIT 1)"

print("DELETE FROM mortalidad_infantil;") # Limpiar tabla de destino
# print("DELETE FROM mortalidad;") # No limpiamos 'mortalidad' ya que el script anterior insertó Neonatal.

for i, registro in enumerate(ID_MAPPING):
    
    # A) INSERT en la tabla 'mortalidad' (Tabla Principal)
    
    # El id_paciente es el último insertado MENOS los registros que quedan pendientes.
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
    
    # B) INSERT en la tabla 'mortalidad_infantil' (Tabla Detalle)
    
    sql_infantil = (
        f"INSERT INTO mortalidad_infantil ("
        f"id_m, nombre_madre"
        f") VALUES ("
        f"LAST_INSERT_ROWID(), " # Usa el ID de la mortalidad recién insertada (¡CRUCIAL!)
        f"'{registro['nombre_madre']}'"
        f");"
    )
    sql_statements_infantil.append(sql_infantil)
    print(sql_infantil)
    
    # Imprimir el diccionario solicitado por el usuario
    print(f"-- IDx Infantil: {registro['idx_defuncion_key']} : {registro['idx_ingreso_val']}")

print("COMMIT;")
print(f"\n-- TOTAL DE REGISTROS DE MORTALIDAD INFANTIL GENERADOS: {NUM_REGISTROS}")
print("-- RECUERDA: Este script asume que la secuencia de IDs de persona_paciente e ID de direccion continúa a partir de los registros anteriores.")

# python 06_Mortalidad_Infantil_Inserts_Multitabla.py > 06_infantil_inserts.sql
# python 06_Mortalidad_Infantil_Inserts_Multitabla.py | Out-File -Encoding utf8 06_infantil_inserts.sql