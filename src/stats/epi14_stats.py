import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from utils.sql_control import operaciones_sql_epi14

def promedio_registros_por_ano():
    df = operaciones_sql_epi14("cargar")
    if df is None or df.empty:
        st.info("No hay datos registrados disponibles.",  icon=":material/warning:")
        return

    df['fecha_registro_formulario'] = pd.to_datetime(df['fecha_registro_formulario'], errors='coerce')
    df['year'] = df['fecha_registro_formulario'].dt.year

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('year:O', title='Año'),
        y=alt.Y('mean(numero):Q', title='Promedio de Registros Diarios (epi14)')
    ).properties(
        title='Promedio de Registros Diarios epi14 por Año'
    )

    st.altair_chart(chart, use_container_width=True)

def total_registros_definitivo():
    df = operaciones_sql_epi14("cargar")
    if df is None or df.empty:
        st.info("No hay datos registrados disponibles.",  icon=":material/warning:")
        return

    total_records = df['numero'].sum()

    st.metric(":material/arrow_right: Total", total_records, border=True)

def epi14_stats():
    col_izq, col_derecha = st.columns([7, 3])
    with col_izq:
        st.header(":material/event_note: Promedio por año", anchor=False, divider="gray")
        promedio_registros_por_ano()
        
    with col_derecha:
        st.header(":material/medical_mask: Total", anchor=False, divider="gray")
        total_registros_definitivo()
    st.markdown("# ")