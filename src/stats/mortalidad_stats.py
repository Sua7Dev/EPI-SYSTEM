import streamlit as st
import sqlite3
import pandas as pd
import altair as alt
import locale
from datetime import datetime, timedelta
import os
DB_PATH = os.getenv("hospital.db", "hospital.db")

def morta_growth_chart():
    """Gráfica del crecimiento de registros de mortalidad"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
                SELECT SUBSTR(m.fecha_defuncion, 7, 4) AS year, 
                    COUNT(*) AS record_count
                FROM mortalidad m
                WHERE m.fecha_defuncion IS NOT NULL 
                AND (EXISTS (SELECT 1 FROM mortalidad_materna mm WHERE mm.id_m = m.id_m)
                    OR EXISTS (SELECT 1 FROM mortalidad_infantil mi WHERE mi.id_m = m.id_m)
                    OR EXISTS (SELECT 1 FROM mortalidad_neonatal mn WHERE mn.id_m = m.id_m))
                GROUP BY year
                ORDER BY year
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            st.info("No hay registros de mortalidad para mostrar.",  icon=":material/warning:")
            return

        df['year'] = df['year'].astype(str)
        
        chart = alt.Chart(df).mark_area(
            color="lightblue",
            interpolate='step-after',
            line=True
        ).encode(
            x=alt.X('year:N', title='Año', axis=alt.Axis(labelAngle=45)),
            y=alt.Y('record_count:Q', title='Número de Registros'),
            tooltip=[alt.Tooltip('year:N', title='Año'), 
                     alt.Tooltip('record_count:Q', title='Registros')]
        ).properties(
            width=300,
            height=280
        )

        st.altair_chart(chart, use_container_width=True)

    except sqlite3.Error as e:
        st.error(f"Error al acceder a la base de datos: {e}", icon=":material/error:")
    except Exception as e:
        st.error(f"Error para generar la gráfica: {e}", icon=":material/error:")


def morta_categ_pie_chart():
    """Gráfico circular de categorías de mortalidad"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
                SELECT 'Maternal' AS category, COUNT(*) AS record_count
                FROM mortalidad_materna
                UNION ALL
                SELECT 'Infantil' AS category, COUNT(*) AS record_count
                FROM mortalidad_infantil
                UNION ALL
                SELECT 'Neonatal' AS category, COUNT(*) AS record_count
                FROM mortalidad_neonatal
            """
            df = pd.read_sql_query(query, conn)

        df = df[df['record_count'] > 0]
        if df.empty:
            st.info("No hay registros por categoría para mostrar.",  icon=":material/warning:")
            return
        
        base = alt.Chart(df).encode(
            theta=alt.Theta("record_count:Q", stack=True, title="Registros"),
            color=alt.Color("category:N", title="Categoría")
        )

        pie = base.mark_arc(outerRadius=120)
        text = base.mark_text(radius=140, size=14).encode(text="category:N")

        chart = (pie + text).properties(
            width=300,
            height=280
        ).configure_view(
            strokeWidth=0
        )

        st.altair_chart(chart, use_container_width=True)

    except sqlite3.Error as e:
        st.error(f"Error al acceder a la base de datos: {e}", icon=":material/error:")
    except Exception as e:
        st.error(f"Error para generar la gráfica: {e}", icon=":material/error:")


def morta_ultimo_ano_chart():
    """Gráfica de registros de mortalidad por año seleccionado con meses en español y filas por categoría estilo 'stocks'"""
    try:
        try:
            locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
        except:
            try:
                locale.setlocale(locale.LC_TIME, "es_ES")
            except:
                try:
                    locale.setlocale(locale.LC_TIME, "Spanish_Spain")
                except:
                    pass  

        with sqlite3.connect(DB_PATH) as conn:
            query_years = """
                SELECT DISTINCT SUBSTR(m.fecha_defuncion, 7, 4) AS year
                FROM mortalidad m
                WHERE m.fecha_defuncion IS NOT NULL
                ORDER BY year DESC
            """
            df_years = pd.read_sql_query(query_years, conn)
            if df_years.empty:
                st.info("No hay registros de mortalidad disponibles.", icon=":material/warning:")
                return

            years = df_years["year"].dropna().astype(int).tolist()

            selected_year = st.selectbox("Seleccione un año", years)

            start_date = f"{selected_year}-01-01"
            end_date = f"{selected_year}-12-31"

            query = """
                SELECT 'Maternal' AS categoria, 
                    strftime('%Y-%m', SUBSTR(m.fecha_defuncion, 7, 4) || '-' || 
                                                SUBSTR(m.fecha_defuncion, 4, 2) || '-' || 
                                                SUBSTR(m.fecha_defuncion, 1, 2)) AS ym, 
                    COUNT(*) AS cantidad
                FROM mortalidad_materna mm
                JOIN mortalidad m ON mm.id_m = m.id_m
                WHERE m.fecha_defuncion IS NOT NULL 
                AND (SUBSTR(m.fecha_defuncion, 7, 4) || '-' || 
                    SUBSTR(m.fecha_defuncion, 4, 2) || '-' || 
                    SUBSTR(m.fecha_defuncion, 1, 2)) BETWEEN ? AND ?
                GROUP BY ym
                UNION ALL
                SELECT 'Infantil' AS categoria, 
                    strftime('%Y-%m', SUBSTR(m.fecha_defuncion, 7, 4) || '-' || 
                                                SUBSTR(m.fecha_defuncion, 4, 2) || '-' || 
                                                SUBSTR(m.fecha_defuncion, 1, 2)) AS ym, 
                    COUNT(*) AS cantidad
                FROM mortalidad_infantil mi
                JOIN mortalidad m ON mi.id_m = m.id_m
                WHERE m.fecha_defuncion IS NOT NULL 
                AND (SUBSTR(m.fecha_defuncion, 7, 4) || '-' || 
                    SUBSTR(m.fecha_defuncion, 4, 2) || '-' || 
                    SUBSTR(m.fecha_defuncion, 1, 2)) BETWEEN ? AND ?
                GROUP BY ym
                UNION ALL
                SELECT 'Neonatal' AS categoria, 
                    strftime('%Y-%m', SUBSTR(m.fecha_defuncion, 7, 4) || '-' || 
                                                SUBSTR(m.fecha_defuncion, 4, 2) || '-' || 
                                                SUBSTR(m.fecha_defuncion, 1, 2)) AS ym, 
                    COUNT(*) AS cantidad
                FROM mortalidad_neonatal mn
                JOIN mortalidad m ON mn.id_m = m.id_m
                WHERE m.fecha_defuncion IS NOT NULL 
                AND (SUBSTR(m.fecha_defuncion, 7, 4) || '-' || 
                    SUBSTR(m.fecha_defuncion, 4, 2) || '-' || 
                    SUBSTR(m.fecha_defuncion, 1, 2)) BETWEEN ? AND ?
                GROUP BY ym
            """

            df = pd.read_sql_query(query, conn, params=(start_date, end_date, start_date, end_date, start_date, end_date))

        if df.empty:
            st.info(f"No hay registros de mortalidad para el año {selected_year}.", icon=":material/warning:")
            return

        df["month"] = pd.to_datetime(df["ym"], format="%Y-%m")
        df["mes_es"] = df["month"].dt.strftime("%B %Y").str.capitalize()

        chart = alt.Chart(df).mark_area().encode(
            x=alt.X("mes_es:O", title="Mes"),   
            y="cantidad:Q",
            color="categoria:N",
            row=alt.Row("categoria:N").sort(["Maternal", "Infantil", "Neonatal"])
        ).properties(
            height=50,
            width=400,
            title=f"Mortalidad por Mes - {selected_year}"
        )

        st.altair_chart(chart, use_container_width=True)

    except sqlite3.Error as e:
        st.error(f"Error al acceder a la base de datos: {e}", icon=":material/error:")
    except Exception as e:
        st.error(f"Error para generar la gráfica: {e}", icon=":material/error:")


def mortalidad_general():
    """Sección general con todas las gráficas"""
    col_casos, col_categoria = st.columns([6, 4])
    with col_casos:
        st.subheader(":material/line_axis: Crecimiento", anchor=False)#, divider="gray"
        morta_growth_chart()
    with col_categoria:
        st.subheader(":material/tv_options_edit_channels: Categorías", anchor=False)#, divider="gray"
        morta_categ_pie_chart()
    _, col_ultimo_ano, _ = st.columns([0.37, 2.8, 1.07])
    with col_ultimo_ano:
        st.subheader(":material/event_note: Por año", anchor=False)#, divider="gray"
        morta_ultimo_ano_chart()


def mortalidad_stats():
    mortalidad_general()
