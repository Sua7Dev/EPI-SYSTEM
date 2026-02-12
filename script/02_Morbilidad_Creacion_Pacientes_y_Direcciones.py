# 02_Morbilidad_Creacion_Pacientes_y_Direcciones.py > 02_Morbilidad_Creacion_Pacientes_y_Direcciones.sql
import random
from datetime import date, timedelta
from faker import Faker
import json
import sys
import codecs

# Configurar la salida estándar para UTF-8
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer)
fake = Faker('es_ES')
NUM_REGISTROS = 300

# --- Listas de Datos Proporcionadas ---
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

ENFERMEDADES_COMUNES = [
    "Abdomen agudo", "Alzheimer", "Anemia", "Apendicitis", "Ansiedad", "Artritis", 
    "Asma", "Bronquitis", "Cáncer de colon", "Cáncer de mama", "Cáncer de próstata", 
    "Cefalea tensional", "Cirrosis hepática", "Cistitis", "Colecistitis", "Colesterol alto", 
    "Colitis ulcerosa", "COVID-19", "Demencia", "Depresión", "Diabetes tipo 1", 
    "Diabetes tipo 2", "Diarrea", "Difteria", "Dispepsia funcional", "Endometriosis", 
    "Enfermedad de Crohn", "Enfermedad de Graves", "Enfermedad de Ménière", "Enfermedad de Parkinson", 
    "Epilepsia", "EPOC (Enfermedad Pulmonar Obstructiva Crónica)", "Esclerosis múltiple", 
    "Esófago de Barrett", "Esquizofrenia", "Estreñimiento", "Escabiosis (sarna)", "Faringitis", 
    "Fiebre amarilla", "Fiebre tifoidea", "Fibromialgia", "Gastritis", "Gripe (influenza)", 
    "Guillain-Barré (síndrome de)", "Hepatitis A", "Hepatitis B", "Hepatitis C", "Hernia discal", 
    "Insuficiencia respiratoria baja", "Hipertiroidismo", "Hipertensión arterial", "Hipotiroidismo", 
    "Hipercolesterolemia", "Infarto agudo al miocardio", "Infección urinaria", "Insomnio", 
    "Intolerancia a la lactosa", "Leucemia", "Lumbalgia", "Lupus", "Malaria", "Meningitis", 
    "Migraña", "Miomatosis uterina", "Miopía", "Mononucleosis infecciosa", "Neumonía", 
    "Obesidad", "Obstrucción intestinal", "Osteoartritis", "Osteoporosis", "Otitis", 
    "Pancreatitis", "Pielonefritis", "Psoriasis", "Rabia", "Reflujo gastroesofágico (ERGE)", 
    "Resfriado común", "Retinopatía diabética", "Rinitis alérgica", "Rubéola", "Sarampión", 
    "Síncope", "Sordera", "TDAH (Trastorno por Déficit de Atención e Hiperactividad)", 
    "TDAH en adultos", "Tétanos", "Toxoplasmosis", "Trastorno bipolar", 
    "Trastorno de ansiedad generalizada", "Trombosis", "Tuberculosis", "Úlcera gástrica", 
    "Urticaria", "Varicela", "Vértigo", "VIH/SIDA", "Virus del Papiloma Humano (VPH)", 
    "Zoster (culebrilla)", "Dengue", "Lues connatal",
]

# Datos Geográficos para mapeo de parroquia/municipio
MUNICIPIOS_DATA = {
    "Simón Rodríguez": ["Edmundo Barrios", "Miguel Otero Silva"],
    "Guanipa": ["San José de Guanipa"],
}
PARROQUIAS_LISTA = [p for subs in MUNICIPIOS_DATA.values() for p in subs]


# --- Funciones Auxiliares ---
START_DATE = date(2024, 1, 1)
END_DATE = date(2025, 12, 31)

def generar_fecha_aleatoria(start_date, end_date):
    """Genera una fecha aleatoria dentro del rango especificado (2024-2025)."""
    random_days = random.randint(0, (end_date - start_date).days)
    return (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

def generar_nombre_completo():
    """Genera un nombre y dos apellidos aleatorios."""
    nombre = random.choice(NOMBRES_HOMBRE + NOMBRES_MUJER)
    apellido1 = random.choice(APELLIDOS)
    apellido2 = random.choice(APELLIDOS)
    return f"{nombre} {apellido1} {apellido2}"

def generar_direccion_exacta(municipio):
    """Genera una descripción de dirección aleatoria basada en el municipio."""
    sectores = {
        "Simón Rodríguez": ["Pueblo Nuevo Sur", "Campo Alegre", "Casco Central", "Las Villas", "Pedro Camejo", "Los Ángeles", "San José", "Paraíso 1", "Paraíso 2", "Campo Oficina"],
        "Guanipa": ["Barrio Blanco", "Las Malvinas", "Bicentenario", "19 de Marzo", "Central", "Colinas", "Cementerio", "Simón Bolívar", "La Floresta", "Valmore Rodríguez"],
    }
    tipo_via = random.choice(["Calle", "Carrera", "Avenida"])
    num_via = random.randint(1, 100)
    sector = random.choice(sectores.get(municipio, ["Sector Genérico"]))
    return f"{tipo_via} {num_via}, Sector {sector}."


# ----------------------------------------------------
# 1. GENERACIÓN DE SENTENCIAS SQL
# ----------------------------------------------------
sql_statements_paciente = []
sql_statements_direccion = []
ID_MAPPING = [] 

for i in range(NUM_REGISTROS):
    
    # --- Datos aleatorios ---
    nombre_completo = generar_nombre_completo()
    edad_paciente = random.randint(0, 90)
    
    # Datos geográficos
    parroquia_random = random.choice(PARROQUIAS_LISTA)
    municipio_random = next(k for k, v in MUNICIPIOS_DATA.items() if parroquia_random in v)
    direccion_exacta = generar_direccion_exacta(municipio_random).replace("'", "''") # Escapar comillas simples
    
    # --- 1. Generar INSERT para persona_paciente ---
    # Usamos NULL para autoincremento (id_paciente)
    sql_statements_paciente.append(
        f"INSERT INTO persona_paciente (edad) VALUES ({edad_paciente});"
    )

    # --- 2. Generar INSERT para direccion ---
    # Usamos subquery para encontrar el id_parroquia correcto por nombre
    sql_statements_direccion.append(
        f"INSERT INTO direccion (descripcion, id_parroquia) VALUES ('{direccion_exacta}', (SELECT id_parroquia FROM parroquia WHERE nombre = '{parroquia_random}'));"
    )

    # --- 3. Guardar Mapeo para el SCRIPT 3 ---
    # Guardamos los valores que usaremos como 'tokens' de búsqueda y los datos de Morbilidad
    ID_MAPPING.append({
        "nombres_apellidos": nombre_completo.replace("'", "''"), # Escapar para SQL
        "direccion_exacta": direccion_exacta, # Usaremos esto para buscar la FK de Direccion
        "diagnostico": random.choice(ENFERMEDADES_COMUNES).replace("'", "''"), 
        "fecha_reg": generar_fecha_aleatoria(START_DATE, END_DATE) 
    })

# ----------------------------------------------------
# 2. IMPRESIÓN DEL SCRIPT SQL FINAL
# ----------------------------------------------------
print("BEGIN TRANSACTION;")
print("-- --------------------------------------------------------------------------------------")
print("-- SCRIPT 02: CREACIÓN DE PACIENTES Y DIRECCIONES (Morbilidad)")
print("-- --------------------------------------------------------------------------------------")

# Es crucial que las tablas estén limpias para que la secuencia de ID sea predecible
print("DELETE FROM persona_paciente;")
print("DELETE FROM direccion WHERE id_direccion > 1;") # Asumimos que ID 1 es la dirección del Hospital

# Pacientes (IDs secuenciales)
print("\n-- 1. INSERTAR PACIENTES (persona_paciente)")
for sql in sql_statements_paciente:
    print(sql)

# Direcciones (IDs secuenciales, ligados a Parroquia por nombre)
print("\n-- 2. INSERTAR DIRECCIONES DE HOGAR")
for sql in sql_statements_direccion:
    print(sql)

print("COMMIT;")

# --- Guardar Mapeo para el siguiente script ---
with open("morbilidad_data_mapping.json", "w") as f:
    json.dump(ID_MAPPING, f, indent=4)
print(f"\n-- Mapeo de datos guardado en 'morbilidad_data_mapping.json' para el SCRIPT 03.")