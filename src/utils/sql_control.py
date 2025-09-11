import streamlit as st
import sqlite3
import pandas as pd
import time
import os
import datetime
import secrets
import string
from utils.contra import borro_cassette

DB_PATH = os.environ.get("DB_PATH", "hospital.db")

def insertar_hospital_info():
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT id_hospital FROM hospital WHERE nombre = ?", 
                      ("Hospital General Dr. Felipe Guevara Rojas",))
        if cursor.fetchone():
            return

        cursor.execute("INSERT OR IGNORE INTO pais (nombre) VALUES (?)", ('Venezuela',))
        cursor.execute("SELECT id_pais FROM pais WHERE nombre = ?", ('Venezuela',))
        id_pais = cursor.fetchone()[0]

        cursor.execute("INSERT OR IGNORE INTO estado (nombre, id_pais) VALUES (?, ?)", ('Anzoátegui', id_pais))
        cursor.execute("SELECT id_estado FROM estado WHERE nombre = ? AND id_pais = ?", ('Anzoátegui', id_pais))
        id_estado = cursor.fetchone()[0]

        cursor.execute("INSERT OR IGNORE INTO ciudad (nombre, id_estado) VALUES (?, ?)", ('El Tigre', id_estado))
        cursor.execute("SELECT id_ciudad FROM ciudad WHERE nombre = ? AND id_estado = ?", ('El Tigre', id_estado))
        id_ciudad = cursor.fetchone()[0]

        cursor.execute("INSERT OR IGNORE INTO municipio (nombre, id_ciudad) VALUES (?, ?)", ('Simón Rodríguez', id_ciudad))
        cursor.execute("SELECT id_municipio FROM municipio WHERE nombre = ? AND id_ciudad = ?", ('Simón Rodríguez', id_ciudad))
        id_municipio = cursor.fetchone()[0]

        cursor.execute("INSERT OR IGNORE INTO parroquia (nombre, id_municipio) VALUES (?, ?)", ('Edmundo Barrios', id_municipio))
        cursor.execute("SELECT id_parroquia FROM parroquia WHERE nombre = ? AND id_municipio = ?", ('Edmundo Barrios', id_municipio))
        id_parroquia = cursor.fetchone()[0]

        descripcion_direccion = "Av. Libertador 17 (17 Av. Libertador), El Tigre, código postal 6050."
        cursor.execute("INSERT OR IGNORE INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (descripcion_direccion, id_parroquia))
        cursor.execute("SELECT id_direccion FROM direccion WHERE descripcion = ? AND id_parroquia = ?", (descripcion_direccion, id_parroquia))
        id_direccion = cursor.fetchone()[0]

        descripcion_hospital = "El Hospital General Dr. Felipe Guevara Rojas es un centro de salud público ubicado en El Tigre, estado Anzoátegui, Venezuela, que pertenece al Distrito Sanitario N° V. Como hospital general, su función es ofrecer una amplia gama de servicios de salud, que van desde consultas de emergencia hasta atención especializada en diversas áreas."
        cursor.execute("INSERT INTO hospital (nombre, descripcion, id_direccion) VALUES (?, ?, ?)", 
                      ("Hospital General Dr. Felipe Guevara Rojas", descripcion_hospital, id_direccion))
        cursor.execute("SELECT id_hospital FROM hospital WHERE nombre = ?", ("Hospital General Dr. Felipe Guevara Rojas",))
        id_hospital = cursor.fetchone()[0]

        descripcion_departamento = (
            """El Departamento de Epidemiología del Hospital General Dr. Felipe Guevara Rojas es una unidad vital dedicada a la prevención y control de enfermedades infecciosas dentro de la institución. Bajo la dirección del Dr. Olivier Ladera, el equipo se centra en la vigilancia activa, investigando cualquier brote potencial para proteger tanto a los pacientes como al personal."""
        )
        cursor.execute("INSERT OR IGNORE INTO departamento (nombre, descripcion) VALUES (?, ?)", 
                      ('Epidemiología', descripcion_departamento))
        cursor.execute("SELECT id_departamento FROM departamento WHERE nombre = ?", ('Epidemiología',))
        id_departamento = cursor.fetchone()[0]

        cursor.execute("INSERT OR IGNORE INTO departamento_hospital (id_departamento, id_hospital) VALUES (?, ?)", 
                      (id_departamento, id_hospital))

        mision_texto = (
            "Departamento de epidemiología hospitalaria 'Dr. Felipe Guevara Rojas' tiene como misión proveer de información "
            "epidemiológica oportuna y de calidad para la vigilancia, investigación, análisis y evaluación del proceso Salud - Enfermedad, "
            "para orientar las acciones de salud de quienes demandan atención medica gratuita y humanizadas, enmarcado en las políticas de "
            "Salud del Estado Venezolano y de los vínculos interinstitucionales que sustentan en conjunto las acciones administrativas, "
            "asistenciales y docentes para la consecución de los objetivos del servicio como elemento organizacional clave dentro del hospital."
        )
        cursor.execute("INSERT OR IGNORE INTO mision (id_departamento, contenido) VALUES (?, ?)", 
                      (id_departamento, mision_texto))

        vision_texto = (
            "Ser un servicio que fortalezca la vigilancia epidemiológica y de los problemas de salud de la población de la zona Sur del "
            "estado Anzoátegui, mediante el análisis de la situación de salud que respondan ante la emergencia epidemiológica y de desastre; "
            "además establecer los lineamientos para la prevención y control de las enfermedades enmarcadas dentro de las políticas de salud "
            "del Estado Venezolano en la cual los usuarios internos y externos se sientan satisfechos por el servicio y producto proporcionado "
            "por el hospital 'Dr. Felipe Guevara Rojas'."
        )
        cursor.execute("INSERT OR IGNORE INTO vision (id_departamento, contenido) VALUES (?, ?)", 
                      (id_departamento, vision_texto))

        conn.commit()
    except sqlite3.Error:
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            
#operaciones de natalidad
def operaciones_sql_natalidad(accion, datos_registro=None):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if accion == "cargar":
                query = """
                    SELECT id_nata AS id, fecha, partos, cesareas, varones, hembras, gemelar, 
                           mto, partos_extrahospitalarios, id_doctor, fecha_registro_formulario
                    FROM natalidad
                """
                return pd.read_sql_query(query, conn)
            elif accion == "registrar" and datos_registro:
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='natalidad'")
                if not cursor.fetchone():
                    raise sqlite3.Error("La tabla 'natalidad' no existe en la base de datos.")
                fecha, partos, cesareas, varones, hembras, gemelar, mto, partos_extrahospitalarios, id_doctor, id_administrador, rol_usuario = datos_registro
                id_doctor_atendi = None
                if rol_usuario == "Doctor (a)" and id_doctor:
                    id_doctor_atendi = id_doctor
                elif rol_usuario == "Administrador (a)" and id_administrador:
                    cursor.execute("SELECT id_doctor FROM administrador WHERE id_administrador = ?", (id_administrador,))
                    result = cursor.fetchone()
                    if result:
                        id_doctor_atendi = result[0]

                if isinstance(fecha, (datetime.date, datetime.datetime, pd.Timestamp)):
                    fecha_formateada_nacimiento = fecha.strftime("%d/%m/%Y")
                else:
                    fecha_formateada_nacimiento = str(fecha)
                #fecha_formateada_nacimiento = fecha.strftime("%d/%m/%Y")
                cursor.execute("""
                    INSERT INTO natalidad (
                        fecha, partos, cesareas, varones, hembras, gemelar, 
                        mto, partos_extrahospitalarios, id_doctor, fecha_registro_formulario
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    fecha_formateada_nacimiento, partos, cesareas, varones, hembras, gemelar, 
                    mto, partos_extrahospitalarios, id_doctor_atendi, datetime.date.today()
                ))
                conn.commit()
                return True
    except sqlite3.Error as e:
        st.error(f"Error en operación SQL: {e}", icon=":material/error:")
        return None

def eliminar_registros_natalidad(edited_df):
    seleccionados = edited_df.loc[edited_df[" "], "id"].tolist()
    if not seleccionados:
        st.warning("No has seleccionado ningún registro para eliminar.", icon=":material/warning:")
        return
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.executemany("DELETE FROM natalidad WHERE id_nata = ?", [(id_,) for id_ in seleccionados])
            conn.commit()
            st.success(f"Se eliminaron {len(seleccionados)} registro(s).", icon=":material/check_circle:")
            st.rerun()
    except sqlite3.Error as e:
        st.error(f"Error al eliminar: {e}", icon=":material/error:")
        
#operaciones de epi14
def operaciones_sql_epi14(accion, datos_registro=None):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            if accion == "cargar":
                query = """
                    SELECT es.id_semanal,
                           es.semana || '-' || strftime('%Y', es.fecha_registro_formulario) AS semana,
                           es.causa,
                           es.numero,
                           es.sexo_edad,
                           SUM(es.numero) OVER (PARTITION BY es.semana) AS total,
                           es.fecha_registro_formulario,
                           COALESCE(p.nombre_apellido, 'No asignado') AS Registrado_por
                    FROM epi14_semanal es
                    LEFT JOIN doctor d ON es.id_doctor = d.id_doctor
                    LEFT JOIN usuario u ON d.id_usuario = u.id_usuario
                    LEFT JOIN persona p ON u.CI = p.CI
                """
                return pd.read_sql_query(query, conn)
            elif accion == "registrar" and datos_registro:
                semana, causa, numero, sexo_edad, id_doctor, id_secretaria, id_administrador, rol_usuario = datos_registro
                semana_str = f"Semana {semana}"
                id_doctor_to_insert = id_doctor

                if rol_usuario == "Administrador (a)" and id_administrador:
                    cursor.execute("SELECT id_doctor FROM administrador WHERE id_administrador = ?", (id_administrador,))
                    result = cursor.fetchone()
                    if result:
                        id_doctor_to_insert = result[0]
                elif rol_usuario == "Secretario (a)" and id_secretaria:
                    id_doctor_to_insert = None  

                # Calcular el total acumulado de esa semana (antes de insertar el nuevo registro)
                cursor.execute("""
                    SELECT COALESCE(SUM(numero), 0) 
                    FROM epi14_semanal 
                    WHERE semana = ?
                """, (semana_str,))
                total_actual = cursor.fetchone()[0]
                nuevo_total = total_actual + numero

                # Insertar el registro con el total
                cursor.execute("""
                    INSERT INTO epi14_semanal 
                    (semana, causa, numero, sexo_edad, id_doctor, fecha_registro_formulario, total)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (semana_str, causa, numero, sexo_edad, id_doctor_to_insert, datetime.date.today(), nuevo_total))

                conn.commit()
                return True
    except sqlite3.Error as e:
        st.error(f"Error en operación SQL: {e}", icon=":material/error:")
        return None

def eliminar_registros_epi14(edited_df):
    ids_a_eliminar = edited_df.loc[edited_df[' '], 'id_semanal'].tolist()
    if not ids_a_eliminar:
        st.warning("Selecciona al menos un registro.", icon=":material/info:")
        return
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            for id_semanal in ids_a_eliminar:
                cursor.execute("DELETE FROM epi14_semanal WHERE id_semanal = ?", (id_semanal,))
            conn.commit()
            st.success(f"{len(ids_a_eliminar)} registros eliminados.", icon=":material/check_circle:")
            st.rerun()
    except sqlite3.Error as e:
        st.error(f"Error al eliminar: {e}", icon=":material/error:")
        
#operaciones de registro diario 
def operaciones_sql_registro_diario(accion, datos_registro=None):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if accion == "cargar":
                query = """
                    SELECT id_registro AS id, 
                           semana || '-' || strftime('%Y', fecha_registro_formulario) AS semana, 
                           fd, edad_sexo, mr, mo, so, cb, cd, gett, nc, peso, talla, autopsia,
                           d.id_doctor, fecha_registro_formulario
                    FROM registro_diario
                    LEFT JOIN doctor d ON registro_diario.id_doctor = d.id_doctor
                """
                df = pd.read_sql_query(query, conn)
                return df
            elif accion == "registrar" and datos_registro:
                semana, fd, edad_sexo, mr, mo, so, cb, cd, gett, nc, peso, talla, autopsia, id_doctor, id_administrador, rol_usuario = datos_registro
                semana_str = f"Semana {semana} "
                id_doctor_atendi = None
                if rol_usuario == "Doctor (a)" and id_doctor:
                    id_doctor_atendi = id_doctor
                elif rol_usuario == "Administrador (a)" and id_administrador:
                    cursor.execute("SELECT id_doctor FROM administrador WHERE id_administrador = ?", (id_administrador,))
                    result = cursor.fetchone()
                    if result:
                        id_doctor_atendi = result[0]
                cursor.execute("""
                    INSERT INTO registro_diario (
                        semana, fd, edad_sexo, mr, mo, so, cb, cd, gett, nc, peso, talla, autopsia, id_doctor, fecha_registro_formulario
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    semana_str, fd, edad_sexo, mr, mo, so, cb, cd, gett, nc, peso, talla, autopsia, id_doctor_atendi, datetime.date.today()
                ))
                conn.commit()
                return True
    except sqlite3.Error as e:
        st.error(f"Error en operación SQL: {e}", icon=":material/error:")
        return None

def eliminar_registros_diario(edited_df):
    # Buscar la columna de id de manera flexible
    id_col = None
    for col in ['id', 'id_registro']:
        if col in edited_df.columns:
            id_col = col
            break
    if id_col is None:
        st.error("No se encontró la columna de ID en los registros.", icon=":material/error:")
        return

    ids_a_eliminar = edited_df.loc[edited_df[' '], id_col].tolist()
    if not ids_a_eliminar:
        st.warning("No se seleccionaron registros para eliminar.", icon=":material/warning:")
        return
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM registro_diario WHERE id_registro IN ({','.join('?' * len(ids_a_eliminar))})",
                ids_a_eliminar
            )
            conn.commit()
            st.success(f"Se eliminaron {len(ids_a_eliminar)} registros.", icon=":material/check_circle:")
            time.sleep(1)
            st.rerun()
    except sqlite3.Error as e:
        st.error(f"Error al eliminar: {e}", icon=":material/error:")
        
#operaciones de morbilidad 

def operaciones_sql_morb_extenso(accion, datos_registro=None):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if accion == "cargar":
                query = """
                    SELECT me.HC, m.id_morb AS id, m.diagnostico, 
                           me.nombres_apellidos, 
                           me.fecha_nacimiento, me.estado_civil, me.cedula, me.telefono,
                           COALESCE(p_h.nombre || ', ', '') || 
                           COALESCE(e_h.nombre || ', ', '') || 
                           COALESCE(c_h.nombre || ', ', '') || 
                           COALESCE(m_h.nombre || ', ', '') || 
                           COALESCE(par_h.nombre || ', ', '') || 
                           dh.descripcion AS direccion_hogar,
                           COALESCE(p_n.nombre || ', ', '') || 
                           COALESCE(e_n.nombre || ', ', '') || 
                           COALESCE(c_n.nombre || ', ', '') || 
                           COALESCE(m_n.nombre || ', ', '') || 
                           COALESCE(par_n.nombre || ', ', '') || 
                           dn.descripcion AS direccion_nacimiento,
                           pp.edad, m.sexo, m.fecha_registro_formulario
                    FROM morb_extenso me
                    JOIN morbilidad m ON me.id_morb = m.id_morb
                    LEFT JOIN persona_paciente pp ON m.id_paciente = pp.id_paciente
                    JOIN direccion dh ON me.id_direccion_hogar = dh.id_direccion
                    LEFT JOIN direccion dn ON me.id_direccion_nacimiento = dn.id_direccion
                    LEFT JOIN parroquia par_h ON dh.id_parroquia = par_h.id_parroquia
                    LEFT JOIN municipio m_h ON par_h.id_municipio = m_h.id_municipio
                    LEFT JOIN ciudad c_h ON m_h.id_ciudad = c_h.id_ciudad
                    LEFT JOIN estado e_h ON c_h.id_estado = e_h.id_estado
                    LEFT JOIN pais p_h ON e_h.id_pais = p_h.id_pais
                    LEFT JOIN parroquia par_n ON dn.id_parroquia = par_n.id_parroquia
                    LEFT JOIN municipio m_n ON par_n.id_municipio = m_n.id_municipio
                    LEFT JOIN ciudad c_n ON m_n.id_ciudad = c_n.id_ciudad
                    LEFT JOIN estado e_n ON c_n.id_estado = e_n.id_estado
                    LEFT JOIN pais p_n ON e_n.id_pais = p_n.id_pais
                """
                return pd.read_sql_query(query, conn)
            elif accion == "registrar" and datos_registro:
                hc, nombres_apellidos, diagnostico, edad, sexo, pais_hogar, estado_hogar, municipio_hogar, parroquia_hogar, ciudad_hogar, direccion_exacta_hogar, pais_nacimiento, estado_nacimiento, municipio_nacimiento, parroquia_nacimiento, ciudad_nacimiento, direccion_exacta_nacimiento, fecha_nacimiento, estado_civil, cedula, telefono, id_doctor, id_administrador, id_secretaria, rol_usuario = datos_registro
                
                # Dirección de hogar
                pais_hogar = pais_hogar or "No disponible"
                estado_hogar = estado_hogar or "No disponible"
                municipio_hogar = municipio_hogar or "No disponible"

                cursor.execute("INSERT OR IGNORE INTO pais (nombre) VALUES (?)", (pais_hogar,))
                cursor.execute("SELECT id_pais FROM pais WHERE nombre = ?", (pais_hogar,))
                id_pais_hogar = cursor.fetchone()[0]
                
                cursor.execute("INSERT OR IGNORE INTO estado (nombre, id_pais) VALUES (?, ?)", (estado_hogar, id_pais_hogar))
                cursor.execute("SELECT id_estado FROM estado WHERE nombre = ? AND id_pais = ?", (estado_hogar, id_pais_hogar))
                id_estado_hogar = cursor.fetchone()[0]
                
                cursor.execute("INSERT OR IGNORE INTO ciudad (nombre, id_estado) VALUES (?, ?)", (ciudad_hogar, id_estado_hogar))
                cursor.execute("SELECT id_ciudad FROM ciudad WHERE nombre = ? AND id_estado = ?", (ciudad_hogar, id_estado_hogar))
                id_ciudad_hogar = cursor.fetchone()[0]
                
                cursor.execute("INSERT OR IGNORE INTO municipio (nombre, id_ciudad) VALUES (?, ?)", (municipio_hogar, id_ciudad_hogar))
                cursor.execute("SELECT id_municipio FROM municipio WHERE nombre = ? AND id_ciudad = ?", (municipio_hogar, id_ciudad_hogar))
                id_municipio_hogar = cursor.fetchone()[0]
                
                cursor.execute("INSERT OR IGNORE INTO parroquia (nombre, id_municipio) VALUES (?, ?)", (parroquia_hogar, id_municipio_hogar))
                cursor.execute("SELECT id_parroquia FROM parroquia WHERE nombre = ? AND id_municipio = ?", (parroquia_hogar, id_municipio_hogar))
                id_parroquia_hogar = cursor.fetchone()[0]
                
                cursor.execute("INSERT OR IGNORE INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", 
                              (direccion_exacta_hogar, id_parroquia_hogar))
                cursor.execute("SELECT id_direccion FROM direccion WHERE descripcion = ? AND id_parroquia = ?", 
                              (direccion_exacta_hogar, id_parroquia_hogar))
                id_direccion_hogar = cursor.fetchone()[0]
                
                # Dirección de nacimiento
                pais_nacimiento = pais_nacimiento or "No disponible"
                estado_nacimiento = estado_nacimiento or "No disponible"
                ciudad_nacimiento = ciudad_nacimiento or "No disponible"
                municipio_nacimiento = municipio_nacimiento or "No disponible"
                parroquia_nacimiento = parroquia_nacimiento or "No disponible"
                direccion_exacta_nacimiento = direccion_exacta_nacimiento or "No disponible"
                
                cursor.execute("INSERT OR IGNORE INTO pais (nombre) VALUES (?)", (pais_nacimiento,))
                cursor.execute("SELECT id_pais FROM pais WHERE nombre = ?", (pais_nacimiento,))
                id_pais_nacimiento = cursor.fetchone()[0]
                
                cursor.execute("INSERT OR IGNORE INTO estado (nombre, id_pais) VALUES (?, ?)", (estado_nacimiento, id_pais_nacimiento))
                cursor.execute("SELECT id_estado FROM estado WHERE nombre = ? AND id_pais = ?", (estado_nacimiento, id_pais_nacimiento))
                id_estado_nacimiento = cursor.fetchone()[0]
                
                cursor.execute("INSERT OR IGNORE INTO ciudad (nombre, id_estado) VALUES (?, ?)", (ciudad_nacimiento, id_estado_nacimiento))
                cursor.execute("SELECT id_ciudad FROM ciudad WHERE nombre = ? AND id_estado = ?", (ciudad_nacimiento, id_estado_nacimiento))
                id_ciudad_nacimiento = cursor.fetchone()[0]
                
                cursor.execute("INSERT OR IGNORE INTO municipio (nombre, id_ciudad) VALUES (?, ?)", (municipio_nacimiento, id_ciudad_nacimiento))
                cursor.execute("SELECT id_municipio FROM municipio WHERE nombre = ? AND id_ciudad = ?", (municipio_nacimiento, id_ciudad_nacimiento))
                id_municipio_nacimiento = cursor.fetchone()[0]
                
                cursor.execute("INSERT OR IGNORE INTO parroquia (nombre, id_municipio) VALUES (?, ?)", (parroquia_nacimiento, id_municipio_nacimiento))
                cursor.execute("SELECT id_parroquia FROM parroquia WHERE nombre = ? AND id_municipio = ?", (parroquia_nacimiento, id_municipio_nacimiento))
                id_parroquia_nacimiento = cursor.fetchone()[0]
                
                cursor.execute("INSERT OR IGNORE INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", 
                              (direccion_exacta_nacimiento, id_parroquia_nacimiento))
                cursor.execute("SELECT id_direccion FROM direccion WHERE descripcion = ? AND id_parroquia = ?", 
                              (direccion_exacta_nacimiento, id_parroquia_nacimiento))
                id_direccion_nacimiento = cursor.fetchone()[0]
                
                # Insertar en persona_paciente, morbilidad y morb_extenso
                cursor.execute("INSERT INTO persona_paciente (edad) VALUES (?)", 
                              (edad,))
                id_paciente = cursor.lastrowid
                
                cursor.execute("INSERT INTO morbilidad (id_paciente, sexo, diagnostico, fecha_registro_formulario) VALUES (?, ?, ?, ?)", 
                              (id_paciente, sexo, diagnostico, datetime.date.today()))
                id_morb = cursor.lastrowid
                
                if isinstance(fecha_nacimiento, (datetime.date, datetime.datetime, pd.Timestamp)):
                    fecha_formateada_nacimiento = fecha_nacimiento.strftime("%d/%m/%Y")
                else:
                    fecha_formateada_nacimiento = str(fecha_nacimiento)    
                #fecha_formateada_nacimiento = fecha_nacimiento.strftime("%d/%m/%Y")
                cursor.execute("INSERT INTO morb_extenso (HC, id_morb, nombres_apellidos, id_direccion_hogar, id_direccion_nacimiento, fecha_nacimiento, estado_civil, cedula, telefono) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                              (hc, id_morb, nombres_apellidos, id_direccion_hogar, id_direccion_nacimiento, fecha_formateada_nacimiento, estado_civil, cedula, telefono))
                
                # Asignar doctor o secretaria según el rol del usuario
                if rol_usuario == "Doctor (a)" and id_doctor:
                    cursor.execute("INSERT INTO doctor_paciente (id_doctor, id_paciente) VALUES (?, ?)", 
                                  (id_doctor, id_paciente))
                elif rol_usuario == "Secretario (a)" and id_secretaria:
                    cursor.execute("INSERT INTO secretaria_paciente (id_secretaria, id_paciente) VALUES (?, ?)", 
                                  (id_secretaria, id_paciente))
                elif rol_usuario == "Administrador (a)" and id_administrador:
                    cursor.execute("SELECT id_doctor FROM administrador WHERE id_administrador = ?", (id_administrador,))
                    result = cursor.fetchone()
                    if result:
                        id_doctor_admin = result[0]
                        cursor.execute("INSERT INTO doctor_paciente (id_doctor, id_paciente) VALUES (?, ?)", 
                                      (id_doctor_admin, id_paciente))
                
                conn.commit()
                return True
    except sqlite3.IntegrityError as e:
        error_message = str(e).lower()
        if 'morb_extenso.hc' in error_message:
            st.error("La Historia Clínica (HC) ya existe.", icon=":material/error:")
        elif 'morb_extenso.cedula' in error_message:
            st.error("La Cédula de identidad ya existe en otro registro.", icon=":material/error:")
        else:
            st.error(f"Error de integridad de datos: {e}", icon=":material/error:")
        return None
    except sqlite3.Error as e:
        st.error(f"Error en operación SQL: {e}", icon=":material/error:")
        return None


def operaciones_sql_morb_simplifica(accion, datos_registro=None, db='hospital.db'):
    try:
        with sqlite3.connect(db) as conn:
            cursor = conn.cursor()
            if accion == "cargar":
                query = """
                    SELECT ms.id_morbsim AS id, m.diagnostico, pp.edad, m.sexo, m.fecha_registro_formulario
                    FROM morb_simplifica ms
                    JOIN morbilidad m ON ms.id_morb = m.id_morb
                    LEFT JOIN persona_paciente pp ON m.id_paciente = pp.id_paciente
                """
                return pd.read_sql_query(query, conn)
            elif accion == "registrar" and datos_registro:
                diagnostico, edad, sexo, id_doctor, id_administrador, id_secretaria, rol_usuario = datos_registro
                cursor.execute("INSERT INTO persona_paciente (edad) VALUES (?)", (edad,))
                id_paciente = cursor.lastrowid
                cursor.execute("""
                    INSERT INTO morbilidad (id_paciente, sexo, diagnostico, fecha_registro_formulario)
                    VALUES (?, ?, ?, ?)
                """, (id_paciente, sexo, diagnostico, datetime.date.today()))
                id_morb = cursor.lastrowid
                cursor.execute("INSERT INTO morb_simplifica (id_morb) VALUES (?)", (id_morb,))
                if rol_usuario == "Doctor (a)" and id_doctor:
                    cursor.execute("INSERT OR IGNORE INTO doctor_paciente (id_doctor, id_paciente) VALUES (?, ?)", (id_doctor, id_paciente))
                elif rol_usuario == "Secretario (a)" and id_secretaria:
                    cursor.execute("INSERT OR IGNORE INTO secretaria_paciente (id_secretaria, id_paciente) VALUES (?, ?)", (id_secretaria, id_paciente))
                elif rol_usuario == "Administrador (a)" and id_administrador:
                    cursor.execute("SELECT id_doctor FROM administrador WHERE id_administrador = ?", (id_administrador,))
                    result = cursor.fetchone()
                    if result:
                        id_doctor_admin = result[0]
                        cursor.execute("INSERT OR IGNORE INTO doctor_paciente (id_doctor, id_paciente) VALUES (?, ?)", (id_doctor_admin, id_paciente))
                conn.commit()
                return True
    except sqlite3.Error as e:
        st.error(f"Error en operación SQL: {e}", icon=":material/error:")
        return None
    
    
def eliminar_registros_morb_extenso(edited_df):
    ids_a_eliminar = edited_df.loc[edited_df[' '], 'id'].tolist()
    if not ids_a_eliminar:
        st.warning("Selecciona al menos un registro.", icon=":material/info:")
        return
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for id_morb in ids_a_eliminar:
                cursor.execute("""
                    SELECT me.id_direccion_hogar, me.id_direccion_nacimiento, m.id_paciente
                    FROM morb_extenso me
                    JOIN morbilidad m ON me.id_morb = m.id_morb
                    WHERE me.id_morb = ?
                """, (id_morb,))
                datos = cursor.fetchone()
                if not datos:
                    continue
                id_dir_hogar, id_dir_nac, id_paciente = datos
                cursor.execute("DELETE FROM morb_extenso WHERE id_morb = ?", (id_morb,))
                cursor.execute("DELETE FROM morbilidad WHERE id_morb = ?", (id_morb,))
                cursor.execute("DELETE FROM doctor_paciente WHERE id_paciente = ?", (id_paciente,))
                cursor.execute("DELETE FROM secretaria_paciente WHERE id_paciente = ?", (id_paciente,))
                cursor.execute("DELETE FROM persona_paciente WHERE id_paciente = ?", (id_paciente,))
                for id_dir in [id_dir_hogar, id_dir_nac]:
                    if id_dir:
                        cursor.execute("""
                            SELECT d.id_parroquia, p.id_municipio, m.id_ciudad, c.id_estado, e.id_pais
                            FROM direccion d
                            LEFT JOIN parroquia p ON d.id_parroquia = p.id_parroquia
                            LEFT JOIN municipio m ON p.id_municipio = m.id_municipio
                            LEFT JOIN ciudad c ON m.id_ciudad = c.id_ciudad
                            LEFT JOIN estado e ON c.id_estado = e.id_estado
                            WHERE d.id_direccion = ?
                        """, (id_dir,))
                        jerarquia = cursor.fetchone()
                        cursor.execute("SELECT COUNT(*) FROM morb_extenso WHERE id_direccion_hogar = ? OR id_direccion_nacimiento = ?", (id_dir, id_dir))
                        if cursor.fetchone()[0] == 0:
                            cursor.execute("DELETE FROM direccion WHERE id_direccion = ?", (id_dir,))
                        if jerarquia:
                            id_parr, id_mun, id_ciud, id_est, id_pais = jerarquia
                            if id_parr:
                                cursor.execute("SELECT COUNT(*) FROM direccion WHERE id_parroquia = ?", (id_parr,))
                                if cursor.fetchone()[0] == 0:
                                    cursor.execute("DELETE FROM parroquia WHERE id_parroquia = ?", (id_parr,))
                            if id_mun:
                                cursor.execute("SELECT COUNT(*) FROM parroquia WHERE id_municipio = ?", (id_mun,))
                                if cursor.fetchone()[0] == 0:
                                    cursor.execute("DELETE FROM municipio WHERE id_municipio = ?", (id_mun,))
                            if id_ciud:
                                cursor.execute("SELECT COUNT(*) FROM municipio WHERE id_ciudad = ?", (id_ciud,))
                                if cursor.fetchone()[0] == 0:
                                    cursor.execute("DELETE FROM ciudad WHERE id_ciudad = ?", (id_ciud,))
                            if id_est:
                                cursor.execute("SELECT COUNT(*) FROM ciudad WHERE id_estado = ?", (id_est,))
                                if cursor.fetchone()[0] == 0:
                                    cursor.execute("DELETE FROM estado WHERE id_estado = ?", (id_est,))
                            if id_pais:
                                cursor.execute("SELECT COUNT(*) FROM estado WHERE id_pais = ?", (id_pais,))
                                if cursor.fetchone()[0] == 0:
                                    cursor.execute("DELETE FROM pais WHERE id_pais = ?", (id_pais,))
            conn.commit()
            st.success(f"{len(ids_a_eliminar)} registros y datos asociados eliminados.", icon=":material/check_circle:")
            st.rerun()
    except sqlite3.IntegrityError:
        st.error("La Historia clinica ya existe.", icon=":material/error:")
        return
    except sqlite3.Error as e:
        st.error(f"Error al eliminar: {e}", icon=":material/error:")

def eliminar_registros_morb_simplifica(edited_df):
    ids_a_eliminar = edited_df.loc[edited_df[' '], 'id'].tolist()
    if not ids_a_eliminar:
        st.warning("Selecciona al menos un registro.", icon=":material/info:")
        return
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for id_morbsim in ids_a_eliminar:
                cursor.execute("""
                    SELECT ms.id_morb, m.id_paciente
                    FROM morb_simplifica ms
                    JOIN morbilidad m ON ms.id_morb = m.id_morb
                    WHERE ms.id_morbsim = ?
                """, (id_morbsim,))
                datos = cursor.fetchone()
                if not datos:
                    continue
                id_morb, id_paciente = datos
                cursor.execute("DELETE FROM morb_simplifica WHERE id_morbsim = ?", (id_morbsim,))
                cursor.execute("DELETE FROM morbilidad WHERE id_morb = ?", (id_morb,))
                cursor.execute("DELETE FROM doctor_paciente WHERE id_paciente = ?", (id_paciente,))
                cursor.execute("DELETE FROM secretaria_paciente WHERE id_paciente = ?", (id_paciente,))
                cursor.execute("DELETE FROM persona_paciente WHERE id_paciente = ?", (id_paciente,))
            conn.commit()
            st.success(f"{len(ids_a_eliminar)} registros y datos asociados eliminados.", icon=":material/check_circle:")
            st.rerun()
    except sqlite3.Error as e:
        st.error(f"Error al eliminar: {e}", icon=":material/error:")
        
#operaciones de mortalidad neonatal 

def operaciones_sql_neonatal(accion, datos_registro=None):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if accion == "cargar":
                query = """
                    SELECT m.id_m AS id, m.historia_clinica, m.nombres_apellidos, m.fecha_nacimiento,
                           m.fecha_ingreso, m.hora_ingreso, m.fecha_defuncion, m.hora_defuncion, pp.edad,
                           m.idx_ingreso, m.idx_defuncion, t.nombre_madre, t.hora_nacimiento,
                           t.semanas_gestacion, t.peso, t.talla,
                           COALESCE(p.nombre || ', ', '') || 
                           COALESCE(e.nombre || ', ', '') || 
                           COALESCE(c.nombre || ', ', '') || 
                           COALESCE(mu.nombre || ', ', '') || 
                           COALESCE(par.nombre || ', ', '') || 
                           d.descripcion AS direccion
                    FROM mortalidad_neonatal t
                    JOIN mortalidad m ON t.id_m = m.id_m
                    JOIN persona_paciente pp ON m.id_paciente = pp.id_paciente
                    LEFT JOIN direccion d ON m.id_direccion = d.id_direccion
                    LEFT JOIN parroquia par ON d.id_parroquia = par.id_parroquia
                    LEFT JOIN municipio mu ON par.id_municipio = mu.id_municipio
                    LEFT JOIN ciudad c ON mu.id_ciudad = c.id_ciudad
                    LEFT JOIN estado e ON c.id_estado = e.id_estado
                    LEFT JOIN pais p ON e.id_pais = p.id_pais
                """
                return pd.read_sql_query(query, conn)
            elif accion == "registrar" and datos_registro:
                historia_clinica, nombres_apellidos, nombre_madre, fecha_nacimiento, hora_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, edad_junto, idx_ingreso, idx_defuncion, semanas_gestacion, peso, talla, pais_hogar, estado_hogar, municipio_hogar, parroquia_hogar, ciudad_hogar, direccion_exacta, id_doctor, id_administrador = datos_registro
                
                pais_hogar = pais_hogar or "No disponible"
                estado_hogar = estado_hogar or "No disponible"
                ciudad_hogar = ciudad_hogar or "No disponible"
                municipio_hogar = municipio_hogar or "No disponible"
                parroquia_hogar = parroquia_hogar or "No disponible"
                direccion_exacta = direccion_exacta or "No disponible"

                cursor.execute("INSERT OR IGNORE INTO pais (nombre) VALUES (?)", (pais_hogar,))
                cursor.execute("SELECT id_pais FROM pais WHERE nombre = ?", (pais_hogar,))
                id_pais = cursor.fetchone()[0]
                
                cursor.execute("INSERT OR IGNORE INTO estado (nombre, id_pais) VALUES (?, ?)", (estado_hogar, id_pais))
                cursor.execute("SELECT id_estado FROM estado WHERE nombre = ? AND id_pais = ?", (estado_hogar, id_pais))
                id_estado = cursor.fetchone()[0]
                
                cursor.execute("INSERT OR IGNORE INTO ciudad (nombre, id_estado) VALUES (?, ?)", (ciudad_hogar, id_estado))
                cursor.execute("SELECT id_ciudad FROM ciudad WHERE nombre = ? AND id_estado = ?", (ciudad_hogar, id_estado))
                id_ciudad = cursor.fetchone()[0]
                
                cursor.execute("INSERT OR IGNORE INTO municipio (nombre, id_ciudad) VALUES (?, ?)", (municipio_hogar, id_ciudad))
                cursor.execute("SELECT id_municipio FROM municipio WHERE nombre = ? AND id_ciudad = ?", (municipio_hogar, id_ciudad))
                id_municipio = cursor.fetchone()[0]
                
                cursor.execute("INSERT OR IGNORE INTO parroquia (nombre, id_municipio) VALUES (?, ?)", (parroquia_hogar, id_municipio))
                cursor.execute("SELECT id_parroquia FROM parroquia WHERE nombre = ? AND id_municipio = ?", (parroquia_hogar, id_municipio))
                id_parroquia = cursor.fetchone()[0]
                
                cursor.execute("INSERT OR IGNORE INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (direccion_exacta, id_parroquia))
                cursor.execute("SELECT id_direccion FROM direccion WHERE descripcion = ? AND id_parroquia = ?", (direccion_exacta, id_parroquia))
                id_direccion = cursor.fetchone()[0]
                
                cursor.execute("INSERT INTO persona_paciente (edad) VALUES (?)", (edad_junto,))
                id_paciente = cursor.lastrowid
                
                if isinstance(fecha_nacimiento, (datetime.date, datetime.datetime, pd.Timestamp)):
                    fecha_formateada_nacimiento = fecha_nacimiento.strftime("%d/%m/%Y")
                else:
                    fecha_formateada_nacimiento = str(fecha_nacimiento)  

                if isinstance(fecha_ingreso, (datetime.date, datetime.datetime, pd.Timestamp)):
                    fecha_formateada_ingreso = fecha_ingreso.strftime("%d/%m/%Y")
                else:
                    fecha_formateada_ingreso = str(fecha_ingreso)   

                if isinstance(fecha_defuncion, (datetime.date, datetime.datetime, pd.Timestamp)):
                    fecha_formateada_defuncion = fecha_defuncion.strftime("%d/%m/%Y")
                else:
                    fecha_formateada_defuncion = str(fecha_defuncion)   

                #fecha_formateada_nacimiento = fecha_nacimiento.strftime("%d/%m/%Y")
                #fecha_formateada_ingreso = fecha_ingreso.strftime("%d/%m/%Y")
                #fecha_formateada_defuncion = fecha_defuncion.strftime("%d/%m/%Y")
                cursor.execute("""
                    INSERT INTO mortalidad (
                        id_paciente, id_direccion, historia_clinica, nombres_apellidos, 
                        fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, 
                        idx_ingreso, idx_defuncion, fecha_registro_formulario
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    id_paciente, id_direccion, historia_clinica, nombres_apellidos, 
                    fecha_formateada_nacimiento, fecha_formateada_ingreso, hora_ingreso, fecha_formateada_defuncion, hora_defuncion, 
                    idx_ingreso, idx_defuncion, datetime.date.today()
                ))
                id_m = cursor.lastrowid
                
                hora_nacimiento_str = ""
                if isinstance(hora_nacimiento, pd.Timestamp):
                    hora_nacimiento_str = hora_nacimiento.strftime("%H:%M:%S")
                elif isinstance(hora_nacimiento, datetime.time):
                    hora_nacimiento_str = hora_nacimiento.strftime("%H:%M:%S")
                else:
                    hora_nacimiento_str = str(hora_nacimiento)
                
                cursor.execute("""
                    INSERT INTO mortalidad_neonatal (
                        id_m, nombre_madre, hora_nacimiento, semanas_gestacion, peso, talla
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (id_m, nombre_madre, hora_nacimiento_str, semanas_gestacion, peso, talla ))
                
                if id_doctor:
                    cursor.execute("INSERT OR IGNORE INTO doctor_paciente (id_doctor, id_paciente) VALUES (?, ?)", (id_doctor, id_paciente))
                elif id_administrador:
                    cursor.execute("SELECT id_doctor FROM administrador WHERE id_administrador = ?", (id_administrador,))
                    result = cursor.fetchone()
                    if result:
                        id_doctor_admin = result[0]
                        cursor.execute("INSERT OR IGNORE INTO doctor_paciente (id_doctor, id_paciente) VALUES (?, ?)", (id_doctor_admin, id_paciente))
                
                conn.commit()
                return True
    except sqlite3.IntegrityError:
        st.error("La Historia clinica ya existe.", icon=":material/error:")
        return
    except sqlite3.Error as e:
        st.error(f"Error en operación SQL: {e}", icon=":material/error:")
        return None

def eliminar_registros_neonatal(edited_df):
    ids_a_eliminar = edited_df.loc[edited_df[' '], 'id'].tolist()
    if not ids_a_eliminar:
        st.warning("Selecciona al menos un registro.", icon=":material/info:")
        return
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for id_m in ids_a_eliminar:
                cursor.execute("""
                    SELECT m.id_direccion, m.id_paciente
                    FROM mortalidad m
                    WHERE m.id_m = ?
                """, (id_m,))
                datos = cursor.fetchone()
                if not datos:
                    continue
                id_dir, id_paciente = datos
                cursor.execute("DELETE FROM mortalidad_neonatal WHERE id_m = ?", (id_m,))
                cursor.execute("DELETE FROM mortalidad WHERE id_m = ?", (id_m,))
                cursor.execute("DELETE FROM doctor_paciente WHERE id_paciente = ?", (id_paciente,))
                cursor.execute("DELETE FROM persona_paciente WHERE id_paciente = ?", (id_paciente,))
                if id_dir:
                    cursor.execute("""
                        SELECT d.id_parroquia, p.id_municipio, m.id_ciudad, c.id_estado, e.id_pais
                        FROM direccion d
                        LEFT JOIN parroquia p ON d.id_parroquia = p.id_parroquia
                        LEFT JOIN municipio m ON p.id_municipio = m.id_municipio
                        LEFT JOIN ciudad c ON m.id_ciudad = c.id_ciudad
                        LEFT JOIN estado e ON c.id_estado = e.id_estado
                        WHERE d.id_direccion = ?
                    """, (id_dir,))
                    jerarquia = cursor.fetchone()
                    cursor.execute("SELECT COUNT(*) FROM mortalidad WHERE id_direccion = ?", (id_dir,))
                    if cursor.fetchone()[0] == 0:
                        cursor.execute("DELETE FROM direccion WHERE id_direccion = ?", (id_dir,))
                    if jerarquia:
                        id_parr, id_mun, id_ciud, id_est, id_pais = jerarquia
                        if id_parr:
                            cursor.execute("SELECT COUNT(*) FROM direccion WHERE id_parroquia = ?", (id_parr,))
                            if cursor.fetchone()[0] == 0:
                                cursor.execute("DELETE FROM parroquia WHERE id_parroquia = ?", (id_parr,))
                        if id_mun:
                            cursor.execute("SELECT COUNT(*) FROM parroquia WHERE id_municipio = ?", (id_mun,))
                            if cursor.fetchone()[0] == 0:
                                cursor.execute("DELETE FROM municipio WHERE id_municipio = ?", (id_mun,))
                        if id_ciud:
                            cursor.execute("SELECT COUNT(*) FROM municipio WHERE id_ciudad = ?", (id_ciud,))
                            if cursor.fetchone()[0] == 0:
                                cursor.execute("DELETE FROM ciudad WHERE id_ciudad = ?", (id_ciud,))
                        if id_est:
                            cursor.execute("SELECT COUNT(*) FROM ciudad WHERE id_estado = ?", (id_est,))
                            if cursor.fetchone()[0] == 0:
                                cursor.execute("DELETE FROM estado WHERE id_estado = ?", (id_est,))
                        if id_pais:
                            cursor.execute("SELECT COUNT(*) FROM estado WHERE id_pais = ?", (id_pais,))
                            if cursor.fetchone()[0] == 0:
                                cursor.execute("DELETE FROM pais WHERE id_pais = ?", (id_pais,))
            conn.commit()
            st.success(f"{len(ids_a_eliminar)} registros y datos asociados eliminados.", icon=":material/check_circle:")
            st.rerun()
    except sqlite3.Error as e:
        st.error(f"Error al eliminar: {e}", icon=":material/error:")
        
#operaciones de infantil
def operaciones_sql_infantil(accion, datos_registro=None):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if accion == "cargar":
                query = """
                    SELECT m.id_m AS id, m.historia_clinica, m.nombres_apellidos, m.fecha_nacimiento,
                           m.fecha_ingreso, m.hora_ingreso, m.fecha_defuncion, m.hora_defuncion, pp.edad,
                           m.idx_ingreso, m.idx_defuncion, t.nombre_madre,
                           COALESCE(p.nombre || ', ', '') || 
                           COALESCE(e.nombre || ', ', '') || 
                           COALESCE(c.nombre || ', ', '') || 
                           COALESCE(mu.nombre || ', ', '') || 
                           COALESCE(par.nombre || ', ', '') || 
                           d.descripcion AS direccion
                    FROM mortalidad_infantil t
                    JOIN mortalidad m ON t.id_m = m.id_m
                    JOIN persona_paciente pp ON m.id_paciente = pp.id_paciente
                    LEFT JOIN direccion d ON m.id_direccion = d.id_direccion
                    LEFT JOIN parroquia par ON d.id_parroquia = par.id_parroquia
                    LEFT JOIN municipio mu ON par.id_municipio = mu.id_municipio
                    LEFT JOIN ciudad c ON mu.id_ciudad = c.id_ciudad
                    LEFT JOIN estado e ON c.id_estado = e.id_estado
                    LEFT JOIN pais p ON e.id_pais = p.id_pais
                """
                return pd.read_sql_query(query, conn)
            elif accion == "registrar" and datos_registro:
                historia_clinica, nombres_apellidos, nombre_madre, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, edad_junto, idx_ingreso, idx_defuncion, pais_hogar, estado_hogar, municipio_hogar, parroquia_hogar, ciudad_hogar, direccion_exacta, id_doctor, id_administrador = datos_registro
                
                pais_hogar = pais_hogar or "No disponible"
                estado_hogar = estado_hogar or "No disponible"
                ciudad_hogar = ciudad_hogar or "No disponible"
                municipio_hogar = municipio_hogar or "No disponible"
                parroquia_hogar = parroquia_hogar or "No disponible"
                direccion_exacta = direccion_exacta or "No disponible"
                
                cursor.execute("INSERT OR IGNORE INTO pais (nombre) VALUES (?)", (pais_hogar or "Venezuela",))
                cursor.execute("SELECT id_pais FROM pais WHERE nombre = ?", (pais_hogar or "Venezuela",))
                id_pais = cursor.fetchone()[0]
                cursor.execute("INSERT OR IGNORE INTO estado (nombre, id_pais) VALUES (?, ?)", (estado_hogar, id_pais))
                cursor.execute("SELECT id_estado FROM estado WHERE nombre = ? AND id_pais = ?", (estado_hogar, id_pais))
                id_estado = cursor.fetchone()[0]
                cursor.execute("INSERT OR IGNORE INTO ciudad (nombre, id_estado) VALUES (?, ?)", (ciudad_hogar, id_estado))
                cursor.execute("SELECT id_ciudad FROM ciudad WHERE nombre = ? AND id_estado = ?", (ciudad_hogar, id_estado))
                id_ciudad = cursor.fetchone()[0]
                id_municipio = None
                if municipio_hogar and municipio_hogar.strip():
                    cursor.execute("INSERT OR IGNORE INTO municipio (nombre, id_ciudad) VALUES (?, ?)", (municipio_hogar, id_ciudad))
                    cursor.execute("SELECT id_municipio FROM municipio WHERE nombre = ? AND id_ciudad = ?", (municipio_hogar, id_ciudad))
                    id_municipio = cursor.fetchone()[0]
                cursor.execute("INSERT OR IGNORE INTO parroquia (nombre, id_municipio) VALUES (?, ?)", (parroquia_hogar, id_municipio))
                cursor.execute("SELECT id_parroquia FROM parroquia WHERE nombre = ? AND id_municipio = ?", (parroquia_hogar, id_municipio))
                id_parroquia = cursor.fetchone()[0]
                cursor.execute("INSERT OR IGNORE INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (direccion_exacta, id_parroquia))
                cursor.execute("SELECT id_direccion FROM direccion WHERE descripcion = ? AND id_parroquia = ?", (direccion_exacta, id_parroquia))
                id_direccion = cursor.fetchone()[0]
                cursor.execute("INSERT INTO persona_paciente (edad) VALUES (?)", (str(edad_junto),))

                id_paciente = cursor.lastrowid

                if isinstance(fecha_nacimiento, (datetime.date, datetime.datetime, pd.Timestamp)):
                    fecha_formateada_nacimiento = fecha_nacimiento.strftime("%d/%m/%Y")
                else:
                    fecha_formateada_nacimiento = str(fecha_nacimiento)  

                if isinstance(fecha_ingreso, (datetime.date, datetime.datetime, pd.Timestamp)):
                    fecha_formateada_ingreso = fecha_ingreso.strftime("%d/%m/%Y")
                else:
                    fecha_formateada_ingreso = str(fecha_ingreso)   

                if isinstance(fecha_defuncion, (datetime.date, datetime.datetime, pd.Timestamp)):
                    fecha_formateada_defuncion = fecha_defuncion.strftime("%d/%m/%Y")
                else:
                    fecha_formateada_defuncion = str(fecha_defuncion)   

                #fecha_formateada_nacimiento = fecha_nacimiento.strftime("%d/%m/%Y")
                #fecha_formateada_ingreso = fecha_ingreso.strftime("%d/%m/%Y")
                #fecha_formateada_defuncion = fecha_defuncion.strftime("%d/%m/%Y")
                cursor.execute("""
                    INSERT INTO mortalidad (
                        id_paciente, id_direccion, historia_clinica, nombres_apellidos, 
                        fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, 
                        idx_ingreso, idx_defuncion, fecha_registro_formulario
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    id_paciente, id_direccion, historia_clinica, nombres_apellidos, 
                    fecha_formateada_nacimiento, fecha_formateada_ingreso, hora_ingreso, fecha_formateada_defuncion, hora_defuncion, 
                    idx_ingreso, idx_defuncion, datetime.date.today()
                ))
                id_m = cursor.lastrowid
                cursor.execute("INSERT INTO mortalidad_infantil (id_m, nombre_madre) VALUES (?, ?)", (id_m, nombre_madre))
                if id_doctor:
                    cursor.execute("INSERT OR IGNORE INTO doctor_paciente (id_doctor, id_paciente) VALUES (?, ?)", (id_doctor, id_paciente))
                elif id_administrador:
                    cursor.execute("SELECT id_doctor FROM administrador WHERE id_administrador = ?", (id_administrador,))
                    result = cursor.fetchone()
                    if result:
                        id_doctor_admin = result[0]
                        cursor.execute("INSERT OR IGNORE INTO doctor_paciente (id_doctor, id_paciente) VALUES (?, ?)", (id_doctor_admin, id_paciente))
                conn.commit()
                return True
    except sqlite3.IntegrityError:
        st.error("La Historia clinica ya existe.", icon=":material/error:")
        return
    except sqlite3.Error as e:
        st.error(f"Error en operación SQL: {e}", icon=":material/error:")
        return None

def eliminar_registros_infantil(edited_df):
    ids_a_eliminar = edited_df.loc[edited_df[' '], 'id'].tolist()
    if not ids_a_eliminar:
        st.warning("Selecciona al menos un registro.", icon=":material/info:")
        return
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for id_m in ids_a_eliminar:
                cursor.execute("""
                    SELECT m.id_direccion, m.id_paciente
                    FROM mortalidad m
                    WHERE m.id_m = ?
                """, (id_m,))
                datos = cursor.fetchone()
                if not datos:
                    continue
                id_dir, id_paciente = datos
                cursor.execute("DELETE FROM mortalidad_infantil WHERE id_m = ?", (id_m,))
                cursor.execute("DELETE FROM mortalidad WHERE id_m = ?", (id_m,))
                cursor.execute("DELETE FROM doctor_paciente WHERE id_paciente = ?", (id_paciente,))
                cursor.execute("DELETE FROM persona_paciente WHERE id_paciente = ?", (id_paciente,))
                if id_dir:
                    cursor.execute("""
                        SELECT d.id_parroquia, p.id_municipio, m.id_ciudad, c.id_estado, e.id_pais
                        FROM direccion d
                        LEFT JOIN parroquia p ON d.id_parroquia = p.id_parroquia
                        LEFT JOIN municipio m ON p.id_municipio = m.id_municipio
                        LEFT JOIN ciudad c ON m.id_ciudad = c.id_ciudad
                        LEFT JOIN estado e ON c.id_estado = e.id_estado
                        WHERE d.id_direccion = ?
                    """, (id_dir,))
                    jerarquia = cursor.fetchone()
                    cursor.execute("SELECT COUNT(*) FROM mortalidad WHERE id_direccion = ?", (id_dir,))
                    if cursor.fetchone()[0] == 0:
                        cursor.execute("DELETE FROM direccion WHERE id_direccion = ?", (id_dir,))
                    if jerarquia:
                        id_parr, id_mun, id_ciud, id_est, id_pais = jerarquia
                        if id_parr:
                            cursor.execute("SELECT COUNT(*) FROM direccion WHERE id_parroquia = ?", (id_parr,))
                            if cursor.fetchone()[0] == 0:
                                cursor.execute("DELETE FROM parroquia WHERE id_parroquia = ?", (id_parr,))
                        if id_mun:
                            cursor.execute("SELECT COUNT(*) FROM parroquia WHERE id_municipio = ?", (id_mun,))
                            if cursor.fetchone()[0] == 0:
                                cursor.execute("DELETE FROM municipio WHERE id_municipio = ?", (id_mun,))
                        if id_ciud:
                            cursor.execute("SELECT COUNT(*) FROM municipio WHERE id_ciudad = ?", (id_ciud,))
                            if cursor.fetchone()[0] == 0:
                                cursor.execute("DELETE FROM ciudad WHERE id_ciudad = ?", (id_ciud,))
                        if id_est:
                            cursor.execute("SELECT COUNT(*) FROM ciudad WHERE id_estado = ?", (id_est,))
                            if cursor.fetchone()[0] == 0:
                                cursor.execute("DELETE FROM estado WHERE id_estado = ?", (id_est,))
                        if id_pais:
                            cursor.execute("SELECT COUNT(*) FROM estado WHERE id_pais = ?", (id_pais,))
                            if cursor.fetchone()[0] == 0:
                                cursor.execute("DELETE FROM pais WHERE id_pais = ?", (id_pais,))
            conn.commit()
            st.success(f"{len(ids_a_eliminar)} registros y datos asociados eliminados.", icon=":material/check_circle:")
            st.rerun()
    except sqlite3.Error as e:
        st.error(f"Error al eliminar: {e}", icon=":material/error:")
        
#operaciones materna
def operaciones_sql_materna(accion, datos_registro=None):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if accion == "cargar":
                query = """
                    SELECT m.id_m AS id, m.historia_clinica, m.nombres_apellidos, m.fecha_nacimiento,
                           m.fecha_ingreso, m.hora_ingreso, m.fecha_defuncion, m.hora_defuncion, pp.edad,
                           m.idx_ingreso, m.idx_defuncion,
                           COALESCE(p.nombre || ', ', '') || 
                           COALESCE(e.nombre || ', ', '') || 
                           COALESCE(c.nombre || ', ', '') || 
                           COALESCE(mu.nombre || ', ', '') || 
                           COALESCE(par.nombre || ', ', '') || 
                           d.descripcion AS direccion
                    FROM mortalidad_materna t
                    JOIN mortalidad m ON t.id_m = m.id_m
                    JOIN persona_paciente pp ON m.id_paciente = pp.id_paciente
                    LEFT JOIN direccion d ON m.id_direccion = d.id_direccion
                    LEFT JOIN parroquia par ON d.id_parroquia = par.id_parroquia
                    LEFT JOIN municipio mu ON par.id_municipio = mu.id_municipio
                    LEFT JOIN ciudad c ON mu.id_ciudad = c.id_ciudad
                    LEFT JOIN estado e ON c.id_estado = e.id_estado
                    LEFT JOIN pais p ON e.id_pais = p.id_pais
                """
                return pd.read_sql_query(query, conn)
            elif accion == "registrar" and datos_registro:
                historia_clinica, nombres_apellidos, fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, edad_junto, idx_ingreso, idx_defuncion, pais_hogar, estado_hogar, municipio_hogar, parroquia_hogar, ciudad_hogar, direccion_exacta, id_doctor, id_administrador = datos_registro
                
                pais_hogar = pais_hogar or "No disponible"
                estado_hogar = estado_hogar or "No disponible"
                ciudad_hogar = ciudad_hogar or "No disponible"
                municipio_hogar = municipio_hogar or "No disponible"
                parroquia_hogar = parroquia_hogar or "No disponible"
                direccion_exacta = direccion_exacta or "No disponible"
                
                cursor.execute("INSERT OR IGNORE INTO pais (nombre) VALUES (?)", (pais_hogar or "Venezuela",))
                cursor.execute("SELECT id_pais FROM pais WHERE nombre = ?", (pais_hogar or "Venezuela",))
                id_pais = cursor.fetchone()[0]
                cursor.execute("INSERT OR IGNORE INTO estado (nombre, id_pais) VALUES (?, ?)", (estado_hogar, id_pais))
                cursor.execute("SELECT id_estado FROM estado WHERE nombre = ? AND id_pais = ?", (estado_hogar, id_pais))
                id_estado = cursor.fetchone()[0]
                cursor.execute("INSERT OR IGNORE INTO ciudad (nombre, id_estado) VALUES (?, ?)", (ciudad_hogar, id_estado))
                cursor.execute("SELECT id_ciudad FROM ciudad WHERE nombre = ? AND id_estado = ?", (ciudad_hogar, id_estado))
                id_ciudad = cursor.fetchone()[0]
                id_municipio = None
                if municipio_hogar and municipio_hogar.strip():
                    cursor.execute("INSERT OR IGNORE INTO municipio (nombre, id_ciudad) VALUES (?, ?)", (municipio_hogar, id_ciudad))
                    cursor.execute("SELECT id_municipio FROM municipio WHERE nombre = ? AND id_ciudad = ?", (municipio_hogar, id_ciudad))
                    id_municipio = cursor.fetchone()[0]
                cursor.execute("INSERT OR IGNORE INTO parroquia (nombre, id_municipio) VALUES (?, ?)", (parroquia_hogar, id_municipio))
                cursor.execute("SELECT id_parroquia FROM parroquia WHERE nombre = ? AND id_municipio = ?", (parroquia_hogar, id_municipio))
                id_parroquia = cursor.fetchone()[0]
                cursor.execute("INSERT OR IGNORE INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (direccion_exacta, id_parroquia))
                cursor.execute("SELECT id_direccion FROM direccion WHERE descripcion = ? AND id_parroquia = ?", (direccion_exacta, id_parroquia))
                id_direccion = cursor.fetchone()[0]
                cursor.execute("INSERT INTO persona_paciente (edad) VALUES (?)", (str(edad_junto),))
                id_paciente = cursor.lastrowid

                if isinstance(fecha_nacimiento, (datetime.date, datetime.datetime, pd.Timestamp)):
                    fecha_formateada_nacimiento = fecha_nacimiento.strftime("%d/%m/%Y")
                else:
                    fecha_formateada_nacimiento = str(fecha_nacimiento)  

                if isinstance(fecha_ingreso, (datetime.date, datetime.datetime, pd.Timestamp)):
                    fecha_formateada_ingreso = fecha_ingreso.strftime("%d/%m/%Y")
                else:
                    fecha_formateada_ingreso = str(fecha_ingreso)   

                if isinstance(fecha_defuncion, (datetime.date, datetime.datetime, pd.Timestamp)):
                    fecha_formateada_defuncion = fecha_defuncion.strftime("%d/%m/%Y")
                else:
                    fecha_formateada_defuncion = str(fecha_defuncion)   

                #fecha_formateada_nacimiento = fecha_nacimiento.strftime("%d/%m/%Y")
                #fecha_formateada_ingreso = fecha_ingreso.strftime("%d/%m/%Y")
                #fecha_formateada_defuncion = fecha_defuncion.strftime("%d/%m/%Y")
                cursor.execute("""
                    INSERT INTO mortalidad (
                        id_paciente, id_direccion, historia_clinica, nombres_apellidos, 
                        fecha_nacimiento, fecha_ingreso, hora_ingreso, fecha_defuncion, hora_defuncion, 
                        idx_ingreso, idx_defuncion, fecha_registro_formulario
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    id_paciente, id_direccion, historia_clinica, nombres_apellidos, 
                    fecha_formateada_nacimiento, fecha_formateada_ingreso, hora_ingreso, fecha_formateada_defuncion, hora_defuncion, 
                    idx_ingreso, idx_defuncion, datetime.date.today()
                ))
                id_m = cursor.lastrowid
                cursor.execute("INSERT INTO mortalidad_materna (id_m) VALUES (?)", (id_m,))
                if id_doctor:
                    cursor.execute("INSERT OR IGNORE INTO doctor_paciente (id_doctor, id_paciente) VALUES (?, ?)", (id_doctor, id_paciente))
                elif id_administrador:
                    cursor.execute("SELECT id_doctor FROM administrador WHERE id_administrador = ?", (id_administrador,))
                    result = cursor.fetchone()
                    if result:
                        id_doctor_admin = result[0]
                        cursor.execute("INSERT OR IGNORE INTO doctor_paciente (id_doctor, id_paciente) VALUES (?, ?)", (id_doctor_admin, id_paciente))
                conn.commit()
                return True
    except sqlite3.IntegrityError:
        st.error("La Historia clinica ya existe.", icon=":material/error:")
        return
    except sqlite3.Error as e:
        st.error(f"Error en operación SQL: {e}", icon=":material/error:")
        return None

def eliminar_registros_materna(edited_df):
    ids_a_eliminar = edited_df.loc[edited_df[' '], 'id'].tolist()
    if not ids_a_eliminar:
        st.warning("Selecciona al menos un registro.", icon=":material/info:")
        return
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for id_m in ids_a_eliminar:
                cursor.execute("""
                    SELECT m.id_direccion, m.id_paciente
                    FROM mortalidad m
                    WHERE m.id_m = ?
                """, (id_m,))
                datos = cursor.fetchone()
                if not datos:
                    continue
                id_dir, id_paciente = datos
                cursor.execute("DELETE FROM mortalidad_materna WHERE id_m = ?", (id_m,))
                cursor.execute("DELETE FROM mortalidad WHERE id_m = ?", (id_m,))
                cursor.execute("DELETE FROM doctor_paciente WHERE id_paciente = ?", (id_paciente,))
                cursor.execute("DELETE FROM persona_paciente WHERE id_paciente = ?", (id_paciente,))
                if id_dir:
                    cursor.execute("""
                        SELECT d.id_parroquia, p.id_municipio, m.id_ciudad, c.id_estado, e.id_pais
                        FROM direccion d
                        LEFT JOIN parroquia p ON d.id_parroquia = p.id_parroquia
                        LEFT JOIN municipio m ON p.id_municipio = m.id_municipio
                        LEFT JOIN ciudad c ON m.id_ciudad = c.id_ciudad
                        LEFT JOIN estado e ON c.id_estado = e.id_estado
                        WHERE d.id_direccion = ?
                    """, (id_dir,))
                    jerarquia = cursor.fetchone()
                    cursor.execute("SELECT COUNT(*) FROM mortalidad WHERE id_direccion = ?", (id_dir,))
                    if cursor.fetchone()[0] == 0:
                        cursor.execute("DELETE FROM direccion WHERE id_direccion = ?", (id_dir,))
                    if jerarquia:
                        id_parr, id_mun, id_ciud, id_est, id_pais = jerarquia
                        if id_parr:
                            cursor.execute("SELECT COUNT(*) FROM direccion WHERE id_parroquia = ?", (id_parr,))
                            if cursor.fetchone()[0] == 0:
                                cursor.execute("DELETE FROM parroquia WHERE id_parroquia = ?", (id_parr,))
                        if id_mun:
                            cursor.execute("SELECT COUNT(*) FROM parroquia WHERE id_municipio = ?", (id_mun,))
                            if cursor.fetchone()[0] == 0:
                                cursor.execute("DELETE FROM municipio WHERE id_municipio = ?", (id_mun,))
                        if id_ciud:
                            cursor.execute("SELECT COUNT(*) FROM municipio WHERE id_ciudad = ?", (id_ciud,))
                            if cursor.fetchone()[0] == 0:
                                cursor.execute("DELETE FROM ciudad WHERE id_ciudad = ?", (id_ciud,))
                        if id_est:
                            cursor.execute("SELECT COUNT(*) FROM ciudad WHERE id_estado = ?", (id_est,))
                            if cursor.fetchone()[0] == 0:
                                cursor.execute("DELETE FROM estado WHERE id_estado = ?", (id_est,))
                        if id_pais:
                            cursor.execute("SELECT COUNT(*) FROM estado WHERE id_pais = ?", (id_pais,))
                            if cursor.fetchone()[0] == 0:
                                cursor.execute("DELETE FROM pais WHERE id_pais = ?", (id_pais,))
            conn.commit()
            st.success(f"{len(ids_a_eliminar)} registros y datos asociados eliminados.", icon=":material/check_circle:")
            st.rerun()
    except sqlite3.Error as e:
        st.error(f"Error al eliminar: {e}", icon=":material/error:")
        
#operacion mensual infantil

def calcular_tasa_por_ano_infantil(db, year):
    try:
        with sqlite3.connect(db) as conn:
            # Contar registros para el año seleccionado
            query_ano = """
                SELECT COUNT(*) as registros_ano
                FROM mortalidad_mensual_infantil t
                JOIN mortalidad_mensual m ON t.id_mortaM = m.id_mortaM
                WHERE strftime('%Y', m.fecha_registro_formulario) = ?
            """
            df_ano = pd.read_sql_query(query_ano, conn, params=(str(year),))
            registros_ano = df_ano['registros_ano'].iloc[0] if not df_ano.empty else 0
            # Contar total de registros
            query_total = """
                SELECT COUNT(*) as total_registros
                FROM mortalidad_mensual_infantil t
                JOIN mortalidad_mensual m ON t.id_mortaM = m.id_mortaM
            """
            df_total = pd.read_sql_query(query_total, conn)
            total_registros = df_total['total_registros'].iloc[0] if not df_total.empty else 0
            # Calcular tasa como porcentaje
            tasa = (registros_ano / total_registros) * 100 if total_registros > 0 else 0
            return round(tasa, 2)
    except sqlite3.Error:
        return 0

def operaciones_sql_mensual_infantil(accion, datos_registro=None):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            if accion == "cargar":
                query = """
                    SELECT m.id_mortaM AS id, m.causas, m.n_casos, m.tasa, m.total, m.fecha_hora, m.fecha_registro_formulario
                    FROM mortalidad_mensual_infantil t
                    JOIN mortalidad_mensual m ON t.id_mortaM = m.id_mortaM
                """
                return pd.read_sql_query(query, conn)
            elif accion == "registrar" and datos_registro:
                causas, n_casos, id_doctor, id_administrador, rol_usuario = datos_registro
                id_doctor_atendi = None
                if rol_usuario == "Doctor (a)" and id_doctor:
                    id_doctor_atendi = id_doctor
                elif rol_usuario == "Administrador (a)" and id_administrador:
                    cursor.execute("SELECT id_doctor FROM administrador WHERE id_administrador = ?", (id_administrador,))
                    result = cursor.fetchone()
                    if result:
                        id_doctor_atendi = result[0]
                
                today = datetime.date.today()
                mes_actual = today.strftime('%Y-%m')
                
                cursor.execute("""
                    INSERT INTO mortalidad_mensual (
                        id_doctor_atendi, causas, n_casos, total, tasa, fecha_hora, fecha_registro_formulario
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    id_doctor_atendi, causas, n_casos, 0, "0.0%", datetime.datetime.now(), today
                ))
                id_mortaM = cursor.lastrowid
                cursor.execute("""
                    INSERT INTO mortalidad_mensual_infantil (
                        id_mortaM
                    ) VALUES (?)
                """, (id_mortaM,))
                
                cursor.execute("""
                    SELECT SUM(m.n_casos)
                    FROM mortalidad_mensual m
                    JOIN mortalidad_mensual_infantil t ON m.id_mortaM = t.id_mortaM
                    WHERE strftime('%Y-%m', m.fecha_registro_formulario) = ?
                """, (mes_actual,))
                type_total = cursor.fetchone()[0] or 0
                
                if type_total > 0:
                    cursor.execute("""
                        UPDATE mortalidad_mensual
                        SET total = ?
                        WHERE strftime('%Y-%m', fecha_registro_formulario) = ?
                        AND id_mortaM IN (
                            SELECT id_mortaM FROM mortalidad_mensual_infantil
                        )
                    """, (type_total, mes_actual))
                
                if type_total > 0:
                    cursor.execute("""
                        SELECT m.causas, SUM(m.n_casos) as causa_total
                        FROM mortalidad_mensual m
                        JOIN mortalidad_mensual_infantil t ON m.id_mortaM = t.id_mortaM
                        WHERE strftime('%Y-%m', m.fecha_registro_formulario) = ?
                        GROUP BY LOWER(m.causas)
                    """, (mes_actual,))
                    for causas_row, causa_total in cursor.fetchall():
                        tasa = f"{(causa_total / type_total) * 100:.1f}%"
                        cursor.execute("""
                            UPDATE mortalidad_mensual
                            SET tasa = ?
                            WHERE strftime('%Y-%m', fecha_registro_formulario) = ?
                            AND LOWER(causas) = LOWER(?)
                            AND id_mortaM IN (
                                SELECT id_mortaM FROM mortalidad_mensual_infantil
                            )
                        """, (tasa, mes_actual, causas_row))
                
                conn.commit()
                return True
    except sqlite3.Error as e:
        st.error(f"Error en operación SQL: {e}", icon=":material/error:")
        return None


def eliminar_registros_mensual_infantil(edited_df):
    ids_a_eliminar = edited_df.loc[edited_df[' '], 'id'].tolist()
    if not ids_a_eliminar:
        st.warning("Selecciona al menos un registro.", icon=":material/info:")
        return
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for id_mortaM in ids_a_eliminar:
                cursor.execute("DELETE FROM mortalidad_mensual_infantil WHERE id_mortaM = ?", (id_mortaM,))
                cursor.execute("DELETE FROM mortalidad_mensual WHERE id_mortaM = ?", (id_mortaM,))
            conn.commit()
            st.success(f"{len(ids_a_eliminar)} registros eliminados.", icon=":material/check_circle:")
            st.rerun()
    except sqlite3.Error as e:
        st.error(f"Error al eliminar: {e}", icon=":material/error:")
        
#operaciones mensual neonatal

def calcular_tasa_por_ano_neonatal(db, year):
    try:
        with sqlite3.connect(db) as conn:
            # Contar registros para el año seleccionado
            query_ano = """
                SELECT COUNT(*) as registros_ano
                FROM mortalidad_mensual_neonatal t
                JOIN mortalidad_mensual m ON t.id_mortaM = m.id_mortaM
                WHERE strftime('%Y', m.fecha_registro_formulario) = ?
            """
            df_ano = pd.read_sql_query(query_ano, conn, params=(str(year),))
            registros_ano = df_ano['registros_ano'].iloc[0] if not df_ano.empty else 0
            # Contar total de registros
            query_total = """
                SELECT COUNT(*) as total_registros
                FROM mortalidad_mensual_neonatal t
                JOIN mortalidad_mensual m ON t.id_mortaM = m.id_mortaM
            """
            df_total = pd.read_sql_query(query_total, conn)
            total_registros = df_total['total_registros'].iloc[0] if not df_total.empty else 0
            # Calcular tasa como porcentaje
            tasa = (registros_ano / total_registros) * 100 if total_registros > 0 else 0
            return round(tasa, 2)
    except sqlite3.Error:
        return 0

def operaciones_sql_mensual_neonatal(accion, datos_registro=None):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()
            if accion == "cargar":
                query = """
                    SELECT m.id_mortaM AS id, m.causas, m.n_casos, m.tasa, m.total, m.fecha_hora
                    FROM mortalidad_mensual_neonatal t
                    JOIN mortalidad_mensual m ON t.id_mortaM = m.id_mortaM
                """
                return pd.read_sql_query(query, conn)
            elif accion == "registrar" and datos_registro:
                causas, n_casos, id_doctor, id_administrador, rol_usuario = datos_registro
                id_doctor_atendi = None
                if rol_usuario == "Doctor (a)" and id_doctor:
                    id_doctor_atendi = id_doctor
                elif rol_usuario == "Administrador (a)" and id_administrador:
                    cursor.execute("SELECT id_doctor FROM administrador WHERE id_administrador = ?", (id_administrador,))
                    result = cursor.fetchone()
                    if result:
                        id_doctor_atendi = result[0]
                
                today = datetime.date.today()
                mes_actual = today.strftime('%Y-%m')
                
                cursor.execute("""
                    INSERT INTO mortalidad_mensual (
                        id_doctor_atendi, causas, n_casos, total, tasa, fecha_hora, fecha_registro_formulario
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    id_doctor_atendi, causas, n_casos, 0, "0.0%", datetime.datetime.now(), today
                ))
                id_mortaM = cursor.lastrowid
                cursor.execute("""
                    INSERT INTO mortalidad_mensual_neonatal (
                        id_mortaM
                    ) VALUES (?)
                """, (id_mortaM,))
                
                cursor.execute("""
                    SELECT SUM(m.n_casos)
                    FROM mortalidad_mensual m
                    JOIN mortalidad_mensual_neonatal t ON m.id_mortaM = t.id_mortaM
                    WHERE strftime('%Y-%m', m.fecha_registro_formulario) = ?
                """, (mes_actual,))
                type_total = cursor.fetchone()[0] or 0
                
                if type_total > 0:
                    cursor.execute("""
                        UPDATE mortalidad_mensual
                        SET total = ?
                        WHERE strftime('%Y-%m', fecha_registro_formulario) = ?
                        AND id_mortaM IN (
                            SELECT id_mortaM FROM mortalidad_mensual_neonatal
                        )
                    """, (type_total, mes_actual))
                
                if type_total > 0:
                    cursor.execute("""
                        SELECT m.causas, SUM(m.n_casos) as causa_total
                        FROM mortalidad_mensual m
                        JOIN mortalidad_mensual_neonatal t ON m.id_mortaM = t.id_mortaM
                        WHERE strftime('%Y-%m', m.fecha_registro_formulario) = ?
                        GROUP BY LOWER(m.causas)
                   
                    """, (mes_actual,))
                    for causas_row, causa_total in cursor.fetchall():
                        tasa = f"{(causa_total / type_total) * 100:.1f}%"
                        cursor.execute("""
                            UPDATE mortalidad_mensual
                            SET tasa = ?
                            WHERE strftime('%Y-%m', fecha_registro_formulario) = ?
                            AND LOWER(causas) = LOWER(?)
                            AND id_mortaM IN (
                                SELECT id_mortaM FROM mortalidad_mensual_neonatal
                            )
                        """, (tasa, mes_actual, causas_row))
                
                conn.commit()
                return True
    except sqlite3.Error as e:
        st.error(f"Error en operación SQL: {e}", icon=":material/error:")
        return None
    
def eliminar_registros_mensual_neonatal(edited_df):
    ids_a_eliminar = edited_df.loc[edited_df[' '], 'id'].tolist()
    if not ids_a_eliminar:
        st.warning("Selecciona al menos un registro.", icon=":material/info:")
        return
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for id_mortaM in ids_a_eliminar:
                cursor.execute("DELETE FROM mortalidad_mensual_neonatal WHERE id_mortaM = ?", (id_mortaM,))
                cursor.execute("DELETE FROM mortalidad_mensual WHERE id_mortaM = ?", (id_mortaM,))
            conn.commit()
            st.success(f"{len(ids_a_eliminar)} registros eliminados.", icon=":material/check_circle:")
            st.rerun()
    except sqlite3.Error as e:
        st.error(f"Error al eliminar: {e}", icon=":material/error:")

#operacion de mensual general
def calcular_tasa_por_ano(db, year):
    try:
        with sqlite3.connect(db) as conn:

            query_ano = """
                SELECT COUNT(*) as registros_ano
                FROM mortalidad_mensual_general t
                JOIN mortalidad_mensual m ON t.id_mortaM = m.id_mortaM
                WHERE strftime('%Y', m.fecha_registro_formulario) = ?
            """
            df_ano = pd.read_sql_query(query_ano, conn, params=(str(year),))
            registros_ano = df_ano['registros_ano'].iloc[0] if not df_ano.empty else 0

            query_total = """
                SELECT COUNT(*) as total_registros
                FROM mortalidad_mensual_general t
                JOIN mortalidad_mensual m ON t.id_mortaM = m.id_mortaM
            """
            df_total = pd.read_sql_query(query_total, conn)
            total_registros = df_total['total_registros'].iloc[0] if not df_total.empty else 0

            tasa = (registros_ano / total_registros) * 100 if total_registros > 0 else 0
            return round(tasa, 2)
    except sqlite3.Error:
        return 0

def operaciones_sql_mensual_general(accion, datos_registro=None):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()

            if accion == "cargar":
                query = """
                    SELECT m.id_mortaM AS id, m.causas, m.n_casos, m.tasa, m.total, m.fecha_hora
                    FROM mortalidad_mensual m
                    WHERE NOT EXISTS (
                        SELECT 1 FROM mortalidad_mensual_infantil t1 WHERE t1.id_mortaM = m.id_mortaM
                        UNION
                        SELECT 1 FROM mortalidad_mensual_neonatal t2 WHERE t2.id_mortaM = m.id_mortaM
                    )
                """
                return pd.read_sql_query(query, conn)

            elif accion == "registrar" and datos_registro:
                causas, n_casos, id_doctor, id_administrador, rol_usuario = datos_registro
                id_doctor_atendi = None

                if rol_usuario == "Doctor (a)" and id_doctor:
                    id_doctor_atendi = id_doctor
                elif rol_usuario == "Administrador (a)" and id_administrador:
                    cursor.execute("SELECT id_doctor FROM administrador WHERE id_administrador = ?", (id_administrador,))
                    result = cursor.fetchone()
                    if result:
                        id_doctor_atendi = result[0]

                today = datetime.date.today()
                mes_actual = today.strftime('%Y-%m')

                cursor.execute("""
                    INSERT INTO mortalidad_mensual (
                        id_doctor_atendi, causas, n_casos, total, tasa, fecha_hora, fecha_registro_formulario
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    id_doctor_atendi, causas, n_casos, 0, "0.0%", datetime.datetime.now(), today
                ))
                id_mortaM = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO mortalidad_mensual_general (id_mortaM)
                    VALUES (?)
                """, (id_mortaM,))

                cursor.execute("""
                    SELECT SUM(m.n_casos)
                    FROM mortalidad_mensual m
                    WHERE strftime('%Y-%m', m.fecha_registro_formulario) = ?
                    AND NOT EXISTS (
                        SELECT 1 FROM mortalidad_mensual_infantil t1 WHERE t1.id_mortaM = m.id_mortaM
                        UNION
                        SELECT 1 FROM mortalidad_mensual_neonatal t2 WHERE t2.id_mortaM = m.id_mortaM
                    )
                """, (mes_actual,))
                type_total = cursor.fetchone()[0] or 0

                if type_total > 0:
                    cursor.execute("""
                        UPDATE mortalidad_mensual
                        SET total = ?
                        WHERE strftime('%Y-%m', fecha_registro_formulario) = ?
                        AND NOT EXISTS (
                            SELECT 1 FROM mortalidad_mensual_infantil t1 WHERE t1.id_mortaM = mortalidad_mensual.id_mortaM
                            UNION
                            SELECT 1 FROM mortalidad_mensual_neonatal t2 WHERE t2.id_mortaM = mortalidad_mensual.id_mortaM
                        )
                    """, (type_total, mes_actual))

                if type_total > 0:
                    cursor.execute("""
                        SELECT m.causas, SUM(m.n_casos) as causa_total
                        FROM mortalidad_mensual m
                        WHERE strftime('%Y-%m', m.fecha_registro_formulario) = ?
                        AND NOT EXISTS (
                            SELECT 1 FROM mortalidad_mensual_infantil t1 WHERE t1.id_mortaM = m.id_mortaM
                            UNION
                            SELECT 1 FROM mortalidad_mensual_neonatal t2 WHERE t2.id_mortaM = m.id_mortaM
                        )
                        GROUP BY LOWER(m.causas)
                    """, (mes_actual,))
                    for causas_row, causa_total in cursor.fetchall():
                        tasa = f"{(causa_total / type_total) * 100:.1f}%"
                        cursor.execute("""
                            UPDATE mortalidad_mensual
                            SET tasa = ?
                            WHERE strftime('%Y-%m', fecha_registro_formulario) = ?
                            AND LOWER(causas) = LOWER(?)
                            AND NOT EXISTS (
                                SELECT 1 FROM mortalidad_mensual_infantil t1 WHERE t1.id_mortaM = mortalidad_mensual.id_mortaM
                                UNION
                                SELECT 1 FROM mortalidad_mensual_neonatal t2 WHERE t2.id_mortaM = mortalidad_mensual.id_mortaM
                            )
                        """, (tasa, mes_actual, causas_row))

                conn.commit()
                return True

    except sqlite3.Error as e:
        st.error(f"Error en operación SQL: {e}", icon=":material/error:")
        return None

def eliminar_registros_mensual_general(edited_df):
    ids_a_eliminar = edited_df.loc[edited_df[' '], 'id'].tolist()
    if not ids_a_eliminar:
        st.warning("Selecciona al menos un registro.", icon=":material/info:")
        return
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for id_mortaM in ids_a_eliminar:
                cursor.execute("DELETE FROM mortalidad_mensual_general WHERE id_mortaM = ?", (id_mortaM,))
                cursor.execute("DELETE FROM mortalidad_mensual WHERE id_mortaM = ?", (id_mortaM,))
            conn.commit()
            st.success(f"{len(ids_a_eliminar)} registros eliminados.", icon=":material/check_circle:")
            st.rerun()
    except sqlite3.Error as e:
        st.error(f"Error al eliminar: {e}", icon=":material/error:")
        
#Esto hay que ver donde o en que parte mas segura o ver si podemos ocultar esta carpeta 
def crear_superusuario(db='hospital.db'):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        ci = secrets.randbelow(100000000) + 10000000
        nombre_apellido = "Administrador Principal"
        sexo = "M"
        nacimiento = "1980-01-01"
        nacionalidad = "N/A"
        rol = "Administrador (a)"
        nombre_usuario = "EPI.admin"
        contrasena = "EPI@hgdfgr2025"
        correo = f"admin_{secrets.token_hex(4)}@epi.hospital"
        caracteres = string.ascii_letters + string.digits + string.punctuation
        pregunta_seguridad = ''.join(secrets.choice(caracteres) for _ in range(20))
        respuesta_seguridad = ''.join(secrets.choice(caracteres) for _ in range(30))
        pregunta_seguridad_dos = ''.join(secrets.choice(caracteres) for _ in range(20))
        respuesta_seguridad_dos = ''.join(secrets.choice(caracteres) for _ in range(30))
        pregunta_seguridad_tres = ''.join(secrets.choice(caracteres) for _ in range(20))
        respuesta_seguridad_tres = ''.join(secrets.choice(caracteres) for _ in range(30))
        contrasena_hasheada = borro_cassette(contrasena)
        cursor.execute(
            "INSERT OR IGNORE INTO persona (CI, nombre_apellido, sexo, nacimiento, rol, nacionalidad) VALUES (?, ?, ?, ?, ?, ?)",
            (ci, nombre_apellido, sexo, nacimiento, rol, nacionalidad)
        )
        cursor.execute(
            """INSERT INTO usuario (CI, nombre_usuario, contrasena, rol, pregunta_seguridad, 
            respuesta_seguridad, pregunta_seguridad_dos, respuesta_seguridad_dos, pregunta_seguridad_tres, 
            respuesta_seguridad_tres) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (ci, nombre_usuario, contrasena_hasheada, rol, pregunta_seguridad, respuesta_seguridad, 
             pregunta_seguridad_dos, respuesta_seguridad_dos, pregunta_seguridad_tres, respuesta_seguridad_tres)
        )
        id_usuario = cursor.lastrowid
        cursor.execute(
            "INSERT INTO correo (id_usuario, correo) VALUES (?, ?)",
            (id_usuario, correo)
        )
        cursor.execute(
            "INSERT INTO doctor (id_usuario) VALUES (?)",
            (id_usuario,)
        )
        id_doctor = cursor.lastrowid
        cursor.execute(
            "INSERT INTO administrador (id_doctor) VALUES (?)",
            (id_doctor,)
        )
        cursor.execute("SELECT id_departamento FROM departamento WHERE nombre = ?", ('Epidemiología',))
        id_departamento = cursor.fetchone()
        if id_departamento:
            cursor.execute(
                "INSERT INTO doctor_departamento (id_doctor, id_departamento) VALUES (?, ?)",
                (id_doctor, id_departamento[0])
            )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False
    except sqlite3.Error as e:
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()


def mostrar_descripcion_departamento():
    """
    Recupera y muestra la descripción del departamento de Epidemiología 
    usando st.markdown.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT descripcion FROM departamento WHERE nombre = ?", ('Epidemiología',))
            resultado = cursor.fetchone()
            if resultado:
                st.markdown(resultado[0])
            else:
                st.warning("No se encontró la descripción del departamento.", icon=":material/warning:")
    except sqlite3.Error as e:
        st.error(f"Error al cargar la descripción del departamento: {e}", icon=":material/error:")

def mostrar_descripcion_hospital():
    """
    Recupera y muestra la descripción del hospital 
    usando st.markdown.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # Se busca la descripción del hospital principal
            cursor.execute("SELECT descripcion FROM hospital WHERE nombre = ?", ("Hospital General Dr. Felipe Guevara Rojas",))
            resultado = cursor.fetchone()
            if resultado:
                st.markdown(resultado[0])
            else:
                st.warning("No se encontró la descripción del hospital.", icon=":material/warning:")
    except sqlite3.Error as e:
        st.error(f"Error al cargar la descripción del hospital: {e}", icon=":material/error:")
