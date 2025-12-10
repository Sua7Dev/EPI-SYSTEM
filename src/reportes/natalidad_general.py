import streamlit as st
import datetime
import sqlite3
import os
DB_PATH = os.getenv("hospital.db", "hospital.db")

def formulario_reporte_general_natalidad():
    st.subheader(":material/description: General de Natalidad", anchor=False)
    with st.container():
        try:
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
                cursor.execute("SELECT DISTINCT strftime('%Y', fecha_registro_formulario) FROM natalidad ORDER BY 1 DESC")
                available_years = [int(row[0]) for row in cursor.fetchall() if row[0]]
                conn.close()

                if not available_years:
                    st.error("Sin datos registrados.", icon=":material/error:")
                    return

                year = st.selectbox("Año", available_years, key="year_general_reporte")
                pdf_buffer = 3#exportar_pdf_Natalidad_general(year=year)

            elif timeframe == "Fecha Específica":
                specific_date = st.date_input(
                    "Fecha", 
                    format="DD/MM/YYYY",
                    min_value=datetime.date(2000, 1, 1), 
                    max_value=datetime.date(2050, 12, 31), 
                    key="specific_date_general_reporte"
                )
                pdf_buffer = 2#exportar_pdf_Natalidad_general(specific_date=specific_date)

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
                    pdf_buffer = 1#exportar_pdf_Natalidad_general(start_date=start_date, end_date=end_date)

            if pdf_buffer:
                fecha_actual = datetime.datetime.now()
                fecha_str = fecha_actual.strftime("%d-%m-%Y")
                hora_str = fecha_actual.strftime("%I-%M-%S")
                meridiano = "PM" if fecha_actual.hour >= 12 else "AM"
                fecha_hora_str = f"{fecha_str}_{hora_str}_{meridiano}"

                st.download_button(
                    label="Descargar Reporte",
                    data=pdf_buffer,
                    file_name=f"Reporte_Natalidad_General_{fecha_hora_str}.pdf",
                    mime="application/pdf",
                    icon=":material/download:",
                    key=f"download_general_{fecha_hora_str}_reporte",
                    use_container_width=True,
                    type="primary"
                )

            else:
                st.error("No hay datos para el período seleccionado.", icon=":material/error:")
        except Exception as e:
            st.error(f"Error al generar el reporte: {e}")