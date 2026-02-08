import streamlit as st
import sqlite3
import pandas as pd
import time
import os
import datetime
import secrets
import string
from utils.contra import borro_cassette
from pages.historial import registrar_actividad_duradera

DB_PATH = os.getenv("hospital.db", "hospital.db")


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
        cursor.execute("INSERT OR IGNORE INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", 
                      (descripcion_direccion, id_parroquia))
        cursor.execute("SELECT id_direccion FROM direccion WHERE descripcion = ? AND id_parroquia = ?", 
                      (descripcion_direccion, id_parroquia))
        id_direccion = cursor.fetchone()[0]

        descripcion_hospital = (
            "El Hospital General Dr. Felipe Guevara Rojas es un centro de salud público ubicado en El Tigre, "
            "estado Anzoátegui, Venezuela, que pertenece al Distrito Sanitario N° V. Como hospital general, "
            "su función es ofrecer una amplia gama de servicios de salud, que van desde consultas de emergencia "
            "hasta atención especializada en diversas áreas."
        )
        cursor.execute("INSERT INTO hospital (nombre, descripcion, id_direccion) VALUES (?, ?, ?)", 
                      ("Hospital General Dr. Felipe Guevara Rojas", descripcion_hospital, id_direccion))
        cursor.execute("SELECT id_hospital FROM hospital WHERE nombre = ?", 
                      ("Hospital General Dr. Felipe Guevara Rojas",))
        id_hospital = cursor.fetchone()[0]


        descripcion_departamento = (
            "El Departamento de Epidemiología del Hospital General Dr. Felipe Guevara Rojas es una unidad vital "
            "dedicada a la prevención y control de enfermedades infecciosas dentro de la institución. Bajo la "
            "dirección del Dr. Olivier Ladera, el equipo se centra en la vigilancia activa, investigando cualquier "
            "brote potencial para proteger tanto a los pacientes como al personal."
        )

        mision_texto = (
            "Departamento de epidemiología hospitalaria 'Dr. Felipe Guevara Rojas' tiene como misión proveer de información "
            "epidemiológica oportuna y de calidad para la vigilancia, investigación, análisis y evaluación del proceso Salud - Enfermedad, "
            "para orientar las acciones de salud de quienes demandan atención medica gratuita y humanizadas, enmarcado en las políticas de "
            "Salud del Estado Venezolano y de los vínculos interinstitucionales que sustentan en conjunto las acciones administrativas, "
            "asistenciales y docentes para la consecución de los objetivos del servicio como elemento organizacional clave dentro del hospital."
        )

        vision_texto = (
            "Ser un servicio que fortalezca la vigilancia epidemiológica y de los problemas de salud de la población de la zona Sur del "
            "estado Anzoátegui, mediante el análisis de la situación de salud que respondan ante la emergencia epidemiológica y de desastre; "
            "además establecer los lineamientos para la prevención y control de las enfermedades enmarcadas dentro de las políticas de salud "
            "del Estado Venezolano en la cual los usuarios internos y externos se sientan satisfechos por el servicio y producto proporcionado "
            "por el hospital 'Dr. Felipe Guevara Rojas'."
        )

        cursor.execute("""
            INSERT OR IGNORE INTO departamento (nombre, descripcion, mision, vision) 
            VALUES (?, ?, ?, ?)
        """, ('Epidemiología', descripcion_departamento, mision_texto, vision_texto))

        cursor.execute("SELECT id_departamento FROM departamento WHERE nombre = ?", ('Epidemiología',))
        id_departamento = cursor.fetchone()[0]

        cursor.execute("INSERT OR IGNORE INTO departamento_hospital (id_departamento, id_hospital) VALUES (?, ?)", 
                      (id_departamento, id_hospital))

        conn.commit()
        #st.success("Datos iniciales del hospital insertados correctamente.")

    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        st.error(f"Error al insertar datos iniciales: {e}")
    finally:
        if conn:
            conn.close()
#operaciones de natalidad
from pathlib import Path

def operaciones_sql_natalidad(accion, datos_registro=None, db=DB_PATH):
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

                # Desempaquetar datos
                fecha, partos, cesareas, varones, hembras, gemelar, mto, partos_extrahospitalarios, id_doctor, id_administrador, rol_usuario = datos_registro

                # Determinar id_doctor que registra
                id_doctor_atendi = None
                if rol_usuario == "Doctor (a)" and id_doctor:
                    id_doctor_atendi = id_doctor
                elif rol_usuario == "Administrador (a)" and id_administrador:
                    cursor.execute("SELECT id_doctor FROM administrador WHERE id_administrador = ?", (id_administrador,))
                    result = cursor.fetchone()
                    if result:
                        id_doctor_atendi = result[0]


                # === INSERTAR EL REGISTRO ===
                cursor.execute("""
                    INSERT INTO natalidad (
                        fecha, partos, cesareas, varones, hembras, gemelar, 
                        mto, partos_extrahospitalarios, id_doctor, fecha_registro_formulario
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    fecha, partos, cesareas, varones, hembras, gemelar, 
                    mto, partos_extrahospitalarios, id_doctor_atendi, datetime.date.today()
                ))

                # Obtener el ID del nuevo registro
                nuevo_id = cursor.lastrowid
                usuario = st.session_state.get("autenticado_usuario", "Desconocido")
                if nuevo_id:
                    registrar_actividad_duradera("CREADO", "Natalidad", nuevo_id, usuario)

                conn.commit()
                return True

    except sqlite3.Error as e:
        st.error(f"Error en operación SQL: {e}", icon=":material/error:")
        return None

def eliminar_registros_natalidad(edited_df):
    seleccionados = edited_df.loc[edited_df[" "], "id"].tolist()
    if not seleccionados:
        return
    usuario = st.session_state["autenticado_usuario"]

    # === REGISTRAR ELIMINACIONES ANTES DE BORRAR ===
    for id_elim in seleccionados:
        registrar_actividad_duradera("ELIMINADO", "Natalidad", id_elim, usuario)

    st.success(
        f"Se eliminaron {len(seleccionados)} registro(s) de natalidad por {usuario}.",
        icon=":material/check_circle:"
    )
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.executemany("DELETE FROM natalidad WHERE id_nata = ?", [(id_,) for id_ in seleccionados])
            conn.commit()
        st.rerun()
    except sqlite3.Error as e:
        st.error(f"Error al eliminar registros en la base de datos: {e}", icon=":material/error:")

def operaciones_sql_morb_extenso(accion, datos_registro=None, db=DB_PATH):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            if accion == "cargar":
                query = """
                    SELECT 
                        m.id_morb AS id,
                        m.nombres_apellidos,
                        pp.edad,
                        m.diagnostico,
                        m.fecha_registro_formulario,
                        TRIM(
                            REPLACE(
                                (
                                    CASE WHEN p.nombre IS NOT NULL AND p.nombre <> 'No disponible' THEN p.nombre || ', ' ELSE '' END ||
                                    CASE WHEN e.nombre IS NOT NULL AND e.nombre <> 'No disponible' THEN e.nombre || ', ' ELSE '' END ||
                                    CASE WHEN c.nombre IS NOT NULL AND c.nombre <> 'No disponible' THEN c.nombre || ', ' ELSE '' END ||
                                    CASE WHEN mu.nombre IS NOT NULL AND mu.nombre <> 'No disponible' THEN mu.nombre || ', ' ELSE '' END ||
                                    CASE WHEN par.nombre IS NOT NULL AND par.nombre <> 'No disponible' THEN par.nombre || ', ' ELSE '' END ||
                                    CASE WHEN d.descripcion IS NOT NULL AND d.descripcion <> 'No disponible' THEN d.descripcion ELSE '' END
                                ),
                                ', ,', ','
                            )
                        ) AS direccion
                    FROM morbilidad m
                    JOIN persona_paciente pp ON m.id_paciente = pp.id_paciente
                    LEFT JOIN direccion d ON m.id_direccion_hogar = d.id_direccion
                    LEFT JOIN parroquia par ON d.id_parroquia = par.id_parroquia
                    LEFT JOIN municipio mu ON par.id_municipio = mu.id_municipio
                    LEFT JOIN ciudad c ON mu.id_ciudad = c.id_ciudad
                    LEFT JOIN estado e ON c.id_estado = e.id_estado
                    LEFT JOIN pais p ON e.id_pais = p.id_pais
                    ORDER BY m.id_morb DESC
                """
                return pd.read_sql_query(query, conn)

            elif accion == "registrar" and datos_registro:

                rol_usuario = datos_registro["rol_usuario"]
                nombres_apellidos = datos_registro["nombres_apellidos"]
                edad = datos_registro["edad"]
                diagnostico = datos_registro["diagnostico"]

                dir_data = datos_registro["direccion"]

                pais = dir_data.get("pais") or "No disponible"
                estado = dir_data.get("estado") or "No disponible"
                ciudad = dir_data.get("ciudad") or "No disponible"
                municipio = dir_data.get("municipio") or "No disponible"
                parroquia = dir_data.get("parroquia") or "No disponible"
                direccion_exacta = dir_data.get("direccion_exacta") or "No disponible"

                id_doctor = datos_registro.get("id_doctor")
                id_secretaria = datos_registro.get("id_secretaria")
                id_administrador = datos_registro.get("id_administrador")

                # === DIRECCIÓN (MISMO PATRÓN NEONATAL) ===
                cursor.execute("INSERT OR IGNORE INTO pais (nombre) VALUES (?)", (pais,))
                cursor.execute("SELECT id_pais FROM pais WHERE nombre = ?", (pais,))
                id_pais = cursor.fetchone()[0]

                cursor.execute("INSERT OR IGNORE INTO estado (nombre, id_pais) VALUES (?, ?)", (estado, id_pais))
                cursor.execute("SELECT id_estado FROM estado WHERE nombre = ? AND id_pais = ?", (estado, id_pais))
                id_estado = cursor.fetchone()[0]

                cursor.execute("INSERT OR IGNORE INTO ciudad (nombre, id_estado) VALUES (?, ?)", (ciudad, id_estado))
                cursor.execute("SELECT id_ciudad FROM ciudad WHERE nombre = ? AND id_estado = ?", (ciudad, id_estado))
                id_ciudad = cursor.fetchone()[0]

                cursor.execute("INSERT OR IGNORE INTO municipio (nombre, id_ciudad) VALUES (?, ?)", (municipio, id_ciudad))
                cursor.execute("SELECT id_municipio FROM municipio WHERE nombre = ? AND id_ciudad = ?", (municipio, id_ciudad))
                id_municipio = cursor.fetchone()[0]

                cursor.execute("INSERT OR IGNORE INTO parroquia (nombre, id_municipio) VALUES (?, ?)", (parroquia, id_municipio))
                cursor.execute("SELECT id_parroquia FROM parroquia WHERE nombre = ? AND id_municipio = ?", (parroquia, id_municipio))
                id_parroquia = cursor.fetchone()[0]

                cursor.execute("INSERT OR IGNORE INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (direccion_exacta, id_parroquia))
                cursor.execute("SELECT id_direccion FROM direccion WHERE descripcion = ? AND id_parroquia = ?", (direccion_exacta, id_parroquia))
                id_direccion = cursor.fetchone()[0]

                # === PACIENTE ===
                cursor.execute("INSERT INTO persona_paciente (edad) VALUES (?)", (edad,))
                id_paciente = cursor.lastrowid

                cursor.execute("""
                    INSERT INTO morbilidad (
                        id_paciente,
                        id_direccion_hogar,
                        nombres_apellidos,
                        diagnostico,
                        fecha_registro_formulario
                    ) VALUES (?, ?, ?, ?, ?)
                """, (
                    id_paciente,
                    id_direccion,
                    nombres_apellidos,
                    diagnostico,
                    datetime.date.today().strftime("%d/%m/%Y")
                ))

                id_morb = cursor.lastrowid  # ← ID del nuevo registro en morbilidad

                # === RELACIÓN USUARIO ===
                if rol_usuario == "Doctor (a)" and id_doctor:
                    cursor.execute("INSERT OR IGNORE INTO doctor_paciente VALUES (?, ?)", (id_doctor, id_paciente))

                elif rol_usuario == "Secretario (a)" and id_secretaria:
                    cursor.execute("INSERT OR IGNORE INTO secretaria_paciente VALUES (?, ?)", (id_secretaria, id_paciente))

                elif rol_usuario == "Administrador (a)" and id_administrador:
                    cursor.execute("SELECT id_doctor FROM administrador WHERE id_administrador = ?", (id_administrador,))
                    result = cursor.fetchone()
                    if result:
                        cursor.execute("INSERT OR IGNORE INTO doctor_paciente VALUES (?, ?)", (result[0], id_paciente))

                conn.commit()

                # === REGISTRAR LA CREACIÓN DURADERA EN EL LOG ===
                usuario = st.session_state.get("autenticado_usuario", "Desconocido")
                if id_morb:
                    registrar_actividad_duradera("CREADO", "Morbilidad", id_morb, usuario)

                return True

    except sqlite3.IntegrityError:
        st.error("El registro ya existe.", icon=":material/error:")
        return

    except sqlite3.Error as e:
        st.error(f"Error en operación SQL: {e}", icon=":material/error:")
        return None

def eliminar_registros_morb_extenso(edited_df):
    # Asegúrate de que la columna con el ID exista
    id_col = 'id'  # Ajusta al nombre de la columna en tu edited_df
    if id_col not in edited_df.columns:
        st.error(f"No se encuentra la columna de ID '{id_col}' en el dataframe.", icon=":material/error:")
        return

    ids_a_eliminar = edited_df.loc[edited_df[' '], id_col].tolist()
    if not ids_a_eliminar:
        st.warning("Selecciona al menos un registro.", icon=":material/info:")
        return

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("PRAGMA foreign_keys = ON;")
            cursor = conn.cursor()

            for id_morb in ids_a_eliminar:
                # Obtener id_paciente y id_direccion de morbilidad
                cursor.execute("""
                    SELECT id_paciente, id_direccion_hogar
                    FROM morbilidad
                    WHERE id_morb = ?
                """, (id_morb,))
                datos = cursor.fetchone()
                if not datos:
                    continue

                id_paciente, id_dir_hogar = datos

                # Eliminar registro principal
                cursor.execute("DELETE FROM morbilidad WHERE id_morb = ?", (id_morb,))
                
                # Eliminar tablas relacionadas con el paciente
                if id_paciente:
                    cursor.execute("DELETE FROM doctor_paciente WHERE id_paciente = ?", (id_paciente,))
                    cursor.execute("DELETE FROM secretaria_paciente WHERE id_paciente = ?", (id_paciente,))
                    cursor.execute("DELETE FROM persona_paciente WHERE id_paciente = ?", (id_paciente,))

                # Procesar eliminación de la dirección
                if id_dir_hogar:
                    # Verificar si la dirección está en uso por otros registros
                    cursor.execute("""
                        SELECT COUNT(*)
                        FROM morbilidad
                        WHERE id_direccion_hogar = ?
                    """, (id_dir_hogar,))
                    if cursor.fetchone()[0] == 0:
                        # Obtener jerarquía completa
                        cursor.execute("""
                            SELECT d.id_parroquia, p.id_municipio, m.id_ciudad, c.id_estado, e.id_pais
                            FROM direccion d
                            LEFT JOIN parroquia p ON d.id_parroquia = p.id_parroquia
                            LEFT JOIN municipio m ON p.id_municipio = m.id_municipio
                            LEFT JOIN ciudad c ON m.id_ciudad = c.id_ciudad
                            LEFT JOIN estado e ON c.id_estado = e.id_estado
                            WHERE d.id_direccion = ?
                        """, (id_dir_hogar,))
                        jerarquia = cursor.fetchone()

                        # Eliminar dirección
                        cursor.execute("DELETE FROM direccion WHERE id_direccion = ?", (id_dir_hogar,))

                        # Eliminar jerarquía huérfana
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
            usuario = st.session_state["autenticado_usuario"]

            for id_elim in ids_a_eliminar:
                registrar_actividad_duradera("ELIMINADO", "Morbilidad" , id_elim, usuario)
            st.success(f"Se eliminaron{len(ids_a_eliminar)} registro(s).", icon=":material/check_circle:")
            st.rerun()
    except sqlite3.Error as e:
        st.error(f"Error al eliminar: {e}", icon=":material/error:")

        
#operaciones de mortalidad neonatal 

def operaciones_sql_neonatal(accion, datos_registro=None, db=DB_PATH):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if accion == "cargar":
                query = """
                    SELECT m.id_m AS id, m.historia_clinica, m.nombres_apellidos, m.fecha_nacimiento,
                           m.fecha_ingreso, m.hora_ingreso, m.fecha_defuncion, m.hora_defuncion, pp.edad,
                           m.idx_ingreso, m.idx_defuncion, t.nombre_madre, t.hora_nacimiento,
                           t.semanas_gestacion, t.peso, t.talla,
                            TRIM(
                                REPLACE(
                                    (
                                        CASE WHEN p.nombre IS NOT NULL AND p.nombre <> 'No disponible' THEN p.nombre || ', ' ELSE '' END ||
                                        CASE WHEN e.nombre IS NOT NULL AND e.nombre <> 'No disponible' THEN e.nombre || ', ' ELSE '' END ||
                                        CASE WHEN c.nombre IS NOT NULL AND c.nombre <> 'No disponible' THEN c.nombre || ', ' ELSE '' END ||
                                        CASE WHEN mu.nombre IS NOT NULL AND mu.nombre <> 'No disponible' THEN mu.nombre || ', ' ELSE '' END ||
                                        CASE WHEN par.nombre IS NOT NULL AND par.nombre <> 'No disponible' THEN par.nombre || ', ' ELSE '' END ||
                                        CASE WHEN d.descripcion IS NOT NULL AND d.descripcion <> 'No disponible' THEN d.descripcion ELSE '' END
                                    ),
                                    ', ,', ','
                                )
                            ) AS direccion
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
                usuario = st.session_state.get("autenticado_usuario", "Desconocido")
                if id_m:
                    registrar_actividad_duradera("CREADO", "Mortalidad Neonatal", id_m, usuario)

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
            
            usuario = st.session_state["autenticado_usuario"]

            for id_elim in ids_a_eliminar:
                registrar_actividad_duradera("ELIMINADO", "Mortalidad Neonatal" , id_elim, usuario)
            st.success(f"Se eliminaron{len(ids_a_eliminar)} registro(s).", icon=":material/check_circle:")
            st.rerun()
    except sqlite3.Error as e:
        st.error(f"Error al eliminar: {e}", icon=":material/error:")
        
#operaciones de infantil
def operaciones_sql_infantil(accion, datos_registro=None, db=DB_PATH):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if accion == "cargar":
                query = """
                        SELECT m.id_m AS id, m.historia_clinica, m.nombres_apellidos, m.fecha_nacimiento,
                            m.fecha_ingreso, m.hora_ingreso, m.fecha_defuncion, m.hora_defuncion, pp.edad,
                            m.idx_ingreso, m.idx_defuncion, t.nombre_madre,

                            TRIM(
                                    TRIM(
                                        COALESCE(NULLIF(p.nombre, 'No disponible') || ', ', '') ||
                                        COALESCE(NULLIF(e.nombre, 'No disponible') || ', ', '') ||
                                        COALESCE(NULLIF(c.nombre, 'No disponible') || ', ', '') ||
                                        COALESCE(NULLIF(mu.nombre, 'No disponible') || ', ', '') ||
                                        COALESCE(NULLIF(par.nombre, 'No disponible') || ', ', '') ||
                                        COALESCE(NULLIF(d.descripcion, 'No disponible'), '')
                                    )
                            , ', ') AS direccion
                            
                        FROM mortalidad_infantil t
                        JOIN mortalidad m ON t.id_m = m.id_m
                        JOIN persona_paciente pp ON m.id_paciente = pp.id_paciente
                        LEFT JOIN direccion d ON m.id_direccion = d.id_direccion
                        LEFT JOIN parroquia par ON d.id_parroquia = par.id_parroquia
                        LEFT JOIN municipio mu ON par.id_municipio = mu.id_municipio
                        LEFT JOIN ciudad c ON mu.id_ciudad = c.id_ciudad
                        LEFT JOIN estado e ON c.id_estado = e.id_estado
                        LEFT JOIN pais p ON e.id_pais = p.id_pais;

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
                usuario = st.session_state.get("autenticado_usuario", "Desconocido")
                if id_m:
                    registrar_actividad_duradera("CREADO", "Mortalidad Infantil", id_m, usuario)

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
            usuario = st.session_state["autenticado_usuario"]

            for id_elim in ids_a_eliminar:
                registrar_actividad_duradera("ELIMINADO", "Mortalidad Infantil" , id_elim, usuario)
            st.success(f"Se eliminaron{len(ids_a_eliminar)} registro(s).", icon=":material/check_circle:")
            st.rerun()
    except sqlite3.Error as e:
        st.error(f"Error al eliminar: {e}", icon=":material/error:")
        
#operaciones materna
def operaciones_sql_materna(accion, datos_registro=None, db=DB_PATH):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            if accion == "cargar":
                query = """
                    SELECT m.id_m AS id, m.historia_clinica, m.nombres_apellidos, m.fecha_nacimiento,
                        m.fecha_ingreso, m.hora_ingreso, m.fecha_defuncion, m.hora_defuncion, pp.edad,
                        m.idx_ingreso, m.idx_defuncion,

                        TRIM(
                                TRIM(
                                    COALESCE(NULLIF(p.nombre, 'No disponible') || ', ', '') ||
                                    COALESCE(NULLIF(e.nombre, 'No disponible') || ', ', '') ||
                                    COALESCE(NULLIF(c.nombre, 'No disponible') || ', ', '') ||
                                    COALESCE(NULLIF(mu.nombre, 'No disponible') || ', ', '') ||
                                    COALESCE(NULLIF(par.nombre, 'No disponible') || ', ', '') ||
                                    COALESCE(NULLIF(d.descripcion, 'No disponible'), '')
                                ),
                        ', ') AS direccion

                    FROM mortalidad_materna t
                    JOIN mortalidad m ON t.id_m = m.id_m
                    JOIN persona_paciente pp ON m.id_paciente = pp.id_paciente
                    LEFT JOIN direccion d ON m.id_direccion = d.id_direccion
                    LEFT JOIN parroquia par ON d.id_parroquia = par.id_parroquia
                    LEFT JOIN municipio mu ON par.id_municipio = mu.id_municipio
                    LEFT JOIN ciudad c ON mu.id_ciudad = c.id_ciudad
                    LEFT JOIN estado e ON c.id_estado = e.id_estado
                    LEFT JOIN pais p ON e.id_pais = p.id_pais;

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
                usuario = st.session_state.get("autenticado_usuario", "Desconocido")
                if id_m:
                    registrar_actividad_duradera("CREADO", "Mortalidad Materna", id_m, usuario)

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
            usuario = st.session_state["autenticado_usuario"]

            for id_elim in ids_a_eliminar:
                registrar_actividad_duradera("ELIMINADO", "Mortalidad Materna" , id_elim, usuario)
            st.success(f"Se eliminaron{len(ids_a_eliminar)} registro(s).", icon=":material/check_circle:")
            st.rerun()
    except sqlite3.Error as e:
        st.error(f"Error al eliminar: {e}", icon=":material/error:")
        
#Esto hay que ver donde o en que parte mas segura o ver si podemos ocultar esta carpeta 
def crear_superusuario(db='hospital.db'):
    conn = None  # <--- INICIALIZAR ANTES DEL TRY
    try:
        conn = sqlite3.connect(DB_PATH)
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
        if conn:
            conn.rollback()
        return False
    except sqlite3.Error as e:
        if conn:
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
                st.markdown(
                    f"""
                    <div style="text-align: justify; margin: 10px 0;">
                        {resultado[0]}
                    </div>
                    """, unsafe_allow_html=True)
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
                st.markdown(
                    f"""
                    <div style="text-align: justify; margin: 10px 0;">
                        {resultado[0]}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning("No se encontró la descripción del hospital.", icon=":material/warning:")
    except sqlite3.Error as e:
        st.error(f"Error al cargar la descripción del hospital: {e}", icon=":material/error:")

