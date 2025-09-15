import sqlite3 
import uuid
import secrets
import streamlit as st
import sys
from pathlib import Path
from utils.contra import verifi_contra_hasheada
import time
import os

if getattr(sys, "frozen", False):
    # Si está empaquetado con PyInstaller, tomar la carpeta donde está el .exe
    PROJECT_ROOT = Path(sys.executable).parent
else:
    # Si está ejecutando desde el código fuente
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Ruta global de la base de datos
DB_PATH = os.getenv("hospital.db", "hospital.db")

def verificar_usuario_cedula(nombre_usuario, ultimos_4_cedula, DB_PATH=None):
    """
    Verifica si el usuario existe y si los últimos 4 dígitos de su cédula coinciden.
    Funciona tanto si CI se guarda como número o como texto en la base de datos.
    """
    if DB_PATH is None:
        DB_PATH = globals().get("DB_PATH")
    
    try:
        # Convertimos los últimos 4 dígitos a string y rellenamos con ceros a la izquierda
        ultimos_4_cedula_str = str(ultimos_4_cedula).zfill(4)
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verificamos si el usuario existe
        cursor.execute(
            "SELECT nombre_usuario FROM usuario WHERE nombre_usuario = ?", 
            (nombre_usuario,)
        )
        usuario_encontrado = cursor.fetchone()
        if usuario_encontrado is None:
            st.error("Usuario no encontrado.", icon=":material/person_off:")
            return False
        
        # Comparamos los últimos 4 dígitos del CI convirtiendo CI a texto
        cursor.execute(
            "SELECT nombre_usuario FROM usuario WHERE nombre_usuario = ? AND SUBSTR(CAST(CI AS TEXT), -4) = ?",
            (nombre_usuario, ultimos_4_cedula_str)
        )
        match_encontrado = cursor.fetchone()
        if match_encontrado:
            st.success("Usuario y cédula verificados correctamente.", icon=":material/check_circle:")
            return True
        else:
            st.warning("Los últimos 4 dígitos de la cédula no coinciden.", icon=":material/lock_open:")
            return False
    except sqlite3.Error as e:
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")
        return False
    finally:
        if conn:
            conn.close()


def verificar_correo_cedula(correo, primeros_4_cedula, DB_PATH=None):
    if DB_PATH is None:
        DB_PATH = globals().get("DB_PATH")
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario FROM correo WHERE correo = ?", (correo,))
        correo_encontrado = cursor.fetchone()
        if correo_encontrado is None:
            st.error("Correo electrónico no registrado.", icon=":material/alternate_email:")
            #return False
        cursor.execute("""
            SELECT u.CI 
            FROM usuario u
            JOIN correo c ON u.id_usuario = c.id_usuario
            WHERE c.correo = ? AND SUBSTR(u.CI, 1, 4) = ?
        """, (correo, primeros_4_cedula))
        match_encontrado = cursor.fetchone()
        if match_encontrado:
            return True
        else:
            st.warning("Los primeros 4 dígitos de la cédula no coinciden.", icon=":material/lock_open:")
            #return False
    except sqlite3.Error as e:
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")
        return False
    finally:
        if conn:
            conn.close()

def verificar_preg_res_seg(respuesta_uno, pregunta_uno, respuesta_dos, pregunta_dos, respuesta_tres, pregunta_tres, usuario, DB_PATH=None):
    if DB_PATH is None:
        DB_PATH = globals().get("DB_PATH")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                pregunta_seguridad, respuesta_seguridad, 
                pregunta_seguridad_dos, respuesta_seguridad_dos, 
                pregunta_seguridad_tres, respuesta_seguridad_tres
            FROM usuario
            WHERE nombre_usuario = ?
        """, (usuario,))
        datos = cursor.fetchone()
        if datos:
            preg_DB_1, resp_DB_1, preg_DB_2, resp_DB_2, preg_DB_3, resp_DB_3 = datos
            if not preg_DB_1 and not preg_DB_2 and not preg_DB_3:
                st.warning("Este usuario no tiene preguntas de seguridad guardadas.", icon=":material/warning:")
                return False, None
            pares_DB = [(preg_DB_1, resp_DB_1), (preg_DB_2, resp_DB_2), (preg_DB_3, resp_DB_3)]
            pares_usuario = [(pregunta_uno, respuesta_uno), (pregunta_dos, respuesta_dos), (pregunta_tres, respuesta_tres)]
            aciertos = 0
            for preg_user, resp_user in pares_usuario:
                for preg_DB, resp_DB in pares_DB:
                    if preg_user == preg_DB and verifi_contra_hasheada(resp_user, resp_DB):
                        aciertos += 1
                        break
            if aciertos == 3:
                st.success("Respuestas de seguridad verificadas correctamente.", icon=":material/check_circle:")
                return True, usuario
            else:
                st.error("Las respuestas de seguridad no son correctas. Por favor, inténtalo de nuevo.", icon=":material/error:")
                return False, None
        else:
            st.warning("Usuario no encontrado.", icon=":material/warning:")
            return False, None
    except sqlite3.Error as e:
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")
        return False, None
    finally:
        conn.close()

def obtener_contrasena_actual(usuario, DB_PATH=None):
    if DB_PATH is None:
        DB_PATH = globals().get("DB_PATH")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT contrasena FROM usuario WHERE nombre_usuario = ?", (usuario,))
        resultado = cursor.fetchone()
        conn.close()
        if not resultado:
            st.error("No se pudo obtener la contraseña actual. Usuario no encontrado.", icon=":material/error:")
            return None
        return resultado[0]
    except sqlite3.Error as e:
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")
        return None

def obtener_info_usuario(nombre_usuario, DB_PATH=None):
    if DB_PATH is None:
        DB_PATH = globals().get("DB_PATH")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.rol, d.id_doctor, s.id_secretaria, a.id_administrador
            FROM usuario u
            LEFT JOIN doctor d ON u.id_usuario = d.id_usuario
            LEFT JOIN secretaria s ON u.id_usuario = s.id_usuario
            LEFT JOIN administrador a ON u.id_usuario = a.id_doctor
            WHERE u.nombre_usuario = ?
        """, (nombre_usuario,))
        result = cursor.fetchone()
        conn.close()
        if result:
            rol, id_doctor, id_secretaria, id_administrador = result
            st.session_state["autenticado_usuario"] = nombre_usuario  
            return {
                "rol": rol,
                "id_doctor": id_doctor if rol == "Doctor (a)" else None,
                "id_secretaria": id_secretaria if rol == "Secretario (a)" else None,
                "id_administrador": id_administrador if rol == "Administrador (a)" else None
            }
        return None
    except sqlite3.Error:
        return None

def obtener_nombre_usuario(correo, primeros_4_cedula, DB_PATH=None):
    if DB_PATH is None:
        DB_PATH = globals().get("DB_PATH")
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.nombre_usuario
            FROM usuario u
            JOIN correo c ON u.id_usuario = c.id_usuario
            WHERE c.correo = ? AND SUBSTR(u.CI, 1, 4) = ?
        """, (correo, primeros_4_cedula))
        resultado = cursor.fetchone()
        if resultado:
            nombre_usuario = resultado[0]
            st.success(f"Tu nombre de usuario es: **{nombre_usuario}**", icon=":material/person_search:")        
            time.sleep(1.5)
            st.rerun()             
            return nombre_usuario
        st.warning("No se encontró un usuario con los datos proporcionados.", icon=":material/person_search:")
        return None
    except sqlite3.Error as e:
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")
        return None
    finally:
        if conn:
            conn.close()

def verificar_usuario(nombre_usuario, contrasena, DB_PATH=None):
    if DB_PATH is None:
        DB_PATH = globals().get("DB_PATH")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT contrasena FROM usuario WHERE nombre_usuario = ?", (nombre_usuario.strip(),))
        resultado = cursor.fetchone()
        conn.close()

        if resultado is None:
            st.error("Usuario no encontrado.", icon=":material/person_off:")
            return False

        hash_guardado = resultado[0]
        if verifi_contra_hasheada(contrasena, hash_guardado):
            return True
        else:
            st.error("Contraseña incorrecta.", icon=":material/lock_open:")
            return False
    except sqlite3.Error as e:
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")
        return False
def verificar_solo_usuario(nombre_usuario, DB_PATH=None):
    if DB_PATH is None:
        DB_PATH = globals().get("DB_PATH")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT nombre_usuario FROM usuario WHERE nombre_usuario = ?", (nombre_usuario,))
        row = cursor.fetchone()
        conn.close()
        return row is not None
    except sqlite3.Error as e:
        st.error(f"Error en la base de datos al verificar usuario: {e}", icon=":material/error:")
        return False

def guardar_usuario(nombre, sexo, nacimiento, nombre_usuario, correo, ci, nacionalidad, contrasena_hasheada, rol="usuario", DB_PATH=None):
    if DB_PATH is None:
        DB_PATH = globals().get("DB_PATH")
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Normalizamos el CI a 8 dígitos (rellenando con ceros a la izquierda si es necesario)
        ci = str(ci).zfill(8)
    
        cursor.execute(
            "INSERT OR IGNORE INTO persona (CI, nombre_apellido, sexo, nacimiento, rol, nacionalidad) VALUES (?, ?, ?, ?, ?, ?)",
            (ci, nombre, sexo, nacimiento, rol, nacionalidad)
        )
        cursor.execute(
            "INSERT INTO usuario (CI, nombre_usuario, contrasena, rol) VALUES (?, ?, ?, ?)",
            (ci, nombre_usuario, contrasena_hasheada, rol)
        )
        id_usuario = cursor.lastrowid
        cursor.execute(
            "INSERT INTO correo (id_usuario, correo) VALUES (?, ?)",
            (id_usuario, correo)
        )
        cursor.execute("SELECT id_departamento FROM departamento WHERE nombre = ?", ('Epidemiología',))
        id_departamento = cursor.fetchone()[0]
        
        if rol == "Doctor (a)":
            cursor.execute("INSERT INTO doctor (id_usuario) VALUES (?)", (id_usuario,))
            cursor.execute(
                "INSERT INTO doctor_departamento (id_doctor, id_departamento) VALUES ((SELECT id_doctor FROM doctor WHERE id_usuario = ?), ?)",
                (id_usuario, id_departamento)
            )
        elif rol == "Secretario (a)":
            cursor.execute("INSERT INTO secretaria (id_usuario) VALUES (?)", (id_usuario,))
            cursor.execute(
                "INSERT INTO secretaria_departamento (id_secretaria, id_departamento) VALUES ((SELECT id_secretaria FROM secretaria WHERE id_usuario = ?), ?)",
                (id_usuario, id_departamento)
            )
        
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        if conn:
            conn.rollback()
        error_message = str(e).lower()
        if 'usuario.nombre_usuario' in error_message:
            st.error("El nombre de usuario ya está registrado. Por favor, elige otro.", icon=":material/error:")
        elif 'correo.correo' in error_message:
            st.error("El correo electrónico ya está registrado. Por favor, utiliza otro.", icon=":material/error:")
        elif 'usuario.ci' in error_message:
            st.error("La cédula de identidad ya está registrada con otro usuario.", icon=":material/error:")
        else:
            st.error(f"Error de integridad de datos: {e}", icon=":material/error:")
        return False
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")
        return False
    finally:
        if conn:
            conn.close()

def guardar_preguntas_seguridad(nombre_usuario, pregunta_seguridad, respuesta_seguridad, pregunta_seguridad_dos, respuesta_seguridad_dos, pregunta_seguridad_tres, respuesta_seguridad_tres, DB_PATH=None):
    if DB_PATH is None:
        DB_PATH = globals().get("DB_PATH")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuario
            SET 
                pregunta_seguridad = ?,
                respuesta_seguridad = ?,
                pregunta_seguridad_dos = ?,
                respuesta_seguridad_dos = ?,
                pregunta_seguridad_tres = ?,
                respuesta_seguridad_tres = ?
            WHERE nombre_usuario = ?;
        """, (pregunta_seguridad, respuesta_seguridad, pregunta_seguridad_dos, respuesta_seguridad_dos, pregunta_seguridad_tres, respuesta_seguridad_tres, nombre_usuario))
        conn.commit()
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        return str(e)
    finally:
        if conn:
            conn.close()


def cambiar_contrasena(nueva_contra, usuario, DB_PATH=None):
    if DB_PATH is None:
        DB_PATH = globals().get("DB_PATH")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET contrasena = ? WHERE nombre_usuario = ?", (nueva_contra, usuario))
        conn.commit()
        return True
    except sqlite3.Error as e:
        st.error(f"Error en la base de datos: {e}")
        return False
    finally:
        if conn:
            conn.close()


def verificar_preguntas_guardadas(nombre_usuario, DB_PATH=None):
    if DB_PATH is None:
        DB_PATH = globals().get("DB_PATH")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pregunta_seguridad, pregunta_seguridad_dos, pregunta_seguridad_tres
            FROM usuario
            WHERE nombre_usuario = ?
        """, (nombre_usuario,))
        datos = cursor.fetchone()
        conn.close()
        return bool(datos and all(datos))
    except Exception as e:
        st.error(f"Error al verificar preguntas de seguridad: {e}", icon=":material/error:")
        return False


def verificar_superusuario(nombre_usuario, contrasena, DB_PATH=None):
    if DB_PATH is None:
        DB_PATH = globals().get("DB_PATH")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT contrasena, rol, id_usuario FROM usuario WHERE nombre_usuario = ?", (nombre_usuario,))
        resultado = cursor.fetchone()
        if resultado is None:
            st.error("Usuario no encontrado.", icon=":material/person_off:")
            return False
        contrasena_bd, rol, id_usuario = resultado
        if rol != "Administrador (a)":
            st.warning("El usuario no tiene permisos de Administrador.", icon=":material/lock_open:")
            return False
        if not verifi_contra_hasheada(contrasena, contrasena_bd):
            st.warning("Contraseña incorrecta.", icon=":material/lock_open:")
            return False
        cursor.execute("""
            SELECT a.id_administrador
            FROM administrador a
            JOIN doctor d ON a.id_doctor = d.id_doctor
            WHERE d.id_usuario = ?
        """, (id_usuario,))
        admin_row = cursor.fetchone()
        if admin_row is None:
            st.error("No se encontró una cuenta de Administrador vinculada al usuario.", icon=":material/error:")
            return False
        st.success("Sesión de Administrador iniciada correctamente.", icon=":material/check_circle:")
        st.session_state["autenticado_usuario"] = nombre_usuario
        return True
    except sqlite3.Error as e:
        st.error(f"Error en la base de datos al verificar Administrador: {e}", icon=":material/error:")
        return False
    finally:
        if conn:
            conn.close()


def eliminar_usuario_completo(nombre_usuario, DB_PATH=None):
    if DB_PATH is None:
        DB_PATH = globals().get("DB_PATH")
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute("SELECT id_usuario, CI FROM usuario WHERE nombre_usuario = ?", (nombre_usuario,))
        fila = cursor.fetchone()
        if fila is None:
            st.warning("Usuario no encontrado.", icon=":material/person_off:")
            return False
        id_usuario, ci = fila
        cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
        cursor.execute("DELETE FROM persona WHERE CI = ?", (ci,))
        conn.commit()
        st.success("Usuario y todos los datos asociados eliminados correctamente.", icon=":material/delete:")
        return True
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        st.error(f"Error al eliminar usuario: {e}", icon=":material/error:")
        return False
    finally:
        if conn:
            conn.close()
