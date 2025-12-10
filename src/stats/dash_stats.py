import sqlite3
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import os

DB_PATH = os.getenv("hospital.db", "hospital.db")


def obtener_totales_por_anio():
    """
    Retrieve yearly totals for mortality, natality and morbidity.
    Accepts both 'dd/mm/yyyy' and 'YYYY-MM-DD' formats for old/new records.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
                SELECT 
                    CASE 
                        WHEN fecha_defuncion LIKE '__/__/____' THEN substr(fecha_defuncion, 7, 4)
                        ELSE strftime('%Y', fecha_defuncion)
                    END AS anio,
                    COUNT(*) AS total_mortalidad,
                    0 AS total_natalidad,
                    0 AS total_morbilidad
                FROM mortalidad
                WHERE fecha_defuncion IS NOT NULL
                GROUP BY anio

                UNION ALL

                SELECT 
                    CASE 
                        WHEN fecha LIKE '__/__/____' THEN substr(fecha, 7, 4)
                        ELSE strftime('%Y', fecha)
                    END AS anio,
                    0 AS total_mortalidad,
                    SUM(varones + hembras) AS total_natalidad,
                    0 AS total_morbilidad
                FROM natalidad
                WHERE fecha IS NOT NULL
                GROUP BY anio

                UNION ALL

                SELECT
                    CASE 
                        WHEN fecha_registro_formulario LIKE '__/__/____'
                            THEN substr(fecha_registro_formulario, 7, 4)
                        ELSE substr(fecha_registro_formulario, 1, 4)
                    END AS anio,
                    0 AS total_mortalidad,
                    0 AS total_natalidad,
                    COUNT(*) AS total_morbilidad
                FROM morbilidad
                WHERE fecha_registro_formulario IS NOT NULL
                GROUP BY anio
            """
            df = pd.read_sql_query(query, conn)
            df['anio'] = pd.to_numeric(df['anio'], errors='coerce')
            df = df[df['anio'] > 1900]
            df = df.groupby('anio').sum().reset_index()
            df = df.sort_values('anio')
            return df

    except sqlite3.Error as e:
        st.error(f"Error al obtener totales por año: {e}", icon=":material/error:")
        return pd.DataFrame()


def obtener_top_areas_registro(top_n=3):
    """
    Retrieve the top N areas with the most records
    (Only mortalidad, natalidad, morbilidad).
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM mortalidad")
            total_mortalidad = cursor.fetchone()[0] or 0

            cursor.execute("SELECT SUM(varones + hembras) FROM natalidad")
            total_natalidad = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(*) FROM morbilidad")
            total_morbilidad = cursor.fetchone()[0] or 0

            areas = [
                {'area': 'Mortalidad', 'total': total_mortalidad},
                {'area': 'Natalidad', 'total': total_natalidad},
                {'area': 'Morbilidad', 'total': total_morbilidad}
            ]

            areas = sorted(areas, key=lambda x: x['total'], reverse=True)[:top_n]
            return areas

    except sqlite3.Error as e:
        st.error(f"Error al obtener top áreas: {e}", icon=":material/error:")
        return []


def obtener_totales():
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM mortalidad")
            total_mortalidad = cursor.fetchone()[0] or 0

            cursor.execute("SELECT SUM(varones + hembras) FROM natalidad")
            total_natalidad = cursor.fetchone()[0] or 0

            cursor.execute("SELECT COUNT(*) FROM morbilidad")
            total_morbilidad = cursor.fetchone()[0] or 0

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
