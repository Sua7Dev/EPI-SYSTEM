import streamlit as st
import pandas as pd
import sqlite3
import datetime
import os
from utils.visuales import notificacion_cambios
from utils.validaciones import (validar_texto, val_texynum, val_notas, val_num_espacios, 
                                val_solo_numeros, validar_cinco_espacios)
DB_PATH = os.getenv("hospital.db", "hospital.db")


### Mortalidad ###

def procesar_guardado_cambios_mortalidad_neonatal(edited_df, DB_PATH=DB_PATH):
    """
    Actualiza registros de mortalidad neonatal de forma dinámica según los cambios en el DataFrame.
    """
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
            # variables para los campos
            historia_clinica = str(row.get("historia_clinica", ""))
            nombres_apellidos = row.get("nombres_apellidos", "")
            nombre_madre = row.get("nombre_madre", "")
            idx_ingreso = row.get("idx_ingreso", "")
            idx_defuncion = row.get("idx_ingreso", "")
            # Validaciones (adaptadas de mortalidad.py)
            #if not val_num_espacios(historia_clinica, "La", "Historia clínica"):
            #    return
            #if not validar_texto(nombres_apellidos, "Los", "Nombres y apellidos"):
            #    return
            #if not validar_texto(nombre_madre, "Los", "Nombre de la madre"):
            #    return
            #if float(row.get("peso", 0)) <= 0 or float(row.get("talla", 0)) <= 0:
            #    st.error("Peso y talla deben ser mayores a 0 para Muerte Neonatal", icon=":material/error:")
            #    return
            peso_raw = row.get("peso", None)
            talla_raw = row.get("talla", None)

            # Detectar None o NaN (pandas/numpy)
            if pd.isna(peso_raw) or pd.isna(talla_raw) or peso_raw is None or talla_raw is None:
                st.error("Peso y talla no deben estar vacíos.", icon=":material/error:")
                return

            # Intentar convertir a float con manejo de errores
            try:
                peso = float(peso_raw)
                talla = float(talla_raw)
            except (TypeError, ValueError):
                st.error("Peso y talla deben ser números válidos.", icon=":material/error:")
                return

            # nuevas
            if not val_num_espacios(historia_clinica, "La", "historia clinica"):
                return
            elif not validar_texto(nombres_apellidos, "Los", "nombres y apellidos"):
                return
            elif not validar_cinco_espacios(nombres_apellidos, "Los", "nombres y apellidos"):
                return
            elif not validar_texto(nombre_madre, "El", "nombre de la madre"):
                return
            elif not validar_cinco_espacios(nombre_madre, "El", "nombre de la madre"):
                return
            elif not val_texynum(idx_ingreso, "La", "IDX de ingreso"):
                return
            elif not val_texynum(idx_defuncion, "La", "IDX de defuncion"):
                return   
            # Validar valores positivos
            if peso <= 0 or talla <= 0:
                st.error("Peso y talla deben ser mayores a 0.", icon=":material/error:")
                return

            # Actualización dinámica
            updates = {
                'mortalidad': {'fields': [], 'values': []},
                'mortalidad_neonatal': {'fields': [], 'values': []},
                'persona_paciente': {'fields': [], 'values': []}
            }
            for col, value in row.items():
                if col in COLUMN_TO_TABLE_MAP:
                    # Convertir Timestamps a string para compatibilidad con SQLite
                    if isinstance(value, pd.Timestamp):
                        value = value.strftime('%d/%m/%Y')

                    table = COLUMN_TO_TABLE_MAP[col]
                    updates[table]['fields'].append(f"{col} = ?")
                    updates[table]['values'].append(value)
            if updates['mortalidad']['fields']:
                sql = f"UPDATE mortalidad SET {', '.join(updates['mortalidad']['fields'])} WHERE id_m = ?"
                values = updates['mortalidad']['values'] + [id_m]
                cursor.execute(sql, tuple(values))
            if updates['mortalidad_neonatal']['fields']:
                sql = f"UPDATE mortalidad_neonatal SET {', '.join(updates['mortalidad_neonatal']['fields'])} WHERE id_m = ?"
                values = updates['mortalidad_neonatal']['values'] + [id_m]
                cursor.execute(sql, tuple(values))
            if updates['persona_paciente']['fields']:
                cursor.execute("SELECT id_paciente FROM mortalidad WHERE id_m = ?", (id_m,))
                result = cursor.fetchone()
                if result:
                    id_paciente = result[0]
                    sql = f"UPDATE persona_paciente SET {', '.join(updates['persona_paciente']['fields'])} WHERE id_paciente = ?"
                    values = updates['persona_paciente']['values'] + [id_paciente]
                    cursor.execute(sql, tuple(values))
        conn.commit()
        notificacion_cambios()
        st.session_state["reset_form_mortalidad"] = True
        st.rerun()

def procesar_guardado_cambios_mortalidad_infantil(edited_df, DB_PATH=DB_PATH):
    """
    Actualiza registros de mortalidad infantil de forma dinámica según los cambios en el DataFrame.
    """
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
            # variables para los campos
            historia_clinica = str(row.get("historia_clinica", ""))
            nombres_apellidos = row.get("nombres_apellidos", "")
            nombre_madre = row.get("nombre_madre", "")
            # Validaciones (adaptadas de mortalidad.py)
            #if not val_num_espacios(historia_clinica, "La", "Historia clínica"):
            #    return
            #if not validar_texto(nombres_apellidos, "Los", "Nombres y apellidos"):
            #    return
            #if not validar_texto(nombre_madre, "Los", "Nombre de la madre"):
            #    return
            idx_ingreso = row.get("idx_ingreso", "")
            idx_defuncion = row.get("idx_ingreso", "")

            # nuevas
            if not val_num_espacios(historia_clinica, "La", "historia clinica"):
                return
            elif not validar_texto(nombres_apellidos, "Los", "nombres y apellidos"):
                return
            elif not validar_cinco_espacios(nombres_apellidos, "Los", "nombres y apellidos"):
                return
            elif not validar_texto(nombre_madre, "El", "nombre de la madre"):
                return
            elif not validar_cinco_espacios(nombre_madre, "El", "nombre de la madre"):
                return
            elif not val_texynum(idx_ingreso, "La", "IDX de ingreso"):
                return
            elif not val_texynum(idx_defuncion, "La", "IDX de defuncion"):
                return   
            
            # Actualización dinámica
            updates = {
                'mortalidad': {'fields': [], 'values': []},
                'mortalidad_infantil': {'fields': [], 'values': []},
                'persona_paciente': {'fields': [], 'values': []}
            }
            for col, value in row.items():
                if col in COLUMN_TO_TABLE_MAP:
                    # Convertir Timestamps a string para compatibilidad con SQLite
                    if isinstance(value, pd.Timestamp):
                        value = value.strftime('%d/%m/%Y')
                    table = COLUMN_TO_TABLE_MAP[col]
                    updates[table]['fields'].append(f"{col} = ?")
                    updates[table]['values'].append(value)
            if updates['mortalidad']['fields']:
                sql = f"UPDATE mortalidad SET {', '.join(updates['mortalidad']['fields'])} WHERE id_m = ?"
                values = updates['mortalidad']['values'] + [id_m]
                cursor.execute(sql, tuple(values))
            if updates['mortalidad_infantil']['fields']:
                sql = f"UPDATE mortalidad_infantil SET {', '.join(updates['mortalidad_infantil']['fields'])} WHERE id_m = ?"
                values = updates['mortalidad_infantil']['values'] + [id_m]
                cursor.execute(sql, tuple(values))
            if updates['persona_paciente']['fields']:
                cursor.execute("SELECT id_paciente FROM mortalidad WHERE id_m = ?", (id_m,))
                result = cursor.fetchone()
                if result:
                    id_paciente = result[0]
                    sql = f"UPDATE persona_paciente SET {', '.join(updates['persona_paciente']['fields'])} WHERE id_paciente = ?"
                    values = updates['persona_paciente']['values'] + [id_paciente]
                    cursor.execute(sql, tuple(values))
        conn.commit()
        notificacion_cambios()
        st.session_state["reset_form_mortalidad"] = True
        st.rerun()

def procesar_guardado_cambios_mortalidad_materna(edited_df, DB_PATH=DB_PATH):
    """
    Actualiza registros de mortalidad materna de forma dinámica según los cambios en el DataFrame.
    Procesa todas las filas, aunque alguna falle en validación.
    """
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
        errores = 0
        for _, row in edited_df.iterrows():
            id_m = row.get("id")
            historia_clinica = str(row.get("historia_clinica", ""))
            nombres_apellidos = row.get("nombres_apellidos", "")
            idx_ingreso = row.get("idx_ingreso", "")
            idx_defuncion = row.get("idx_ingreso", "")

            # Validaciones (adaptadas de mortalidad.py)
            # nuevas
            if not val_num_espacios(historia_clinica, "La", "historia clinica"):
                return
            elif not validar_texto(nombres_apellidos, "Los", "nombres y apellidos"):
                return
            elif not validar_cinco_espacios(nombres_apellidos, "Los", "nombres y apellidos"):
                return
            #elif not validar_texto(nombre_madre, "El", "nombre de la madre"):
            #    return
            #elif not validar_cinco_espacios(nombre_madre, "El", "nombre de la madre"):
                return
            elif not val_texynum(idx_ingreso, "La", "IDX de ingreso"):
                return
            elif not val_texynum(idx_defuncion, "La", "IDX de defuncion"):
                return  
            # Actualización dinámica
            updates = {
                'mortalidad': {'fields': [], 'values': []},
                'persona_paciente': {'fields': [], 'values': []}
            }
            for col, value in row.items():
                if col in COLUMN_TO_TABLE_MAP:
                    # Convertir Timestamps a string para compatibilidad con SQLite
                    if isinstance(value, pd.Timestamp):
                        value = value.strftime('%d/%m/%Y')
                    table = COLUMN_TO_TABLE_MAP[col]
                    updates[table]['fields'].append(f"{col} = ?")
                    updates[table]['values'].append(value)
            if updates['mortalidad']['fields']:
                sql = f"UPDATE mortalidad SET {', '.join(updates['mortalidad']['fields'])} WHERE id_m = ?"
                values = updates['mortalidad']['values'] + [id_m]
                cursor.execute(sql, tuple(values))
            if updates['persona_paciente']['fields']:
                cursor.execute("SELECT id_paciente FROM mortalidad WHERE id_m = ?", (id_m,))
                result = cursor.fetchone()
                if result:
                    id_paciente = result[0]
                    sql = f"UPDATE persona_paciente SET {', '.join(updates['persona_paciente']['fields'])} WHERE id_paciente = ?"
                    values = updates['persona_paciente']['values'] + [id_paciente]
                    cursor.execute(sql, tuple(values))
        conn.commit()
        notificacion_cambios()
        st.session_state["reset_form_mortalidad"] = True
        st.rerun()

def procesar_guardado_cambios_mensual_neonatal(edited_df, DB_PATH=DB_PATH):
    """
    Actualiza registros de mortalidad mensual neonatal de forma dinámica según los cambios en el DataFrame.
    """
    COLUMN_TO_TABLE_MAP = {
        'causas': 'mortalidad_mensual',
        'n_casos': 'mortalidad_mensual',
        'tasa': 'mortalidad_mensual',
        'total': 'mortalidad_mensual',
        'fecha_hora': 'mortalidad_mensual',
        'fecha_registro_formulario': 'mortalidad_mensual',
    }
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for _, row in edited_df.iterrows():
            id_mortaM = row.get("id")
            causas = row.get("causas", "")
            n_casos = int(row.get("n_casos", 0)) if pd.notna(row.get("n_casos", 0)) else 0
            # Validaciones (adaptadas de mortalidad.py)
            if not val_notas(causas, "La", "causa"):
                return
            if n_casos <= 0:
                st.error("El número de casos debe ser mayor que cero.", icon=":material/error:")
                return
            # Actualización dinámica
            updates = {
                'mortalidad_mensual': {'fields': [], 'values': []}
            }
            for col, value in row.items():
                if col in COLUMN_TO_TABLE_MAP:
                    # Convertir fechas a string si son Timestamp
                    if isinstance(value, pd.Timestamp):
                        value = value.strftime('%d/%m/%Y')
                    table = COLUMN_TO_TABLE_MAP[col]
                    updates[table]['fields'].append(f"{col} = ?")
                    updates[table]['values'].append(value)
            if updates['mortalidad_mensual']['fields']:
                sql = f"UPDATE mortalidad_mensual SET {', '.join(updates['mortalidad_mensual']['fields'])} WHERE id_mortaM = ?"
                values = updates['mortalidad_mensual']['values'] + [id_mortaM]
                cursor.execute(sql, tuple(values))
        conn.commit()
        notificacion_cambios()
        st.session_state["reset_form_mensual_neonatal"] = True
        st.rerun()

def procesar_guardado_cambios_mensual_infantil(edited_df, DB_PATH=DB_PATH):
    """
    Actualiza registros de mortalidad mensual infantil de forma dinámica según los cambios en el DataFrame.
    """
    COLUMN_TO_TABLE_MAP = {
        'causas': 'mortalidad_mensual',
        'n_casos': 'mortalidad_mensual',
        'tasa': 'mortalidad_mensual',
        'total': 'mortalidad_mensual',
        'fecha_hora': 'mortalidad_mensual',
        'fecha_registro_formulario': 'mortalidad_mensual',
    }
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for _, row in edited_df.iterrows():
            id_mortaM = row.get("id")
            causas = row.get("causas", "")
            n_casos = int(row.get("n_casos", 0)) if pd.notna(row.get("n_casos", 0)) else 0
            # Validaciones (adaptadas de mortalidad.py)
            if not val_notas(causas, "La", "causa"):
                return
            if n_casos <= 0:
                st.error("El número de casos debe ser mayor que cero.", icon=":material/error:")
                return
            # Actualización dinámica
            updates = {
                'mortalidad_mensual': {'fields': [], 'values': []}
            }
            for col, value in row.items():
                if col in COLUMN_TO_TABLE_MAP:
                    # Convertir fechas a string si son Timestamp
                    if isinstance(value, pd.Timestamp):
                        value = value.strftime('%d/%m/%Y')
                    table = COLUMN_TO_TABLE_MAP[col]
                    updates[table]['fields'].append(f"{col} = ?")
                    updates[table]['values'].append(value)
            if updates['mortalidad_mensual']['fields']:
                sql = f"UPDATE mortalidad_mensual SET {', '.join(updates['mortalidad_mensual']['fields'])} WHERE id_mortaM = ?"
                values = updates['mortalidad_mensual']['values'] + [id_mortaM]
                cursor.execute(sql, tuple(values))
        conn.commit()
        notificacion_cambios()
        st.session_state["reset_form_mensual_infantil"] = True
        st.rerun()

def procesar_guardado_cambios_mensual_general(edited_df, DB_PATH=DB_PATH):
    """
    Actualiza registros de mortalidad mensual general de forma dinámica según los cambios en el DataFrame.
    """
    COLUMN_TO_TABLE_MAP = {
        'causas': 'mortalidad_mensual',
        'n_casos': 'mortalidad_mensual',
        'tasa': 'mortalidad_mensual',
        'total': 'mortalidad_mensual',
        'fecha_hora': 'mortalidad_mensual',
        'fecha_registro_formulario': 'mortalidad_mensual',
    }
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for _, row in edited_df.iterrows():
            id_mortaM = row.get("id")
            causas = row.get("causas", "")
            n_casos = int(row.get("n_casos", 0)) if pd.notna(row.get("n_casos", 0)) else 0
            # Validaciones (adaptadas de mortalidad.py)
            if not val_notas(causas, "La", "causa"):
                return
            if n_casos <= 0:
                st.error("El número de casos debe ser mayor que cero.", icon=":material/error:")
                return
            # Actualización dinámica
            updates = {
                'mortalidad_mensual': {'fields': [], 'values': []}
            }
            for col, value in row.items():
                if col in COLUMN_TO_TABLE_MAP:
                    # Convertir fechas a string si son Timestamp
                    if isinstance(value, pd.Timestamp):
                        value = value.strftime('%d/%m/%Y')
                    table = COLUMN_TO_TABLE_MAP[col]
                    updates[table]['fields'].append(f"{col} = ?")
                    updates[table]['values'].append(value)
            if updates['mortalidad_mensual']['fields']:
                sql = f"UPDATE mortalidad_mensual SET {', '.join(updates['mortalidad_mensual']['fields'])} WHERE id_mortaM = ?"
                values = updates['mortalidad_mensual']['values'] + [id_mortaM]
                cursor.execute(sql, tuple(values))
        conn.commit()
        notificacion_cambios()
        st.session_state["reset_form_mensual_general"] = True
        st.rerun()

### Natalidad ###

def procesar_guardado_cambios_natalidad(edited_df, DB_PATH=DB_PATH):
    # Guardar cambios (solo para roles no secretarios)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for _, row in edited_df.iterrows():
            # Asegurar claves y tipos por defecto para evitar KeyError
            sexo_gemelar = row.get('sexo_gemelar', '') or ''
            gemelar = int(row.get('gemelar', 0)) if pd.notna(row.get('gemelar', 0)) else 0
            varones = int(row.get('varones', 0)) if pd.notna(row.get('varones', 0)) else 0
            hembras = int(row.get('hembras', 0)) if pd.notna(row.get('hembras', 0)) else 0

            # Ajustar varones y hembras según el valor de gemelar y sexo_gemelar
            if sexo_gemelar == "Varones":
                varones = varones + (gemelar * 2)  # Cada gemelar implica dos varones
            elif sexo_gemelar == "Hembras":
                hembras = hembras + (gemelar * 2)  # Cada gemelar implica dos hembras
            elif sexo_gemelar == "Mixto":
                varones = varones + gemelar  # La mitad son varones
                hembras = hembras + gemelar  # La mitad son hembras

            # Convertir fecha_display a datetime para la base de datos
            fecha_display = row.get('fecha_display', '')
            fecha_db = pd.to_datetime(fecha_display, format='%d/%m/%Y', errors='coerce')
            if pd.isna(fecha_db):
                fecha_db = pd.Timestamp('2025-01-01')
            # Convertir fecha_db a string para la base de datos
            fecha_db_str = fecha_db.strftime('%d/%m/%Y')

            # Preparar otros campos con valores por defecto
            partos = int(row.get("partos", 0)) if pd.notna(row.get("partos", 0)) else 0
            cesareas = int(row.get("cesareas", 0)) if pd.notna(row.get("cesareas", 0)) else 0
            mto = int(row.get("mto", 0)) if pd.notna(row.get("mto", 0)) else 0
            partos_extra = int(row.get("partos_extra", 0)) if pd.notna(row.get("partos_extra", 0)) else 0

            # Si el registro tiene un ID, actualizarlo en la tabla natalidad (id en SQL: id_nata)
            if pd.notna(row.get('id')):
                cursor.execute("""
                    UPDATE natalidad SET
                        fecha = ?, partos = ?, cesareas = ?, varones = ?, hembras = ?,
                        gemelar = ?, mto = ?, partos_extrahospitalarios = ?
                    WHERE id_nata = ?
                """, (
                    fecha_db_str, partos, cesareas, varones, hembras,
                    gemelar, mto, partos_extra, row['id']
                ))
            else:
                cursor.execute("""
                    INSERT INTO natalidad 
                    (fecha, partos, cesareas, varones, hembras, gemelar, mto, partos_extrahospitalarios, id_doctor, fecha_registro_formulario)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    fecha_db_str, partos, cesareas, varones, hembras, gemelar,
                    mto, partos_extra, None, datetime.date.today()
                ))
        conn.commit()
        notificacion_cambios()
        st.rerun()



### Morbilidad ###

# --- Funciones de Guardado Refactorizadas ---

def procesar_guardado_morb_extenso(edited_df, DB_PATH=DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            for _, row in edited_df.iterrows():
                id_morb = row.get("id")
                if pd.isna(id_morb):
                    continue
                nombres = (row.get("nombres_apellidos") or "").strip()
                edad = row.get("edad", None)
                diagnostico = (row.get("diagnostico") or "").strip()

                if not validar_texto(nombres, "Los", "Nombres y apellidos"):
                    return
                if not validar_cinco_espacios(nombres, "Los", "nombres y apellidos"): return
                if not val_texynum(diagnostico, "El", "diagnóstico"): return

                # actualizar nombres en morbilidad
                cursor.execute(
                    "UPDATE morbilidad SET nombres_apellidos = ? WHERE id_morb = ?",
                    (nombres, id_morb)
                )

                # actualizar edad en persona_paciente si existe id_paciente relacionado
                cursor.execute("SELECT id_paciente FROM morbilidad WHERE id_morb = ?", (id_morb,))
                res = cursor.fetchone()
                if res and res[0] is not None and pd.notna(edad):
                    try:
                        edad_val = int(edad)
                        cursor.execute("UPDATE persona_paciente SET edad = ? WHERE id_paciente = ?", (edad_val, res[0]))
                    except Exception:
                        st.error("Edad inválida" + str(id_morb), icon=":material/error:")
                        return

            conn.commit()
            notificacion_cambios()
            st.session_state["reset_form_morb_extenso"] = True
            st.rerun()
            return 
    
def procesar_guardado_morb_simplificado(edited_df, DB_PATH=DB_PATH):
    """
    Procesa el guardado (INSERT o UPDATE) de registros para Morbilidad Simplificada.
    Construye sentencias UPDATE dinámicas para las tablas afectadas.
    """
    COLUMN_TO_TABLE_MAP = {
        'diagnostico': 'morbilidad',
        'sexo': 'morbilidad',
        'edad': 'persona_paciente',
    }

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for _, row in edited_df.iterrows():
            # El id principal para morb_simplifica es id_morbsim, pero para UPDATE necesitamos id_morb
            id_morbsim = row.get("id") if pd.notna(row.get("id")) else row.get("id_morbsim")
            id_morb = None
            if pd.notna(id_morbsim):
                cursor.execute("SELECT id_morb FROM morb_simplifica WHERE id_morbsim = ?", (id_morbsim,))
                result = cursor.fetchone()
                if result:
                    id_morb = result[0]
            else:
                id_morb = row.get("id_morb")

            # --- Validaciones de datos de entrada ---
            diagnostico = row.get("diagnostico", "")
            if not diagnostico:
                st.error("Por favor completa el diagnóstico", icon=":material/error:")
                return
            elif not val_notas(diagnostico, "El", "diagnóstico"):
                return

            # --- Lógica de UPDATE ---
            if pd.notna(id_morb):
                updates = {
                    'morbilidad': {'fields': [], 'values': []},
                    'persona_paciente': {'fields': [], 'values': []}
                }
                for col, value in row.items():
                    if col in COLUMN_TO_TABLE_MAP:
                        table = COLUMN_TO_TABLE_MAP[col]
                        updates[table]['fields'].append(f"{col} = ?")
                        updates[table]['values'].append(value)
                if updates['morbilidad']['fields']:
                    sql = f"UPDATE morbilidad SET {', '.join(updates['morbilidad']['fields'])} WHERE id_morb = ?"
                    values = updates['morbilidad']['values'] + [id_morb]
                    cursor.execute(sql, tuple(values))
                if updates['persona_paciente']['fields']:
                    cursor.execute("SELECT id_paciente FROM morbilidad WHERE id_morb = ?", (id_morb,))
                    result = cursor.fetchone()
                    if result:
                        id_paciente = result[0]
                        sql = f"UPDATE persona_paciente SET {', '.join(updates['persona_paciente']['fields'])} WHERE id_paciente = ?"
                        values = updates['persona_paciente']['values'] + [id_paciente]
                        cursor.execute(sql, tuple(values))

            # --- Lógica de INSERT ---
            else:
                cursor.execute("INSERT INTO persona_paciente (edad) VALUES (?)", (row.get("edad"),))
                id_paciente = cursor.lastrowid
                cursor.execute("""
                    INSERT INTO morbilidad (id_paciente, sexo, diagnostico, fecha_registro_formulario)
                    VALUES (?, ?, ?, ?)
                """, (id_paciente, row.get("sexo"), diagnostico, datetime.date.today()))
                id_morb = cursor.lastrowid
                cursor.execute("INSERT INTO morb_simplifica (id_morb) VALUES (?)", (id_morb,))
        conn.commit()
        notificacion_cambios()
        st.rerun()
        return


### EPI14 ###
# no se edita

### Registro Diario ###

def procesar_guardado_cambios_reg_diario(edited_df, DB_PATH=DB_PATH):
    # Guardar cambios en los registros existentes (solo para roles no secretarios)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        for _, row in edited_df.iterrows():
            # Normalizar fecha (acepta 'fecha', 'fd' o 'fecha_display')
            fecha_raw = row.get('fecha') or row.get('fd') or row.get('fecha_display') or ''
            if isinstance(fecha_raw, pd.Timestamp):
                fecha_dt = fecha_raw
            else:
                fecha_dt = pd.to_datetime(fecha_raw, dayfirst=True, errors='coerce')
            fecha_db = fecha_dt.date() if not pd.isna(fecha_dt) else None

            # Validaciones (usar .get para evitar KeyError)
            #if not val_texynum(row.get("edad_sexo", ""), "La", "edad y sexo"):
            #    return
            for field, label in [("mr", "MR"), ("mo", "MO"), ("so", "SO"),
                                 ("cd", "CD"), ("cb", "CB"), ("gett", "GETT"), ("nc", "NC")]:
                if not validar_texto(row.get(field, ""), "El", label):
                    return

            peso_raw = row.get("peso", None)
            talla_raw = row.get("talla", None)

            # Detectar None o NaN (pandas/numpy)
            if pd.isna(peso_raw) or pd.isna(talla_raw) or peso_raw is None or talla_raw is None:
                st.error("Peso y talla no deben estar vacíos.", icon=":material/error:")
                return

            # Intentar convertir a float con manejo de errores
            try:
                peso = float(peso_raw)
                talla = float(talla_raw)
            except (TypeError, ValueError):
                st.error("Peso y talla deben ser números válidos.", icon=":material/error:")
                return

            # Validar valores positivos
            if peso <= 0 or talla <= 0:
                st.error("Peso y talla deben ser mayores a 0 para los registros diarios.", icon=":material/error:")
                return

            if not val_notas(row.get("autopsia", ""), "La", "autopsia"):
                return

            # Determinar id del registro (soporta 'id' o 'id_registro')
            id_reg = row.get("id") if row.get("id") is not None else row.get("id_registro")

            # UPDATE si existe id, INSERT si no
            if pd.notna(id_reg):
                cursor.execute("""
                    UPDATE registro_diario SET
                        fd = ?, edad_sexo = ?, mr = ?, mo = ?, so = ?, cb = ?, cd = ?,
                        gett = ?, nc = ?, peso = ?, talla = ?, autopsia = ?
                    WHERE id_registro = ?
                """, (
                    fecha_db, row.get("edad_sexo"), row.get("mr"), row.get("mo"), row.get("so"),
                    row.get("cb"), row.get("cd"), row.get("gett"), row.get("nc"),
                    peso, talla, row.get("autopsia"), id_reg
                ))
            else:
                id_doctor = row.get("id_doctor", None)
                # Calcular semana solo para el INSERT
                semana = None
                if fecha_db:
                    try:
                        semana_num = fecha_db.isocalendar()[1]
                        semana = f"Semana {semana_num}"
                    except Exception:
                        semana = "Semana desconocida"
                else:
                    semana = "Semana desconocida"
                cursor.execute("""
                    INSERT INTO registro_diario (
                        semana, fd, edad_sexo, mr, mo, so, cb, cd, gett, nc, peso, talla, autopsia, id_doctor, fecha_registro_formulario
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    semana, fecha_db, row.get("edad_sexo"), row.get("mr"), row.get("mo"), row.get("so"),
                    row.get("cb"), row.get("cd"), row.get("gett"), row.get("nc"),
                    peso, talla, row.get("autopsia"), id_doctor, datetime.date.today()
                ))
        conn.commit()
        notificacion_cambios()
        st.session_state["reset_form_reg_diario"] = True
        st.rerun()