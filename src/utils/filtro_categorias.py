import streamlit as st
import pandas as pd
import unicodedata
from utils.validaciones import bloquear_caracteres

def filtro_categorias_natalidad(df):
    """
    Filtro tag-based de Natalidad.
    - Sexo: Varones / Hembras
    - Tipo de Natalidad: Partos, Cesáreas, Gemelar, PEH, MTO
    Devuelve (df_filtrado, columnas_activas).
    """
    if df.empty:
        return df, []

    # Mapas de etiqueta → columna real
    SEXO_MAP = {
        "Varones": "varones",
        "Hembras": "hembras",
    }
    TIPO_MAP = {
        "Partos":    "partos",
        "Cesáreas":  "cesareas",
        "Gemelar":   "gemelar",
        "PEH":       "partos_extrahospitalarios",
        "MTO":       "mto",
    }

    col_sexo, col_tipo = st.columns(2)

    with col_sexo:
        sel_sexo = st.multiselect(
            ":material/female: :material/male: Sexo",
            options=list(SEXO_MAP.keys()),
            default=[],
            placeholder="Todos (Varones y Hembras)",
            key="nat_tag_sexo",
        )

    with col_tipo:
        sel_tipo = st.multiselect(
            ":material/category: Tipo de Natalidad",
            options=list(TIPO_MAP.keys()),
            default=[],
            placeholder="Todos los tipos",
            key="nat_tag_tipo",
        )

    # Calcular columnas activas
    cols_sexo = [SEXO_MAP[t] for t in sel_sexo] if sel_sexo else list(SEXO_MAP.values())
    cols_tipo = [TIPO_MAP[t] for t in sel_tipo] if sel_tipo else list(TIPO_MAP.values())

    columnas_activas = list(dict.fromkeys(cols_sexo + cols_tipo))  # orden estable, sin duplicados

    # Guardar en session_state para que el PDF lo lea
    label_sexo  = ", ".join(sel_sexo)  if sel_sexo  else "Todos"
    label_tipo  = ", ".join(sel_tipo)  if sel_tipo  else "Todos"
    st.session_state["nat_columnas_activas"]  = columnas_activas
    st.session_state["nat_filtros_label"]     = {"sexo": label_sexo, "tipo": label_tipo}
    st.session_state["nat_sel_sexo"]          = sel_sexo
    st.session_state["nat_sel_tipo"]          = sel_tipo

    return df.copy(), columnas_activas

def filtro_morbilidad(df):
    """
    Filtro avanzado para Morbilidad.
    Permite filtrar por nombres y apellidos, edad (selectbox) y diagnóstico.
    Ignora tildes y mayúsculas en la búsqueda.
    """
    if df.empty:
        return df

    cols = st.columns(3)
    
    with cols[0]:
        busqueda_nombre = st.text_input(":material/person: Nombres y Apellidos", placeholder="Ej. Juan Pérez", max_chars=40, key="filtro_morb_nombre")
        bloquear_caracteres(
            caracteres=list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~--^"),
            tipo_de_input="text",
            max_chars=40,
            label="Nombres y Apellidos"
        )
        
    with cols[1]:
        if pd.api.types.is_numeric_dtype(df["edad"]) and not df.empty:
            valores_edad = sorted([int(x) for x in df["edad"].dropna().unique()])
        else:
            valores_edad = sorted(df["edad"].dropna().unique().tolist())
            
        edad_sel = st.selectbox(
            ":material/cake: Edad",
            options=["Todos"] + valores_edad,
            key="filtro_morb_edad"
        )
        
    with cols[2]:
        busqueda_diagnostico = st.text_input(":material/medical_services: Diagnóstico", placeholder="Ej. Asma", max_chars=150, key="filtro_morb_diag")
        bloquear_caracteres(
            caracteres=list("!@#$%¨&*_=+[]{}:;\"\\|<>?`~^°¡¿§±←→•#"),
            tipo_de_input="text",
            max_chars=150,
            label="Diagnóstico"
        )

    df_filtrado = df.copy()

    def normalizar_texto(texto):
        if not isinstance(texto, str): return ""
        t = texto.lower()
        return ''.join(c for c in unicodedata.normalize('NFKD', t) if unicodedata.category(c) != 'Mn')

    if busqueda_nombre:
        bn = normalizar_texto(busqueda_nombre)
        df_filtrado = df_filtrado[df_filtrado["nombres_apellidos"].astype(str).apply(normalizar_texto).str.contains(bn, na=False)]
        
    if busqueda_diagnostico:
        bd = normalizar_texto(busqueda_diagnostico)
        df_filtrado = df_filtrado[df_filtrado["diagnostico"].astype(str).apply(normalizar_texto).str.contains(bd, na=False)]
        
    if edad_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["edad"] == edad_sel]

    return df_filtrado

def filtro_muerte_neonatal(df):
    if df.empty: return df
    busqueda_hc, busqueda_nombre, busqueda_madre, edad_sel, sem_sel = "", "", "", "Todos", "Todos"
    sort_elegido = "Sin orden"
    componentes = []
    
    def render_hc():
        nonlocal busqueda_hc
        busqueda_hc = st.text_input(":material/assignment: Historia Clínica", placeholder="Ej. 12345678", key="neo_hc")
        bloquear_caracteres(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑüÜ!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-- "), "text", 8, "Historia Clínica")
    componentes.append(render_hc)
    
    def render_nombre():
        nonlocal busqueda_nombre
        busqueda_nombre = st.text_input(":material/person: Nombre del paciente", placeholder="Ej. Juan Pérez", key="neo_nom")
        bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~--^"), "text", 40, "Nombre del paciente")
    componentes.append(render_nombre)
    
    def render_madre():
        nonlocal busqueda_madre
        busqueda_madre = st.text_input(":material/female: Nombre de la madre", placeholder="Ej. María García", key="neo_madre")
        bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~--^"), "text", 40, "Nombre de la madre")
    componentes.append(render_madre)
    
    def render_sem():
        nonlocal sem_sel
        v_sem = sorted(df["semanas_gestacion"].dropna().unique().tolist())
        sem_sel = st.selectbox(":material/pregnant_woman: Semanas Gestación", options=["Todos"] + v_sem, key="neo_sem")
    componentes.append(render_sem)
    
    def render_edad():
        nonlocal edad_sel
        v_e = sorted(df["edad"].dropna().astype(str).unique().tolist()) if "edad" in df.columns else []
        edad_sel = st.selectbox(":material/cake: Edad", options=["Todos"] + v_e, key="neo_edad_num")
    componentes.append(render_edad)
 
    tiene_peso, tiene_talla = "peso" in df.columns, "talla" in df.columns
    if tiene_peso or tiene_talla:
        def render_orden():
            nonlocal sort_elegido
            opc = ["Sin orden"]
            if tiene_peso: opc += ["Peso: Menor a mayor ↑", "Peso: Mayor a menor ↓"]
            if tiene_talla: opc += ["Talla: Menor a mayor ↑", "Talla: Mayor a menor ↓"]
            sort_elegido = st.selectbox(":material/sort: Ordenar por", opc, key="ord_neo")
        componentes.append(render_orden)

    for i in range(0, len(componentes), 3):
        chunk = [componentes[k] for k in range(i, min(i+3, len(componentes)))]
        cols = st.columns(3)
        for j, func in enumerate(chunk):
            with cols[j]: func()


    df_f = df.copy()
    def norm(t): return ''.join(c for c in unicodedata.normalize('NFKD', str(t).lower()) if unicodedata.category(c) != 'Mn')
    if busqueda_hc: df_f = df_f[df_f["historia_clinica"].astype(str).str.contains(busqueda_hc, na=False)]
    if busqueda_nombre: df_f = df_f[df_f["nombres_apellidos"].astype(str).apply(norm).str.contains(norm(busqueda_nombre), na=False)]
    if busqueda_madre: df_f = df_f[df_f["nombre_madre"].astype(str).apply(norm).str.contains(norm(busqueda_madre), na=False)]
    if edad_sel != "Todos": df_f = df_f[df_f["edad"].astype(str) == str(edad_sel)]
    if sem_sel != "Todos": df_f = df_f[df_f["semanas_gestacion"] == sem_sel]
    if sort_elegido != "Sin orden" and not df_f.empty:
        col = "peso" if sort_elegido.startswith("Peso") else "talla"
        df_f["_s"] = pd.to_numeric(df_f[col], errors="coerce")
        df_f = df_f.sort_values("_s", ascending="Menor" in sort_elegido).drop(columns=["_s"])
    return df_f

def filtro_muerte_infantil(df):
    if df.empty: return df
    busqueda_hc, busqueda_nombre, busqueda_madre, edad_sel = "", "", "", "Todos"
    sort_elegido = "Sin orden"
    componentes = []
    
    def render_hc():
        nonlocal busqueda_hc
        busqueda_hc = st.text_input(":material/assignment: Historia Clínica", placeholder="Ej. 12345678", key="inf_hc")
        bloquear_caracteres(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑüÜ!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-- "), "text", 8, "Historia Clínica")
    componentes.append(render_hc)
    
    def render_nombre():
        nonlocal busqueda_nombre
        busqueda_nombre = st.text_input(":material/person: Nombre del paciente", placeholder="Ej. Juan Pérez", key="inf_nom")
        bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~--^"), "text", 40, "Nombre del paciente")
    componentes.append(render_nombre)
    
    def render_madre():
        nonlocal busqueda_madre
        busqueda_madre = st.text_input(":material/female: Nombre de la madre", placeholder="Ej. María García", key="inf_madre")
        bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~--^"), "text", 40, "Nombre de la madre")
    componentes.append(render_madre)
    
    def render_edad():
        nonlocal edad_sel
        v_e = sorted(df["edad"].dropna().astype(str).unique().tolist()) if "edad" in df.columns else []
        edad_sel = st.selectbox(":material/cake: Edad", options=["Todos"] + v_e, key="inf_edad_num")
    componentes.append(render_edad)
 
    tiene_peso, tiene_talla = "peso" in df.columns, "talla" in df.columns
    if tiene_peso or tiene_talla:
        def render_orden():
            nonlocal sort_elegido
            opc = ["Sin orden"]
            if tiene_peso: opc += ["Peso: Menor a mayor ↑", "Peso: Mayor a menor ↓"]
            if tiene_talla: opc += ["Talla: Menor a mayor ↑", "Talla: Mayor a menor ↓"]
            sort_elegido = st.selectbox(":material/sort: Ordenar por", opc, key="ord_inf")
        componentes.append(render_orden)

    c1, c2, c3 = st.columns(3)
    with c1: render_hc()
    with c2: render_nombre()
    with c3: render_madre()
    cb1, cb2, cb3 = st.columns(3)
    if tiene_peso or tiene_talla:
        with cb1: render_orden()
    with cb2: render_edad()

    df_f = df.copy()
    def norm(t): return ''.join(c for c in unicodedata.normalize('NFKD', str(t).lower()) if unicodedata.category(c) != 'Mn')
    if busqueda_hc: df_f = df_f[df_f["historia_clinica"].astype(str).str.contains(busqueda_hc, na=False)]
    if busqueda_nombre: df_f = df_f[df_f["nombres_apellidos"].astype(str).apply(norm).str.contains(norm(busqueda_nombre), na=False)]
    if busqueda_madre: df_f = df_f[df_f["nombre_madre"].astype(str).apply(norm).str.contains(norm(busqueda_madre), na=False)]
    if edad_sel != "Todos": df_f = df_f[df_f["edad"].astype(str) == str(edad_sel)]
    if sort_elegido != "Sin orden" and not df_f.empty:
        col = "peso" if sort_elegido.startswith("Peso") else "talla"
        df_f["_s"] = pd.to_numeric(df_f[col], errors="coerce")
        df_f = df_f.sort_values("_s", ascending="Menor" in sort_elegido).drop(columns=["_s"])
    return df_f

def filtro_muerte_materna(df):
    if df.empty: return df
    busqueda_hc, busqueda_nombre = "", ""
    busqueda_dx_ing, busqueda_dx_def, edad_sel = "", "", "Todos"
    componentes = []
    
    def render_hc():
        nonlocal busqueda_hc
        busqueda_hc = st.text_input(":material/assignment: Historia Clínica", placeholder="Ej. 12345678", key="mat_hc")
        bloquear_caracteres(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑüÜ!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-- "), "text", 8, "Historia Clínica")
    componentes.append(render_hc)
    
    def render_nombre():
        nonlocal busqueda_nombre
        busqueda_nombre = st.text_input(":material/person: Nombre del paciente", placeholder="Ej. Ana García", key="mat_nom")
        bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~--^"), "text", 40, "Nombre del paciente")
    componentes.append(render_nombre)
    
    def render_dx_ing():
        nonlocal busqueda_dx_ing
        busqueda_dx_ing = st.text_input(":material/medical_services: Diagnóstico de ingreso", placeholder="Ej. I10", key="mat_dx_ing")
        bloquear_caracteres(list("!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~--^"), "text", 20, "Diagnóstico de ingreso")
    componentes.append(render_dx_ing)
    
    def render_dx_def():
        nonlocal busqueda_dx_def
        busqueda_dx_def = st.text_input(":material/medical_services: Diagnóstico de defunción", placeholder="Ej. I21", key="mat_dx_def")
        bloquear_caracteres(list("!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~--^"), "text", 20, "Diagnóstico de defunción")
    componentes.append(render_dx_def)
    
    def render_edad():
        nonlocal edad_sel
        valores_e = sorted(df["edad"].dropna().astype(str).unique().tolist()) if "edad" in df.columns else []
        edad_sel  = st.selectbox(":material/cake: Edad (en años)", ["Todos"] + valores_e, key="mat_edad_num")
    componentes.append(render_edad)

    # Layout: 4 inputs arriba, edad abajo al medio
    col1, col2 = st.columns(2)
    with col1: render_hc()
    with col2: render_nombre()

    col3, col4 = st.columns(2)
    with col3: render_dx_ing()
    with col4: render_dx_def()

    _, col_cent, _ = st.columns([1, 2, 1])
    with col_cent: render_edad()



    df_f = df.copy()
    def nrm(t): return ''.join(c for c in unicodedata.normalize('NFKD', str(t).lower()) if unicodedata.category(c) != 'Mn')
    if busqueda_hc: df_f = df_f[df_f["historia_clinica"].astype(str).str.contains(busqueda_hc, na=False)]
    if busqueda_nombre: df_f = df_f[df_f["nombres_apellidos"].astype(str).apply(nrm).str.contains(nrm(busqueda_nombre), na=False)]
    if busqueda_dx_ing: df_f = df_f[df_f["idx_ingreso"].astype(str).apply(nrm).str.contains(nrm(busqueda_dx_ing), na=False)]
    if busqueda_dx_def: df_f = df_f[df_f["idx_defuncion"].astype(str).apply(nrm).str.contains(nrm(busqueda_dx_def), na=False)]
    if "edad" in df_f.columns and edad_sel != "Todos": df_f = df_f[df_f["edad"].astype(str) == str(edad_sel)]
    return df_f
