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


def _ensure_default_jerarquia(cursor):
    pais = "Venezuela"
    estado = "Anzoátegui"
    ciudad = "El Tigre"
    municipio = "Simón Rodríguez"
    parroquia = "Edmundo Barrios"

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

    return id_parroquia


def _overwrite_hierarchy_defaults(cursor, id_parroquia):
    if not id_parroquia:
        return
    pais = "Venezuela"
    estado = "Anzoátegui"
    ciudad = "El Tigre"
    municipio = "Simón Rodríguez"
    parroquia = "Edmundo Barrios"

    try:
        cursor.execute("UPDATE parroquia SET nombre = ? WHERE id_parroquia = ?", (parroquia, id_parroquia))
        cursor.execute("SELECT id_municipio FROM parroquia WHERE id_parroquia = ?", (id_parroquia,))
        row = cursor.fetchone()
        if not row or row[0] is None:
            return
        id_municipio = row[0]

        cursor.execute("UPDATE municipio SET nombre = ? WHERE id_municipio = ?", (municipio, id_municipio))
        cursor.execute("SELECT id_ciudad FROM municipio WHERE id_municipio = ?", (id_municipio,))
        row = cursor.fetchone()
        if not row or row[0] is None:
            return
        id_ciudad = row[0]

        cursor.execute("UPDATE ciudad SET nombre = ? WHERE id_ciudad = ?", (ciudad, id_ciudad))
        cursor.execute("SELECT id_estado FROM ciudad WHERE id_ciudad = ?", (id_ciudad,))
        row = cursor.fetchone()
        if not row or row[0] is None:
            return
        id_estado = row[0]

        cursor.execute("UPDATE estado SET nombre = ? WHERE id_estado = ?", (estado, id_estado))
        cursor.execute("SELECT id_pais FROM estado WHERE id_estado = ?", (id_estado,))
        row = cursor.fetchone()
        if not row or row[0] is None:
            return
        id_pais = row[0]

        cursor.execute("UPDATE pais SET nombre = ? WHERE id_pais = ?", (pais, id_pais))
    except Exception:
        # No interrumpir el guardado si algo falla aquí
        pass

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
            #if not val_diagnostico(row.get("idx_ingreso", ""), "La", "IDX de ingreso"): return
            #if not val_diagnostico(row.get("idx_defuncion", ""), "La", "IDX de defuncion"): return

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

            # Guardar cambios en la dirección si se editó la columna 'direccion'
            direccion_val = (row.get('direccion') or row.get('direccion_hogar') or '')
            if pd.notna(direccion_val) and str(direccion_val).strip() != '':
                direccion_text = str(direccion_val).strip()
                cursor.execute("SELECT id_direccion FROM mortalidad WHERE id_m = ?", (id_m,))
                r = cursor.fetchone()
                id_dir = r[0] if r and r[0] is not None else None
                if id_dir:
                    cursor.execute("SELECT descripcion FROM direccion WHERE id_direccion = ?", (id_dir,))
                    cur = cursor.fetchone()
                    cur_desc = cur[0] if cur and cur[0] is not None else ''
                    if cur_desc != direccion_text:
                        cursor.execute("SELECT COUNT(*) FROM mortalidad WHERE id_direccion = ?", (id_dir,))
                        uso = cursor.fetchone()[0]
                        if uso <= 1:
                            cursor.execute("SELECT id_parroquia FROM direccion WHERE id_direccion = ?", (id_dir,))
                            rpar = cursor.fetchone()
                            if rpar and rpar[0] is not None:
                                _overwrite_hierarchy_defaults(cursor, rpar[0])
                            cursor.execute("UPDATE direccion SET descripcion = ? WHERE id_direccion = ?", (direccion_text, id_dir))
                            if cursor.rowcount > 0:
                                cambio_local = True
                        else:
                            id_parroquia = _ensure_default_jerarquia(cursor)
                            cursor.execute("INSERT INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (direccion_text, id_parroquia))
                            new_id = cursor.lastrowid
                            cursor.execute("UPDATE mortalidad SET id_direccion = ? WHERE id_m = ?", (new_id, id_m))
                            if cursor.rowcount > 0:
                                cambio_local = True
                else:
                    id_parroquia = _ensure_default_jerarquia(cursor)
                    cursor.execute("INSERT INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (direccion_text, id_parroquia))
                    new_id = cursor.lastrowid
                    cursor.execute("UPDATE mortalidad SET id_direccion = ? WHERE id_m = ?", (new_id, id_m))
                    if cursor.rowcount > 0:
                        cambio_local = True

            # Guardar cambios en la dirección si se editó la columna 'direccion'
            direccion_val = (row.get('direccion') or row.get('direccion_hogar') or '')
            if pd.notna(direccion_val) and str(direccion_val).strip() != '':
                direccion_text = str(direccion_val).strip()
                cursor.execute("SELECT id_direccion FROM mortalidad WHERE id_m = ?", (id_m,))
                r = cursor.fetchone()
                id_dir = r[0] if r and r[0] is not None else None
                if id_dir:
                    cursor.execute("SELECT descripcion FROM direccion WHERE id_direccion = ?", (id_dir,))
                    cur = cursor.fetchone()
                    cur_desc = cur[0] if cur and cur[0] is not None else ''
                    if cur_desc != direccion_text:
                        cursor.execute("SELECT COUNT(*) FROM mortalidad WHERE id_direccion = ?", (id_dir,))
                        uso = cursor.fetchone()[0]
                        if uso <= 1:
                            cursor.execute("SELECT id_parroquia FROM direccion WHERE id_direccion = ?", (id_dir,))
                            rpar = cursor.fetchone()
                            if rpar and rpar[0] is not None:
                                _overwrite_hierarchy_defaults(cursor, rpar[0])
                            cursor.execute("UPDATE direccion SET descripcion = ? WHERE id_direccion = ?", (direccion_text, id_dir))
                            if cursor.rowcount > 0:
                                cambio_local = True
                        else:
                            id_parroquia = _ensure_default_jerarquia(cursor)
                            cursor.execute("INSERT INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (direccion_text, id_parroquia))
                            new_id = cursor.lastrowid
                            cursor.execute("UPDATE mortalidad SET id_direccion = ? WHERE id_m = ?", (new_id, id_m))
                            if cursor.rowcount > 0:
                                cambio_local = True
                else:
                    id_parroquia = _ensure_default_jerarquia(cursor)
                    cursor.execute("INSERT INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (direccion_text, id_parroquia))
                    new_id = cursor.lastrowid
                    cursor.execute("UPDATE mortalidad SET id_direccion = ? WHERE id_m = ?", (new_id, id_m))
                    if cursor.rowcount > 0:
                        cambio_local = True

            # Guardar cambios en la dirección si se editó la columna 'direccion'
            direccion_val = (row.get('direccion') or row.get('direccion_hogar') or '')
            if pd.notna(direccion_val) and str(direccion_val).strip() != '':
                direccion_text = str(direccion_val).strip()
                cursor.execute("SELECT id_direccion FROM mortalidad WHERE id_m = ?", (id_m,))
                r = cursor.fetchone()
                id_dir = r[0] if r and r[0] is not None else None
                if id_dir:
                    cursor.execute("SELECT descripcion FROM direccion WHERE id_direccion = ?", (id_dir,))
                    cur = cursor.fetchone()
                    cur_desc = cur[0] if cur and cur[0] is not None else ''
                    if cur_desc != direccion_text:
                        cursor.execute("SELECT COUNT(*) FROM mortalidad WHERE id_direccion = ?", (id_dir,))
                        uso = cursor.fetchone()[0]
                        if uso <= 1:
                            # Forzar la jerarquía a los valores por defecto antes de actualizar
                            cursor.execute("SELECT id_parroquia FROM direccion WHERE id_direccion = ?", (id_dir,))
                            rpar = cursor.fetchone()
                            if rpar and rpar[0] is not None:
                                _overwrite_hierarchy_defaults(cursor, rpar[0])
                            cursor.execute("UPDATE direccion SET descripcion = ? WHERE id_direccion = ?", (direccion_text, id_dir))
                            if cursor.rowcount > 0:
                                cambio_local = True
                        else:
                            id_parroquia = _ensure_default_jerarquia(cursor)
                            cursor.execute("INSERT INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (direccion_text, id_parroquia))
                            new_id = cursor.lastrowid
                            cursor.execute("UPDATE mortalidad SET id_direccion = ? WHERE id_m = ?", (new_id, id_m))
                            if cursor.rowcount > 0:
                                cambio_local = True
                else:
                    id_parroquia = _ensure_default_jerarquia(cursor)
                    cursor.execute("INSERT INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (direccion_text, id_parroquia))
                    new_id = cursor.lastrowid
                    cursor.execute("UPDATE mortalidad SET id_direccion = ? WHERE id_m = ?", (new_id, id_m))
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
            #if not val_diagnostico(row.get("idx_ingreso", ""), "La", "IDX de ingreso"): return
            #if not val_diagnostico(row.get("idx_defuncion", ""), "La", "IDX de defuncion"): return

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
            #if not val_diagnostico(row.get("idx_ingreso", ""), "La", "IDX de ingreso"): return
            #if not val_diagnostico(row.get("idx_defuncion", ""), "La", "IDX de defuncion"): return

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
            # ─────────────────────────────────────────────────────────────
            # 1. Obtener y convertir valores
            # ─────────────────────────────────────────────────────────────
            sexo_gemelar = row.get('sexo_gemelar', '') or ''
            gemelar = int(row.get('gemelar', 0)) if pd.notna(row.get('gemelar', 0)) else 0
            varones = int(row.get('varones', 0)) if pd.notna(row.get('varones', 0)) else 0
            hembras = int(row.get('hembras', 0)) if pd.notna(row.get('hembras', 0)) else 0

            # Ajuste por gemelares
            if sexo_gemelar == "Varones":
                varones += gemelar * 2
            elif sexo_gemelar == "Hembras":
                hembras += gemelar * 2
            elif sexo_gemelar == "Mixto":
                varones += gemelar
                hembras += gemelar

            # Fecha
            fecha_display = row.get('fecha_display', row.get('fecha', ''))
            if not fecha_display:
                st.error("No se pudo determinar la fecha del registro.", icon=":material/error:")
                return  # Detener todo el guardado

            fecha_db = pd.to_datetime(fecha_display, format='%d/%m/%Y', errors='coerce')
            if pd.isna(fecha_db):
                st.error(
                    f"Formato de fecha inválido: '{fecha_display}'. "
                    "Use el formato dd/mm/yyyy.",
                    icon=":material/error:"
                )
                return  # No guardar nada si hay fecha inválida

            fecha_db_str = fecha_db.strftime('%d/%m/%Y')

            # Valores numéricos
            partos = int(row.get("partos", 0)) if pd.notna(row.get("partos", 0)) else 0
            cesareas = int(row.get("cesareas", 0)) if pd.notna(row.get("cesareas", 0)) else 0
            mto = int(row.get("mto", 0)) if pd.notna(row.get("mto", 0)) else 0
            partos_extra = int(row.get("partos_extrahospitalarios", 0)) if pd.notna(row.get("partos_extrahospitalarios", 0)) else 0

            # ─────────────────────────────────────────────────────────────
            # 2. Validación clave: PEH no puede ser mayor que partos
            # ─────────────────────────────────────────────────────────────
            if partos_extra > partos:
                st.error(
                    f"**Error de validación**: Los partos extrahospitalarios ({partos_extra}) "
                    f"no pueden ser mayores que el total de partos ({partos}).",
                    icon=":material/error:"
                )
                return  # ← Importante: detiene todo el proceso de guardado

            # ─────────────────────────────────────────────────────────────
            # 3. Guardar el registro
            # ─────────────────────────────────────────────────────────────
            registro_id = row.get('id')

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
        notificacion_cambios()
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
            #if not val_diagnostico(diagnostico, "El", "diagnóstico"): return

            cursor.execute(
                "UPDATE morbilidad SET nombres_apellidos = ? WHERE id_morb = ?",
                (nombres, id_morb)
            )
            if cursor.rowcount > 0:
                hubo_cambios = True

            # Obtener id_paciente e id_direccion_hogar para actualizar edad y dirección
            cursor.execute("SELECT id_paciente, id_direccion_hogar FROM morbilidad WHERE id_morb = ?", (id_morb,))
            res = cursor.fetchone()
            id_paciente = None
            id_dir_hogar = None
            if res:
                id_paciente = res[0]
                if len(res) > 1:
                    id_dir_hogar = res[1]

            if id_paciente is not None and pd.notna(edad):
                try:
                    edad_val = int(edad)
                except Exception:
                    edad_val = None
                if edad_val is not None:
                    cursor.execute(
                        "UPDATE persona_paciente SET edad = ? WHERE id_paciente = ?",
                        (edad_val, id_paciente)
                    )
                    if cursor.rowcount > 0:
                        hubo_cambios = True

            # Guardar cambios en la dirección si el usuario la editó
            direccion_val = (row.get("direccion") or row.get("direccion_hogar") or "")
            if pd.notna(direccion_val) and str(direccion_val).strip() != "":
                direccion_text = str(direccion_val).strip()
                if id_dir_hogar:
                    cursor.execute("SELECT descripcion FROM direccion WHERE id_direccion = ?", (id_dir_hogar,))
                    cur = cursor.fetchone()
                    cur_desc = cur[0] if cur and cur[0] is not None else ""
                    if cur_desc != direccion_text:
                        # Si la dirección está siendo usada por otros registros, crear nueva entrada
                        cursor.execute("SELECT COUNT(*) FROM morbilidad WHERE id_direccion_hogar = ?", (id_dir_hogar,))
                        uso = cursor.fetchone()[0]
                        if uso <= 1:
                            cursor.execute("SELECT id_parroquia FROM direccion WHERE id_direccion = ?", (id_dir_hogar,))
                            rpar = cursor.fetchone()
                            if rpar and rpar[0] is not None:
                                _overwrite_hierarchy_defaults(cursor, rpar[0])
                            cursor.execute("UPDATE direccion SET descripcion = ? WHERE id_direccion = ?", (direccion_text, id_dir_hogar))
                            if cursor.rowcount > 0:
                                hubo_cambios = True
                        else:
                            id_parroquia = _ensure_default_jerarquia(cursor)
                            cursor.execute("INSERT INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (direccion_text, id_parroquia))
                            new_id = cursor.lastrowid
                            cursor.execute("UPDATE morbilidad SET id_direccion_hogar = ? WHERE id_morb = ?", (new_id, id_morb))
                            if cursor.rowcount > 0:
                                hubo_cambios = True
                else:
                    # No existía dirección previa: insertar nueva y enlazar (usar jerarquía por defecto)
                    id_parroquia = _ensure_default_jerarquia(cursor)
                    cursor.execute("INSERT INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (direccion_text, id_parroquia))
                    new_id = cursor.lastrowid
                    cursor.execute("UPDATE morbilidad SET id_direccion_hogar = ? WHERE id_morb = ?", (new_id, id_morb))
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
