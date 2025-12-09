import sqlite3
import streamlit as st
import threading
import os
DB_LOCK = threading.Lock()

# Usa la ruta de la BD del launcher si está disponible, si no, usa la local.
# Esto hace que funcione tanto en desarrollo como en producción.
DB_PATH = os.getenv("hospital.db", "hospital.db")

def create_table_persona(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS persona (
            CI INTEGER PRIMARY KEY UNIQUE,
            nombre_apellido TEXT NOT NULL,
            sexo TEXT NOT NULL,
            nacimiento DATE,
            rol TEXT NOT NULL,
            nacionalidad TEXT
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_usuario(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
            CI INTEGER NOT NULL UNIQUE,
            nombre_usuario TEXT NOT NULL UNIQUE,
            contrasena TEXT NOT NULL,
            pregunta_seguridad TEXT,
            respuesta_seguridad TEXT,
            pregunta_seguridad_dos TEXT,
            respuesta_seguridad_dos TEXT,
            pregunta_seguridad_tres TEXT,
            respuesta_seguridad_tres TEXT,
            rol TEXT NOT NULL,
            FOREIGN KEY (CI) REFERENCES persona(CI) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_correo(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS correo (
            id_correo INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL,
            correo TEXT NOT NULL UNIQUE,
            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_doctor(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS doctor (
            id_doctor INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL UNIQUE,
            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_secretaria(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS secretaria (
            id_secretaria INTEGER PRIMARY KEY AUTOINCREMENT,
            id_usuario INTEGER NOT NULL UNIQUE,
            FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")
        
def create_table_administrador(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS administrador (
            id_administrador INTEGER PRIMARY KEY AUTOINCREMENT,
            id_doctor INTEGER NOT NULL UNIQUE,
            FOREIGN KEY (id_doctor) REFERENCES doctor(id_doctor) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_pais(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS pais (
            id_pais INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_estado(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS estado (
            id_estado INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            id_pais INTEGER NOT NULL,
            FOREIGN KEY (id_pais) REFERENCES pais(id_pais) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_ciudad(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS ciudad (
            id_ciudad INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            id_estado INTEGER NOT NULL,
            FOREIGN KEY (id_estado) REFERENCES estado(id_estado) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_municipio(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS municipio (
            id_municipio INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            id_ciudad INTEGER NOT NULL,
            FOREIGN KEY (id_ciudad) REFERENCES ciudad(id_ciudad) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_parroquia(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS parroquia (
            id_parroquia INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            id_municipio INTEGER NOT NULL,
            FOREIGN KEY (id_municipio) REFERENCES municipio(id_municipio) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_direccion(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS direccion (
            id_direccion INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT,
            id_parroquia INTEGER NOT NULL,
            FOREIGN KEY (id_parroquia) REFERENCES parroquia(id_parroquia) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_hospital(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS hospital (
            id_hospital INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL,
            id_direccion INTEGER,
            FOREIGN KEY (id_direccion) REFERENCES direccion(id_direccion) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_departamento(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS departamento (
            id_departamento INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT,
            nombre TEXT NOT NULL UNIQUE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_departamento_hospital(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS departamento_hospital (
            id_departamento INTEGER NOT NULL,
            id_hospital INTEGER NOT NULL,
            PRIMARY KEY (id_departamento, id_hospital),
            FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento) ON DELETE CASCADE,
            FOREIGN KEY (id_hospital) REFERENCES hospital(id_hospital) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_secretaria_departamento(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS secretaria_departamento (
            id_secretaria INTEGER NOT NULL,
            id_departamento INTEGER NOT NULL,
            PRIMARY KEY (id_secretaria, id_departamento),
            FOREIGN KEY (id_secretaria) REFERENCES secretaria(id_secretaria) ON DELETE CASCADE,
            FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_doctor_departamento(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS doctor_departamento (
            id_doctor INTEGER NOT NULL,
            id_departamento INTEGER NOT NULL,
            PRIMARY KEY (id_doctor, id_departamento),
            FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento) ON DELETE CASCADE,
            FOREIGN KEY (id_doctor) REFERENCES doctor(id_doctor) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_mision(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS mision (
            id_mision INTEGER PRIMARY KEY AUTOINCREMENT,
            id_departamento INTEGER NOT NULL UNIQUE,
            contenido TEXT NOT NULL,
            FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_vision(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS vision (
            id_vision INTEGER PRIMARY KEY AUTOINCREMENT,
            id_departamento INTEGER NOT NULL UNIQUE,
            contenido TEXT NOT NULL,
            FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_persona_paciente(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS persona_paciente (
            id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
            edad INTEGER
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_doctor_paciente(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS doctor_paciente (
            id_doctor INTEGER NOT NULL,
            id_paciente INTEGER NOT NULL,
            PRIMARY KEY (id_doctor, id_paciente),
            FOREIGN KEY (id_doctor) REFERENCES doctor(id_doctor) ON DELETE CASCADE,
            FOREIGN KEY (id_paciente) REFERENCES persona_paciente(id_paciente) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_secretaria_paciente(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS secretaria_paciente (
            id_secretaria INTEGER NOT NULL,
            id_paciente INTEGER NOT NULL,
            PRIMARY KEY (id_secretaria, id_paciente),
            FOREIGN KEY (id_secretaria) REFERENCES secretaria(id_secretaria) ON DELETE CASCADE,
            FOREIGN KEY (id_paciente) REFERENCES persona_paciente(id_paciente) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_mortalidad(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS mortalidad (
            id_m INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER NOT NULL,
            historia_clinica INTEGER UNIQUE,
            nombres_apellidos TEXT NOT NULL,
            fecha_nacimiento DATE,
            fecha_ingreso DATE,
            hora_ingreso TIME,
            fecha_defuncion DATE,
            hora_defuncion TIME,
            id_direccion INTEGER,
            idx_ingreso TEXT NOT NULL,
            idx_defuncion TEXT NOT NULL,
            fecha_registro_formulario DATE,
            FOREIGN KEY (id_paciente) REFERENCES persona_paciente(id_paciente) ON DELETE CASCADE,
            FOREIGN KEY (id_direccion) REFERENCES direccion(id_direccion) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_mortalidad_infantil(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS mortalidad_infantil (
            id_MI INTEGER PRIMARY KEY AUTOINCREMENT,
            id_m INTEGER NOT NULL,
            nombre_madre TEXT NOT NULL,
            FOREIGN KEY (id_m) REFERENCES mortalidad(id_m) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_mortalidad_neonatal(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS mortalidad_neonatal (
            id_MN INTEGER PRIMARY KEY AUTOINCREMENT,
            id_m INTEGER NOT NULL,
            nombre_madre TEXT NOT NULL,
            hora_nacimiento TIME,
            semanas_gestacion TEXT,
            peso TEXT NOT NULL,
            talla TEXT NOT NULL,
            FOREIGN KEY (id_m) REFERENCES mortalidad(id_m) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_mortalidad_materna(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS mortalidad_materna (
            id_MM INTEGER PRIMARY KEY AUTOINCREMENT,
            id_m INTEGER NOT NULL,
            FOREIGN KEY (id_m) REFERENCES mortalidad(id_m) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_mortalidad_mensual(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS mortalidad_mensual (
            id_mortaM INTEGER PRIMARY KEY AUTOINCREMENT,
            id_doctor_atendi,
            causas TEXT NOT NULL,
            n_casos INTEGER,
            tasa TEXT,
            total INTEGER,
            fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_registro_formulario DATE,
            FOREIGN KEY (id_doctor_atendi) REFERENCES doctor(id_doctor) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_mortalidad_mensual_infantil(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS mortalidad_mensual_infantil (
            id_mortaMI INTEGER PRIMARY KEY AUTOINCREMENT,
            id_mortaM INTEGER NOT NULL,
            FOREIGN KEY (id_mortaM) REFERENCES mortalidad_mensual(id_mortaM) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_mortalidad_mensual_neonatal(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS mortalidad_mensual_neonatal (
            id_mortaMN INTEGER PRIMARY KEY AUTOINCREMENT,
            id_mortaM INTEGER NOT NULL,
            FOREIGN KEY (id_mortaM) REFERENCES mortalidad_mensual(id_mortaM) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_mortalidad_mensual_general(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS mortalidad_mensual_general (
            id_mortaMNG INTEGER PRIMARY KEY AUTOINCREMENT,
            id_mortaM INTEGER NOT NULL,
            FOREIGN KEY (id_mortaM) REFERENCES mortalidad_mensual(id_mortaM) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_morbilidad(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS morbilidad (
            id_morb INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER,
            id_direccion_hogar INTEGER,
            nombres_apellidos TEXT,
            edad INTEGER,
            diagnostico TEXT,
            fecha_registro_formulario DATE,
            FOREIGN KEY (id_paciente) REFERENCES persona_paciente(id_paciente) ON DELETE CASCADE,
            FOREIGN KEY (id_direccion_hogar) REFERENCES direccion(id_direccion) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_morb_extenso(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS morb_extenso (
            HC INTEGER PRIMARY KEY UNIQUE,
            id_morb INTEGER NOT NULL,
            nombres_apellidos TEXT,
            id_direccion_hogar INTEGER,
            id_direccion_nacimiento INTEGER,
            fecha_nacimiento DATE,
            estado_civil TEXT,
            cedula TEXT UNIQUE,
            telefono TEXT,
            FOREIGN KEY (id_morb) REFERENCES morbilidad(id_morb) ON DELETE CASCADE,
            FOREIGN KEY (id_direccion_hogar) REFERENCES direccion(id_direccion) ON DELETE CASCADE,
            FOREIGN KEY (id_direccion_nacimiento) REFERENCES direccion(id_direccion) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_morb_simplifica(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS morb_simplifica (
            id_morbsim INTEGER PRIMARY KEY AUTOINCREMENT,
            id_morb INTEGER NOT NULL,
            FOREIGN KEY (id_morb) REFERENCES morbilidad(id_morb) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_natalidad(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS natalidad (
            id_nata INTEGER PRIMARY KEY AUTOINCREMENT,
            id_doctor,
            fecha DATE,
            partos INTEGER,
            cesareas INTEGER,
            varones INTEGER,
            hembras INTEGER,
            gemelar INTEGER,
            mto INTEGER,
            partos_extrahospitalarios INTEGER,
            fecha_registro_formulario DATE,
            FOREIGN KEY (id_doctor) REFERENCES doctor(id_doctor) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_epi14_semanal(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS epi14_semanal (
            id_semanal INTEGER PRIMARY KEY AUTOINCREMENT,
            id_doctor,
            semana TEXT NOT NULL, 
            causa TEXT NOT NULL,
            numero INTEGER,
            sexo_edad TEXT,
            total INTEGER,
            fecha_registro_formulario DATE,
            FOREIGN KEY (id_doctor) REFERENCES doctor(id_doctor) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_table_registro_diario(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS registro_diario (
            id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
            id_doctor INTEGER,
            semana TEXT NOT NULL,
            fd DATE, 
            edad_sexo TEXT,
            mr TEXT,
            mo TEXT,
            so TEXT,
            cb TEXT,
            cd TEXT,
            gett TEXT,
            nc TEXT,
            peso REAL,
            talla REAL,
            autopsia TEXT,
            fecha_registro_formulario DATE,
            FOREIGN KEY (id_doctor) REFERENCES doctor(id_doctor) ON DELETE CASCADE
        );
        ''')
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

def create_all_tables(db='hospital.db'):#
    try:
        conn = sqlite3.connect(DB_PATH)#DB_PATH
        conn.execute("PRAGMA foreign_keys = ON;")
        create_table_persona(conn)
        create_table_usuario(conn)
        create_table_correo(conn)
        create_table_doctor(conn)
        create_table_secretaria(conn)
        create_table_administrador(conn)
        create_table_pais(conn)
        create_table_estado(conn)
        create_table_ciudad(conn)
        create_table_municipio(conn)
        create_table_parroquia(conn)
        create_table_direccion(conn)
        create_table_hospital(conn)
        create_table_departamento(conn)
        create_table_departamento_hospital(conn)
        create_table_secretaria_departamento(conn)
        create_table_doctor_departamento(conn)
        create_table_mision(conn)
        create_table_vision(conn)
        create_table_persona_paciente(conn)
        create_table_doctor_paciente(conn)
        create_table_secretaria_paciente(conn)
        create_table_mortalidad(conn)
        create_table_mortalidad_infantil(conn)
        create_table_mortalidad_neonatal(conn)
        create_table_mortalidad_materna(conn)
        #create_table_mortalidad_mensual(conn)
        #create_table_mortalidad_mensual_infantil(conn)
        #create_table_mortalidad_mensual_neonatal(conn)
        #create_table_mortalidad_mensual_general(conn)
        create_table_morbilidad(conn)
        #create_table_morb_extenso(conn)
        #create_table_morb_simplifica(conn)
        create_table_natalidad(conn)
        #create_table_epi14_semanal(conn)
        #create_table_registro_diario(conn)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")