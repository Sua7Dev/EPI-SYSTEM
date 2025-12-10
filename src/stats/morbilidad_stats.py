import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
from datetime import datetime
import locale
import os

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
DB_PATH = os.getenv("hospital.db", "hospital.db")

def convertir_fecha_df(df, columna):
    df[columna] = pd.to_datetime(
        df[columna],
        format="%d/%m/%Y",
        errors="coerce"
    )
    return df


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
            df = pd.read_sql_query("SELECT fecha_registro_formulario FROM morbilidad", conn)

        # Convertir fecha SOLO para cálculos
        df = convertir_fecha_df(df, "fecha_registro_formulario")
        df = df.dropna(subset=["fecha_registro_formulario"])

        df["ano"] = df["fecha_registro_formulario"].dt.year
        df["mes_num"] = df["fecha_registro_formulario"].dt.month
        df["mes"] = df["fecha_registro_formulario"].dt.strftime("%B").str.capitalize()

        df = df[df["ano"] == ano_seleccionado]

        if df.empty:
            return None

        conteo = df.groupby(["mes", "mes_num"]).size().reset_index(name="casos")
        conteo = conteo.sort_values("mes_num")

        mes_maximo = conteo.loc[conteo["casos"].idxmax()]["mes"]

        color = alt.condition(
            alt.datum.mes == mes_maximo,
            alt.value("orange"),
            alt.value("steelblue")
        )

        chart = alt.Chart(conteo).mark_bar().encode(
            x=alt.X("mes:N", title="Mes", sort=None),
            y=alt.Y("casos:Q", title="Número de casos"),
            color=color
        ).properties(
            title=f"Registros de Morbilidad por Mes - {ano_seleccionado}",
            width=600
        )

        return chart

    except sqlite3.Error:
        st.error("Error al generar gráfica por mes", icon=":material/error:")
        return None

def crear_grafica_cumulativa_casos():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query(
                "SELECT fecha_registro_formulario FROM morbilidad WHERE fecha_registro_formulario IS NOT NULL",
                conn
            )

        df = convertir_fecha_df(df, "fecha_registro_formulario")
        df = df.dropna(subset=["fecha_registro_formulario"])

        df = df.sort_values("fecha_registro_formulario")
        df["year"] = df["fecha_registro_formulario"].dt.year
        df["mes"] = df["fecha_registro_formulario"].dt.strftime("%B %Y").str.capitalize()

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
                x=alt.X("mes:O", title="Mes"),
                y=alt.Y("cumulative_count:Q", title="Casos acumulados")
            ).properties(
                title="Conteo acumulativo mensual",
                width=600
            )

        elif opcion == "Anual":
            chart = alt.Chart(df).transform_window(
                cumulative_count="count()",
                sort=[{"field": "year"}]
            ).mark_area().encode(
                x=alt.X("year:O", title="Año"),
                y=alt.Y("cumulative_count:Q", title="Casos acumulados")
            ).properties(
                title="Conteo acumulativo anual",
                width=600
            )

        else:  # Total
            chart = alt.Chart(df).transform_window(
                cumulative_count="count()",
                sort=[{"field": "fecha_registro_formulario"}]
            ).mark_area().encode(
                x=alt.X("fecha_registro_formulario:T", title="Fecha"),
                y=alt.Y("cumulative_count:Q", title="Casos acumulados")
            ).properties(
                title="Total general de casos",
                width=600
            )

        return chart

    except sqlite3.Error:
        st.error("Error al generar la gráfica acumulativa", icon=":material/error:")
        return None

def obtener_edad_promedio():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
                SELECT AVG(pp.edad) AS promedio
                FROM persona_paciente pp
                JOIN morbilidad m ON pp.id_paciente = m.id_paciente
                WHERE pp.edad IS NOT NULL
            """
            result = pd.read_sql_query(query, conn)['promedio'][0]
            return round(result, 1) if result else 0
    except sqlite3.Error:
        st.error("Error al obtener edad promedio", icon=":material/error:")
        return 0

def obtener_anios():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query(
                "SELECT fecha_registro_formulario FROM morbilidad",
                conn
            )

        df = convertir_fecha_df(df, "fecha_registro_formulario")
        df = df.dropna(subset=["fecha_registro_formulario"])

        return sorted(df["fecha_registro_formulario"].dt.year.unique(), reverse=True)

    except sqlite3.Error:
        st.error("Error al obtener años disponibles", icon=":material/error:")
        return []


def mostrar_selector_anio():
    anos = obtener_anios()
    return st.selectbox("Selecciona un año", anos, key="morbilidad_anio_select") if anos else None


def morbilidad_stats():
    col_year, _, col_mes = st.columns([4.9, 0.1, 4.9])

    with col_year:
        st.subheader(":material/healing: Total", anchor=False, divider="gray")
        chart_cumulativa = crear_grafica_cumulativa_casos()
        if chart_cumulativa:
            st.altair_chart(chart_cumulativa, use_container_width=True)

    with col_mes:
        st.subheader(":material/calendar_month: Por año", anchor=False, divider="gray")
        anio = mostrar_selector_anio()
        if anio:
            chart_mes = crear_grafica_por_mes(anio)
            if chart_mes:
                st.altair_chart(chart_mes, use_container_width=True)

    st.markdown("## ")
