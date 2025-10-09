import streamlit as st
from utils.sql_control import operaciones_sql_registro_diario, eliminar_registros_diario
import datetime
import sqlite3
from pathlib import Path
import pandas as pd
from dateutil.relativedelta import relativedelta
from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez, copyright_footer_dos
from utils.filtro import descargar_pdf, descargar_registros_seleccionados, filtrar_por_fechas
from utils.verificaciones import obtener_info_usuario
from pages.menu import menu
from utils.base_64 import img_a_base64
from utils.limpieza import limpiar_campos_registro_diario
from utils.validaciones import validar_texto, val_texynum, val_notas
from utils.botones import confirmar_eliminar, guadar_btn
from utils.guardar_cambios import procesar_guardado_cambios_reg_diario
from reportes.report_reg_diario import exportar_pdf_registro_diario
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
menu()
DB_PATH = os.getenv("hospital.db", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'

def formulario_reporte_registro_diario():
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a esta area.", icon=":material/error:")
        return
    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)
    if not info_usuario:
        st.error("Usuario no encontrado. Por favor, inicia sesión nuevamente.", icon=":material/error:")
        return
    with st.container():
        try:
            with sqlite3.connect(DB_PATH) as conn:
                query = """
                    SELECT DISTINCT TRIM(semana) || '-' || strftime('%Y', fecha_registro_formulario) AS semana
                    FROM registro_diario
                    WHERE semana IS NOT NULL AND fecha_registro_formulario IS NOT NULL
                """
                df_weeks = pd.read_sql_query(query, conn)

                if not df_weeks.empty:
                    # Acepta espacios opcionales alrededor del guion
                    extracted = df_weeks['semana'].str.extract(r'Semana\s+(\d+)\s*-\s*(\d{4})')
                    df_weeks['week'] = pd.to_numeric(extracted[0], errors='coerce')
                    df_weeks['year'] = pd.to_numeric(extracted[1], errors='coerce')

                    df_weeks = df_weeks.dropna(subset=['week', 'year'])
                    available_weeks = sorted(
                        df_weeks[['week', 'year']].drop_duplicates().astype(int).values.tolist(),
                        key=lambda x: (x[1], x[0])
                    )
                    available_years = sorted({y for _, y in available_weeks})
                else:
                    available_weeks, available_years = [], []
        except sqlite3.Error:
            available_weeks, available_years = [], []

        timeframe_key = "timeframe_registro_diario"
        if timeframe_key not in st.session_state:
            st.session_state[timeframe_key] = "Semana"

        timeframe = st.selectbox(
            "Seleccionar período",
            ["Semana", "Fecha Específica", "Rango de Fechas"],
            key="keykey",
            on_change=lambda: st.session_state.update({timeframe_key: st.session_state[timeframe_key]})
        )

        year, week, specific_date, start_date, end_date = None, None, None, None, None
        pdf_buffer = None

        if timeframe == "Semana":
            if not available_years:
                st.warning("No hay semanas disponibles en la base de datos.", icon=":material/warning:")
            else:
                col_year, col_week = st.columns(2)
                with col_year:
                    year = st.selectbox("Año", available_years, key="year_registro_diario")
                with col_week:
                    weeks_for_year = [int(w) for w, y in available_weeks if int(y) == year]
                    if not weeks_for_year:
                        st.warning(f"No hay semanas disponibles para el año {year}.", icon=":material/warning:")
                        week = None
                    else:
                        week = st.selectbox("Semana", weeks_for_year, key="week_registro_diario")

                if year and week:
                    pdf_buffer = exportar_pdf_registro_diario(year=year, week=week)

        elif timeframe == "Fecha Específica":
            specific_date = st.date_input(
                "Fecha",
                format="DD/MM/YYYY",
                min_value=datetime.date(2000, 1, 1),
                max_value=datetime.date(2050, 12, 31),
                key="specific_date_registro_diario"
            )
            pdf_buffer = exportar_pdf_registro_diario(specific_date=specific_date)

        else:  # Rango de Fechas
            col_start, col_end = st.columns(2)
            with col_start:
                start_date = st.date_input(
                    "Fecha Inicio",
                    format="DD/MM/YYYY",
                    min_value=datetime.date(2000, 1, 1),
                    max_value=datetime.date(2050, 12, 31),
                    key="start_date_registro_diario"
                )
            with col_end:
                end_date = st.date_input(
                    "Fecha Fin",
                    format="DD/MM/YYYY",
                    min_value=datetime.date(2000, 1, 1),
                    max_value=datetime.date(2050, 12, 31),
                    value=datetime.date.today(),
                    key="end_date_registro_diario"
                )
            if end_date >= start_date:
                pdf_buffer = exportar_pdf_registro_diario(start_date=start_date, end_date=end_date)

        if pdf_buffer:
            fecha_actual = datetime.datetime.now()
            fecha_str = fecha_actual.strftime("%d-%m-%Y")
            hora_str = fecha_actual.strftime("%I-%M-%S") 
            meridiano = "PM" if fecha_actual.hour >= 12 else "AM"
            fecha_hora_str = f"{fecha_str}_{hora_str}_{meridiano}"

            st.download_button(
                label="Descargar Reporte Registro Diario",
                data=pdf_buffer,
                file_name=f"Reporte_Registro_Diario_{fecha_hora_str}.pdf",
                mime="application/pdf",
                icon=":material/download:",
                key=f"download_registro_diario_{fecha_hora_str}",
                disabled=not pdf_buffer,
                type="primary"
            )
        else:
            st.error("No hay datos para el período seleccionado.", icon=":material/error:")

def data_editor_registro_diario(df, rol_usuario):
    df.insert(0, ' ', False)

    editable_columns = [' ', 'fd', 'edad_sexo', 'mr', 'mo', 'so', 'cb', 'cd', 'gett', 'nc', 
                        'peso', 'talla', 'autopsia', 'id', 'semana', 'id_doctor', 'fecha_registro_formulario']

    df = df[editable_columns]

    column_config = {
        " ": st.column_config.CheckboxColumn(" ", default=False, disabled=False),
        "fd": st.column_config.DateColumn("FO (Fecha de ocurrencia)",format='DD/MM/YYYY' ,disabled=(rol_usuario == "Secretario (a)")),
        "edad_sexo": st.column_config.TextColumn("Edad y Sexo", disabled=True),
        "mr": st.column_config.TextColumn("MR", disabled=(rol_usuario == "Secretario (a)")),
        "mo": st.column_config.TextColumn("MO", disabled=(rol_usuario == "Secretario (a)")),
        "so": st.column_config.TextColumn("SO", disabled=(rol_usuario == "Secretario (a)")),
        "cb": st.column_config.TextColumn("CB", disabled=(rol_usuario == "Secretario (a)")),
        "cd": st.column_config.TextColumn("CD", disabled=(rol_usuario == "Secretario (a)")),
        "gett": st.column_config.TextColumn("GETT", disabled=(rol_usuario == "Secretario (a)")),
        "nc": st.column_config.TextColumn("NC", disabled=(rol_usuario == "Secretario (a)")),
        "peso": st.column_config.NumberColumn("Peso (kg)", format="%.1f", disabled=(rol_usuario == "Secretario (a)")),
        "talla": st.column_config.NumberColumn("Talla (cm)", format="%.1f", disabled=(rol_usuario == "Secretario (a)")),
        "autopsia": st.column_config.TextColumn("Autopsia", disabled=(rol_usuario == "Secretario (a)")),
        "id": st.column_config.TextColumn("ID", disabled=True),
        "id_doctor": st.column_config.TextColumn("ID_Doctor", disabled=True),
        "fecha_registro_formulario": st.column_config.DateColumn("Registro De Formulario", format='DD/MM/YYYY', disabled=True),
        "semana": st.column_config.TextColumn("Semana", disabled=True)
    }

    edited_df = st.data_editor(
        df,
        hide_index=True,
        column_config=column_config,
        key="editor_registro_diario"
    )
    return edited_df

@st.fragment
def formulario_registro_diario(db=DB_PATH):
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
    id_administrador = info_usuario["id_administrador"]

    st.subheader(":material/table: Datos de Registro Diario", anchor=False)
    df = operaciones_sql_registro_diario("cargar")
    if df is None:
        return

    if df.empty:
        st.info("No hay datos para mostrar.", icon=":material/info:")
    else:
        mostrar_editor = st.toggle("Mostrar datos de registros", value=False, key="toggle_editor_natalidad")

        if mostrar_editor:
            df_filtrado = filtrar_por_fechas(df, 'fd')
            edited_df = data_editor_registro_diario(df_filtrado, rol_usuario)
            col1, col3 = st.columns(2)
            has_selection = edited_df[' '].any()
            col_guardar, col_descargar, col_descargar_seleccionado, col_eliminar = st.columns(4)

            if rol_usuario == "Secretario (a)":
                with col1:
                    descargar_pdf(edited_df, "registro_diario", label="Descargar PDF")
                with col3:
                    df_sel = edited_df[edited_df[' '] == True]
                    descargar_registros_seleccionados(edited_df, "registro_diario")
                    descargar_pdf(df_sel, "registro_diario_seleccionado", label="Descarga selección", disabled=not has_selection)
            else:
                with col_guardar:
                    guadar_btn(procesar_guardado_cambios_reg_diario, edited_df)
                with col_descargar:
                    descargar_pdf(edited_df, "registro_diario")            
                with col_descargar_seleccionado:
                    df_sel = edited_df[edited_df[' '] == True]
                    descargar_registros_seleccionados(edited_df, "registro_diario")
                    descargar_pdf(df_sel, "registro_diario_seleccionado", label="Descarga selección", disabled=not has_selection)
                with col_eliminar:
                    btn_eliminar = st.button("Eliminar", icon=":material/delete:", key="delete_registro_diario", 
                                            disabled=not has_selection, width="stretch",
                                            help="Eliminar registros seleccionados.")
                    if btn_eliminar:
                        confirmar_eliminar(eliminar_registros_diario, edited_df)

    if rol_usuario != "Secretario (a)":
        st.subheader(":material/new_label: Registrar Registro Diario", anchor=False)
        with st.form("form_registro_diario"):

            col_semana, col_fd = st.columns(2)
            with col_semana:
                semana = st.selectbox("Semana", options=list(range(1, 53)),index=0, key="semana_registro_diario")
            with col_fd:
                fecha_minima = datetime.datetime.now().date() - relativedelta(months=1)
                fecha_maxima_hoy = datetime.date.today()
                fecha_minimi_1935 = datetime.date(1935, 1, 1)
                fd = st.date_input("FO (Fecha de ocurrencia)", format="DD/MM/YYYY", min_value=fecha_minimi_1935, 
                                   max_value=fecha_maxima_hoy, key="fd_registro_diario") 

            col_edad, col_sexo = st.columns(2)

            with col_edad:
                edad = st.number_input("Edad (años)", min_value=0, max_value=120, step=1, key="edad_registro_diario")

            with col_sexo:
                sexo = st.selectbox("Sexo", ["M", "F"], key="sexo_registro_diario")

            col_mr, col_mo = st.columns(2)
            with col_mr:
                mr = st.text_input("MR", max_chars=50, key="mr_registro_diario", placeholder="Municipio de residencia")
            with col_mo:
                mo = st.text_input("MO", max_chars=50, key="mo_registro_diario", placeholder="Municipio de ocurrencia")

            col_so, col_cb = st.columns(2)
            with col_so:
                so = st.text_input("SO", max_chars=50, key="so_registro_diario", placeholder="Sitio de ocurrencia")
            with col_cb:
                cb = st.text_input("CB", max_chars=50, key="cb_registro_diario", placeholder="Causa básica")

            col_cd, col_gett = st.columns(2)
            with col_cd:
                cd = st.text_input("CD", max_chars=50, key="cd_registro_diario", placeholder="Causa de directa")
            with col_gett:
                gett = st.text_input("GETT", max_chars=50, key="gett_registro_diario", placeholder="Semanas de gestación")

            nc = st.text_input("NC", max_chars=50, key="nc_registro_diario", placeholder="Número de control de consulta")

            col_izq, col_der = st.columns(2)
            with col_der:
                peso = st.number_input("Peso (kg)", min_value=0.0, step=0.25, format="%.1f", key="peso_registro_diario")
                talla = st.number_input("Talla (cm)", min_value=0.0, step=0.25, format="%.1f", key="talla_registro_diario")
            with col_izq:
                autopsia = st.text_area("Autopsia", max_chars=150, key="autopsia_registro_diario", 
                                        placeholder="Descripción de la autopsia", height=150)

            col_reg, col_limp = st.columns([30, 1])
            with col_reg:
                registrar = st.form_submit_button("Registrar", icon=":material/save:", type="primary")
            with col_limp:
                limpiar = st.form_submit_button("", icon=":material/cleaning_services:", on_click=limpiar_campos_registro_diario, 
                                                type="tertiary", help="Limpia todos los campos del formulario.")
            if registrar:
                if not all([f"{edad},{sexo}", mr, mo, so, cd, cb, gett, nc]):
                    st.error("Por favor completa todos los campos obligatorios.", icon=":material/error:")
                    return
                elif not validar_texto(mr, "El", "MR"):
                    return
                elif not validar_texto(mo, "El", "MO"):
                    return
                elif not validar_texto(so, "El", "SO"):
                    return
                elif not validar_texto(cd, "El", "CD"):
                    return
                elif not validar_texto(cb, "El", "CB"):
                    return
                elif not validar_texto(gett, "El", "GETT"):
                    return
                elif not validar_texto(nc, "El", "NC"):
                    return
                elif peso == 0.0 or talla == 0.0:
                    st.error("El peso y la talla deben ser mayores a 0 para los registros diarios.", icon=":material/error:")
                    return
                elif not val_notas(autopsia, "La", "autopsia"):
                    return
                else:
                    fecha_formateada_nacimiento = fd.strftime("%d/%m/%Y")
                    datos_registro = (
                        semana, fecha_formateada_nacimiento, f"{edad}/{sexo}", mr, mo, so, cb, cd, gett, nc, peso, talla, autopsia,
                        id_doctor, id_administrador, rol_usuario
                    )
                    if operaciones_sql_registro_diario("registrar", datos_registro=datos_registro):
                        st.success("Registro guardado.", icon=":material/check_circle:")
                        st.rerun()

def mostrar_registro_diario():
    logo_bandera = ASSETS_DIR / "imagebanderanueva2.png"
    logo_base64 = img_a_base64(logo_bandera)
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) # Llama a la función para recargar la página una vez.
    logo(tamano="100%")
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a este formulario.", icon=":material/error:")
        return
    tabs = st.tabs(["| :material/calendar_today: Registro Diario |", "| :material/article_shortcut: Reporte Registro Diario |"])
    
    with tabs[0]:
        formulario_registro_diario()
    
    with tabs[1]:
        st.subheader(":material/arrow_circle_down: Descarga de reportes registro diario", anchor=False, divider="gray")
        formulario_reporte_registro_diario()
        st.markdown("")
    copyright_footer_dos("SAMUEL URBANO & GUSTAVO HEREDIA")

if __name__ == "__main__":
    mostrar_registro_diario()