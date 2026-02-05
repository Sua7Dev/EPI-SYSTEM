import streamlit as st
import datetime
import sqlite3
import os
from reportes.morta_general import exportar_pdf_mortalidad_general
DB_PATH = os.getenv("hospital.db", "hospital.db")
from pages.historial import registrar_actividad_duradera

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

        # Conexión a DB para obtener fechas de registros
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT MIN(fecha_registro_formulario),
                   MAX(fecha_registro_formulario)
            FROM mortalidad
            WHERE fecha_registro_formulario IS NOT NULL
            """
        )
        result = cursor.fetchone()
        conn.close()

        min_fecha = (
            datetime.datetime.strptime(result[0], "%Y-%m-%d").date()
            if result and result[0]
            else datetime.date.today()
        )
        max_fecha = (
            datetime.datetime.strptime(result[1], "%Y-%m-%d").date()
            if result and result[1]
            else datetime.date.today()
        )

        if timeframe == "Año":
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT DISTINCT strftime('%Y', fecha_registro_formulario)
                FROM mortalidad
                ORDER BY 1 DESC
                """
            )
            available_years = [int(row[0]) for row in cursor.fetchall() if row[0]]
            conn.close()

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
            pdf_buffer = exportar_pdf_mortalidad_general(year=year)

        elif timeframe == "Fecha Específica":
            specific_date = st.date_input(
                "Fecha",
                value=max_fecha,
                min_value=min_fecha,
                max_value=max_fecha,
                format="DD/MM/YYYY",
                key="specific_date_general_reporte"
            )
            pdf_buffer = exportar_pdf_mortalidad_general(
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

            pdf_buffer = exportar_pdf_mortalidad_general(
                start_date=start_date,
                end_date=end_date
            )

        # ------------------ DESCARGA PDF ------------------
        if pdf_buffer:
            fecha_actual = datetime.datetime.now()
            fecha_str = fecha_actual.strftime("%d-%m-%Y")
            hora_str = fecha_actual.strftime("%I-%M-%S")
            meridiano = "PM" if fecha_actual.hour >= 12 else "AM"
            fecha_hora_str = f"{fecha_str}_{hora_str}_{meridiano}"

            st.download_button(
                label="Descargar Reporte",
                data=pdf_buffer,
                file_name=f"Reporte_Mortalidad_General_{fecha_hora_str}.pdf",
                mime="application/pdf",
                icon=":material/download:",
                key=f"download_general_{fecha_hora_str}_reporte",
                use_container_width=True,
                type="primary",
                on_click=registrar_actividad_duradera,
                args=("DESCARGA PDF", "Reportes Mortalidad")
            )

        else:
            st.error(
                "No hay datos para el período seleccionado.",
                icon=":material/error:"
            )

    st.markdown("#")
    st.markdown("#####") 