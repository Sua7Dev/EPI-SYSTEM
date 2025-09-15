import streamlit as st
import pandas as pd
import time
import sqlite3
import os
DB_PATH = os.getenv("hospital.db", "hospital.db")


def obtener_usuarios():
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT 
        u.id_usuario,
        p.nombre_apellido AS 'Nombre y Apellido',
        p.CI AS 'Cédula',
        u.rol AS 'Rol',
        c.correo AS 'Correo'
    FROM usuario u
    JOIN persona p ON u.CI = p.CI
    LEFT JOIN correo c ON u.id_usuario = c.id_usuario
    WHERE u.rol IN ('Doctor (a)', 'Secretario (a)')
    """
    df = pd.read_sql_query(query, conn)
    df['Rol'] = df['Rol'].str.capitalize()
    conn.close()
    return df

def eliminar_usuarios_seleccionados(usuarios_seleccionados):
    """
    Elimina sin confirmación los usuarios seleccionados y sus datos asociados.
    Llamar desde el handler del botón (ver abajo).
    """
    if usuarios_seleccionados.empty:
        st.warning("No ha seleccionado ningún usuario para eliminar.", icon=":material/account_circle_off:")
        return

    conn = sqlite3.connect(DB_PATH)
    try:
        cursor = conn.cursor()
        for index, row in usuarios_seleccionados.iterrows():
            id_usuario = row.get('id_usuario')
            cedula = row.get('Cédula')
            if not id_usuario:
                continue
            # Eliminar registros relacionados (se ejecutan aunque no existan)
            cursor.execute("DELETE FROM correo WHERE id_usuario = ?", (id_usuario,))
            cursor.execute("DELETE FROM doctor WHERE id_usuario = ?", (id_usuario,))
            cursor.execute("DELETE FROM secretaria WHERE id_usuario = ?", (id_usuario,))
            cursor.execute("DELETE FROM usuario WHERE id_usuario = ?", (id_usuario,))
            if cedula:
                cursor.execute("DELETE FROM persona WHERE CI = ?", (cedula,))
        conn.commit()
        st.success("Usuario(s) seleccionado(s) eliminado(s) exitosamente.", icon=":material/delete:")
        time.sleep(1)
        st.rerun()
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error al eliminar usuarios: {e}", icon=":material/error:")
    finally:
        conn.close()


def actualizar_usuario(id_usuario, nuevo_rol, nuevo_correo):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Obtener el rol actual del usuario
        cursor.execute("SELECT rol, CI FROM usuario WHERE id_usuario = ?", (id_usuario,))
        result = cursor.fetchone()
        if not result:
            st.error("Usuario no encontrado.")
            return False
        rol_actual, ci = result

        # Actualizar el rol en la tabla usuario
        cursor.execute("UPDATE usuario SET rol = ? WHERE id_usuario = ?", (nuevo_rol, id_usuario))

        # Actualizar el rol en la tabla persona
        cursor.execute("UPDATE persona SET rol = ? WHERE CI = ?", (nuevo_rol, ci))

        # Manejar las tablas doctor y secretaria
        if rol_actual != nuevo_rol:
            # Eliminar de la tabla correspondiente al rol actual
            if rol_actual == 'Doctor (a)':
                cursor.execute("DELETE FROM doctor WHERE id_usuario = ?", (id_usuario,))
            elif rol_actual == 'Secretario (a)':
                cursor.execute("DELETE FROM secretaria WHERE id_usuario = ?", (id_usuario,))

            # Insertar en la tabla correspondiente al nuevo rol, si no existe
            if nuevo_rol == 'Doctor (a)':
                cursor.execute("SELECT COUNT(*) FROM doctor WHERE id_usuario = ?", (id_usuario,))
                if cursor.fetchone()[0] == 0:  # Solo insertar si no existe
                    cursor.execute("INSERT INTO doctor (id_usuario) VALUES (?)", (id_usuario,))
            elif nuevo_rol == 'Secretario (a)':
                cursor.execute("SELECT COUNT(*) FROM secretaria WHERE id_usuario = ?", (id_usuario,))
                if cursor.fetchone()[0] == 0:  # Solo insertar si no existe
                    cursor.execute("INSERT INTO secretaria (id_usuario) VALUES (?)", (id_usuario,))

        # Actualizar el correo
        if nuevo_correo:
            cursor.execute("SELECT COUNT(*) FROM correo WHERE correo = ? AND id_usuario != ?", (nuevo_correo, id_usuario))
            if cursor.fetchone()[0] > 0:
                st.error(f"El correo '{nuevo_correo}' ya está en uso por otro usuario.")
                return False
            else:
                cursor.execute("SELECT correo FROM correo WHERE id_usuario = ?", (id_usuario,))
                correo_existente = cursor.fetchone()
                if correo_existente:
                    cursor.execute("UPDATE correo SET correo = ? WHERE id_usuario = ?", (nuevo_correo, id_usuario))
                else:
                    cursor.execute("INSERT INTO correo (id_usuario, correo) VALUES (?, ?)", (id_usuario, nuevo_correo))
        else:
            cursor.execute("DELETE FROM correo WHERE id_usuario = ?", (id_usuario,))
        
        conn.commit()
        return True
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")
        return False
    finally:
        conn.close()

# --- FUNCIONES NUEVAS ---  LISTA
def eliminar_datos_seguridad(nombre_usuario):
    """
    Pone a NULL la contraseña y las 3 preguntas/respuestas del usuario,
    buscando primero el id_usuario por nombre_usuario.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id_usuario FROM usuario WHERE nombre_usuario = ?", (nombre_usuario,))
        fila = cur.fetchone()
        if fila is None:
            st.warning(f"No se encontró el usuario '{nombre_usuario}' para eliminar datos de seguridad.", icon=":material/person_off:")
            return False
        id_usuario = fila[0]
        cur.execute("""
            UPDATE usuario
            SET pregunta_seguridad = NULL,
                respuesta_seguridad = NULL,
                pregunta_seguridad_dos = NULL,
                respuesta_seguridad_dos = NULL,
                pregunta_seguridad_tres = NULL,
                respuesta_seguridad_tres = NULL
            WHERE id_usuario = ?
        """, (id_usuario,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        st.error(f"Error al eliminar datos de seguridad para '{nombre_usuario}': {e}", icon=":material/error:")
        return False
    finally:
        if conn:
            conn.close()

def agregar_contra_nueva(nombre_usuario, contrasena_hasheada): # NO ESTA LISTA
    """
    Guarda la contraseña (ya hasheada) en la fila del usuario identificado por nombre_usuario.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id_usuario FROM usuario WHERE nombre_usuario = ?", (nombre_usuario,))
        fila = cur.fetchone()
        if fila is None:
            st.warning(f"No se encontró el usuario '{nombre_usuario}' para actualizar contraseña.", icon=":material/person_off:")
            return False
        cur.execute("""
            UPDATE usuario
            SET contrasena = ?
            WHERE nombre_usuario = ?
        """, (contrasena_hasheada, nombre_usuario))
        conn.commit()
        return True
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        st.error(f"Error al actualizar la contraseña de '{nombre_usuario}': {e}", icon=":material/error:")
        return False
    finally:
        if conn:
            conn.close()
# --- FIN FUNCIONES NUEVAS ---