import streamlit as st
import pandas as pd
import sqlite3
import datetime
import os
import time
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
        pass

def procesar_guardado_cambios_mortalidad_neonatal(edited_df, DB_PATH=DB_PATH):
    usuario = st.session_state.get("autenticado_usuario", "Desconocido")
    hubo_cambios = False
    ultimo_id = None
    error_occured = False

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
        
        editor_state = st.session_state.get("editor_neonatal", {})
        edited_rows = editor_state.get("edited_rows", {})
        cambios_directos = {}
        for chgs in edited_rows.values():
            for col, val in chgs.items():
                if col != " ": cambios_directos[col] = val
                
        seleccionadas = [idx for idx, r in edited_df.iterrows() if r.get(" ") == True]
        
        filas_editadas = []
        for k, chgs in edited_rows.items():
            if any(c != " " for c in chgs.keys()):
                try: idx = int(k)
                except: idx = k
                filas_editadas.append(idx)
                
        filas_a_procesar = sorted(list(set(filas_editadas) | set(seleccionadas)))
        
        if filas_a_procesar:
            st.toast(f"💾 Guardando {len(filas_a_procesar)} cambios en Mortalidad Neonatal...")
            
        for idx in filas_a_procesar:
            if idx in edited_df.index: row = edited_df.loc[idx].copy()
            else:
                try: row = edited_df.iloc[int(idx)].copy()
                except: continue
                
            str_idx = str(idx)
            int_idx = idx if isinstance(idx, int) else None
            edits_for_row = {}
            if str_idx in edited_rows: edits_for_row = edited_rows[str_idx]
            elif int_idx in edited_rows: edits_for_row = edited_rows[int_idx]
            
            # DETERMINAR CAMPOS REALMENTE CAMBIADOS
            campos_cambiados = set()
            if str_idx in edited_rows: campos_cambiados.update(edited_rows[str_idx].keys())
            if int_idx in edited_rows: campos_cambiados.update(edited_rows[int_idx].keys())
            if idx in seleccionadas: campos_cambiados.update(cambios_directos.keys())
            if " " in campos_cambiados: campos_cambiados.remove(" ")

            if not campos_cambiados:
                continue

            try: id_m = int(row.get("id"))
            except: 
                st.error(f"Fila {idx}: ID de registro no válido.")
                error_occured = True; continue
            
            ultimo_id = id_m

            # Validaciones solo si el campo fue cambiado
            if 'peso' in campos_cambiados:
                val = row.get("peso")
                if pd.isna(val) or str(val).strip() == "":
                    st.error(f"Fila {idx}: Peso no debe estar vacío."); error_occured = True; continue
                try: 
                    if float(val) <= 0: raise ValueError()
                except: st.error(f"Fila {idx}: Peso debe ser número > 0."); error_occured = True; continue

            if 'talla' in campos_cambiados:
                val = row.get("talla")
                if pd.isna(val) or str(val).strip() == "":
                    st.error(f"Fila {idx}: Talla no debe estar vacío."); error_occured = True; continue
                try: 
                    if float(val) <= 0: raise ValueError()
                except: st.error(f"Fila {idx}: Talla debe ser número > 0."); error_occured = True; continue

            if 'historia_clinica' in campos_cambiados:
                if not val_num_espacios(str(row.get("historia_clinica", "")), "La", "historia clinica"): error_occured = True; continue
            if 'nombres_apellidos' in campos_cambiados:
                if not validar_texto(row.get("nombres_apellidos", ""), "Los", "nombres y apellidos"): error_occured = True; continue
                if not validar_cinco_espacios(row.get("nombres_apellidos", ""), "Los", "nombres y apellidos"): error_occured = True; continue
            if 'nombre_madre' in campos_cambiados:
                if not validar_texto(row.get("nombre_madre", ""), "El", "nombre de la madre"): error_occured = True; continue
                if not validar_cinco_espacios(row.get("nombre_madre", ""), "El", "nombre de la madre"): error_occured = True; continue

            updates = {
                'mortalidad': {'fields': [], 'values': []},
                'mortalidad_neonatal': {'fields': [], 'values': []},
                'persona_paciente': {'fields': [], 'values': []}
            }

            for col in campos_cambiados:
                if col in COLUMN_TO_TABLE_MAP:
                    value = row[col]
                    if isinstance(value, (pd.Timestamp, datetime.date, datetime.datetime)):
                        value = value.strftime('%d/%m/%Y')
                    table = COLUMN_TO_TABLE_MAP[col]
                    updates[table]['fields'].append(f"{col} = ?")
                    updates[table]['values'].append(value)

            cambio_local = False
            if updates['mortalidad']['fields']:
                cursor.execute(f"UPDATE mortalidad SET {', '.join(updates['mortalidad']['fields'])} WHERE id_m = ?", 
                              tuple(updates['mortalidad']['values'] + [id_m]))
                cambio_local = True

            if updates['mortalidad_neonatal']['fields']:
                cursor.execute(f"UPDATE mortalidad_neonatal SET {', '.join(updates['mortalidad_neonatal']['fields'])} WHERE id_m = ?", 
                              tuple(updates['mortalidad_neonatal']['values'] + [id_m]))
                cambio_local = True

            if updates['persona_paciente']['fields']:
                cursor.execute("SELECT id_paciente FROM mortalidad WHERE id_m = ?", (id_m,))
                res = cursor.fetchone()
                if res:
                    cursor.execute(f"UPDATE persona_paciente SET {', '.join(updates['persona_paciente']['fields'])} WHERE id_paciente = ?", 
                                  tuple(updates['persona_paciente']['values'] + [res[0]]))
                    if cursor.rowcount > 0: cambio_local = True

            # Manejo de dirección
            if 'direccion' in campos_cambiados or 'direccion_hogar' in campos_cambiados:
                direccion_val = (row.get('direccion') or row.get('direccion_hogar') or '')
                direccion_text = str(direccion_val).strip()
                cursor.execute("SELECT id_direccion FROM mortalidad WHERE id_m = ?", (id_m,))
                r = cursor.fetchone()
                id_dir = r[0] if r and r[0] is not None else None
                if id_dir:
                    cursor.execute("SELECT descripcion FROM direccion WHERE id_direccion = ?", (id_dir,))
                    curQuery = cursor.fetchone()
                    cur_desc = curQuery[0] if curQuery and curQuery[0] is not None else ''
                    if cur_desc != direccion_text:
                        cursor.execute("SELECT COUNT(*) FROM mortalidad WHERE id_direccion = ?", (id_dir,))
                        uso = cursor.fetchone()[0]
                        if uso <= 1:
                            cursor.execute("SELECT id_parroquia FROM direccion WHERE id_direccion = ?", (id_dir,))
                            rpar = cursor.fetchone()
                            if rpar and rpar[0] is not None: _overwrite_hierarchy_defaults(cursor, rpar[0])
                            cursor.execute("UPDATE direccion SET descripcion = ? WHERE id_direccion = ?", (direccion_text, id_dir))
                            if cursor.rowcount > 0: cambio_local = True
                        else:
                            id_parroquia = _ensure_default_jerarquia(cursor)
                            cursor.execute("INSERT INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (direccion_text, id_parroquia))
                            new_id = cursor.lastrowid
                            cursor.execute("UPDATE mortalidad SET id_direccion = ? WHERE id_m = ?", (new_id, id_m))
                            if cursor.rowcount > 0: cambio_local = True
                else:
                    id_parroquia = _ensure_default_jerarquia(cursor)
                    cursor.execute("INSERT INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (direccion_text, id_parroquia))
                    new_id = cursor.lastrowid
                    cursor.execute("UPDATE mortalidad SET id_direccion = ? WHERE id_m = ?", (new_id, id_m))
                    if cursor.rowcount > 0: cambio_local = True

            if cambio_local: hubo_cambios = True

        if hubo_cambios and not error_occured:
            conn.commit()
        else:
            conn.rollback()

    if hubo_cambios and not error_occured:
        registrar_actividad_duradera("EDITADO", "Mortalidad Neonatal", ultimo_id, usuario)
        notificacion_cambios()
        st.session_state["reset_form_mortalidad"] = True
        if "editor_neonatal" in st.session_state: del st.session_state["editor_neonatal"]
        st.rerun()
    elif error_occured:
        st.warning("Algunos cambios no se guardaron debido a errores de validación.", icon=":material/warning:")
    else:
        st.info("No se detectaron cambios para guardar.", icon=":material/info:")


def procesar_guardado_cambios_mortalidad_infantil(edited_df, DB_PATH=DB_PATH):
    usuario = st.session_state.get("autenticado_usuario", "Desconocido")
    hubo_cambios = False
    ultimo_id = None
    error_occured = False

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
        
        editor_state = st.session_state.get("editor_infantil", {})
        edited_rows = editor_state.get("edited_rows", {})
        cambios_directos = {}
        for chgs in edited_rows.values():
            for col, val in chgs.items():
                if col != " ": cambios_directos[col] = val
                
        seleccionadas = [idx for idx, r in edited_df.iterrows() if r.get(" ") == True]
        
        filas_editadas = []
        for k, chgs in edited_rows.items():
            if any(c != " " for c in chgs.keys()):
                try: idx = int(k)
                except: idx = k
                filas_editadas.append(idx)
                
        filas_a_procesar = sorted(list(set(filas_editadas) | set(seleccionadas)))
        
        if filas_a_procesar:
            st.toast(f"💾 Guardando {len(filas_a_procesar)} cambios en Mortalidad Infantil...")
            
        for idx in filas_a_procesar:
            if idx in edited_df.index: row = edited_df.loc[idx].copy()
            else:
                try: row = edited_df.iloc[int(idx)].copy()
                except: continue
                
            str_idx = str(idx)
            int_idx = idx if isinstance(idx, int) else None
            edits_for_row = {}
            if str_idx in edited_rows: edits_for_row = edited_rows[str_idx]
            elif int_idx in edited_rows: edits_for_row = edited_rows[int_idx]
            
            # DETERMINAR CAMPOS REALMENTE CAMBIADOS
            campos_cambiados = set()
            if str_idx in edited_rows: campos_cambiados.update(edited_rows[str_idx].keys())
            if int_idx in edited_rows: campos_cambiados.update(edited_rows[int_idx].keys())
            if idx in seleccionadas: campos_cambiados.update(cambios_directos.keys())
            if " " in campos_cambiados: campos_cambiados.remove(" ")

            if not campos_cambiados:
                continue

            try: id_m = int(row.get("id"))
            except: 
                st.error(f"Fila {idx}: ID de registro no válido.")
                error_occured = True; continue
            
            ultimo_id = id_m

            # Validaciones solo si el campo fue cambiado
            if 'historia_clinica' in campos_cambiados:
                if not val_num_espacios(str(row.get("historia_clinica", "")), "La", "historia clinica"): error_occured = True; continue
            if 'nombres_apellidos' in campos_cambiados:
                if not validar_texto(row.get("nombres_apellidos", ""), "Los", "nombres y apellidos"): error_occured = True; continue
                if not validar_cinco_espacios(row.get("nombres_apellidos", ""), "Los", "nombres y apellidos"): error_occured = True; continue
            if 'nombre_madre' in campos_cambiados:
                if not validar_texto(row.get("nombre_madre", ""), "El", "nombre de la madre"): error_occured = True; continue
                if not validar_cinco_espacios(row.get("nombre_madre", ""), "El", "nombre de la madre"): error_occured = True; continue

            updates = {
                'mortalidad': {'fields': [], 'values': []},
                'mortalidad_infantil': {'fields': [], 'values': []},
                'persona_paciente': {'fields': [], 'values': []}
            }

            for col in campos_cambiados:
                if col in COLUMN_TO_TABLE_MAP:
                    value = row[col]
                    if isinstance(value, (pd.Timestamp, datetime.date, datetime.datetime)):
                        value = value.strftime('%d/%m/%Y')
                    table = COLUMN_TO_TABLE_MAP[col]
                    updates[table]['fields'].append(f"{col} = ?")
                    updates[table]['values'].append(value)

            cambio_local = False
            if updates['mortalidad']['fields']:
                cursor.execute(f"UPDATE mortalidad SET {', '.join(updates['mortalidad']['fields'])} WHERE id_m = ?", 
                              tuple(updates['mortalidad']['values'] + [id_m]))
                cambio_local = True
            if updates['mortalidad_infantil']['fields']:
                cursor.execute(f"UPDATE mortalidad_infantil SET {', '.join(updates['mortalidad_infantil']['fields'])} WHERE id_m = ?", 
                              tuple(updates['mortalidad_infantil']['values'] + [id_m]))
                cambio_local = True
            if updates['persona_paciente']['fields']:
                cursor.execute("SELECT id_paciente FROM mortalidad WHERE id_m = ?", (id_m,))
                res = cursor.fetchone()
                if res:
                    cursor.execute(f"UPDATE persona_paciente SET {', '.join(updates['persona_paciente']['fields'])} WHERE id_paciente = ?", 
                                  tuple(updates['persona_paciente']['values'] + [res[0]]))
                    if cursor.rowcount > 0: cambio_local = True

            if cambio_local: hubo_cambios = True

        if hubo_cambios and not error_occured:
            conn.commit()
        else:
            conn.rollback()

    if hubo_cambios and not error_occured:
        registrar_actividad_duradera("EDITADO", "Mortalidad Infantil", ultimo_id, usuario)
        notificacion_cambios()
        st.session_state["reset_form_mortalidad"] = True
        if "editor_infantil" in st.session_state: del st.session_state["editor_infantil"]
        st.rerun()
    elif error_occured:
        st.warning("Algunos cambios no se guardaron debido a errores de validación.", icon=":material/warning:")
    else:
        st.info("No se detectaron cambios para guardar.", icon=":material/info:")


def procesar_guardado_cambios_mortalidad_materna(edited_df, DB_PATH=DB_PATH):
    usuario = st.session_state.get("autenticado_usuario", "Desconocido")
    hubo_cambios = False
    ultimo_id = None
    error_occured = False

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
        
        editor_state = st.session_state.get("editor_materna", {})
        edited_rows = editor_state.get("edited_rows", {})
        cambios_directos = {}
        for chgs in edited_rows.values():
            for col, val in chgs.items():
                if col != " ": cambios_directos[col] = val
                
        seleccionadas = [idx for idx, r in edited_df.iterrows() if r.get(" ") == True]
        
        filas_editadas = []
        for k, chgs in edited_rows.items():
            if any(c != " " for c in chgs.keys()):
                try: idx = int(k)
                except: idx = k
                filas_editadas.append(idx)
                
        filas_a_procesar = sorted(list(set(filas_editadas) | set(seleccionadas)))
        
        if filas_a_procesar:
            st.toast(f"💾 Guardando {len(filas_a_procesar)} cambios en Mortalidad Materna...")
            
        for idx in filas_a_procesar:
            if idx in edited_df.index: row = edited_df.loc[idx].copy()
            else:
                try: row = edited_df.iloc[int(idx)].copy()
                except: continue
                
            str_idx = str(idx)
            int_idx = idx if isinstance(idx, int) else None
            edits_for_row = {}
            if str_idx in edited_rows: edits_for_row = edited_rows[str_idx]
            elif int_idx in edited_rows: edits_for_row = edited_rows[int_idx]
            
            # DETERMINAR CAMPOS REALMENTE CAMBIADOS
            campos_cambiados = set()
            if str_idx in edited_rows: campos_cambiados.update(edited_rows[str_idx].keys())
            if int_idx in edited_rows: campos_cambiados.update(edited_rows[int_idx].keys())
            if idx in seleccionadas: campos_cambiados.update(cambios_directos.keys())
            if " " in campos_cambiados: campos_cambiados.remove(" ")

            if not campos_cambiados:
                continue

            try: id_m = int(row.get("id"))
            except: 
                st.error(f"Fila {idx}: ID de registro no válido.")
                error_occured = True; continue
            
            ultimo_id = id_m

            # Validaciones solo si el campo fue cambiado
            if 'historia_clinica' in campos_cambiados:
                if not val_num_espacios(str(row.get("historia_clinica", "")), "La", "historia clinica"): error_occured = True; continue
            if 'nombres_apellidos' in campos_cambiados:
                if not validar_texto(row.get("nombres_apellidos", ""), "Los", "nombres y apellidos"): error_occured = True; continue
                if not validar_cinco_espacios(row.get("nombres_apellidos", ""), "Los", "nombres y apellidos"): error_occured = True; continue

            updates = {
                'mortalidad': {'fields': [], 'values': []},
                'persona_paciente': {'fields': [], 'values': []}
            }

            for col in campos_cambiados:
                if col in COLUMN_TO_TABLE_MAP:
                    value = row[col]
                    if isinstance(value, (pd.Timestamp, datetime.date, datetime.datetime)):
                        value = value.strftime('%d/%m/%Y')
                    table = COLUMN_TO_TABLE_MAP[col]
                    updates[table]['fields'].append(f"{col} = ?")
                    updates[table]['values'].append(value)

            cambio_local = False
            if updates['mortalidad']['fields']:
                cursor.execute(f"UPDATE mortalidad SET {', '.join(updates['mortalidad']['fields'])} WHERE id_m = ?", 
                              tuple(updates['mortalidad']['values'] + [id_m]))
                cambio_local = True

            if updates['persona_paciente']['fields']:
                cursor.execute("SELECT id_paciente FROM mortalidad WHERE id_m = ?", (id_m,))
                res = cursor.fetchone()
                if res:
                    cursor.execute(f"UPDATE persona_paciente SET {', '.join(updates['persona_paciente']['fields'])} WHERE id_paciente = ?", 
                                  tuple(updates['persona_paciente']['values'] + [res[0]]))
                    if cursor.rowcount > 0: cambio_local = True

            if cambio_local: hubo_cambios = True

        if hubo_cambios and not error_occured:
            conn.commit()
        else:
            conn.rollback()

    if hubo_cambios and not error_occured:
        registrar_actividad_duradera("EDITADO", "Mortalidad Materna", ultimo_id, usuario)
        notificacion_cambios()
        st.session_state["reset_form_mortalidad"] = True
        if "editor_materna" in st.session_state: del st.session_state["editor_materna"]
        st.rerun()
    elif error_occured:
        st.warning("Algunos cambios no se guardaron debido a errores de validación.", icon=":material/warning:")
    else:
        st.info("No se detectaron cambios para guardar.", icon=":material/info:")


def procesar_guardado_cambios_natalidad(edited_df, DB_PATH=DB_PATH):
    usuario = st.session_state.get("autenticado_usuario", "Desconocido")
    hubo_cambios = False
    ultimo_id = None
    error_occured = False

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        editor_state = st.session_state.get("editor_natalidad", {})
        edited_rows = editor_state.get("edited_rows", {})
        cambios_directos = {}
        for chgs in edited_rows.values():
            for col, val in chgs.items():
                if col != " ": cambios_directos[col] = val
                
        seleccionadas = [idx for idx, r in edited_df.iterrows() if r.get(" ") == True]
        
        filas_editadas = []
        for k, chgs in edited_rows.items():
            if any(c != " " for c in chgs.keys()):
                try: idx = int(k)
                except: idx = k
                filas_editadas.append(idx)
                
        filas_a_procesar = sorted(list(set(filas_editadas) | set(seleccionadas)))
        
        if filas_a_procesar:
            st.toast(f"💾 Guardando {len(filas_a_procesar)} cambios en Natalidad...")
            
        for idx in filas_a_procesar:
            if idx in edited_df.index: row = edited_df.loc[idx].copy()
            else:
                try: row = edited_df.iloc[int(idx)].copy()
                except: continue
                
            str_idx = str(idx)
            int_idx = idx if isinstance(idx, int) else None
            edits_for_row = {}
            if str_idx in edited_rows: edits_for_row = edited_rows[str_idx]
            elif int_idx in edited_rows: edits_for_row = edited_rows[int_idx]
            
            # DETERMINAR CAMPOS REALMENTE CAMBIADOS
            campos_cambiados = set()
            if str_idx in edited_rows: campos_cambiados.update(edited_rows[str_idx].keys())
            if int_idx in edited_rows: campos_cambiados.update(edited_rows[int_idx].keys())
            if idx in seleccionadas: campos_cambiados.update(cambios_directos.keys())
            if " " in campos_cambiados: campos_cambiados.remove(" ")

            if not campos_cambiados:
                continue

            try: registro_id = int(row.get('id', 0))
            except: registro_id = 0

            # ─────────────────────────────────────────────────────────────
            # 1. Obtener y convertir valores para validación
            # ─────────────────────────────────────────────────────────────
            # (Incluso si no se cambian, los necesitamos para la validación de sumas del registro completo)
            sexo_gemelar = row.get('sexo_gemelar', '') or ''
            gemelar = int(row.get('gemelar', 0)) if pd.notna(row.get('gemelar', 0)) else 0
            varones = int(row.get('varones', 0)) if pd.notna(row.get('varones', 0)) else 0
            hembras = int(row.get('hembras', 0)) if pd.notna(row.get('hembras', 0)) else 0
            partos = int(row.get("partos", 0)) if pd.notna(row.get("partos", 0)) else 0
            cesareas = int(row.get("cesareas", 0)) if pd.notna(row.get("cesareas", 0)) else 0
            mto = int(row.get("mto", 0)) if pd.notna(row.get("mto", 0)) else 0
            partos_extra = int(row.get("partos_extrahospitalarios", 0)) if pd.notna(row.get("partos_extrahospitalarios", 0)) else 0

            fecha_display = row.get('fecha_display', row.get('fecha', ''))
            if not fecha_display:
                st.error(f"Fila {idx}: No se pudo determinar la fecha del registro."); error_occured = True; continue

            try:
                fecha_db = pd.to_datetime(fecha_display, dayfirst=True, errors='coerce')
            except:
                fecha_db = pd.NaT

            if pd.isna(fecha_db):
                st.error(f"Fila {idx}: Formato de fecha inválido: '{fecha_display}'."); error_occured = True; continue

            fecha_db_str = fecha_db.strftime('%d/%m/%Y')

            # Validaciones de integridad
            if partos_extra > partos:
                st.error(f"Fila {idx}: Partos extra ({partos_extra}) > total partos ({partos})."); error_occured = True; continue

            if sexo_gemelar == "No aplica" and gemelar > 0:
                gemelar = 0

            v_aj, h_aj = varones, hembras
            if sexo_gemelar == "Varones": v_aj += gemelar * 2
            elif sexo_gemelar == "Hembras": h_aj += gemelar * 2
            elif sexo_gemelar == "Mixto":
                v_aj += gemelar; h_aj += gemelar
            
            if (v_aj + h_aj + mto) != (partos + cesareas):
                st.error(f"Fila {idx}: La suma de nacidos no coincide con partos + cesáreas."); error_occured = True; continue

            if registro_id > 0:
                # CONSTRUCCIÓN DINÁMICA DE LA CONSULTA UPDATE
                # Mapeo de columnas internas a columnas de BD
                BD_COLS = {
                    'fecha': 'fecha', 'partos': 'partos', 'cesareas': 'cesareas',
                    'varones': 'varones', 'hembras': 'hembras', 'gemelar': 'gemelar',
                    'mto': 'mto', 'partos_extrahospitalarios': 'partos_extrahospitalarios',
                    'sexo_gemelar': 'sexo_gemelar' # Si existe en la tabla
                }
                
                fields_to_update = []
                values_to_update = []
                
                for col in campos_cambiados:
                    if col in BD_COLS:
                        db_col = BD_COLS[col]
                        val = row[col]
                        if col == 'fecha': val = fecha_db_str
                        fields_to_update.append(f"{db_col} = ?")
                        values_to_update.append(val)
                
                if fields_to_update:
                    query = f"UPDATE natalidad SET {', '.join(fields_to_update)} WHERE id_nata = ?"
                    cursor.execute(query, tuple(values_to_update + [registro_id]))
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

        if hubo_cambios and not error_occured:
            conn.commit()
        else:
            conn.rollback()

    if hubo_cambios and not error_occured:
        registrar_actividad_duradera("EDITADO", "Natalidad", ultimo_id, usuario)
        notificacion_cambios()
        if "editor_natalidad" in st.session_state: del st.session_state["editor_natalidad"]
        st.rerun()
    elif error_occured:
        st.warning("Algunos cambios no se guardaron debido a errores de validación.", icon=":material/warning:")
    else:
        st.info("No se detectaron cambios para guardar.", icon=":material/info:")

def procesar_guardado_morb_extenso(edited_df, DB_PATH=DB_PATH):
    usuario = st.session_state.get("autenticado_usuario", "Desconocido")
    hubo_cambios = False
    ultimo_id = None
    error_occured = False

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        
        editor_state = st.session_state.get("editor_morb_extenso", {})
        edited_rows = editor_state.get("edited_rows", {})
        cambios_directos = {}
        for chgs in edited_rows.values():
            for col, val in chgs.items():
                if col != " ": cambios_directos[col] = val
                
        seleccionadas = [idx for idx, r in edited_df.iterrows() if r.get(" ") == True]
        
        filas_editadas = []
        for k, chgs in edited_rows.items():
            if any(c != " " for c in chgs.keys()):
                try: idx = int(k)
                except: idx = k
                filas_editadas.append(idx)
                
        filas_a_procesar = sorted(list(set(filas_editadas) | set(seleccionadas)))
            
        if filas_a_procesar:
            st.toast(f"💾 Guardando {len(filas_a_procesar)} cambios en Morbilidad...")

        for idx in filas_a_procesar:
            if idx in edited_df.index: row = edited_df.loc[idx].copy()
            else:
                try: row = edited_df.iloc[int(idx)].copy()
                except: continue
                
            str_idx = str(idx)
            int_idx = idx if isinstance(idx, int) else None
            edits_for_row = {}
            if str_idx in edited_rows: edits_for_row = edited_rows[str_idx]
            elif int_idx in edited_rows: edits_for_row = edited_rows[int_idx]
            
            # DETERMINAR CAMPOS REALMENTE CAMBIADOS
            campos_cambiados = set()
            if str_idx in edited_rows: campos_cambiados.update(edited_rows[str_idx].keys())
            if int_idx in edited_rows: campos_cambiados.update(edited_rows[int_idx].keys())
            if idx in seleccionadas: campos_cambiados.update(cambios_directos.keys())
            if " " in campos_cambiados: campos_cambiados.remove(" ")

            if not campos_cambiados:
                continue

            try: id_morb = int(row.get("id"))
            except: 
                st.error(f"Fila {idx}: ID de registro no válido."); error_occured = True; continue
            
            ultimo_id = id_morb

            cambio_local = False

            # 1. Update Morbilidad (Nombres y Diagnóstico)
            morb_fields = []
            morb_values = []
            if 'nombres_apellidos' in campos_cambiados:
                nombres = (row.get("nombres_apellidos") or "").strip()
                if not validar_texto(nombres, "Los", "Nombres y apellidos"): error_occured = True; continue
                if not validar_cinco_espacios(nombres, "Los", "nombres y apellidos"): error_occured = True; continue
                morb_fields.append("nombres_apellidos = ?")
                morb_values.append(nombres)
            
            if 'diagnostico' in campos_cambiados:
                diagnostico = (row.get("diagnostico") or "").strip()
                if not val_texynum(diagnostico, "El", "diagnóstico"): error_occured = True; continue
                morb_fields.append("diagnostico = ?")
                morb_values.append(diagnostico)
            
            if morb_fields:
                cursor.execute(f"UPDATE morbilidad SET {', '.join(morb_fields)} WHERE id_morb = ?", tuple(morb_values + [id_morb]))
                if cursor.rowcount > 0: cambio_local = True

            # 2. Update Persona Paciente (Edad)
            if 'edad' in campos_cambiados:
                edad = row.get("edad")
                cursor.execute("SELECT id_paciente FROM morbilidad WHERE id_morb = ?", (id_morb,))
                res_p = cursor.fetchone()
                if res_p and res_p[0] is not None:
                    try: edad_val = int(edad)
                    except: edad_val = None
                    if edad_val is not None:
                        cursor.execute("UPDATE persona_paciente SET edad = ? WHERE id_paciente = ?", (edad_val, res_p[0]))
                        if cursor.rowcount > 0: cambio_local = True

            # 3. Update Dirección
            if 'direccion' in campos_cambiados or 'direccion_hogar' in campos_cambiados:
                direccion_val = (row.get("direccion") or row.get("direccion_hogar") or "")
                direccion_text = str(direccion_val).strip()
                cursor.execute("SELECT id_direccion_hogar FROM morbilidad WHERE id_morb = ?", (id_morb,))
                res_d = cursor.fetchone()
                id_dir_hogar = res_d[0] if res_d and res_d[0] is not None else None
                
                if id_dir_hogar:
                    cursor.execute("SELECT descripcion FROM direccion WHERE id_direccion = ?", (id_dir_hogar,))
                    curQuery = cursor.fetchone()
                    cur_desc = curQuery[0] if curQuery and curQuery[0] is not None else ""
                    if cur_desc != direccion_text:
                        cursor.execute("SELECT COUNT(*) FROM morbilidad WHERE id_direccion_hogar = ?", (id_dir_hogar,))
                        uso = cursor.fetchone()[0]
                        if uso <= 1:
                            cursor.execute("SELECT id_parroquia FROM direccion WHERE id_direccion = ?", (id_dir_hogar,))
                            rpar = cursor.fetchone()
                            if rpar and rpar[0] is not None: _overwrite_hierarchy_defaults(cursor, rpar[0])
                            cursor.execute("UPDATE direccion SET descripcion = ? WHERE id_direccion = ?", (direccion_text, id_dir_hogar))
                            if cursor.rowcount > 0: cambio_local = True
                        else:
                            id_parroquia = _ensure_default_jerarquia(cursor)
                            cursor.execute("INSERT INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (direccion_text, id_parroquia))
                            new_id_dir = cursor.lastrowid
                            cursor.execute("UPDATE morbilidad SET id_direccion_hogar = ? WHERE id_morb = ?", (new_id_dir, id_morb))
                            if cursor.rowcount > 0: cambio_local = True
                else:
                    id_parroquia = _ensure_default_jerarquia(cursor)
                    cursor.execute("INSERT INTO direccion (descripcion, id_parroquia) VALUES (?, ?)", (direccion_text, id_parroquia))
                    new_id_dir = cursor.lastrowid
                    cursor.execute("UPDATE morbilidad SET id_direccion_hogar = ? WHERE id_morb = ?", (new_id_dir, id_morb))
                    if cursor.rowcount > 0: cambio_local = True

            if cambio_local: hubo_cambios = True

        if hubo_cambios and not error_occured:
            conn.commit()
        else:
            conn.rollback()

    if hubo_cambios and not error_occured:
        registrar_actividad_duradera("EDITADO", "Morbilidad", ultimo_id, usuario)
        notificacion_cambios()
        if "editor_morb_extenso" in st.session_state: del st.session_state["editor_morb_extenso"]
        st.rerun()
    elif error_occured:
        st.warning("Algunos cambios no se guardaron debido a errores de validación.", icon=":material/warning:")
    else:
        st.info("No se detectaron cambios para guardar.", icon=":material/info:")
