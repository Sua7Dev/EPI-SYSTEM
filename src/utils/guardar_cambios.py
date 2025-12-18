import streamlit as st
import pandas as pd
import sqlite3
import datetime
import os
from utils.visuales import notificacion_cambios
from utils.validaciones import (val_diagnostico, validar_texto, val_texynum, val_notas, val_num_espacios, 
                                val_solo_numeros, validar_cinco_espacios)
DB_PATH = os.getenv("hospital.db", "hospital.db")
from pages.historial import registrar_actividad_duradera

def procesar_guardado_cambios_mortalidad_neonatal(edited_df, DB_PATH=DB_PATH):
    usuario = st.session_state.get("autenticado_usuario", "Desconocido")
    hubo_cambios = False
    ultimo_id = None

    COLUMN_TO_TABLE_MAP = {
        'historia_clinica': 'mortalidad',
        'nombres_apellidos': 'mortalidad',
        'fecha_nacimiento': 'mortalidad',
        'fecha_ingreso': 'mortalidad',
        'hora_ingreso': 'mortalidad',
        'fecha_defuncion': 'mortalidad',
        'hora_defuncion': 'mortalidad',
        'idx_ingreso': 'mortalidad',
        'idx_defuncion': 'mortalidad',
        'nombre_madre': 'mortalidad_neonatal',
        'hora_nacimiento': 'mortalidad_neonatal',
        'semanas_gestacion': 'mortalidad_neonatal',
        'peso': 'mortalidad_neonatal',
        'talla': 'mortalidad_neonatal',
        'edad': 'persona_paciente',
    }

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for _, row in edited_df.iterrows():
            id_m = row.get("id")
            ultimo_id = id_m

            peso_raw = row.get("peso", None)
            talla_raw = row.get("talla", None)

            if pd.isna(peso_raw) or pd.isna(talla_raw):
                st.error("Peso y talla no deben estar vacíos.", icon=":material/error:")
                return

            try:
                peso = float(peso_raw)
                talla = float(talla_raw)
            except:
                st.error("Peso y talla deben ser números válidos.", icon=":material/error:")
                return

            if peso <= 0 or talla <= 0:
                st.error("Peso y talla deben ser mayores a 0.", icon=":material/error:")
                return

            if not val_num_espacios(str(row.get("historia_clinica", "")), "La", "historia clinica"): return
            if not validar_texto(row.get("nombres_apellidos", ""), "Los", "nombres y apellidos"): return
            if not validar_cinco_espacios(row.get("nombres_apellidos", ""), "Los", "nombres y apellidos"): return
            if not validar_texto(row.get("nombre_madre", ""), "El", "nombre de la madre"): return
            if not validar_cinco_espacios(row.get("nombre_madre", ""), "El", "nombre de la madre"): return
            if not val_diagnostico(row.get("idx_ingreso", ""), "La", "IDX de ingreso"): return
            if not val_diagnostico(row.get("idx_defuncion", ""), "La", "IDX de defuncion"): return

            updates = {
                'mortalidad': {'fields': [], 'values': []},
                'mortalidad_neonatal': {'fields': [], 'values': []},
                'persona_paciente': {'fields': [], 'values': []}
            }

            for col, value in row.items():
                if col in COLUMN_TO_TABLE_MAP:
                    if isinstance(value, pd.Timestamp):
                        value = value.strftime('%d/%m/%Y')
                    table = COLUMN_TO_TABLE_MAP[col]
                    updates[table]['fields'].append(f"{col} = ?")
                    updates[table]['values'].append(value)

            cambio_local = False

            if updates['mortalidad']['fields']:
                cursor.execute(
                    f"UPDATE mortalidad SET {', '.join(updates['mortalidad']['fields'])} WHERE id_m = ?",
                    tuple(updates['mortalidad']['values'] + [id_m])
                )
                if cursor.rowcount > 0:
                    cambio_local = True

            if updates['mortalidad_neonatal']['fields']:
                cursor.execute(
                    f"UPDATE mortalidad_neonatal SET {', '.join(updates['mortalidad_neonatal']['fields'])} WHERE id_m = ?",
                    tuple(updates['mortalidad_neonatal']['values'] + [id_m])
                )
                if cursor.rowcount > 0:
                    cambio_local = True

            if updates['persona_paciente']['fields']:
                cursor.execute("SELECT id_paciente FROM mortalidad WHERE id_m = ?", (id_m,))
                res = cursor.fetchone()
                if res:
                    cursor.execute(
                        f"UPDATE persona_paciente SET {', '.join(updates['persona_paciente']['fields'])} WHERE id_paciente = ?",
                        tuple(updates['persona_paciente']['values'] + [res[0]])
                    )
                    if cursor.rowcount > 0:
                        cambio_local = True

            if cambio_local:
                hubo_cambios = True

        conn.commit()

    if hubo_cambios:
        registrar_actividad_duradera("EDITADO", "Mortalidad Neonatal", ultimo_id, usuario)
        notificacion_cambios()
        st.session_state["reset_form_mortalidad"] = True
        #
        st.rerun()
    else:
        st.info("No se detectaron cambios para guardar.", icon=":material/info:")


def procesar_guardado_cambios_mortalidad_infantil(edited_df, DB_PATH=DB_PATH):
    usuario = st.session_state.get("autenticado_usuario", "Desconocido")
    hubo_cambios = False
    ultimo_id = None

    COLUMN_TO_TABLE_MAP = {
        'historia_clinica': 'mortalidad',
        'nombres_apellidos': 'mortalidad',
        'fecha_nacimiento': 'mortalidad',
        'fecha_ingreso': 'mortalidad',
        'hora_ingreso': 'mortalidad',
        'fecha_defuncion': 'mortalidad',
        'hora_defuncion': 'mortalidad',
        'idx_ingreso': 'mortalidad',
        'idx_defuncion': 'mortalidad',
        'nombre_madre': 'mortalidad_infantil',
        'edad': 'persona_paciente',
    }

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for _, row in edited_df.iterrows():
            id_m = row.get("id")
            ultimo_id = id_m

            if not val_num_espacios(str(row.get("historia_clinica", "")), "La", "historia clinica"): return
            if not validar_texto(row.get("nombres_apellidos", ""), "Los", "nombres y apellidos"): return
            if not validar_cinco_espacios(row.get("nombres_apellidos", ""), "Los", "nombres y apellidos"): return
            if not validar_texto(row.get("nombre_madre", ""), "El", "nombre de la madre"): return
            if not validar_cinco_espacios(row.get("nombre_madre", ""), "El", "nombre de la madre"): return
            if not val_diagnostico(row.get("idx_ingreso", ""), "La", "IDX de ingreso"): return
            if not val_diagnostico(row.get("idx_defuncion", ""), "La", "IDX de defuncion"): return

            updates = {
                'mortalidad': {'fields': [], 'values': []},
                'mortalidad_infantil': {'fields': [], 'values': []},
                'persona_paciente': {'fields': [], 'values': []}
            }

            for col, value in row.items():
                if col in COLUMN_TO_TABLE_MAP:
                    if isinstance(value, pd.Timestamp):
                        value = value.strftime('%d/%m/%Y')
                    table = COLUMN_TO_TABLE_MAP[col]
                    updates[table]['fields'].append(f"{col} = ?")
                    updates[table]['values'].append(value)

            cambio_local = False

            if updates['mortalidad']['fields']:
                cursor.execute(
                    f"UPDATE mortalidad SET {', '.join(updates['mortalidad']['fields'])} WHERE id_m = ?",
                    tuple(updates['mortalidad']['values'] + [id_m])
                )
                if cursor.rowcount > 0:
                    cambio_local = True

            if updates['mortalidad_infantil']['fields']:
                cursor.execute(
                    f"UPDATE mortalidad_infantil SET {', '.join(updates['mortalidad_infantil']['fields'])} WHERE id_m = ?",
                    tuple(updates['mortalidad_infantil']['values'] + [id_m])
                )
                if cursor.rowcount > 0:
                    cambio_local = True

            if updates['persona_paciente']['fields']:
                cursor.execute("SELECT id_paciente FROM mortalidad WHERE id_m = ?", (id_m,))
                res = cursor.fetchone()
                if res:
                    cursor.execute(
                        f"UPDATE persona_paciente SET {', '.join(updates['persona_paciente']['fields'])} WHERE id_paciente = ?",
                        tuple(updates['persona_paciente']['values'] + [res[0]])
                    )
                    if cursor.rowcount > 0:
                        cambio_local = True

            if cambio_local:
                hubo_cambios = True

        conn.commit()

    if hubo_cambios:
        registrar_actividad_duradera("EDITADO", "Mortalidad Infantil", ultimo_id, usuario)
        notificacion_cambios()
        st.session_state["reset_form_mortalidad"] = True
        #
        st.rerun()
    else:
        st.info("No se detectaron cambios para guardar.", icon=":material/info:")


def procesar_guardado_cambios_mortalidad_materna(edited_df, DB_PATH=DB_PATH):
    usuario = st.session_state.get("autenticado_usuario", "Desconocido")
    hubo_cambios = False
    ultimo_id = None

    COLUMN_TO_TABLE_MAP = {
        'historia_clinica': 'mortalidad',
        'nombres_apellidos': 'mortalidad',
        'fecha_nacimiento': 'mortalidad',
        'fecha_ingreso': 'mortalidad',
        'hora_ingreso': 'mortalidad',
        'fecha_defuncion': 'mortalidad',
        'hora_defuncion': 'mortalidad',
        'idx_ingreso': 'mortalidad',
        'idx_defuncion': 'mortalidad',
        'edad': 'persona_paciente',
    }

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for _, row in edited_df.iterrows():
            id_m = row.get("id")
            ultimo_id = id_m

            if not val_num_espacios(str(row.get("historia_clinica", "")), "La", "historia clinica"): return
            if not validar_texto(row.get("nombres_apellidos", ""), "Los", "nombres y apellidos"): return
            if not validar_cinco_espacios(row.get("nombres_apellidos", ""), "Los", "nombres y apellidos"): return
            if not val_diagnostico(row.get("idx_ingreso", ""), "La", "IDX de ingreso"): return
            if not val_diagnostico(row.get("idx_defuncion", ""), "La", "IDX de defuncion"): return

            updates = {
                'mortalidad': {'fields': [], 'values': []},
                'persona_paciente': {'fields': [], 'values': []}
            }

            for col, value in row.items():
                if col in COLUMN_TO_TABLE_MAP:
                    if isinstance(value, pd.Timestamp):
                        value = value.strftime('%d/%m/%Y')
                    table = COLUMN_TO_TABLE_MAP[col]
                    updates[table]['fields'].append(f"{col} = ?")
                    updates[table]['values'].append(value)

            cambio_local = False

            if updates['mortalidad']['fields']:
                cursor.execute(
                    f"UPDATE mortalidad SET {', '.join(updates['mortalidad']['fields'])} WHERE id_m = ?",
                    tuple(updates['mortalidad']['values'] + [id_m])
                )
                if cursor.rowcount > 0:
                    cambio_local = True

            if updates['persona_paciente']['fields']:
                cursor.execute("SELECT id_paciente FROM mortalidad WHERE id_m = ?", (id_m,))
                res = cursor.fetchone()
                if res:
                    cursor.execute(
                        f"UPDATE persona_paciente SET {', '.join(updates['persona_paciente']['fields'])} WHERE id_paciente = ?",
                        tuple(updates['persona_paciente']['values'] + [res[0]])
                    )
                    if cursor.rowcount > 0:
                        cambio_local = True

            if cambio_local:
                hubo_cambios = True

        conn.commit()

    if hubo_cambios:
        registrar_actividad_duradera("EDITADO", "Mortalidad Materna", ultimo_id, usuario)
        notificacion_cambios()
        st.session_state["reset_form_mortalidad"] = True
        #
        st.rerun()
    else:
        st.info("No se detectaron cambios para guardar.", icon=":material/info:")


def procesar_guardado_cambios_natalidad(edited_df, DB_PATH=DB_PATH):
    usuario = st.session_state.get("autenticado_usuario", "Desconocido")
    hubo_cambios = False
    ultimo_id = None

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for _, row in edited_df.iterrows():
            sexo_gemelar = row.get('sexo_gemelar', '') or ''
            gemelar = int(row.get('gemelar', 0)) if pd.notna(row.get('gemelar', 0)) else 0
            varones = int(row.get('varones', 0)) if pd.notna(row.get('varones', 0)) else 0
            hembras = int(row.get('hembras', 0)) if pd.notna(row.get('hembras', 0)) else 0

            if sexo_gemelar == "Varones":
                varones += gemelar * 2
            elif sexo_gemelar == "Hembras":
                hembras += gemelar * 2
            elif sexo_gemelar == "Mixto":
                varones += gemelar
                hembras += gemelar

            fecha_display = row.get('fecha_display', '')
            fecha_db = pd.to_datetime(fecha_display, format='%d/%m/%Y', errors='coerce')
            if pd.isna(fecha_db):
                fecha_db = pd.Timestamp('2025-01-01')
            fecha_db_str = fecha_db.strftime('%d/%m/%Y')

            partos = int(row.get("partos", 0)) if pd.notna(row.get("partos", 0)) else 0
            cesareas = int(row.get("cesareas", 0)) if pd.notna(row.get("cesareas", 0)) else 0
            mto = int(row.get("mto", 0)) if pd.notna(row.get("mto", 0)) else 0
            partos_extra = int(row.get("partos_extra", 0)) if pd.notna(row.get("partos_extra", 0)) else 0

            registro_id = row.get('id')
            ultimo_id = registro_id

            if pd.notna(registro_id):
                cursor.execute(
                    """UPDATE natalidad SET
                       fecha = ?, partos = ?, cesareas = ?, varones = ?, hembras = ?,
                       gemelar = ?, mto = ?, partos_extrahospitalarios = ?
                       WHERE id_nata = ?""",
                    (fecha_db_str, partos, cesareas, varones, hembras,
                     gemelar, mto, partos_extra, registro_id)
                )
                if cursor.rowcount > 0:
                    hubo_cambios = True
            else:
                cursor.execute(
                    """INSERT INTO natalidad
                       (fecha, partos, cesareas, varones, hembras, gemelar, mto,
                        partos_extrahospitalarios, id_doctor, fecha_registro_formulario)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (fecha_db_str, partos, cesareas, varones, hembras,
                     gemelar, mto, partos_extra, None, datetime.date.today())
                )
                ultimo_id = cursor.lastrowid
                hubo_cambios = True

        conn.commit()

    if hubo_cambios:
        registrar_actividad_duradera("EDITADO", "Natalidad", ultimo_id, usuario)
        #
        st.rerun()
    else:
        st.info("No se detectaron cambios para guardar.", icon=":material/info:")


def procesar_guardado_morb_extenso(edited_df, DB_PATH=DB_PATH):
    usuario = st.session_state.get("autenticado_usuario", "Desconocido")
    hubo_cambios = False
    ultimo_id = None

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for _, row in edited_df.iterrows():
            id_morb = row.get("id")
            if pd.isna(id_morb):
                continue
            ultimo_id = id_morb

            nombres = (row.get("nombres_apellidos") or "").strip()
            edad = row.get("edad", None)
            diagnostico = (row.get("diagnostico") or "").strip()

            if not validar_texto(nombres, "Los", "Nombres y apellidos"): return
            if not validar_cinco_espacios(nombres, "Los", "nombres y apellidos"): return
            if not val_diagnostico(diagnostico, "El", "diagnóstico"): return

            cursor.execute(
                "UPDATE morbilidad SET nombres_apellidos = ? WHERE id_morb = ?",
                (nombres, id_morb)
            )
            if cursor.rowcount > 0:
                hubo_cambios = True

            cursor.execute("SELECT id_paciente FROM morbilidad WHERE id_morb = ?", (id_morb,))
            res = cursor.fetchone()
            if res and res[0] is not None and pd.notna(edad):
                edad_val = int(edad)
                cursor.execute(
                    "UPDATE persona_paciente SET edad = ? WHERE id_paciente = ?",
                    (edad_val, res[0])
                )
                if cursor.rowcount > 0:
                    hubo_cambios = True

        conn.commit()

    if hubo_cambios:
        registrar_actividad_duradera("EDITADO", "Morbilidad", ultimo_id, usuario)
        notificacion_cambios()
        st.session_state["reset_form_morb_extenso"] = True
        #
        st.rerun()
    else:
        st.info("No se detectaron cambios para guardar.", icon=":material/info:")
