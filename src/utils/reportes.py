import streamlit as st
import datetime
import sqlite3
import os
from reportes.morta_general import consultar_mortalidad_general
DB_PATH = os.getenv("hospital.db", "hospital.db")
from pages.historial import registrar_actividad_duradera
from utils.botones import ver_btn
from utils.filtro import ver_pdf, descargar_pdf

def formulario_reporte_general():
    st.subheader(":material/description: General de Mortalidad", anchor=False)
    with st.container():
        timeframe_key = "timeframe_general_reporte"
        if timeframe_key not in st.session_state:
            st.session_state[timeframe_key] = "Año"

        timeframe = st.selectbox(
            "Seleccionar período",
            ["Año", "Fecha Específica", "Rango de Fechas"], 
            key="mortag", 
            on_change=lambda: st.session_state.update(
                {timeframe_key: st.session_state[timeframe_key]}
            )
        )

        year, specific_date, start_date, end_date = None, None, None, None
        pdf_buffer = None

        # Conexión a DB para obtener fechas de registros y calcular min/max/años de forma robusta
        import pandas as pd
        conn = sqlite3.connect(DB_PATH)
        try:
            df_dates = pd.read_sql_query("SELECT fecha_defuncion FROM mortalidad WHERE fecha_defuncion IS NOT NULL", conn)
        finally:
            conn.close()

        if not df_dates.empty:
            # Convertir a datetime usando pandas (detecta DD/MM/YYYY o YYYY-MM-DD)
            df_dates["fecha_iso"] = pd.to_datetime(df_dates["fecha_defuncion"], dayfirst=True, errors="coerce")
            
            # Eliminar NaT
            valid_dates = df_dates["fecha_iso"].dropna()
            
            if not valid_dates.empty:
                min_fecha = valid_dates.min().date()
                max_fecha = valid_dates.max().date()
                available_years = sorted(valid_dates.dt.year.unique().astype(int), reverse=True)
            else:
                 min_fecha = datetime.date.today()
                 max_fecha = datetime.date.today()
                 available_years = []
        else:
            min_fecha = datetime.date.today()
            max_fecha = datetime.date.today()
            available_years = []

        if timeframe == "Año":
            if not available_years:
                st.error("Sin datos registrados.", icon=":material/error:")
                return

            default_year = max(available_years)
            year = st.selectbox(
                "Año",
                available_years,
                index=available_years.index(default_year),
                key="year_general_reporte"
            )
            pdf_df = consultar_mortalidad_general(year=year)

        elif timeframe == "Fecha Específica":
            specific_date = st.date_input(
                "Fecha",
                value=max_fecha,
                min_value=min_fecha,
                max_value=max_fecha,
                format="DD/MM/YYYY",
                key="specific_date_general_reporte"
            )
            pdf_df = consultar_mortalidad_general(
                specific_date=specific_date
            )

        else:  # Rango de Fechas
            col_start, col_end = st.columns(2)
            with col_start:
                start_date = st.date_input(
                    "Fecha Inicio",
                    value=min_fecha,
                    min_value=min_fecha,
                    max_value=max_fecha,
                    format="DD/MM/YYYY",
                    key="start_date_general_reporte"
                )
            with col_end:
                end_date = st.date_input(
                    "Fecha Fin",
                    value=max_fecha,
                    min_value=min_fecha,
                    max_value=max_fecha,
                    format="DD/MM/YYYY",
                    key="end_date_general_reporte"
                )

            if end_date < start_date:
                st.error(
                    "La fecha fin debe ser igual o posterior a la fecha inicio.",
                    icon=":material/error:"
                )
                return

            pdf_df = consultar_mortalidad_general(
                start_date=start_date,
                end_date=end_date
            )

        # ------------------ BOTONES LAZY (PDF) ------------------
        if pdf_df is not None and not pdf_df.empty:
            
            col_ver, col_descargar = st.columns(2)
            with col_ver:
                ver_pdf(pdf_df, "mortalidad_general", key_btn="ver_reporte_general_morta")

            with col_descargar:
                descargar_pdf(pdf_df, "mortalidad_general", label="Descargar Reporte")

        else:
            st.error(
                "No hay datos para el período seleccionado.",
                icon=":material/error:"
            )

    st.markdown("#")
    st.markdown("#####") 