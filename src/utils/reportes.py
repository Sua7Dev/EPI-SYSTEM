import streamlit as st
import datetime
import sqlite3
import os
import unicodedata
import pandas as pd
from reportes.morta_general import consultar_mortalidad_general
DB_PATH = os.getenv("hospital.db", "hospital.db")
from pages.historial import registrar_actividad_duradera
from utils.botones import ver_btn
from utils.filtro import ver_pdf, descargar_pdf
from utils.validaciones import bloquear_caracteres

TIPOS_MORTALIDAD = ["Neonatal", "Infantil", "Materna"]

MESES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}


def limpiar_filtros_morta():
    for key in [
        "morta_timeframe", "morta_year", "morta_specific_date",
        "morta_start_date", "morta_end_date", "morta_filtro_aplicado",
        "morta_mes_sel", "morta_anio_mes", "morta_tipos_multiselect",
        "morta_hc", "morta_nombre", "morta_madre", "morta_idx_ing", "morta_idx_def",
        "morta_edad_meta", "morta_sem_meta", "morta_ord_neo"
    ]:
        if key in st.session_state:
            del st.session_state[key]


def formulario_reporte_general():
    st.subheader(":material/description: General de Mortalidad", anchor=False)
    with st.container():
        timeframe = st.selectbox(
            ":material/calendar_view_day: Seleccionar período",
            ["Todo", "Año", "Año y Mes", "Fecha Específica", "Rango de Fechas"],
            key="morta_timeframe"
        )


        year, specific_date, start_date, end_date = None, None, None, None
        meses_filtro = []

        conn = sqlite3.connect(DB_PATH)
        try:
            df_dates = pd.read_sql_query(
                "SELECT fecha_defuncion FROM mortalidad WHERE fecha_defuncion IS NOT NULL", conn
            )
        finally:
            conn.close()

        if not df_dates.empty:
            df_dates["fecha_iso"] = pd.to_datetime(df_dates["fecha_defuncion"], dayfirst=True, errors="coerce")
            valid_dates = df_dates["fecha_iso"].dropna()
            if not valid_dates.empty:
                min_fecha = valid_dates.min().date()
                max_fecha = valid_dates.max().date()
                available_years = sorted(valid_dates.dt.year.unique().astype(int), reverse=True)
            else:
                min_fecha = datetime.date.today()
                max_fecha = datetime.date.today()
                available_years = []
        else:
            min_fecha = datetime.date.today()
            max_fecha = datetime.date.today()
            available_years = []

        if timeframe == "Año":
            if not available_years:
                st.error("Sin datos registrados.", icon=":material/error:")
                return
            year = st.selectbox(
                ":material/calendar_today: Año",
                available_years,
                index=0,
                key="morta_year"
            )


        elif timeframe == "Año y Mes":
            if not available_years:
                st.error("Sin datos registrados.", icon=":material/error:")
                return
            col_y, col_m = st.columns(2)
            with col_y:
                year = st.selectbox(":material/calendar_today: Año", available_years, index=0, key="morta_anio_mes")

            df_temp = consultar_mortalidad_general(year=year)
            if df_temp is not None and not df_temp.empty:
                df_temp["_fecha_iso"] = pd.to_datetime(df_temp["fecha_defuncion"], dayfirst=True, errors="coerce")
                meses_num = sorted(df_temp["_fecha_iso"].dt.month.dropna().unique().astype(int).tolist())
                meses_opts = [MESES_ES[m] for m in meses_num if m in MESES_ES]
            else:
                meses_opts = list(MESES_ES.values())
            with col_m:
                meses_filtro = st.multiselect(
                    ":material/calendar_month: Mes(es)",
                    options=meses_opts,
                    placeholder="Todos los meses",
                    key="morta_mes_sel"
                )


        elif timeframe == "Fecha Específica":
            specific_date = st.date_input(
                ":material/event: Fecha",
                value=max_fecha,
                min_value=min_fecha,
                max_value=max_fecha,
                format="DD/MM/YYYY",
                key="morta_specific_date"
            )


        elif timeframe == "Rango de Fechas":
            col_start, col_end = st.columns(2)
            with col_start:
                start_date = st.date_input(
                    ":material/date_range: Fecha Inicio",
                    value=min_fecha,
                    min_value=min_fecha,
                    max_value=max_fecha,
                    format="DD/MM/YYYY",
                    key="morta_start_date"
                )
            with col_end:
                end_date = st.date_input(
                    ":material/date_range: Fecha Fin",
                    value=max_fecha,
                    min_value=min_fecha,
                    max_value=max_fecha,
                    format="DD/MM/YYYY",
                    key="morta_end_date"
                )

            if end_date < start_date:
                st.error(
                    "La fecha fin debe ser igual o posterior a la fecha inicio.",
                    icon=":material/error:"
                )
                return

        # Pre-consultar datos para las opciones de los filtros
        pdf_df = consultar_mortalidad_general(year=year, specific_date=specific_date, start_date=start_date, end_date=end_date)
        if pdf_df is not None and not pdf_df.empty and timeframe == "Año y Mes" and meses_filtro:
            pdf_df["_mes_iso"] = pd.to_datetime(pdf_df["fecha_defuncion"], dayfirst=True, errors="coerce")
            m_nums = [k for k, v in MESES_ES.items() if v in meses_filtro]
            pdf_df = pdf_df[pdf_df["_mes_iso"].dt.month.isin(m_nums)].drop(columns=["_mes_iso"])

        # --- CONSTRUCCIÓN DINÁMICA DE FILTROS ---
        hc_busq, nom_busq, madre_busq, idx_ing_busq, idx_def_busq = "", "", "", "", ""
        edad_sel_val, sem_sel_val, sort_elegido = "Todos", "Todos", "Sin orden"

        # 0. Tipo de Mortalidad
        def render_tipos():
            st.multiselect(
                ":material/category: Tipo de Mortalidad",
                options=TIPOS_MORTALIDAD,
                default=st.session_state.get("morta_tipos_multiselect", []),
                placeholder="Todos (Neonatal, Infantil y Materna)",
                key="morta_tipos_multiselect"
            )


        # 1. Historia Clínica (Común a Todos)
        def render_hc():
            nonlocal hc_busq
            hc_busq = st.text_input(":material/assignment: Historia Clínica", placeholder="Ej. 12345678", max_chars=8, key="morta_hc")
            bloquear_caracteres(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑüÜ!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-- "), "text", 8, "Historia Clínica")


        # 2. Nombre del paciente (Común a Todos)
        def render_nombre():
            nonlocal nom_busq
            nom_busq = st.text_input(":material/person: Nombre del paciente", placeholder="Ej. Juan Pérez", max_chars=40, key="morta_nombre")
            bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~--^"), "text", 40, "Nombre del paciente")


        # 3. Edad (Común a Todos)
        def render_edad():
            nonlocal edad_sel_val
            v_e = sorted(pdf_df["edad"].dropna().astype(str).unique().tolist()) if pdf_df is not None and not pdf_df.empty and "edad" in pdf_df.columns else []
            edad_sel_val = st.selectbox(":material/cake: Edad", options=["Todos"] + v_e, key="morta_edad_meta")


        # 4. Nombre de la madre (Para tags individuales)
        def render_madre():
            nonlocal madre_busq
            madre_busq = st.text_input(":material/female: Nombre de la madre", placeholder="Ej. María García", max_chars=40, key="morta_madre")
            bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~--^"), "text", 40, "Nombre de la madre")


        def render_vacio():
            st.write("")

        tipos_activos = st.session_state.get("morta_tipos_multiselect", [])
        if not tipos_activos: tipos_activos = TIPOS_MORTALIDAD

        # Posicionamiento de "Tipo de Mortalidad"
        if tipos_activos == ["Materna"]:
            componentes = [render_tipos]
        else:
            render_tipos()
            componentes = []

        # Filtros exclusivos dependiendo de los tags
        if tipos_activos == ["Neonatal"]:
            def render_sem():
                nonlocal sem_sel_val
                v_s = sorted(pdf_df["semanas_gestacion"].dropna().unique().tolist()) if pdf_df is not None and not pdf_df.empty and "semanas_gestacion" in pdf_df.columns else []
                sem_sel_val = st.selectbox(":material/pregnant_woman: Semanas Gestación", options=["Todos"] + v_s, key="morta_sem_meta")

            
            def render_orden():
                nonlocal sort_elegido
                opc = ["Sin orden", "Peso: Menor a mayor ↑", "Peso: Mayor a menor ↓", "Talla: Menor a mayor ↑", "Talla: Mayor a menor ↓"]
                sort_elegido = st.selectbox(":material/sort: Ordenar por", opc, key="morta_ord_neo")


            componentes.extend([render_hc, render_nombre, render_madre, render_sem, render_edad, render_orden])
            
        elif tipos_activos == ["Infantil"]:
            # Edad abajo pero en medio: Row 1 (HC, Nombre, Madre), Row 2 (VACIO, Edad, VACIO)
            componentes.extend([render_hc, render_nombre, render_madre, render_vacio, render_edad, render_vacio])

        elif tipos_activos == ["Materna"]:
            def render_dx_ing():
                nonlocal idx_ing_busq
                idx_ing_busq = st.text_input(":material/medical_services: Diagnóstico de ingreso", placeholder="Ej. I10", max_chars=50, key="morta_idx_ing")
                bloquear_caracteres(list("!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~--^"), "text", 50, "Diagnóstico de ingreso")


            def render_dx_def():
                nonlocal idx_def_busq
                idx_def_busq = st.text_input(":material/medical_services: Diagnóstico de defunción", placeholder="Ej. I21", max_chars=50, key="morta_idx_def")
                bloquear_caracteres(list("!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~--^"), "text", 50, "Diagnóstico de defunción")


            componentes.extend([render_hc, render_nombre, render_dx_ing, render_dx_def, render_edad])

        else:
            # All or mixed selected, common fields only!
            componentes.extend([render_hc, render_nombre, render_edad])

        # Mostrar componentes en un grid balanceado de 3 columnas
        for i in range(0, len(componentes), 3):
            chunk = [componentes[k] for k in range(i, min(i+3, len(componentes)))]
            cols = st.columns(3)
            for j, render_func in enumerate(chunk):
                with cols[j]:
                    render_func()


        def norm(t):
            if not isinstance(t, str):
                return ""
            return ''.join(c for c in unicodedata.normalize('NFKD', t.lower()) if unicodedata.category(c) != 'Mn')

        if pdf_df is not None and not pdf_df.empty:
            pdf_df_final = pdf_df.copy()
            pdf_df_final = pdf_df_final[pdf_df_final["tipo"].isin(tipos_activos)]
            
            if hc_busq and "historia_clinica" in pdf_df_final.columns:
                pdf_df_final = pdf_df_final[pdf_df_final["historia_clinica"].astype(str).str.contains(hc_busq, na=False)]
            if nom_busq and "nombres_apellidos" in pdf_df_final.columns:
                pdf_df_final = pdf_df_final[pdf_df_final["nombres_apellidos"].astype(str).apply(norm).str.contains(norm(nom_busq), na=False)]
            if madre_busq and "nombre_madre" in pdf_df_final.columns:
                pdf_df_final = pdf_df_final[pdf_df_final["nombre_madre"].astype(str).apply(norm).str.contains(norm(madre_busq), na=False)]
            if edad_sel_val != "Todos" and "edad" in pdf_df_final.columns:
                pdf_df_final = pdf_df_final[pdf_df_final["edad"].astype(str) == str(edad_sel_val)]
            if sem_sel_val != "Todos" and "semanas_gestacion" in pdf_df_final.columns:
                pdf_df_final = pdf_df_final[pdf_df_final["semanas_gestacion"] == sem_sel_val]
            if idx_ing_busq and "idx_ingreso" in pdf_df_final.columns:
                pdf_df_final = pdf_df_final[pdf_df_final["idx_ingreso"].astype(str).apply(norm).str.contains(norm(idx_ing_busq), na=False)]
            if idx_def_busq and "idx_defuncion" in pdf_df_final.columns:
                pdf_df_final = pdf_df_final[pdf_df_final["idx_defuncion"].astype(str).apply(norm).str.contains(norm(idx_def_busq), na=False)]

            if sort_elegido != "Sin orden":
                col = "peso" if sort_elegido.startswith("Peso") else "talla"
                if col in pdf_df_final.columns:
                    pdf_df_final["_s"] = pd.to_numeric(pdf_df_final[col], errors="coerce")
                    pdf_df_final = pdf_df_final.sort_values("_s", ascending="Menor" in sort_elegido).drop(columns=["_s"])
        else:
            pdf_df_final = pd.DataFrame()

        st.markdown("<br>", unsafe_allow_html=True)
        col_f_filt, col_f_ver, col_f_desc, col_f_limp = st.columns(4)
        with col_f_filt:
            st.button("Filtrar", icon=":material/search:", use_container_width=True, type="primary", key="morta_btn_filtrar")
        
        if not pdf_df_final.empty:
            # Leer selección desde session_state del data_editor
            _editor_state = st.session_state.get("editor_morta_general")
            if _editor_state is not None and isinstance(_editor_state, dict):
                try:
                    # Las claves en edited_rows son strings, castear a int
                    _sel_indices = [int(i) for i, row in _editor_state.get("edited_rows", {}).items() if row.get(" ", False)]
                except Exception:
                    _sel_indices = []
            else:
                _sel_indices = []
            
            _df_export_morta = pdf_df_final.iloc[_sel_indices] if _sel_indices else pdf_df_final
            
            with col_f_ver:
                ver_pdf(_df_export_morta, "mortalidad_general", key_btn="ver_reporte_general_morta")
            with col_f_desc:
                descargar_pdf(_df_export_morta, "mortalidad_general", label="Descargar Reporte")
        else:
            with col_f_ver: st.write("")
            with col_f_desc: st.write("")

        with col_f_limp:
            st.button("Limpiar filtros", icon=":material/cleaning_services:", use_container_width=True, key="morta_btn_limpiar", on_click=limpiar_filtros_morta)

        if not pdf_df_final.empty:
            num = len(pdf_df_final)
            if timeframe == "Todo" and not any([hc_busq, nom_busq, madre_busq, edad_sel_val != "Todos", sem_sel_val != "Todos", idx_ing_busq, idx_def_busq]):
                st.info(f"Mostrando todos los registros de mortalidad disponibles ({num} en total).", icon=":material/info:")
            else:
                st.info(f"Se encontraron {num} registros de mortalidad que coinciden con los filtros aplicados.", icon=":material/filter_alt:")

            # Preparar el dataframe para mostrar
            df_show = pdf_df_final.copy()
            
            # 1. Definir columnas y orden
            desired_columns = [
                "tipo", "historia_clinica", "nombres_apellidos", "nombre_madre", "edad",
                "fecha_nacimiento", "hora_nacimiento", "fecha_defuncion", "hora_defuncion",
                "idx_ingreso", "idx_defuncion", "semanas_gestacion", "peso", "talla",
                "direccion", "id"
            ]
            df_show = df_show[[c for c in desired_columns if c in df_show.columns]]

            # 2. Formatear y manejar nulos (Todo a string para visualización uniforme)
            for col in df_show.columns:
                if col == "tipo":
                    # Limpiar tipo (sin emojis, usaremos colores de fondo)
                    df_show[col] = df_show[col].astype(str).str.strip().replace(["None", "nan", "NaN", ""], "Dato no disponible")
                elif col in ["fecha_defuncion", "fecha_nacimiento", "fecha_ingreso"]:
                    # Robustecer el parseo de fechas para asegurar formato DD/MM/YYYY
                    def format_date_robust(val):
                        if pd.isna(val) or val == "" or str(val).lower() in ["none", "nat", "nan"]:
                            return "Dato no disponible"
                        try:
                            # Intentar varios formatos comunes
                            dt = pd.to_datetime(val, dayfirst=True, errors='coerce')
                            if pd.notnull(dt):
                                return dt.strftime('%d/%m/%Y')
                            return "Dato no disponible"
                        except:
                            return "Dato no disponible"
                    
                    df_show[col] = df_show[col].apply(format_date_robust)
                    
                elif col in ["peso", "talla"]:
                    # Formatear números a 1 decimal
                    df_show[col] = df_show[col].apply(lambda x: f"{float(x):.1f}" if pd.notnull(x) and x != "" and str(x).replace('.','',1).isdigit() else "Dato no disponible")
                elif col in ["semanas_gestacion", "id"]:
                    # Enteros o IDs
                    df_show[col] = df_show[col].apply(lambda x: str(int(float(x))) if pd.notnull(x) and x != "" and str(x).replace('.','',1).isdigit() else str(x) if pd.notnull(x) and x != "" else "Dato no disponible")
                else:
                    # Texto general
                    df_show[col] = df_show[col].fillna("Dato no disponible").astype(str).replace(["", "None", "nan", "NaN"], "Dato no disponible")

            # Agregar columna de selección
            if " " not in df_show.columns:
                df_show.insert(0, " ", False)

            column_config_morta = {
                " ": st.column_config.CheckboxColumn("✓", default=False),
                "tipo": st.column_config.TextColumn("Tipo", disabled=True),
                "historia_clinica": st.column_config.TextColumn("Historia clínica", disabled=True),
                "nombres_apellidos": st.column_config.TextColumn("Nombres y Apellidos", disabled=True),
                "nombre_madre": st.column_config.TextColumn("Nombre de la madre", disabled=True),
                "fecha_nacimiento": st.column_config.TextColumn("Fecha de nacimiento", disabled=True),
                "hora_nacimiento": st.column_config.TextColumn("Hora de nacimiento", disabled=True),
                "fecha_defuncion": st.column_config.TextColumn("Fecha de defunción", disabled=True),
                "hora_defuncion": st.column_config.TextColumn("Hora de defunción", disabled=True),
                "edad": st.column_config.TextColumn("Edad", disabled=True),
                "idx_ingreso": st.column_config.TextColumn("IDX de ingreso", disabled=True),
                "idx_defuncion": st.column_config.TextColumn("IDX de defunción", disabled=True),
                "semanas_gestacion": st.column_config.TextColumn("Semanas de gestación", disabled=True),
                "peso": st.column_config.TextColumn("Peso (kg)", disabled=True),
                "talla": st.column_config.TextColumn("Talla (cm)", disabled=True),
                "direccion": st.column_config.TextColumn("Dirección", disabled=True),
                "id": st.column_config.TextColumn("ID", disabled=True),
            }

            # Aplicar estilos de realce tipo "Badge" Pastel para la columna Tipo
            def style_tipo(val):
                # Paleta Pastel con texto contrastado para estética Material
                if "Neonatal" in val:
                    return 'background-color: #E3F2FD; color: #1565C0; font-weight: bold; border-radius: 8px; border: 1px solid #BBDEFB; text-align: center;'
                elif "Infantil" in val:
                    return 'background-color: #E8F5E9; color: #2E7D32; font-weight: bold; border-radius: 8px; border: 1px solid #C8E6C9; text-align: center;'
                elif "Materna" in val:
                    return 'background-color: #FCE4EC; color: #C2185B; font-weight: bold; border-radius: 8px; border: 1px solid #F8BBD0; text-align: center;'
                return ''

            st.data_editor(
                df_show.style.applymap(style_tipo, subset=['tipo']),
                use_container_width=True,
                hide_index=True,
                column_config=column_config_morta,
                key="editor_morta_general"
            )
        else:
            st.warning("No hay datos para mostrar con los filtros actuales.", icon=":material/warning:")

    st.markdown("#")
    st.markdown("#####")