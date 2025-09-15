import streamlit as st
import datetime
import sqlite3
import os
from reportes.morta_general import exportar_pdf_mortalidad_general
from reportes.morta_mensual_combinado import exportar_pdf_mortalidad_mensual_combinado
from reportes.morta_mensual_general import exportar_pdf_mortalidad_mensual_general
DB_PATH = os.getenv("hospital.db", "hospital.db")

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
            on_change=lambda: st.session_state.update({timeframe_key: st.session_state[timeframe_key]})
        )
        
        year, specific_date, start_date, end_date = None, None, None, None
        pdf_buffer = None

        if timeframe == "Año":
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT strftime('%Y', fecha_registro_formulario) FROM mortalidad ORDER BY 1 DESC")
            available_years = [int(row[0]) for row in cursor.fetchall() if row[0]]
            conn.close()

            if not available_years:
                st.error("Sin datos registrados.", icon=":material/error:")
                return

            year = st.selectbox("Año", available_years, key="year_general_reporte")
            pdf_buffer = exportar_pdf_mortalidad_general(year=year)

        elif timeframe == "Fecha Específica":
            specific_date = st.date_input(
                "Fecha", 
                format="DD/MM/YYYY",
                min_value=datetime.date(2000, 1, 1), 
                max_value=datetime.date(2050, 12, 31), 
                key="specific_date_general_reporte"
            )
            pdf_buffer = exportar_pdf_mortalidad_general(specific_date=specific_date)

        else:  
            col_start, col_end = st.columns(2)
            with col_start:
                start_date = st.date_input(
                    "Fecha Inicio", 
                    format="DD/MM/YYYY", 
                    min_value=datetime.date(2000, 1, 1), 
                    max_value=datetime.date(2050, 12, 31), 
                    key="start_date_general_reporte"
                )
            with col_end:
                end_date = st.date_input(
                    "Fecha Fin", 
                    format="DD/MM/YYYY", 
                    min_value=datetime.date(2000, 1, 1), 
                    max_value=datetime.date(2050, 12, 31), 
                    value=datetime.date.today(), 
                    key="end_date_general_reporte"
                )
            if end_date >= start_date:
                pdf_buffer = exportar_pdf_mortalidad_general(start_date=start_date, end_date=end_date)

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
                type="primary"
            )

        else:
            st.error("No hay datos para el período seleccionado.", icon=":material/error:")
            
def formulario_reporte_mensual_combinado():
    st.subheader(":material/description: Infantil y Neonatal mensual", anchor=False)
    with st.container():
        timeframe_key = "timeframe_mensual_combinado"
        if timeframe_key not in st.session_state:
            st.session_state[timeframe_key] = "Año"

        timeframe = st.selectbox(
            "Seleccionar período",
            ["Año", "Fecha Específica", "Rango de Fechas"], 
            key="mortac", 
            on_change=lambda: st.session_state.update({timeframe_key: st.session_state[timeframe_key]})
        )
        
        year, month, specific_date, start_date, end_date = None, None, None, None, None
        pdf_buffer = None
        
        if timeframe == "Año":
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT strftime('%Y', fecha_registro_formulario) FROM mortalidad ORDER BY 1 DESC")
            available_years = [int(row[0]) for row in cursor.fetchall() if row[0]]
            conn.close()

            if not available_years:
                st.error("Sin datos registrados.", icon=":material/error:")
                return

            col_year, col_month = st.columns(2)
            with col_year:
                year = st.selectbox("Año", available_years, key="year_mensual_combinado")
            with col_month:
                month = st.selectbox(
                    "Mes", 
                    list(range(1, 13)), 
                    format_func=lambda x: datetime.date(2023, x, 1).strftime('%B'), 
                    key="month_mensual_combinado"
                )
            pdf_buffer = exportar_pdf_mortalidad_mensual_combinado(year=year, month=month)

        elif timeframe == "Fecha Específica":
            specific_date = st.date_input(
                "Fecha", 
                format="DD/MM/YYYY", 
                min_value=datetime.date(2000, 1, 1), 
                max_value=datetime.date(2050, 12, 31), 
                key="specific_date_mensual_combinado"
            )
            pdf_buffer = exportar_pdf_mortalidad_mensual_combinado(specific_date=specific_date)

        else:
            col_start, col_end = st.columns(2)
            with col_start:
                start_date = st.date_input(
                    "Fecha Inicio", 
                    format="DD/MM/YYYY", 
                    min_value=datetime.date(2000, 1, 1), 
                    max_value=datetime.date(2050, 12, 31), 
                    key="start_date_mensual_combinado"
                )
            with col_end:
                end_date = st.date_input(
                    "Fecha Fin", 
                    format="DD/MM/YYYY", 
                    min_value=datetime.date(2000, 1, 1), 
                    max_value=datetime.date(2050, 12, 31), 
                    value=datetime.date.today(), 
                    key="end_date_mensual_combinado"
                )
            if end_date >= start_date:
                pdf_buffer = exportar_pdf_mortalidad_mensual_combinado(start_date=start_date, end_date=end_date)

        if pdf_buffer:
            fecha_actual = datetime.datetime.now()
            fecha_str = fecha_actual.strftime("%d-%m-%Y")
            hora_str = fecha_actual.strftime("%I-%M-%S")
            meridiano = "PM" if fecha_actual.hour >= 12 else "AM"
            fecha_hora_str = f"{fecha_str}_{hora_str}_{meridiano}"

            st.download_button(
                label="Descargar Reporte",
                data=pdf_buffer,
                file_name=f"Reporte_Mortalidad_Mensual_Combinado_{fecha_hora_str}.pdf",
                mime="application/pdf",
                icon=":material/download:",
                key=f"download_mensual_combinado_{fecha_hora_str}",
                use_container_width=True,
                type="primary"
            )

        else:
            st.error("No hay datos para el período seleccionado.", icon=":material/error:")


def formulario_reporte_mensual_general():
    st.subheader(":material/description: Mensual General", anchor=False)
    with st.container():
        timeframe_key = "timeframe_mensual_general"
        if timeframe_key not in st.session_state:
            st.session_state[timeframe_key] = "Año"

        timeframe = st.selectbox(
            "Seleccionar período",
            ["Año", "Fecha Específica", "Rango de Fechas"], 
            key="morrtagg", 
            on_change=lambda: st.session_state.update({timeframe_key: st.session_state[timeframe_key]})
        )
        
        year, month, specific_date, start_date, end_date = None, None, None, None, None
        pdf_buffer = None
        
        if timeframe == "Año":
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT strftime('%Y', fecha_registro_formulario) FROM mortalidad ORDER BY 1 DESC")
            available_years = [int(row[0]) for row in cursor.fetchall() if row[0]]
            conn.close()

            if not available_years:
                st.error("Sin datos registrados.", icon=":material/error:")
                return

            col_year, col_month = st.columns(2)
            with col_year:
                year = st.selectbox("Año", available_years, key="year_mensual_general")
            with col_month:
                month = st.selectbox(
                    "Mes", 
                    list(range(1, 13)), 
                    format_func=lambda x: datetime.date(2023, x, 1).strftime('%B'), 
                    key="month_mensual_general"
                )
            pdf_buffer = exportar_pdf_mortalidad_mensual_general(year=year, month=month)

        elif timeframe == "Fecha Específica":
            specific_date = st.date_input(
                "Fecha", 
                format="DD/MM/YYYY", 
                min_value=datetime.date(2000, 1, 1), 
                max_value=datetime.date(2050, 12, 31), 
                key="specific_date_mensual_general"
            )
            pdf_buffer = exportar_pdf_mortalidad_mensual_general(specific_date=specific_date)

        else:
            col_start, col_end = st.columns(2)
            with col_start:
                start_date = st.date_input(
                    "Fecha Inicio", 
                    format="DD/MM/YYYY", 
                    min_value=datetime.date(2000, 1, 1), 
                    max_value=datetime.date(2050, 12, 31), 
                    key="start_date_mensual_general"
                )
            with col_end:
                end_date = st.date_input(
                    "Fecha Fin", 
                    format="DD/MM/YYYY", 
                    min_value=datetime.date(2000, 1, 1), 
                    max_value=datetime.date(2050, 12, 31), 
                    value=datetime.date.today(), 
                    key="end_date_mensual_general"
                )
            if end_date >= start_date:
                pdf_buffer = exportar_pdf_mortalidad_mensual_general(start_date=start_date, end_date=end_date)

        if pdf_buffer:
            fecha_actual = datetime.datetime.now()
            fecha_str = fecha_actual.strftime("%d-%m-%Y")
            hora_str = fecha_actual.strftime("%I-%M-%S")
            meridiano = "PM" if fecha_actual.hour >= 12 else "AM"
            fecha_hora_str = f"{fecha_str}_{hora_str}_{meridiano}"

            st.download_button(
                label="Descargar Reporte",
                data=pdf_buffer,
                file_name=f"Reporte_Mortalidad_Mensual_General_{fecha_hora_str}.pdf",
                mime="application/pdf",
                icon=":material/download:",
                key=f"download_mensual_general_{fecha_hora_str}",
                use_container_width=True,
                type="primary"
            )
        else:
            st.error("No hay datos para el período seleccionado.", icon=":material/error:")