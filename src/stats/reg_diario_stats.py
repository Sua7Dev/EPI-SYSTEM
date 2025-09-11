import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
import locale
import os
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
DB_PATH = os.environ.get("DB_PATH", "hospital.db")


def total_registros_por_ano():
    """Muestra el total de registros diarios por mes para un año seleccionado"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query("SELECT fd FROM registro_diario WHERE fd IS NOT NULL", conn)
        if df.empty:
            st.info("No hay datos de registro diario disponibles.", icon=":material/warning:")
            return

        df['fd'] = pd.to_datetime(df['fd'], errors='coerce')
        df = df.dropna(subset=['fd'])
        df['year'] = df['fd'].dt.year

        years = sorted(df['year'].unique())
        if not years:
            st.info("No hay años disponibles para mostrar.", icon=":material/warning:")
            return

        selected_year = st.selectbox("Seleccione un año", years, index=len(years)-1, key="selectbox_reg_diario_ano")
        df = df[df['year'] == selected_year]

        # Agrupar por mes
        df['mes'] = df['fd'].dt.to_period('M').dt.to_timestamp()
        total_data = df.groupby('mes').size().reset_index(name='total')
        total_data['mes_es'] = total_data['mes'].dt.strftime("%B %Y").str.capitalize()

        # Gráfico de área
        chart = alt.Chart(total_data).mark_area(
            line={'color': '#1f77b4'},
            color=alt.Gradient(
                gradient='linear',
                stops=[
                    alt.GradientStop(color='white', offset=0),
                    alt.GradientStop(color='#1f77b4', offset=1)
                ],
                x1=1, x2=1, y1=1, y2=0
            )
        ).encode(
            x=alt.X('mes_es:O', title='Mes'),
            y=alt.Y('total:Q', title='Total de Registros Diarios')
        ).properties(
            title=f"Total de Registros Diarios por Mes - {selected_year}"
        )

        st.altair_chart(chart, use_container_width=True)

    except sqlite3.Error:
        st.error("Error al obtener datos de registro diario", icon=":material/error:")


def reg_diario_stats():
    col_izq, col_derecha = st.columns([3, 7])
    with col_izq:
        st.header(":material/medical_services: Total", anchor=False, divider="gray")
        try:
            with sqlite3.connect(DB_PATH) as conn:
                df = pd.read_sql_query("SELECT fd FROM registro_diario WHERE fd IS NOT NULL", conn)
            if df.empty:
                total = 0
            else:
                df['fd'] = pd.to_datetime(df['fd'], errors='coerce')
                df = df.dropna(subset=['fd'])
                total = len(df)
        except sqlite3.Error:
            total = 0
        st.metric(":material/arrow_right: Total Registros", total, border=True)

    with col_derecha:
        st.header(":material/calendar_view_month: Registros por Año", anchor=False, divider="gray")
        total_registros_por_ano()
