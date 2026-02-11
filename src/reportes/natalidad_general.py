import streamlit as st
import datetime
import datetime
import sqlite3
import time
import os
import pandas as pd
from io import BytesIO
from descargas.descarga_natalidad import _exportar_pdf_natalidad
from pages.historial import registrar_actividad_duradera
DB_PATH = os.getenv("hospital.db", "hospital.db")
DATE_FORMAT = "DD/MM/YYYY"
from utils.botones import ver_btn

# ===============================================================
# CONSULTAS PRINCIPALES
# ===============================================================

def _consultar_natalidad(year=None, specific_date=None, start_date=None, end_date=None, iso_week=None):
    """Consulta los registros de natalidad, calcula semanas ISO y filtra según los parámetros"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            query = """
                SELECT
                    id_nata AS id,
                    fecha,
                    partos,
                    cesareas,
                    varones,
                    hembras,
                    gemelar,
                    mto,
                    partos_extrahospitalarios,
                    id_doctor,
                    fecha_registro_formulario
                FROM natalidad
            """
            df = pd.read_sql_query(query, conn)

        if df.empty:
            return df

        # Convertir fecha a datetime usando pandas directamente (más robusto)
        df["fecha_iso"] = pd.to_datetime(df["fecha"], dayfirst=True, errors="coerce")

        # Calcular semana y año ISO
        df["iso_year"] = df["fecha_iso"].dt.isocalendar().year
        df["iso_week"] = df["fecha_iso"].dt.isocalendar().week

        # Aplicar filtros
        if year:
            df = df[df["iso_year"] == int(year)]
        if iso_week:
            df = df[df["iso_week"] == int(iso_week)]
        if specific_date:
            df = df[df["fecha_iso"] == pd.to_datetime(specific_date)]
        if start_date and end_date:
            df = df[(df["fecha_iso"] >= pd.to_datetime(start_date)) & (df["fecha_iso"] <= pd.to_datetime(end_date))]

        return df

    except Exception:
        return pd.DataFrame()


def exportar_pdf_natalidad_general(year=None, specific_date=None, start_date=None, end_date=None, iso_week=None):
    df = _consultar_natalidad(year=year, specific_date=specific_date, start_date=start_date, end_date=end_date, iso_week=iso_week)
    nombre_archivo = "Natalidad_General"
    return _exportar_pdf_natalidad(df, nombre_archivo)


# ===============================================================
# FUNCIONES DE APOYO PARA FILTROS
# ===============================================================

def obtener_anios_disponibles():
    """Devuelve los años que tienen registros, usando pandas para consistencia ISO"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query("""
                SELECT fecha
                FROM natalidad
                WHERE fecha IS NOT NULL
            """, conn)
        if df.empty:
            st.error("Sin datos registrados.", icon=":material/error:")
            return None
        df["fecha_iso"] = pd.to_datetime(df["fecha"], dayfirst=True, errors="coerce")
        years = sorted(df["fecha_iso"].dt.isocalendar().year.dropna().unique(), reverse=True)
        if not years:
            st.error("Sin datos registrados.", icon=":material/error:")
            return None
        return st.selectbox("Año", years, key="year_general_reporte_natalidad")
    except Exception:
        st.error("Error al obtener años disponibles.", icon=":material/error:")
        return None


def obtener_semanas_por_anio(year):
    """Devuelve una lista de semanas ISO reales que existen para el año"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query("""
                SELECT fecha
                FROM natalidad
                WHERE fecha IS NOT NULL
            """, conn)
        if df.empty:
            return []

        df["fecha_iso"] = pd.to_datetime(df["fecha"], dayfirst=True, errors="coerce")
        df = df[df["fecha_iso"].dt.isocalendar().year == int(year)]
        semanas = sorted(df["fecha_iso"].dt.isocalendar().week.dropna().unique())
        return semanas
    except Exception:
        return []


# ===============================================================
# FORMULARIO DE REPORTES
# ===============================================================

def formulario_reporte_general_natalidad():
    st.subheader(":material/description: General de Natalidad", anchor=False)
    with st.container():
        try:
            timeframe = st.selectbox(
                "Seleccionar período",
                ["Año", "Año y Semana", "Fecha Específica", "Rango de Fechas"],
                key="natalidad_timeframe"
            )

            year = None
            iso_week = None
            specific_date = None
            start_date = None
            end_date = None
            pdf_buffer = None

            # ----------------------------
            # FILTRO POR AÑO
            # ----------------------------
            pdf_df = None

            # ----------------------------
            # FILTRO POR AÑO
            # ----------------------------
            if timeframe == "Año":
                year = obtener_anios_disponibles()
                if not year:
                    return
                pdf_df = _consultar_natalidad(year=year)

            # ----------------------------
            # FILTRO POR AÑO + SEMANA ISO
            # ----------------------------
            elif timeframe == "Año y Semana":
                year = obtener_anios_disponibles()
                if not year:
                    return

                semanas = obtener_semanas_por_anio(year)
                if not semanas:
                    st.error(
                        "No existen semanas con registros para este año.",
                        icon=":material/error:"
                    )
                    return

                iso_week = st.selectbox(
                    "Semana disponible",
                    semanas,
                    key="semana_iso"
                )
                pdf_df = _consultar_natalidad(
                    year=year,
                    iso_week=iso_week
                )

            # ----------------------------
            # FECHA ESPECÍFICA
            # ----------------------------
            elif timeframe == "Fecha Específica":
                specific_date = st.date_input(
                    "Fecha",
                    value=datetime.date.today(),
                    format=DATE_FORMAT,
                    max_value=datetime.date.today()
                )
                pdf_df = _consultar_natalidad(
                    specific_date=specific_date
                )

            # ----------------------------
            # RANGO DE FECHAS
            # ----------------------------
            else:
                try:
                    with sqlite3.connect(DB_PATH) as conn:
                        df_fechas = pd.read_sql_query("""
                            SELECT fecha
                            FROM natalidad
                            WHERE fecha IS NOT NULL
                        """, conn)

                    if not df_fechas.empty:
                        df_fechas["fecha_iso"] = pd.to_datetime(
                            df_fechas["fecha"],
                            dayfirst=True,
                            errors="coerce"
                        )
                        min_fecha = df_fechas["fecha_iso"].min().date()
                        max_fecha = df_fechas["fecha_iso"].max().date()
                    else:
                        min_fecha = datetime.date.today() - datetime.timedelta(days=30)
                        max_fecha = datetime.date.today()
                except Exception:
                    min_fecha = datetime.date.today() - datetime.timedelta(days=30)
                    max_fecha = datetime.date.today()

                col_start, col_end = st.columns(2)
                with col_start:
                    start_date = st.date_input(
                        "Fecha Inicio",
                        value=min_fecha,
                        format=DATE_FORMAT,
                        max_value=datetime.date.today()
                    )
                with col_end:
                    end_date = st.date_input(
                        "Fecha Fin",
                        value=max_fecha,
                        format=DATE_FORMAT,
                        max_value=datetime.date.today()
                    )

                if end_date < start_date:
                    st.error(
                        "La fecha fin debe ser igual o posterior a la fecha inicio.",
                        icon=":material/error:"
                    )
                    return

                pdf_df = _consultar_natalidad(
                    start_date=start_date,
                    end_date=end_date
                )

            # ----------------------------
            # BOTONES LAZY (PDF)
            # ----------------------------
            if pdf_df is not None and not pdf_df.empty:
                from utils.filtro import ver_pdf, descargar_pdf
                col_ver, col_descargar = st.columns(2)
                with col_ver:
                    ver_pdf(pdf_df, "natalidad_general", key_btn="ver_reporte_general_natalidad")

                with col_descargar:
                    descargar_pdf(pdf_df, "natalidad_general", label="Descargar Reporte")

            else:
                st.error(
                    "No hay datos para el período seleccionado.",
                    icon=":material/error:"
                )

        except Exception as e:
            st.error(f"Error al generar el reporte: {e}")

    st.markdown("#")
    st.markdown("#####") 
