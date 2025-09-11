import streamlit as st
import datetime
import sqlite3
import pandas as pd
from pathlib import Path
from utils.sql_control import operaciones_sql_epi14, eliminar_registros_epi14
from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez
from utils.verificaciones import obtener_info_usuario
from pages.menu import menu
from utils.filtro import descargar_pdf, descargar_registros_seleccionados, filtrar_por_fechas
from utils.base_64 import img_a_base64
from utils.limpieza import limpiar_campos_epi14
from utils.validaciones import val_texynum, val_notas
from utils.botones import confirmar_eliminar
from reportes.report_epi14 import exportar_pdf_epi14_semanal
import os
configurar_pagina_espanol()

import sys


def get_project_root() -> Path:
    """Devuelve la raíz del proyecto, incluso empaquetado con PyInstaller."""
    if getattr(sys, "frozen", False):  # Si está empaquetado
        # Carpeta base del ejecutable
        return Path(sys._MEIPASS)
    else:
        # Carpeta base del código fuente
        return Path(__file__).resolve().parent.parent.parent

PROJECT_ROOT = get_project_root()
ASSETS_DIR = PROJECT_ROOT / "static" / "assets" / "imagenes"
DB_PATH = os.environ.get("DB_PATH", "hospital.db")
menu()

def formulario_reporte_epi14_semanal():
    with st.container():
        try:
            with sqlite3.connect(DB_PATH) as conn:
                query = """
                    SELECT DISTINCT es.semana || '-' || strftime('%Y', es.fecha_registro_formulario) AS semana
                    FROM epi14_semanal es
                """
                df_weeks = pd.read_sql_query(query, conn)
                if not df_weeks.empty:
                    extracted = df_weeks['semana'].str.extract(r'Semana (\d+)-(\d{4})')
                    df_weeks['week'] = pd.to_numeric(extracted[0], errors='coerce').fillna(0)
                    df_weeks['year'] = pd.to_numeric(extracted[1], errors='coerce').fillna(0)
                    available_weeks = sorted(df_weeks[['week', 'year']].drop_duplicates().values, key=lambda x: (x[1], x[0]))
                    available_years = sorted(set(int(y) for _, y in available_weeks))
                else:
                    available_weeks = []
                    available_years = []
        except sqlite3.Error:
            available_weeks = []
            available_years = []

        timeframe_key = "timeframe_epi14_semanal"
        if timeframe_key not in st.session_state:
            st.session_state[timeframe_key] = "Semana"

        timeframe = st.selectbox("Seleccionar período", ["Semana", "Fecha Específica", "Rango de Fechas"], 
                                 key="kkkkk", 
                                 on_change=lambda: st.session_state.update({timeframe_key: st.session_state[timeframe_key]}))
        
        year, week, specific_date, start_date, end_date = None, None, None, None, None
        pdf_buffer = None
        
        if timeframe == "Semana":
            if not available_years:
                st.warning("No hay semanas disponibles en la base de datos.", icon=":material/warning:")
            else:
                col_year, col_week = st.columns(2)
                with col_year:
                    year = st.selectbox("Año", available_years, 
                                        key="year_epi14_semanal")
                with col_week:
                    weeks_for_year = [int(w) for w, y in available_weeks if int(y) == year]
                    if not weeks_for_year:
                        st.warning(f"No hay semanas disponibles para el año {year}.", icon=":material/warning:")
                        week = None
                    else:
                        week = st.selectbox("Semana", weeks_for_year, key="week_epi14_semanal")
                if year and week:
                    pdf_buffer = exportar_pdf_epi14_semanal(year=year, week=week)
        elif timeframe == "Fecha Específica":
            specific_date = st.date_input("Fecha", format="DD/MM/YYYY", min_value=datetime.date(2000, 1, 1), 
                                          max_value=datetime.date(2050, 12, 31), key="specific_date_epi14_semanal")
            pdf_buffer = exportar_pdf_epi14_semanal(specific_date=specific_date)
        else:
            col_start, col_end = st.columns(2)
            with col_start:
                start_date = st.date_input("Fecha Inicio", format="DD/MM/YYYY", min_value=datetime.date(2000, 1, 1), 
                                           max_value=datetime.date(2050, 12, 31), key="start_date_epi14_semanal")
            with col_end:
                end_date = st.date_input("Fecha Fin", format="DD/MM/YYYY", min_value=datetime.date(2000, 1, 1), 
                                         max_value=datetime.date(2050, 12, 31), value=datetime.date.today(), 
                                         key="end_date_epi14_semanal")
            if end_date >= start_date:
                pdf_buffer = exportar_pdf_epi14_semanal(start_date=start_date, end_date=end_date)

        if pdf_buffer:
            fecha_actual = datetime.datetime.now()
            fecha_str = fecha_actual.strftime("%d-%m-%Y")
            hora_str = fecha_actual.strftime("%I-%M-%S")
            meridiano = "PM" if fecha_actual.hour >= 12 else "AM"
            fecha_hora_str = f"{fecha_str}_{hora_str}_{meridiano}"

            st.download_button(
                label="Descargar Reporte EPI-14 Semanal",
                data=pdf_buffer,
                file_name=f"Reporte_EPI14_Semanal_{fecha_hora_str}.pdf",  
                mime="application/pdf",
                icon=":material/download:",
                key=f"descargaepi14semanal{fecha_hora_str}",
                type="primary"
            )
        else:
            st.error("No hay datos para el período seleccionado.", icon=":material/error:")

def data_editor_epi14(df, rol_usuario):
    if " " not in df.columns:
        df.insert(0, " ", False)

    columns_to_display = [col for col in df.columns if col not in (" ", "id_semanal")]
    columns_to_show = [" "] + columns_to_display + (["id_semanal"] if "id_semanal" in df.columns else [])
    df = df[columns_to_show]

    column_config = {
        " ": st.column_config.CheckboxColumn(" ", default=False, disabled=False),
        "semana": st.column_config.TextColumn("Semana", disabled=True),
        "causa": st.column_config.TextColumn("Causa", disabled=True),
        "numero": st.column_config.NumberColumn("Número de casos", min_value=0, step=1, disabled=True),
        "sexo_edad": st.column_config.TextColumn("Sexo/Edad", disabled=True),
        "total": st.column_config.NumberColumn("Total", disabled=True),
        "fecha_registro_formulario": st.column_config.DateColumn(
            "Fecha de registro",
            disabled=True,
            format="DD/MM/YYYY"
        ),
        "Registrado_por": st.column_config.TextColumn("Registrado por", disabled=True),
        "id_semanal": st.column_config.NumberColumn("ID Semanal", disabled=True)
    }

    for col in columns_to_show:
        if col not in column_config and col != " ":
            column_config[col] = st.column_config.TextColumn(col, disabled=True)

    edited_df = st.data_editor(
        df,
        hide_index=True,
        column_config=column_config,
        key="editor_epi14"
    )
    return edited_df

@st.fragment
def formulario_epi14_semanal(db=DB_PATH):
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a este formulario.", icon=":material/error:")
        return

    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)
    if not info_usuario:
        st.error("Usuario no encontrado. Por favor, inicia sesión nuevamente.", icon=":material/error:")
        return

    rol_usuario = info_usuario["rol"]
    id_doctor = info_usuario["id_doctor"]
    id_secretaria = info_usuario["id_secretaria"]
    id_administrador = info_usuario["id_administrador"]

    tab1, tab2 = st.tabs([
        "| :material/coronavirus: Epi-14 Semanal |",
        "| :material/article_shortcut: Reporte General |"
    ])

    with tab1:
        st.subheader(":material/table: Datos de EPI-14 Semanal", anchor=False)
        df = operaciones_sql_epi14("cargar")
        if df is not None and not df.empty:
            mostrar_editor = st.toggle("Mostrar datos de registros", value=False, key="toggle_editor_epi14")
            
            if mostrar_editor:
                df_filtrado = filtrar_por_fechas(df, "fecha_registro_formulario")
                edited_df = data_editor_epi14(df_filtrado, rol_usuario)
                has_selection = edited_df[" "].any()
                
                if rol_usuario == "Secretario (a)":
                    col1, col3 = st.columns(2)
                    with col1:
                        descargar_pdf(edited_df, "epi14_semanal")
                    with col3:
                        df_sel = edited_df[edited_df[" "] == True]
                        descargar_registros_seleccionados(edited_df, "epi14_semanal")
                        descargar_pdf(df_sel, "epi14_semanal_seleccionado",
                                    label="Descarga selección", disabled=not has_selection)
                else:
                    col_descargar, col_descargar_seleccionado, col_eliminar = st.columns(3)
                    with col_descargar:
                        descargar_pdf(edited_df, "epi14_semanal")
                    with col_descargar_seleccionado:
                        df_sel = edited_df[edited_df[" "] == True]
                        descargar_registros_seleccionados(edited_df, "epi14_semanal")
                        descargar_pdf(df_sel, "epi14_semanal_seleccionado",
                                    label="Descarga selección", disabled=not has_selection)
                    with col_eliminar:
                        if st.button("Eliminar", icon=":material/delete:", key="delete_epi14_semanal",
                                    disabled=not has_selection, use_container_width=True,
                                    help="Eliminar registros seleccionados."):
                            confirmar_eliminar(eliminar_registros_epi14, edited_df)
        else:
            st.info("No hay datos para mostrar.", icon=":material/info:")

        if rol_usuario != "Secretario (a)":
            _, col_titulo = st.columns([1.4, 2.7])
            with col_titulo:
                st.subheader(":material/new_label: Registrar EPI-14 Semanal", anchor=False)

            _, col_form, _ = st.columns([1.0, 4, 1.0])
            with col_form:
                with st.form("form_epi14", clear_on_submit=False):
                    semana = st.selectbox("Semana", list(range(1, 53)))
                    causa = st.text_area("Causa", max_chars=150,
                                         placeholder="Descripción de la causa", key="causa_epi14")

                    numero = st.number_input("Número de casos", min_value=0,
                                             step=1, key="n_casos_epi14")

                    st.warning(
                        '**Nota:** El número de casos debe ser **mayor a 0** y darle **click al boton** "Agregar caso" '
                        'para generar los campos de Sexo y Edad. (El boton :material/cleaning_services: cierra los campos generados.)',
                        icon=":material/info:"
                    )

                    sexo_edad_list = []

                    col_reg, col_agregar, col_limpiar = st.columns([3, 11, 1], gap=None)
                    with col_reg:
                        registrar = st.form_submit_button("Registrar", icon=":material/save:", type="primary")
                    with col_agregar:
                        generar = st.form_submit_button("Agregar caso", icon=":material/add:",
                                                        help="Generar campos de Sexo y Edad", type="secondary")
                    with col_limpiar:
                        st.form_submit_button("", icon=":material/cleaning_services:",
                                              on_click=limpiar_campos_epi14, type="tertiary",
                                              help="Limpia todos los campos del formulario.")

                    if generar and numero > 0:
                        st.session_state["num_casos_epi14"] = int(numero)
                        for i in range(st.session_state["num_casos_epi14"]):
                            c1, c2 = st.columns(2)
                            with c1:
                                sexo = st.selectbox(f"Sexo (Caso {i+1})", ["M", "F"],
                                                    key=f"sexo_epi14_{i}")
                            with c2:
                                edad = st.number_input(f"Edad (Caso {i+1})", min_value=0,
                                                       step=1, key=f"edad_epi14_{i}")
                            sexo_edad_list.append(f"{sexo}/{edad}")

                    if "num_casos_epi14" in st.session_state and st.session_state["num_casos_epi14"] > 0 and not generar:
                        for i in range(st.session_state["num_casos_epi14"]):
                            c1, c2 = st.columns(2)
                            with c1:
                                sexo = st.selectbox(f"Sexo (Caso {i+1})", ["M", "F"],
                                                    key=f"sexo_epi14_{i}")
                            with c2:
                                edad = st.number_input(f"Edad (Caso {i+1})", min_value=0,
                                                       step=1, key=f"edad_epi14_{i}")
                            sexo_edad_list.append(f"{sexo}/{edad}")

                    if registrar:
                        if not causa:
                            st.error("Por favor completa el campo Causa.", icon=":material/error:")
                            return
                        if not val_notas(causa, "La", "causa"):
                            return
                        if numero <= 0:
                            st.error("Número de casos debe ser mayor a 0.", icon=":material/error:")
                            return
                        if "num_casos_epi14" not in st.session_state:
                            st.error("Presiona '+' para generar los campos de Sexo y Edad.", icon=":material/error:")
                            return
                        if int(numero) != st.session_state["num_casos_epi14"]:
                            st.error("El número de casos cambió, vuelve a presionar '+'.", icon=":material/error:")
                            return
                        if len(sexo_edad_list) != st.session_state["num_casos_epi14"]:
                            st.error(f"Debes ingresar exactamente {st.session_state['num_casos_epi14']} "
                                     f"combinación de Sexo y Edad.", icon=":material/error:")
                            return
                        for se in sexo_edad_list:
                            if not val_texynum(se, "El", "sexo y edad"):
                                return

                        sexo_edad = ", ".join(sexo_edad_list)
                        datos = (semana, causa, numero, sexo_edad,
                                 id_doctor, id_secretaria, id_administrador, rol_usuario)
                        if operaciones_sql_epi14("registrar", datos_registro=datos):
                            st.success("Registro guardado", icon=":material/check_circle:")
                            del st.session_state["num_casos_epi14"]
                            st.rerun()

    with tab2:
        st.subheader(":material/arrow_circle_down: Descarga de reportes EPI-14 Semanal",
                     anchor=False, divider="gray")
        formulario_reporte_epi14_semanal()

def mostrar_epi14_semanal():
    logo_bandera = ASSETS_DIR / "imagebanderanueva2.png"
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) # Llama a la función para recargar la página una vez.
    logo(tamano="100%")
    formulario_epi14_semanal()

mostrar_epi14_semanal()