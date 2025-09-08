import sqlite3 
#from streamlit_cookies_manager import CookieManager
import uuid
import secrets
import streamlit as st
from utils.contra import verifi_contra_hasheada
import time


def verificar_usuario_cedula(nombre_usuario, ultimos_4_cedula, db='hospital.db'):
    """
    Verifica si el nombre de usuario y los últimos 4 dígitos de la cédula
    coinciden en la base de datos actual.
    """
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # Paso 1: Verificar si el usuario existe
        cursor.execute("SELECT nombre_usuario FROM usuario WHERE nombre_usuario = ?", (nombre_usuario,))
        usuario_encontrado = cursor.fetchone()

        if usuario_encontrado is None:
            # Si la primera consulta no devuelve nada, el usuario no existe.
            st.error("Usuario no encontrado.", icon=":material/person_off:")
            return False

        # Paso 2: Si el usuario existe, validar si la cédula coincide
        # Esta consulta solo se ejecuta si el usuario ya fue validado
        query = """
        SELECT nombre_usuario FROM usuario
        WHERE nombre_usuario = ? AND SUBSTR(CI, -4) = ?
        """
        cursor.execute(query, (nombre_usuario, ultimos_4_cedula))
        match_encontrado = cursor.fetchone()
        
        if match_encontrado:
            st.success("Usuario y cédula verificados correctamente.", icon=":material/check_circle:")
            return True
        else:
            # El usuario existe, pero la cédula no coincide
            st.warning("Los últimos 4 dígitos de la cédula no coinciden.", icon=":material/lock_open:")
            return False

    except sqlite3.Error as e:
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")
        return False


def verificar_correo_cedula(correo, primeros_4_cedula, db='hospital.db'):
    """
    Verifica si el correo electrónico y los primeros 4 dígitos de la cédula
    coinciden en la base de datos.
    """
    conn = None  # Inicializar conn a None
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        # Paso 1: Verificar si el correo existe en la tabla 'correo'
        cursor.execute("SELECT id_usuario FROM correo WHERE correo = ?", (correo,))
        correo_encontrado = cursor.fetchone()

        if correo_encontrado is None:
            # Si la primera consulta no devuelve nada, el correo no existe.
            st.error("Correo electrónico no registrado.", icon=":material/alternate_email:")
            return False

        # Paso 2: Si el correo existe, validar si la cédula coincide.
        # Se necesita un JOIN para vincular el correo con la cédula del usuario.
        query = """
        SELECT u.CI 
        FROM usuario u
        JOIN correo c ON u.id_usuario = c.id_usuario
        WHERE c.correo = ? AND SUBSTR(u.CI, 1, 4) = ?
        """
        cursor.execute(query, (correo, primeros_4_cedula))
        match_encontrado = cursor.fetchone()
        
        if match_encontrado:
            #st.success("Correo y cédula verificados correctamente.", icon=":material/check_circle:")
            return True
        else:
            # El correo existe, pero la cédula no coincide.
            st.warning("Los primeros 4 dígitos de la cédula no coinciden.", icon=":material/lock_open:")
            return False

    except sqlite3.Error as e:
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")
        return False
    finally:
        if conn:
            conn.close()

# Función para verificar el pin de seguridad a
def verificar_preg_res_seg(
    respuesta_uno, pregunta_uno,
    respuesta_dos, pregunta_dos,
    respuesta_tres, pregunta_tres,
    usuario, db='hospital.db'
):
    """
    Verifica las respuestas a las preguntas de seguridad sin importar el orden.
    """
    try:
        conn = sqlite3.connect(db)
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
            # Desempaqueta los datos de la base de datos
            preg_db_1, resp_db_1, preg_db_2, resp_db_2, preg_db_3, resp_db_3 = datos

            # Aviso si no tiene preguntas de seguridad guardadas
            if not preg_db_1 and not preg_db_2 and not preg_db_3:
                st.warning("Este usuario no tiene preguntas de seguridad guardadas.", icon=":material/warning:")
                return False, None
                

            # Crea una lista de los pares (pregunta, respuesta_hasheada) de la base de datos
            pares_db = [
                (preg_db_1, resp_db_1),
                (preg_db_2, resp_db_2),
                (preg_db_3, resp_db_3)
            ]

            # Crea una lista de los pares (pregunta, respuesta) ingresados por el usuario
            pares_usuario = [
                (pregunta_uno, respuesta_uno),
                (pregunta_dos, respuesta_dos),
                (pregunta_tres, respuesta_tres)
            ]

            # Inicializa un contador para los aciertos
            aciertos = 0
            
            # Recorre los pares del usuario y verifica si cada uno coincide
            # con alguno de los pares de la base de datos
            for preg_user, resp_user in pares_usuario:
                for preg_db, resp_db in pares_db:
                    # Verifica si la pregunta coincide y la respuesta es correcta
                    if preg_user == preg_db and verifi_contra_hasheada(resp_user, resp_db):
                        aciertos += 1
                        break  # Pasa al siguiente par de usuario una vez que se encuentra la coincidencia
            
            if aciertos == 3:
                st.success("Respuestas de seguridad verificadas correctamente.", icon=":material/check_circle:")
                # Aquí debes devolver una tupla de dos elementos
                return True, usuario 
            else:
                # Si las respuestas no son correctas
                st.error("Las respuestas de seguridad no son correctas. Por favor, inténtalo de nuevo.", icon=":material/error:")
                # Aquí también debes devolver una tupla de dos elementos
                return False, None

        else:
            # Si el usuario no fue encontrado
            st.warning("Usuario no encontrado.", icon=":material/warning:")
            # Devolver una tupla de dos elementos
            return False, None
    except sqlite3.Error as e:
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")
        return False, None
    finally:
        conn.close()

def obtener_contrasena_actual(usuario, db='hospital.db'):
    # Conectar a la base de datos y obtener la contraseña actual
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    # Consulta para obtener la contraseña actual de la tabla 'registro'
    cursor.execute("SELECT contrasena FROM usuario WHERE nombre_usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    
    conn.close()
    
    if resultado:
        return resultado[0]  # Devuelve la contraseña hash actual
    return None

#prueba xd 
def obtener_info_usuario(nombre_usuario, db='hospital.db'):
    try:
        conn = sqlite3.connect(db)
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
        else:
            return None
    except sqlite3.Error as e:
        #st.error(f"Error en la base de datos: {e}", icon=":material/error:")
        return None
    
def obtener_nombre_usuario(correo, primeros_4_cedula, db='hospital.db'):
    """
    Obtiene el nombre de usuario a partir del correo y los primeros 4 dígitos de la cédula.
    Si lo encuentra, muestra un mensaje de éxito y devuelve el nombre de usuario.
    """
    conn = None
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        query = """
        SELECT u.nombre_usuario
        FROM usuario u
        JOIN correo c ON u.id_usuario = c.id_usuario
        WHERE c.correo = ? AND SUBSTR(u.CI, 1, 4) = ?
        """
        cursor.execute(query, (correo, primeros_4_cedula))
        resultado = cursor.fetchone()

        if resultado:
            nombre_usuario = resultado[0]
            st.success(f"Tu nombre de usuario es: **{nombre_usuario}**", icon=":material/person_search:")        
            time.sleep(1.5)
            st.rerun()             
            return nombre_usuario
  

        else:
            st.warning("No se encontró un usuario con los datos proporcionados.", icon=":material/person_search:")
            return None

    except sqlite3.Error as e:
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")
        return None
    finally:
        if conn:
            conn.close()
            
def verificar_usuario(nombre_usuario, contrasena, db='hospital.db'):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT contrasena FROM usuario WHERE nombre_usuario = ?",
            (nombre_usuario,)
        )
        resultado = cursor.fetchone()
        conn.close()
        if resultado is None:
            st.error("Usuario no encontrado.", icon=":material/person_off:")
            return False
        else:
            contrasena_bd = resultado[0]
            if verifi_contra_hasheada(contrasena, contrasena_bd):
                st.success("Sesión iniciada correctamente.", icon=":material/check_circle:")
                return True
            else:
                st.warning("Contraseña incorrecta.", icon=":material/lock_open:")
                return False
    except sqlite3.Error as e:
        st.error(f"Error en la base de datos al verificar usuario: {e}", icon=":material/error:")
        return False

def verificar_solo_usuario(nombre_usuario, db='hospital.db'):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nombre_usuario FROM usuario WHERE nombre_usuario = ?",
            (nombre_usuario,)
        )
        row = cursor.fetchone()
        conn.close()
        return row is not None
    except sqlite3.Error as e:
        st.error(f"Error en la base de datos al verificar usuario: {e}", icon=":material/error:")
        return False

def guardar_usuario(nombre, sexo, nacimiento, nombre_usuario, correo, ci, nacionalidad, contrasena_hasheada, rol="usuario", db='hospital.db'):
    conn = None
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
    
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
            cursor.execute(
                "INSERT INTO doctor (id_usuario) VALUES (?)",
                (id_usuario,)
            )
            cursor.execute(
                "INSERT INTO doctor_departamento (id_doctor, id_departamento) VALUES ((SELECT id_doctor FROM doctor WHERE id_usuario = ?), ?)",
                (id_usuario, id_departamento)
            )
        elif rol == "Secretario (a)":
            cursor.execute(
                "INSERT INTO secretaria (id_usuario) VALUES (?)",
                (id_usuario,)
            )
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
        return
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")
        return False
    finally:
        if conn:
            conn.close()
        
def guardar_preguntas_seguridad(nombre_usuario, pregunta_seguridad, respuesta_seguridad, pregunta_seguridad_dos, respuesta_seguridad_dos, pregunta_seguridad_tres, respuesta_seguridad_tres, db='hospital.db'):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE usuario
            SET 
                pregunta_seguridad = ?,
                respuesta_seguridad = ?,
                pregunta_seguridad_dos = ?,
                respuesta_seguridad_dos = ?,
                pregunta_seguridad_tres = ?,
                respuesta_seguridad_tres = ?
            WHERE nombre_usuario = ?;
            """,
            (pregunta_seguridad, respuesta_seguridad, pregunta_seguridad_dos, respuesta_seguridad_dos, pregunta_seguridad_tres, respuesta_seguridad_tres,nombre_usuario, )
        )
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        return str(e)
    finally:
        conn.close()

# el que se usa en olvprueba.py
def cambiar_contrasena(nueva_contra, usuario, db='hospital.db'):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET contrasena = ? WHERE nombre_usuario = ?", 
                      (nueva_contra, usuario))
        conn.commit()
        return True
    except sqlite3.Error as e:
        st.error(f"Error en la base de datos: {e}")
        return False
    finally:
        conn.close()


def verificar_preguntas_guardadas(nombre_usuario, db='hospital.db'):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pregunta_seguridad, pregunta_seguridad_dos, pregunta_seguridad_tres
            FROM usuario
            WHERE nombre_usuario = ?
        """, (nombre_usuario,))
        datos = cursor.fetchone()
        conn.close()
        # Si las tres preguntas existen y no están vacías, retorna True
        if datos and all(datos):
            return True
        return False
    except Exception as e:
        st.error(f"Error al verificar preguntas de seguridad: {e}", icon=":material/error:")
        return False
    
def verificar_superusuario(nombre_usuario, contrasena, db='hospital.db'):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT contrasena, rol, id_usuario FROM usuario WHERE nombre_usuario = ?",
            (nombre_usuario,)
        )
        resultado = cursor.fetchone()
        if resultado is None:
            st.error("Usuario no encontrado.", icon=":material/person_off:")
            return False

        contrasena_bd, rol, id_usuario = resultado

        # Solo permitir si el rol es Administrador (a)
        if rol != "Administrador (a)":
            st.warning("El usuario no tiene permisos de superusuario.", icon=":material/lock_open:")
            return False

        # Verificar contraseña
        if not verifi_contra_hasheada(contrasena, contrasena_bd):
            st.warning("Contraseña incorrecta.", icon=":material/lock_open:")
            return False

        # Verificar que exista registro en la tabla administrador vinculado al usuario (a través de doctor)
        cursor.execute("""
            SELECT a.id_administrador
            FROM administrador a
            JOIN doctor d ON a.id_doctor = d.id_doctor
            WHERE d.id_usuario = ?
        """, (id_usuario,))
        admin_row = cursor.fetchone()
        if admin_row is None:
            st.error("No se encontró una cuenta de administrador vinculada al usuario.", icon=":material/error:")
            return False

        # Éxito: establecer sesión y retornar True
        st.success("Sesión de superusuario iniciada correctamente.", icon=":material/check_circle:")
        st.session_state["autenticado_usuario"] = nombre_usuario
        return True
    except sqlite3.Error as e:
        st.error(f"Error en la base de datos al verificar superusuario: {e}", icon=":material/error:")
        return False
    finally:
        if conn:
            conn.close()



def eliminar_usuario_completo(nombre_usuario, db='hospital.db'):
    """
    Elimina por completo un usuario y todos los registros asociados creados
    al guardar un usuario (correo, doctor/secretaria y sus enlaces).
    Usa PRAGMA foreign_keys = ON para que las FK con ON DELETE CASCADE funcionen.
    Retorna True si se eliminó, False en caso contrario.
    """
    conn = None
    try:
        conn = sqlite3.connect(db)
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        # Obtener id_usuario y CI del usuario
        cursor.execute("SELECT id_usuario, CI FROM usuario WHERE nombre_usuario = ?", (nombre_usuario,))
        fila = cursor.fetchone()
        if fila is None:
            st.warning("Usuario no encontrado.", icon=":material/person_off:")
            return False

        id_usuario, ci = fila

        # Eliminar usuario (esto debería cascadear a correo, doctor, secretaria, etc.)
        cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
        # Eliminar persona (por si quedó registro; si usuario todavía existiera lo eliminaría por cascade)
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
