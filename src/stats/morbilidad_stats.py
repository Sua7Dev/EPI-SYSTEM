import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
import locale
import os

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
DB_PATH = os.getenv("hospital.db", "hospital.db")

def obtener_total_casos():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = "SELECT COUNT(*) as total FROM morbilidad"
            return pd.read_sql_query(query, conn)['total'][0]
    except sqlite3.Error:
        st.error("Error al obtener total de casos", icon=":material/error:")
        return 0

def crear_grafica_por_mes(ano_seleccionado):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = "SELECT fecha_registro_formulario FROM morbilidad"
            df = pd.read_sql_query(query, conn)
            df['fecha_registro_formulario'] = pd.to_datetime(df['fecha_registro_formulario'], errors='coerce')
            df['ano'] = df['fecha_registro_formulario'].dt.year
            df['mes'] = df['fecha_registro_formulario'].dt.strftime('%B').str.capitalize()
            df = df[df['ano'] == ano_seleccionado]
            if df.empty:
                return None
            conteo_mensual = df.groupby('mes').size().reset_index(name='casos')
            mes_maximo = conteo_mensual.loc[conteo_mensual['casos'].idxmax()]['mes'] if not conteo_mensual.empty else 'Enero'
            color = alt.condition(
                alt.datum.mes == mes_maximo,
                alt.value('orange'),
                alt.value('steelblue')
            )
            chart = alt.Chart(conteo_mensual).mark_bar().encode(
                x=alt.X('mes:N', title='Mes', sort=['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']),
                y=alt.Y('casos:Q', title='Número de Casos'),
                color=color
            ).properties(
                title=f'Registros de Morbilidad por Mes - {ano_seleccionado}',
                width=600
            )
            return chart
    except sqlite3.Error:
        st.error("Error al generar gráfica", icon=":material/error:")
        return None

def crear_grafica_cumulativa_casos():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = "SELECT fecha_registro_formulario FROM morbilidad WHERE fecha_registro_formulario IS NOT NULL"
            df = pd.read_sql_query(query, conn)
            df['fecha_registro_formulario'] = pd.to_datetime(df['fecha_registro_formulario'], errors='coerce')

            if df.empty or df['fecha_registro_formulario'].isna().all():
                st.info("No hay datos registrados disponibles.", icon=":material/warning:")
                return None

            df = df.sort_values('fecha_registro_formulario')
            df['year'] = df['fecha_registro_formulario'].dt.year
            df['month'] = df['fecha_registro_formulario'].dt.month
            df['mes_es'] = df['fecha_registro_formulario'].dt.strftime("%B %Y").str.capitalize()
            opcion = st.selectbox(
                "Seleccione el tipo de acumulado",
                ["Mensual", "Anual", "Total general"],
                key="selectbox_cumulativo_morbilidad"
            )

            if opcion == "Mensual":
                chart = alt.Chart(df).transform_window(
                    cumulative_count="count()",
                    sort=[{"field": "fecha_registro_formulario"}]
                ).mark_area().encode(
                    x=alt.X("mes_es:O", title="Mes"),
                    y=alt.Y("cumulative_count:Q", title="Casos acumulados", stack=False)
                ).properties(
                    title="Conteo acumulativo mensual de casos de morbilidad",
                    width=600
                )

            elif opcion == "Anual":
                chart = alt.Chart(df).transform_window(
                    cumulative_count="count()",
                    sort=[{"field": "year"}]
                ).mark_area().encode(
                    x=alt.X("year:O", title="Año"),
                    y=alt.Y("cumulative_count:Q", title="Casos acumulados", stack=False)
                ).properties(
                    title="Conteo acumulativo anual de casos de morbilidad",
                    width=600
                )

            else:  # Total general
                chart = alt.Chart(df).transform_window(
                    cumulative_count="count()",
                    sort=[{"field": "fecha_registro_formulario"}]
                ).mark_area().encode(
                    x=alt.X("fecha_registro_formulario:T", title="Fecha"),
                    y=alt.Y("cumulative_count:Q", title="Casos acumulados", stack=False)
                ).properties(
                    title="Total general de casos de morbilidad",
                    width=600
                )

            return chart

    except sqlite3.Error:
        st.error("Error al generar gráfica acumulativa", icon=":material/error:")
        return None


    except sqlite3.Error:
        st.error("Error al generar gráfica acumulativa", icon=":material/error:")
        return None



def obtener_edad_promedio():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = "SELECT AVG(edad) as promedio FROM persona_paciente pp JOIN morbilidad m ON pp.id_paciente = m.id_paciente WHERE pp.edad IS NOT NULL"
            result = pd.read_sql_query(query, conn)['promedio'][0]
            return round(result, 1) if result else 0
    except sqlite3.Error:
        st.error("Error al obtener edad promedio", icon=":material/error:")
        return 0

def obtener_anios():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            anos = sorted(pd.read_sql_query(
                "SELECT DISTINCT strftime('%Y', fecha_registro_formulario) as ano FROM morbilidad WHERE fecha_registro_formulario IS NOT NULL",
                conn
            )['ano'].dropna().astype(int).unique(), reverse=True)
            return anos
    except sqlite3.Error:
        st.error("Error al obtener los años", icon=":material/error:")
        return []

def mostrar_selector_anio():
    anos = obtener_anios()
    anios_seleccionado = st.selectbox(
        "Selecciona un año",
        anos,
        index=0 if anos else None,
        key="morbilidad_anio_select"
    )
    return anios_seleccionado

def morbilidad_stats():
    #_, col_edad, _ = st.columns([1.5, 1.2, 1.5])
    #with col_edad:
    #    st.header(":material/date_range: Edad Promedio", anchor=False, divider="gray")
    #    st.metric(":material/arrow_right: Total", obtener_edad_promedio(), border=True)   

    col_year, _, col_mes = st.columns([4.9, 0.1, 4.9])
    
    with col_year:
        st.header(":material/healing: Total", anchor=False, divider="gray")
        chart_cumulativa = crear_grafica_cumulativa_casos()
        if chart_cumulativa:
            st.altair_chart(chart_cumulativa, use_container_width=True)
    
    with col_mes:
        st.header(":material/calendar_month: Por año", anchor=False, divider="gray")
        anios_seleccionado = mostrar_selector_anio()
        chart_mes = crear_grafica_por_mes(anios_seleccionado)
        if chart_mes:
            st.altair_chart(chart_mes, use_container_width=True)
    st.markdown("## ")
    
