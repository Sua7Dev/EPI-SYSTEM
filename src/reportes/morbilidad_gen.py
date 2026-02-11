import streamlit as st
import datetime
import time
import sqlite3
import os
import pandas as pd
from io import BytesIO
from descargas.descarga_morbilidad import exportar_pdf_morbilidad_extensa
from pages.historial import registrar_actividad_duradera
from utils.botones import ver_btn

DB_PATH = os.getenv("hospital.db", "hospital.db")


def _consultar_morbilidad(year=None, specific_date=None, start_date=None, end_date=None):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            where_clauses = []
            params = []

            fecha_iso_expr = """
                CASE
                    WHEN instr(m.fecha_registro_formulario, '/') > 0 AND length(m.fecha_registro_formulario) >= 8
                        THEN substr(m.fecha_registro_formulario, 7, 4) || '-' || substr(m.fecha_registro_formulario, 4, 2) || '-' || substr(m.fecha_registro_formulario, 1, 2)
                    ELSE m.fecha_registro_formulario
                END
            """

            if year:
                where_clauses.append(f"strftime('%Y', date({fecha_iso_expr})) = ?")
                params.append(str(year))
            if specific_date:
                where_clauses.append(f"date({fecha_iso_expr}) = date(?)")
                params.append(specific_date.strftime("%Y-%m-%d"))
            if start_date and end_date:
                where_clauses.append(f"date({fecha_iso_expr}) BETWEEN date(?) AND date(?)")
                params.extend([start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")])

            where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

            query = f"""
                SELECT 
                    m.id_morb AS id,
                    m.id_paciente,
                    m.id_direccion_hogar,
                    m.nombres_apellidos,
                    pp.edad,
                    m.diagnostico,
                    m.fecha_registro_formulario,
                    COALESCE(p.nombre || ', ', '') ||
                    COALESCE(e.nombre || ', ', '') ||
                    COALESCE(c.nombre || ', ', '') ||
                    COALESCE(mu.nombre || ', ', '') ||
                    COALESCE(par.nombre || ', ', '') ||
                    COALESCE(d.descripcion, '') AS direccion_hogar
                FROM morbilidad m
                LEFT JOIN direccion d ON m.id_direccion_hogar = d.id_direccion
                LEFT JOIN parroquia par ON d.id_parroquia = par.id_parroquia
                LEFT JOIN municipio mu ON par.id_municipio = mu.id_municipio
                LEFT JOIN ciudad c ON mu.id_ciudad = c.id_ciudad
                LEFT JOIN estado e ON c.id_estado = e.id_estado
                LEFT JOIN pais p ON e.id_pais = p.id_pais
                LEFT JOIN persona_paciente pp ON m.id_paciente = pp.id_paciente
                {where_sql}
                ORDER BY m.id_morb DESC
            """
            df = pd.read_sql_query(query, conn, params=params)

            # Convertir a datetime usando pandas robusto (detecta DD/MM/YYYY)
            if 'fecha_registro_formulario' in df.columns:
                 df['fecha_iso'] = pd.to_datetime(df['fecha_registro_formulario'], dayfirst=True, errors='coerce')
            
            # Re-filtrar por fechas usando pandas si es necesario (ya que SQL podría no haber filtrado bien sin conversión)
            if start_date and end_date:
                df = df[(df['fecha_iso'].dt.date >= start_date) & (df['fecha_iso'].dt.date <= end_date)]
            if specific_date:
                 df = df[df['fecha_iso'].dt.date == specific_date]
            if year:
                 df = df[df['fecha_iso'].dt.year == int(year)]

            return df
    except Exception:
        return pd.DataFrame()


def exportar_pdf_morbilidad_general(year=None, specific_date=None, start_date=None, end_date=None):
    df = _consultar_morbilidad(
        year=year,
        specific_date=specific_date,
        start_date=start_date,
        end_date=end_date
    )
    nombre_archivo = "Morbilidad"
    return exportar_pdf_morbilidad_extensa(df, nombre_archivo)


def formulario_reporte_general_morbilidad():
    st.subheader(":material/description: General de Morbilidad", anchor=False)

    with st.container():
        try:
            timeframe_key = "timeframe_general_reporte"
            if timeframe_key not in st.session_state:
                st.session_state[timeframe_key] = "Año"

            timeframe = st.selectbox(
                "Seleccionar período",
                ["Año", "Fecha Específica", "Rango de Fechas"],
                key="mortag",
                on_change=lambda: st.session_state.update(
                    {timeframe_key: st.session_state[timeframe_key]}
                )
            )

            year = None
            specific_date = None
            start_date = None
            end_date = None
            pdf_df = None

            # ------------------ AÑO ------------------
            if timeframe == "Año":
                try:
                    with sqlite3.connect(DB_PATH) as conn:
                        df_years = pd.read_sql_query("SELECT fecha_registro_formulario FROM morbilidad", conn)
                    
                    if df_years.empty:
                         available_years = []
                    else:
                        df_years['fecha_iso'] = pd.to_datetime(df_years['fecha_registro_formulario'], dayfirst=True, errors='coerce')
                        available_years = sorted(df_years['fecha_iso'].dt.year.dropna().unique().astype(int), reverse=True)
                        
                except Exception:
                    available_years = []

                if not available_years:
                    st.error("Sin datos registrados.", icon=":material/error:")
                    return

                year = st.selectbox("Año", available_years, key="year_general_reporte")
                pdf_df = _consultar_morbilidad(year=year)

            elif timeframe == "Fecha Específica":
                specific_date = st.date_input(
                    "Fecha",
                    value=datetime.date.today(),
                    format="DD/MM/YYYY",
                    min_value=datetime.date(2000, 1, 1),
                    max_value=datetime.date.today(),
                    key="specific_date_general_reporte"
                )
                pdf_df = _consultar_morbilidad(
                    specific_date=specific_date
                )
            else:
                try:
                    with sqlite3.connect(DB_PATH) as conn:
                        df_fechas = pd.read_sql_query("""
                            SELECT fecha_registro_formulario
                            FROM morbilidad
                            WHERE fecha_registro_formulario IS NOT NULL
                        """, conn)

                    if not df_fechas.empty:
                        df_fechas["fecha_iso"] = pd.to_datetime(
                            df_fechas["fecha_registro_formulario"],
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
                        format="DD/MM/YYYY",
                        max_value=datetime.date.today(),
                        key="start_date_general_reporte"
                    )
                with col_end:
                    end_date = st.date_input(
                        "Fecha Fin",
                        value=max_fecha,
                        format="DD/MM/YYYY",
                        max_value=datetime.date.today(),
                        key="end_date_general_reporte"
                    )

                if end_date < start_date:
                    st.error(
                        "La fecha fin debe ser igual o posterior a la fecha inicio.",
                        icon=":material/error:"
                    )
                    return

                pdf_df = _consultar_morbilidad(
                    start_date=start_date,
                    end_date=end_date
                )


            if pdf_df is not None and not pdf_df.empty:
                from utils.filtro import ver_pdf, descargar_pdf
                col_ver, col_descargar = st.columns(2)
                with col_ver:
                    ver_pdf(pdf_df, "morbilidad", key_btn="ver_reporte_general_morbilidad")

                with col_descargar:
                    descargar_pdf(pdf_df, "morbilidad", label="Descargar Reporte")

            else:
                st.error(
                    "No hay datos para el período seleccionado.",
                    icon=":material/error:"
                )

        except Exception as e:
            st.error(f"Error al generar el reporte: {e}")

    st.markdown("#")
    st.markdown("#####") 
