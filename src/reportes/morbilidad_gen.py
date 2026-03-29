import streamlit as st
import datetime
import time
import sqlite3
import os
import unicodedata
import pandas as pd
from io import BytesIO
from descargas.descarga_morbilidad import exportar_pdf_morbilidad_extensa
from pages.historial import registrar_actividad_duradera

from utils.botones import ver_btn
from utils.validaciones import bloquear_caracteres

DB_PATH = os.getenv("hospital.db", "hospital.db")

MESES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}


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

            if 'fecha_registro_formulario' in df.columns:
                from utils.validaciones import parse_fecha_robusta
                df['fecha_iso'] = df['fecha_registro_formulario'].apply(parse_fecha_robusta)

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


def _defaults_morbi():
    for key in [
        "morbi_timeframe", "morbi_year", "morbi_specific_date",
        "morbi_start_date", "morbi_end_date",
        "morbi_anio_mes", "morbi_mes_sel",
        "gen_morbi_nombre", "gen_morbi_diag", "gen_morbi_edad_select"
    ]:
        if key in st.session_state:
            del st.session_state[key]


def formulario_reporte_general_morbilidad():
    st.subheader(":material/description: General de Morbilidad", anchor=False)

    with st.container():
        try:
            timeframe = st.selectbox(
                ":material/calendar_view_day: Seleccionar período",
                ["Todo", "Año", "Año y Mes", "Fecha Específica", "Rango de Fechas"],
                key="morbi_timeframe"
            )


            year = None
            specific_date = None
            start_date = None
            end_date = None
            meses_filtro = []
            pdf_df = None

            if timeframe == "Todo":
                pdf_df = _consultar_morbilidad()

            elif timeframe == "Año":
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

                year = st.selectbox(":material/calendar_today: Año", available_years, key="morbi_year")

                pdf_df = _consultar_morbilidad(year=year)

            elif timeframe == "Año y Mes":
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

                col_y, col_m = st.columns(2)
                with col_y:
                    year = st.selectbox(":material/calendar_today: Año", available_years, key="morbi_anio_mes")


                df_temp = _consultar_morbilidad(year=year)
                if df_temp is not None and not df_temp.empty:
                    meses_num = sorted(df_temp["fecha_iso"].dt.month.dropna().unique().astype(int).tolist())
                    meses_opts = [MESES_ES[m] for m in meses_num if m in MESES_ES]
                else:
                    meses_opts = list(MESES_ES.values())

                with col_m:
                    meses_filtro = st.multiselect(
                        ":material/calendar_month: Mes(es)",
                        options=meses_opts,
                        placeholder="Todos los meses",
                        key="morbi_mes_sel"
                    )


                pdf_df = _consultar_morbilidad(year=year)
                if meses_filtro and pdf_df is not None and not pdf_df.empty:
                    m_nums = [k for k, v in MESES_ES.items() if v in meses_filtro]
                    pdf_df = pdf_df[pdf_df["fecha_iso"].dt.month.isin(m_nums)]

            elif timeframe == "Fecha Específica":
                specific_date = st.date_input(
                    ":material/event: Fecha",
                    value=datetime.date.today(),
                    format="DD/MM/YYYY",
                    min_value=datetime.date(2000, 1, 1),
                    max_value=datetime.date.today(),
                    key="morbi_specific_date"
                )

                pdf_df = _consultar_morbilidad(specific_date=specific_date)

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
                        umbral_futuro = pd.Timestamp.now() + pd.Timedelta(days=1)
                        df_fechas = df_fechas[df_fechas["fecha_iso"] <= umbral_futuro]

                        if not df_fechas.empty:
                            min_fecha = df_fechas["fecha_iso"].min().date()
                            max_fecha = df_fechas["fecha_iso"].max().date()
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
                        ":material/date_range: Fecha Inicio",
                        value=min_fecha,
                        format="DD/MM/YYYY",
                        max_value=datetime.date.today(),
                        key="morbi_start_date"
                    )
                with col_end:
                    end_date = st.date_input(
                        ":material/date_range: Fecha Fin",
                        value=max_fecha,
                        format="DD/MM/YYYY",
                        max_value=datetime.date.today(),
                        key="morbi_end_date"
                    )


                if end_date < start_date:
                    st.error(
                        "La fecha fin debe ser igual o posterior a la fecha inicio.",
                        icon=":material/error:"
                    )
                    return

                pdf_df = _consultar_morbilidad(start_date=start_date, end_date=end_date)

            col_nom, col_diag, col_edad = st.columns(3)
            with col_nom:
                nombre_busq = st.text_input(
                    ":material/person: Nombres y Apellidos",
                    placeholder="Ej. Juan Pérez",
                    max_chars=40,
                    key="gen_morbi_nombre"
                )

                bloquear_caracteres(
                    caracteres=list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~--^"),
                    tipo_de_input="text",
                    max_chars=40,
                    label="Nombres y Apellidos"
                )
            with col_diag:
                diag_busq = st.text_input(
                    ":material/medical_services: Diagnóstico",
                    placeholder="Ej. Asma",
                    max_chars=150,
                    key="gen_morbi_diag"
                )

                bloquear_caracteres(
                    caracteres=list("!@#$%¨&*_=+[]{}:;\"\\|<>?`~^°¡¿§±←→•#"),
                    tipo_de_input="text",
                    max_chars=150,
                    label="Diagnóstico"
                )
            with col_edad:
                if pdf_df is not None and not pdf_df.empty and "edad" in pdf_df.columns:
                    if pd.api.types.is_numeric_dtype(pdf_df["edad"]):
                        valores_edad = sorted([int(x) for x in pdf_df["edad"].dropna().unique()])
                    else:
                        valores_edad = sorted(pdf_df["edad"].dropna().unique().tolist())
                else:
                    valores_edad = []

                edad_options = ["Todos"] + valores_edad
                
                edad_sel = st.selectbox(
                    ":material/cake: Edad",
                    options=edad_options,
                    index=0,
                    key="gen_morbi_edad_select"
                )


            st.markdown("<br>", unsafe_allow_html=True)
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            with col_f1:
                st.button("Filtrar", icon=":material/search:", use_container_width=True, type="primary", key="gen_morbi_btn_filtrar")

            nombre_activo = nombre_busq
            diag_activo = diag_busq
            edad_activa = edad_sel

            def normalizar(texto):
                if not isinstance(texto, str):
                    return ""
                t = texto.lower()
                return ''.join(c for c in unicodedata.normalize('NFKD', t) if unicodedata.category(c) != 'Mn')

            with col_f4:
                st.button("Limpiar filtros", icon=":material/cleaning_services:", use_container_width=True, key="gen_morbi_btn_limpiar", on_click=_defaults_morbi)

            if pdf_df is not None and not pdf_df.empty:
                df_cat = pdf_df.copy()

                if nombre_activo:
                    bn = normalizar(nombre_activo)
                    df_cat = df_cat[df_cat["nombres_apellidos"].astype(str).apply(normalizar).str.contains(bn, na=False)]

                if diag_activo:
                    bd = normalizar(diag_activo)
                    df_cat = df_cat[df_cat["diagnostico"].astype(str).apply(normalizar).str.contains(bd, na=False)]

                if edad_activa != "Todos":
                    df_cat = df_cat[df_cat["edad"] == edad_activa]

                from utils.filtro import ver_pdf, descargar_pdf
                if not df_cat.empty:
                    # Leer selección desde session_state del data_editor
                    _editor_morbi = st.session_state.get("editor_morbi_general")
                    if _editor_morbi is not None and isinstance(_editor_morbi, dict):
                        _sel_morbi = [int(i) for i, row in _editor_morbi.get("edited_rows", {}).items() if row.get(" ", False)]
                    else:
                        _sel_morbi = []
                    _df_export_morbi = df_cat.iloc[_sel_morbi] if _sel_morbi else df_cat
                    with col_f2:
                        ver_pdf(_df_export_morbi, "morbilidad", key_btn="ver_reporte_general_morbilidad")
                    with col_f3:
                        descargar_pdf(_df_export_morbi, "morbilidad", label="Descargar Reporte")
                    
                    num = len(df_cat)
                    if timeframe == "Todo" and not any([nombre_activo, diag_activo, edad_activa != "Todos"]):
                        st.info(f"Mostrando todos los registros de morbilidad disponibles ({num} en total).", icon=":material/info:")
                    else:
                        st.info(f"Se encontraron {num} registros de morbilidad que coinciden con los filtros aplicados.", icon=":material/filter_alt:")

                    # Preparar el dataframe
                    df_show_morbi = df_cat.copy()
                    
                    # 1. Columnas deseadas y orden
                    desired_cols = ["nombres_apellidos", "edad", "diagnostico", "direccion_hogar", "fecha_registro_formulario", "id"]
                    df_show_morbi = df_show_morbi[[c for c in desired_cols if c in df_show_morbi.columns]]

                    # 2. Formatear y manejar nulos
                    def format_date_robust(val):
                        if pd.isna(val) or val == "" or str(val).lower() in ["none", "nat", "nan"]:
                            return "Dato no disponible"
                        try:
                            dt = pd.to_datetime(val, dayfirst=True, errors='coerce')
                            if pd.notnull(dt):
                                return dt.strftime('%d/%m/%Y')
                            return "Dato no disponible"
                        except:
                            return "Dato no disponible"

                    for col in df_show_morbi.columns:
                        if col == "fecha_registro_formulario":
                            df_show_morbi[col] = df_show_morbi[col].apply(format_date_robust)
                        elif col == "edad":
                             df_show_morbi[col] = df_show_morbi[col].apply(lambda x: str(int(float(x))) if pd.notnull(x) and x != "" and str(x).replace('.','',1).isdigit() else "Dato no disponible")
                        else:
                            df_show_morbi[col] = df_show_morbi[col].fillna("Dato no disponible").astype(str).replace(["", "None", "nan", "NaN"], "Dato no disponible")

                    if " " not in df_show_morbi.columns:
                        df_show_morbi.insert(0, " ", False)

                    column_config_morbi = {
                        " ": st.column_config.CheckboxColumn("✓", default=False),
                        "nombres_apellidos": st.column_config.TextColumn("Nombres y Apellidos", disabled=True),
                        "edad": st.column_config.TextColumn("Edad", disabled=True),
                        "diagnostico": st.column_config.TextColumn("Diagnóstico", disabled=True),
                        "direccion_hogar": st.column_config.TextColumn("Dirección", disabled=True),
                        "fecha_registro_formulario": st.column_config.TextColumn("Registro Formulario", disabled=True),
                        "id": st.column_config.TextColumn("ID", disabled=True),
                    }

                    edited_df_morbi = st.data_editor(
                        df_show_morbi,
                        use_container_width=True,
                        hide_index=True,
                        column_config=column_config_morbi,
                        key="editor_morbi_general"
                    )
                else:
                    with col_f2: st.write("")
                    with col_f3: st.write("")
                    st.warning("No hay datos para los filtros seleccionados.", icon=":material/warning:")
            else:
                with col_f2: st.write("")
                with col_f3: st.write("")
                st.error("No hay datos para el período seleccionado.", icon=":material/error:")



        except Exception as e:
            st.error(f"Error al generar el reporte: {e}")

    st.markdown("#")
    st.markdown("#####")
