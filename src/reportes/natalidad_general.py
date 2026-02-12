import streamlit as st
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
# FUNCIÓN AUXILIAR PARA PARSEO ROBUSTO DE FECHAS
# ===============================================================
def parse_fecha_robusta(date_value):
    """
    Intenta parsear la fecha de múltiples formatos comunes.
    Devuelve pd.Timestamp o pd.NaT si no puede.
    """
    if pd.isna(date_value) or str(date_value).strip() == '':
        return pd.NaT
    
    date_str = str(date_value).strip()

    # Formatos más comunes primero
    formatos = [
        '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y',             # 25/12/2023
        '%Y-%m-%d', '%Y/%m/%d',                         # 2023-12-25
        '%d/%m/%y', '%d-%m-%y',                         # 25/12/23
        '%m/%d/%Y', '%m-%d-%Y',                         # americano
        '%Y%m%d',                                       # 20231225
        '%d %b %Y', '%d %B %Y',                         # 25 dic 2023
        '%d/%b/%Y', '%d-%b-%Y',                         # 25/dic/2023
        '%d %b %y', '%d %B %y',
        '%b %d, %Y', '%B %d, %Y',                       # Dec 25, 2023
    ]

    for fmt in formatos:
        try:
            return pd.to_datetime(date_str, format=fmt, dayfirst=True)
        except ValueError:
            continue

    # Último intento: dejar que pandas infiera (con preferencia día primero)
    try:
        return pd.to_datetime(date_str, dayfirst=True, errors='raise')
    except Exception:
        return pd.NaT


# ===============================================================
# CONSULTAS PRINCIPALES
# ===============================================================

def _consultar_natalidad(year=None, specific_date=None, start_date=None, end_date=None, iso_week=None):
    """Consulta los registros de natalidad, parsea fechas de forma robusta y filtra"""
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

        # ────────────────────────────────────────────────
        # PARSEO ROBUSTO DE LA COLUMNA 'fecha'
        # ────────────────────────────────────────────────
        df['fecha_dt'] = df['fecha'].apply(parse_fecha_robusta)

        # Para compatibilidad con el resto del código: columna auxiliar iso
        df["fecha_iso"] = df["fecha_dt"]

        # Calcular semana y año ISO (usando la fecha parseada correctamente)
        df["iso_year"] = df["fecha_dt"].dt.isocalendar().year
        df["iso_week"] = df["fecha_dt"].dt.isocalendar().week

        # Aplicar filtros
        if year:
            df = df[df["iso_year"] == int(year)]
        if iso_week:
            df = df[df["iso_week"] == int(iso_week)]
        if specific_date:
            specific_dt = parse_fecha_robusta(specific_date)
            if pd.notna(specific_dt):
                df = df[df["fecha_dt"].dt.date == specific_dt.date()]
        if start_date and end_date:
            start_dt = parse_fecha_robusta(start_date)
            end_dt = parse_fecha_robusta(end_date)
            if pd.notna(start_dt) and pd.notna(end_dt):
                df = df[(df["fecha_dt"] >= start_dt) & (df["fecha_dt"] <= end_dt)]

        return df

    except Exception as e:
        st.error(f"Error en consulta de natalidad: {e}")
        return pd.DataFrame()


def exportar_pdf_natalidad_general(year=None, specific_date=None, start_date=None, end_date=None, iso_week=None):
    df = _consultar_natalidad(
        year=year,
        specific_date=specific_date,
        start_date=start_date,
        end_date=end_date,
        iso_week=iso_week
    )
    nombre_archivo = "Natalidad_General"
    return _exportar_pdf_natalidad(df, nombre_archivo)


# ===============================================================
# FUNCIONES DE APOYO PARA FILTROS
# ===============================================================

def obtener_anios_disponibles():
    """Devuelve los años disponibles según fechas parseadas correctamente"""
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

        df['fecha_dt'] = df['fecha'].apply(parse_fecha_robusta)
        df = df[df['fecha_dt'].notna()]
        
        if df.empty:
            st.error("Sin fechas válidas registradas.", icon=":material/error:")
            return None

        years = sorted(df["fecha_dt"].dt.isocalendar().year.dropna().unique(), reverse=True)
        if not years:
            st.error("Sin datos válidos registrados.", icon=":material/error:")
            return None

        return st.selectbox("Año", years, key="year_general_reporte_natalidad")

    except Exception as e:
        st.error(f"Error al obtener años: {e}", icon=":material/error:")
        return None


def obtener_semanas_por_anio(year):
    """Devuelve semanas ISO reales para el año seleccionado"""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query("""
                SELECT fecha
                FROM natalidad
                WHERE fecha IS NOT NULL
            """, conn)
        
        if df.empty:
            return []

        df['fecha_dt'] = df['fecha'].apply(parse_fecha_robusta)
        df = df[df['fecha_dt'].notna()]
        df = df[df["fecha_dt"].dt.isocalendar().year == int(year)]
        
        semanas = sorted(df["fecha_dt"].dt.isocalendar().week.dropna().unique())
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
            pdf_df = None

            # FILTRO POR AÑO
            if timeframe == "Año":
                year = obtener_anios_disponibles()
                if not year:
                    return
                pdf_df = _consultar_natalidad(year=year)

            # FILTRO POR AÑO + SEMANA ISO
            elif timeframe == "Año y Semana":
                year = obtener_anios_disponibles()
                if not year:
                    return

                semanas = obtener_semanas_por_anio(year)
                if not semanas:
                    st.error("No existen semanas con registros para este año.", icon=":material/error:")
                    return

                iso_week = st.selectbox("Semana disponible", semanas, key="semana_iso")
                pdf_df = _consultar_natalidad(year=year, iso_week=iso_week)

            # FECHA ESPECÍFICA
            elif timeframe == "Fecha Específica":
                specific_date = st.date_input(
                    "Fecha",
                    value=datetime.date.today(),
                    format="DD/MM/YYYY",
                    max_value=datetime.date.today()
                )
                pdf_df = _consultar_natalidad(specific_date=specific_date)

            # RANGO DE FECHAS
            else:
                # Intentar obtener rango real de fechas válidas
                try:
                    with sqlite3.connect(DB_PATH) as conn:
                        df_fechas = pd.read_sql_query("SELECT fecha FROM natalidad WHERE fecha IS NOT NULL", conn)

                    if not df_fechas.empty:
                        df_fechas['fecha_dt'] = df_fechas['fecha'].apply(parse_fecha_robusta)
                        df_fechas = df_fechas[df_fechas['fecha_dt'].notna()]
                        df_fechas = df_fechas[df_fechas["fecha_dt"] <= pd.Timestamp.now()]

                        if not df_fechas.empty:
                            min_fecha = df_fechas["fecha_dt"].min().date()
                            max_fecha = df_fechas["fecha_dt"].max().date()
                        else:
                            min_fecha = datetime.date.today() - datetime.timedelta(days=30)
                            max_fecha = datetime.date.today()
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
                        format="DD/MM/YYYY",
                        max_value=datetime.date.today()
                    )
                with col_end:
                    end_date = st.date_input(
                        "Fecha Fin",
                        value=max_fecha,
                        format="DD/MM/YYYY",
                        max_value=datetime.date.today()
                    )

                if end_date < start_date:
                    st.error("La fecha fin debe ser igual o posterior a la fecha inicio.", icon=":material/error:")
                    return

                pdf_df = _consultar_natalidad(start_date=start_date, end_date=end_date)

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
                st.error("No hay datos para el período seleccionado.", icon=":material/error:")

        except Exception as e:
            st.error(f"Error al generar el reporte: {e}")

    st.markdown("#")
    st.markdown("#####")