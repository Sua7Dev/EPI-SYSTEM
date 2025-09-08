import sqlite3
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import os

DB_PATH = os.environ.get("AUTH_DB_PATH", "hospital.db")

def obtener_totales_por_anio():
    """
    Retrieve yearly totals for mortality, natality, morbidity, epi14_semanal, and registro_diario.
    Uses specific date fields for each table with appropriate year extraction based on date format:
    - 'dd/mm/yyyy' format: substr(date_field, 7, 4)
    - 'YYYY-MM-DD' format: strftime('%Y', date_field)
    Returns a DataFrame with yearly totals.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
                SELECT 
                    substr(fecha_defuncion, 7, 4) AS anio,
                    COUNT(*) AS total_mortalidad,
                    0 AS total_natalidad,
                    0 AS total_morbilidad,
                    0 AS total_epi14,
                    0 AS total_registro_diario
                FROM mortalidad
                WHERE fecha_defuncion IS NOT NULL AND length(fecha_defuncion) = 10
                GROUP BY substr(fecha_defuncion, 7, 4)
                UNION ALL
                SELECT 
                    substr(fecha, 7, 4) AS anio,
                    0 AS total_mortalidad,
                    SUM(varones + hembras) AS total_natalidad,
                    0 AS total_morbilidad,
                    0 AS total_epi14,
                    0 AS total_registro_diario
                FROM natalidad
                WHERE fecha IS NOT NULL AND length(fecha) = 10
                GROUP BY substr(fecha, 7, 4)
                UNION ALL
                SELECT 
                    strftime('%Y', fecha_registro_formulario) AS anio,
                    0 AS total_mortalidad,
                    0 AS total_natalidad,
                    COUNT(*) AS total_morbilidad,
                    0 AS total_epi14,
                    0 AS total_registro_diario
                FROM morbilidad
                WHERE fecha_registro_formulario IS NOT NULL
                GROUP BY strftime('%Y', fecha_registro_formulario)
                UNION ALL
                SELECT 
                    strftime('%Y', fecha_registro_formulario) AS anio,
                    0 AS total_mortalidad,
                    0 AS total_natalidad,
                    0 AS total_morbilidad,
                    SUM(numero) AS total_epi14,
                    0 AS total_registro_diario
                FROM epi14_semanal
                WHERE fecha_registro_formulario IS NOT NULL
                GROUP BY strftime('%Y', fecha_registro_formulario)
                UNION ALL
                SELECT 
                    substr(fd, 7, 4) AS anio,
                    0 AS total_mortalidad,
                    0 AS total_natalidad,
                    0 AS total_morbilidad,
                    0 AS total_epi14,
                    COUNT(*) AS total_registro_diario
                FROM registro_diario
                WHERE fd IS NOT NULL AND length(fd) = 10
                GROUP BY substr(fd, 7, 4)
            """
            df = pd.read_sql_query(query, conn)
            # Aggregate by year, summing all columns, and filter out invalid years
            df = df.groupby('anio').sum().reset_index()
            df = df[df['anio'].str.isdigit() & (df['anio'].astype(int) > 1900)]  # Filter valid years
            df = df.sort_values('anio')
            return df
    except sqlite3.Error as e:
        st.error(f"Error al obtener totales por año: {e}", icon=":material/error:")
        return pd.DataFrame()

def obtener_top_areas_registro(top_n=3):
    """
    Retrieve the top N areas with the most records across all categories.
    Returns a list of dictionaries with area names and their totals.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # Total mortality (count of records in mortalidad table)
            cursor.execute("SELECT COUNT(*) FROM mortalidad")
            total_mortalidad = cursor.fetchone()[0] or 0

            # Total natality (sum of varones and hembras in natalidad table)
            cursor.execute("SELECT SUM(varones + hembras) FROM natalidad")
            total_natalidad = cursor.fetchone()[0] or 0

            # Total morbidity (count of records in morbilidad table)
            cursor.execute("SELECT COUNT(*) FROM morbilidad")
            total_morbilidad = cursor.fetchone()[0] or 0

            # Total epi14 (sum of numero in epi14_semanal table)
            cursor.execute("SELECT SUM(numero) FROM epi14_semanal")
            total_epi14 = cursor.fetchone()[0] or 0

            # Total registro_diario (count of records in registro_diario table)
            cursor.execute("SELECT COUNT(*) FROM registro_diario")
            total_registro_diario = cursor.fetchone()[0] or 0

            # Create list of areas and their totals
            areas = [
                {'area': 'Mortalidad', 'total': total_mortalidad},
                {'area': 'Natalidad', 'total': total_natalidad},
                {'area': 'Morbilidad', 'total': total_morbilidad},
                {'area': 'EPI14-Semanal', 'total': total_epi14},
                {'area': 'Registro Diario', 'total': total_registro_diario}
            ]
            # Sort by total in descending order and take top N
            areas = sorted(areas, key=lambda x: x['total'], reverse=True)[:top_n]
            return areas
    except sqlite3.Error as e:
        st.error(f"Error al obtener top áreas: {e}", icon=":material/error:")
        return []


def obtener_totales():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            # Total mortality (count of records in mortalidad table)
            cursor.execute("SELECT COUNT(*) FROM mortalidad")
            total_mortalidad = cursor.fetchone()[0] or 0

            # Total natality (sum of varones and hembras in natalidad table)
            cursor.execute("SELECT SUM(varones + hembras) FROM natalidad")
            total_natalidad = cursor.fetchone()[0] or 0

            # Total morbidity (count of records in morbilidad table)
            cursor.execute("SELECT COUNT(*) FROM morbilidad")
            total_morbilidad = cursor.fetchone()[0] or 0

            # Total general (sum of mortality, natality, and morbidity)
            total_general = total_mortalidad + total_natalidad + total_morbilidad

            return {
                'total_general': total_general,
                'total_mortalidad': total_mortalidad,
                'total_natalidad': total_natalidad,
                'total_morbilidad': total_morbilidad
            }
    except sqlite3.Error as e:
        st.error(f"Error al calcular totales: {e}", icon=":material/error:")
        return {
            'total_general': 0,
            'total_mortalidad': 0,
            'total_natalidad': 0,
            'total_morbilidad': 0
        }