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

SEXO_MAP = {
    "Varones": "varones",
    "Hembras": "hembras",
}
TIPO_NATA_MAP = {
    "Partos":    "partos",
    "Cesáreas":  "cesareas",
    "Gemelar":   "gemelar",
    "PEH":       "partos_extrahospitalarios",
    "MTO":       "mto",
}
MESES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}


def parse_fecha_robusta(date_value):
    if pd.isna(date_value) or str(date_value).strip() == '':
        return pd.NaT

    date_str = str(date_value).strip()

    formatos = [
        '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y',
        '%Y-%m-%d', '%Y/%m/%d',
        '%d/%m/%y', '%d-%m-%y',
        '%m/%d/%Y', '%m-%d-%Y',
        '%Y%m%d',
        '%d %b %Y', '%d %B %Y',
        '%d/%b/%Y', '%d-%b-%Y',
        '%d %b %y', '%d %B %y',
        '%b %d, %Y', '%B %d, %Y',
    ]

    for fmt in formatos:
        try:
            return pd.to_datetime(date_str, format=fmt, dayfirst=True)
        except ValueError:
            continue

    try:
        return pd.to_datetime(date_str, dayfirst=True, errors='raise')
    except Exception:
        return pd.NaT


def _consultar_natalidad(year=None, specific_date=None, start_date=None, end_date=None, iso_week=None):
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

        df['fecha_dt'] = df['fecha'].apply(parse_fecha_robusta)
        df["fecha_iso"] = df["fecha_dt"]
        df["iso_year"] = df["fecha_dt"].dt.isocalendar().year
        df["iso_week"] = df["fecha_dt"].dt.isocalendar().week

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


def obtener_anios_disponibles():
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

        return st.selectbox(":material/calendar_today: Año", years, key="nata_year")


    except Exception as e:
        st.error(f"Error al obtener años: {e}", icon=":material/error:")
        return None


def obtener_semanas_por_anio(year):
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


def _defaults_nata():
    for key in [
        "nata_timeframe", "nata_year", "nata_semana_iso",
        "nata_specific_date", "nata_start_date", "nata_end_date",
        "nata_anio_mes", "nata_mes_sel", "nata_gen_sexo", "nata_gen_tipo",
        "nat_columnas_activas", "nat_filtros_label", "nat_sel_sexo", "nat_sel_tipo"
    ]:
        if key in st.session_state:
            del st.session_state[key]


def formulario_reporte_general_natalidad():
    st.subheader(":material/description: General de Natalidad", anchor=False)

    with st.container():
        try:
            timeframe = st.selectbox(
                ":material/calendar_view_day: Seleccionar período",
                ["Todo", "Año", "Año y Mes", "Año y Semana", "Fecha Específica", "Rango de Fechas"],
                key="nata_timeframe"
            )


            year = None
            iso_week = None
            specific_date = None
            start_date = None
            end_date = None
            meses_filtro = []
            pdf_df = None

            if timeframe == "Todo":
                pdf_df = _consultar_natalidad()

            elif timeframe == "Año":
                year = obtener_anios_disponibles()
                if not year:
                    return
                pdf_df = _consultar_natalidad(year=year)

            elif timeframe == "Año y Mes":
                col_y, col_m = st.columns(2)
                with col_y:
                    year = obtener_anios_disponibles()
                if not year:
                    return
                df_temp = _consultar_natalidad(year=year)
                if df_temp is not None and not df_temp.empty:
                    meses_num = sorted(df_temp["fecha_dt"].dt.month.dropna().unique().astype(int).tolist())
                    meses_opts = [MESES_ES[m] for m in meses_num if m in MESES_ES]
                else:
                    meses_opts = list(MESES_ES.values())
                with col_m:
                    meses_filtro = st.multiselect(
                        ":material/calendar_month: Mes(es)",
                        options=meses_opts,
                        placeholder="Todos los meses",
                        key="nata_mes_sel"
                    )

                pdf_df = _consultar_natalidad(year=year)
                if _editor_nata is not None and isinstance(_editor_nata, dict):
                    _sel_nata = [int(i) for i, row in _editor_nata.get("edited_rows", {}).items() if row.get(" ", False)]
                else:    pdf_df = pdf_df[pdf_df["fecha_dt"].dt.month.isin(m_nums)]

            elif timeframe == "Año y Semana":
                col_y, col_s = st.columns(2)
                with col_y:
                    year = obtener_anios_disponibles()
                if not year:
                    return

                semanas = obtener_semanas_por_anio(year)
                if not semanas:
                    st.error("No existen semanas con registros para este año.", icon=":material/error:")
                    return

                with col_s:
                    iso_week = st.selectbox(":material/calendar_view_week: Semana disponible", semanas, key="nata_semana_iso")

                pdf_df = _consultar_natalidad(year=year, iso_week=iso_week)

            elif timeframe == "Fecha Específica":
                specific_date = st.date_input(
                    ":material/event: Fecha",
                    value=datetime.date.today(),
                    format="DD/MM/YYYY",
                    max_value=datetime.date.today(),
                    key="nata_specific_date"
                )

                pdf_df = _consultar_natalidad(specific_date=specific_date)

            else:
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
                        ":material/date_range: Fecha Inicio",
                        value=min_fecha,
                        format="DD/MM/YYYY",
                        max_value=datetime.date.today(),
                        key="nata_start_date"
                    )
                with col_end:
                    end_date = st.date_input(
                        ":material/date_range: Fecha Fin",
                        value=max_fecha,
                        format="DD/MM/YYYY",
                        max_value=datetime.date.today(),
                        key="nata_end_date"
                    )


                if end_date < start_date:
                    st.error("La fecha fin debe ser igual o posterior a la fecha inicio.", icon=":material/error:")
                    return

                pdf_df = _consultar_natalidad(start_date=start_date, end_date=end_date)

            col_sexo, col_tipo = st.columns(2)
            with col_sexo:
                sexo_sel = st.multiselect(
                    ":material/female: :material/male: Sexo",
                    options=list(SEXO_MAP.keys()),
                    default=st.session_state.get("nata_gen_sexo", []),
                    placeholder="Todos (Varones y Hembras)",
                    key="nata_gen_sexo"
                )

            with col_tipo:
                tipo_sel = st.multiselect(
                    ":material/category: Tipo de Natalidad",
                    options=list(TIPO_NATA_MAP.keys()),
                    default=st.session_state.get("nata_gen_tipo", []),
                    placeholder="Todos los tipos",
                    key="nata_gen_tipo"
                )


            # Lógica de filtrado de columnas (Sync con Data Editor y PDF Generator)
            sexo_activo = sexo_sel
            tipo_activo = tipo_sel

            cols_sexo = [SEXO_MAP[s] for s in sexo_activo] if sexo_activo else list(SEXO_MAP.values())
            cols_tipo = [TIPO_NATA_MAP[t] for t in tipo_activo] if tipo_activo else list(TIPO_NATA_MAP.values())
            columnas_activas = list(dict.fromkeys(cols_sexo + cols_tipo))
            
            # Actualizar session_state PARA EL GENERADOR DE PDF
            st.session_state["nat_columnas_activas"] = columnas_activas
            st.session_state["nat_filtros_label"] = {
                "sexo": ", ".join(sexo_sel) if sexo_sel else "Todos",
                "tipo": ", ".join(tipo_sel) if tipo_sel else "Todos"
            }
            
            # Columnas base siempre visibles
            BASE_COLS = ["fecha", "registrado_por"]
            
            if pdf_df is not None and not pdf_df.empty:
                # Asegurar columnas base
                if "registrado_por" not in pdf_df.columns and "id_doctor" in pdf_df.columns:
                    pdf_df["registrado_por"] = pdf_df["id_doctor"]
                
                cols_to_show = [c for c in BASE_COLS if c in pdf_df.columns] + [c for c in columnas_activas if c in pdf_df.columns]
                pdf_df_final = pdf_df[cols_to_show]
            else:
                pdf_df_final = pdf_df

            st.markdown("<br>", unsafe_allow_html=True)
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            with col_f1:
                st.button("Filtrar", icon=":material/search:", use_container_width=True, type="primary", key="nata_gen_btn_filtrar")
            
            if pdf_df_final is not None and not pdf_df_final.empty:
                from utils.filtro import ver_pdf, descargar_pdf
                # Leer selección desde session_state del data_editor
                _editor_nata = st.session_state.get("editor_nata_general")
                if _editor_nata is not None and isinstance(_editor_nata, dict):
                    _sel_nata = [int(i) for i, row in _editor_nata.get("edited_rows", {}).items() if row.get(" ", False)]
                else:
                    _sel_nata = []
                
                _df_export_nata = pdf_df_final.iloc[_sel_nata] if _sel_nata else pdf_df_final
                
                with col_f2:
                    ver_pdf(_df_export_nata, "natalidad_general", key_btn="ver_reporte_general_natalidad")
                with col_f3:
                    descargar_pdf(_df_export_nata, "natalidad_general", label="Descargar Reporte")
            else:
                with col_f2: st.write("")
                with col_f3: st.write("")

            with col_f4:
                st.button("Limpiar filtros", icon=":material/cleaning_services:", use_container_width=True, key="nata_gen_btn_limpiar", on_click=_defaults_nata)

            if pdf_df_final is not None and not pdf_df_final.empty:
                num = len(pdf_df_final)
                if timeframe == "Todo" and not any([sexo_sel, tipo_sel]):
                    st.info(f"Mostrando todos los registros de natalidad disponibles ({num} en total).", icon=":material/info:")
                else:
                    st.info(f"Se encontraron {num} registros de natalidad que coinciden con los filtros aplicados.", icon=":material/filter_alt:")

                # Preparar el dataframe
                df_show_nata = pdf_df_final.copy()
                
                # 1. Definir columnas y orden
                desired_cols = ["fecha", "partos", "cesareas", "varones", "hembras", "gemelar", "mto", "partos_extrahospitalarios", "fecha_registro_formulario", "id"]
                df_show_nata = df_show_nata[[c for c in desired_cols if c in df_show_nata.columns]]

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

                for col in df_show_nata.columns:
                    if col in ["fecha", "fecha_registro_formulario"]:
                        df_show_nata[col] = df_show_nata[col].apply(format_date_robust)
                    elif col in ["partos", "cesareas", "varones", "hembras", "gemelar", "mto", "partos_extrahospitalarios"]:
                        df_show_nata[col] = df_show_nata[col].apply(lambda x: str(int(float(x))) if pd.notnull(x) and x != "" and str(x).replace('.','',1).isdigit() else "Dato no disponible")
                    else:
                        df_show_nata[col] = df_show_nata[col].fillna("Dato no disponible").astype(str).replace(["", "None", "nan", "NaN"], "Dato no disponible")

                if " " not in df_show_nata.columns:
                    df_show_nata.insert(0, " ", False)

                column_config_nata = {
                    " ": st.column_config.CheckboxColumn("✓", default=False),
                    "fecha": st.column_config.TextColumn("Fecha", disabled=True),
                    "partos": st.column_config.TextColumn("Partos", disabled=True),
                    "cesareas": st.column_config.TextColumn("Cesáreas", disabled=True),
                    "varones": st.column_config.TextColumn("Varones", disabled=True),
                    "hembras": st.column_config.TextColumn("Hembras", disabled=True),
                    "gemelar": st.column_config.TextColumn("Gemelar", disabled=True),
                    "mto": st.column_config.TextColumn("MTO", disabled=True),
                    "partos_extrahospitalarios": st.column_config.TextColumn("PEH", disabled=True),
                    "fecha_registro_formulario": st.column_config.TextColumn("Registro Formulario", disabled=True),
                    "id": st.column_config.TextColumn("ID", disabled=True),
                }

                st.data_editor(
                    df_show_nata,
                    use_container_width=True,
                    hide_index=True,
                    column_config=column_config_nata,
                    key="editor_nata_general"
                )
            else:
                st.warning("No hay datos para mostrar con los filtros actuales.", icon=":material/warning:")





        except Exception as e:
            st.error(f"Error al generar el reporte: {e}")

    st.markdown("#")
    st.markdown("#####")
    st.markdown("#")
    st.markdown("#####")