import streamlit as st
import pandas as pd
import unicodedata
from utils.validaciones import bloquear_caracteres

def filtro_categorias_natalidad(df):
    """
    Filtro de categorías numéricas de natalidad (Partos, Hembras, Varones, Cesáreas, Muertos, PEH).
    Permite seleccionar múltiples categorías y las cantidades a filtrar según los datos disponibles.
    """
    if df.empty:
        return df

    # Inicializar states
    if "nat_categorias" not in st.session_state:
        st.session_state["nat_categorias"] = ["Todas"]
    if "prev_nat_categorias" not in st.session_state:
        st.session_state["prev_nat_categorias"] = ["Todas"]

    def _on_change_cats():
        actual = st.session_state.get("nat_categorias", [])
        prev = st.session_state.get("prev_nat_categorias", ["Todas"])
        
        if "Todas" in actual and "Todas" not in prev:
            st.session_state["nat_categorias"] = ["Todas"]
            st.session_state["prev_nat_categorias"] = ["Todas"]
            return

        if "Todas" in prev and "Todas" in actual and len(actual) > 1:
            new = [c for c in actual if c != "Todas"]
            st.session_state["nat_categorias"] = new
            st.session_state["prev_nat_categorias"] = new
            return

        if len(actual) == 0:
            st.session_state["nat_categorias"] = ["Todas"]
            st.session_state["prev_nat_categorias"] = ["Todas"]
            return

        st.session_state["prev_nat_categorias"] = actual

    categorias_map = {
        "Partos": "partos",
        "Hembras": "hembras",
        "Varones": "varones",
        "Cesáreas": "cesareas",
        "Muertos": "mto",
        "Partos Extrahospitalarios (PEH)": "partos_extrahospitalarios"
    }

    st.markdown("**:material/manage_search: Filtros por Categoría — Natalidad**")
    
    df_filtrado = df.copy()

    # Renderizar todos los filtros en grid de 3 columnas
    cats = list(categorias_map.keys())
    for i in range(0, len(cats), 3):
        chunk = cats[i:i+3]
        cols = st.columns(3)
        for j, cat_nombre in enumerate(chunk):
            columna_df = categorias_map[cat_nombre]
            
            if pd.api.types.is_numeric_dtype(df[columna_df]):
                valores_unicos = sorted([int(x) for x in df[columna_df].dropna().unique()])
            else:
                valores_unicos = sorted(df[columna_df].dropna().unique().tolist())
            
            with cols[j]:
                valor_sel = st.selectbox(
                    f"{cat_nombre}",
                    options=["Todos"] + valores_unicos,
                    key=f"nat_sel_{columna_df}"
                )
                
            if valor_sel != "Todos":
                df_filtrado = df_filtrado[df_filtrado[columna_df] == valor_sel]

    return df_filtrado

def filtro_morbilidad(df):
    """
    Filtro avanzado para Morbilidad.
    Permite filtrar por nombres y apellidos, edad (selectbox) y diagnóstico.
    Ignora tildes y mayúsculas en la búsqueda.
    """
    if df.empty:
        return df

    st.markdown("**:material/manage_search: Filtros por Categoría — Morbilidad**")
    
    cols = st.columns(3)
    
    with cols[0]:
        busqueda_nombre = st.text_input("Nombres y Apellidos", placeholder="Ej. Juan Pérez", max_chars=40, key="filtro_morb_nombre")
        bloquear_caracteres(
            caracteres=list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"),
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
            "Edad",
            options=["Todos"] + valores_edad,
            key="filtro_morb_edad"
        )
        
    with cols[2]:
        busqueda_diagnostico = st.text_input("Diagnóstico", placeholder="Ej. Asma", max_chars=150, key="filtro_morb_diag")
        bloquear_caracteres(
            caracteres=list("!@#$%¨&*_=+[]{}:;\"\\|<>?`~^°¡¿§±←→•#"),
            tipo_de_input="text",
            max_chars=150,
            label="Diagnóstico"
        )

    df_filtrado = df.copy()

    def normalizar_texto(texto):
        if not isinstance(texto, str):
            return ""
        t = texto.lower()
        return ''.join(c for c in unicodedata.normalize('NFKD', t) if unicodedata.category(c) != 'Mn')

    if busqueda_nombre:
        busqueda_n_norm = normalizar_texto(busqueda_nombre)
        df_nombres_norm = df_filtrado["nombres_apellidos"].astype(str).apply(normalizar_texto)
        df_filtrado = df_filtrado[df_nombres_norm.str.contains(busqueda_n_norm, na=False)]
        
    if busqueda_diagnostico:
        busqueda_d_norm = normalizar_texto(busqueda_diagnostico)
        df_diag_norm = df_filtrado["diagnostico"].astype(str).apply(normalizar_texto)
        df_filtrado = df_filtrado[df_diag_norm.str.contains(busqueda_d_norm, na=False)]
        
    if edad_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["edad"] == edad_sel]

    return df_filtrado

def filtro_muerte_neonatal(df):
    """
    Filtro avanzado para Muerte Neonatal.
    Tags: Historia Clínica, Nombre, Nombre Madre, Semanas de Gestación, Peso, Talla, Edad.
    """
    if df.empty: return df
    st.markdown("**:material/manage_search: Filtros por Categoría — Muerte Neonatal**")

    # Inicialización de variables de búsqueda
    busqueda_hc, busqueda_nombre, busqueda_madre, edad_sel, sem_sel = "", "", "", "Todos", "Todos"
    sort_elegido = "Sin orden"

    # Lista de componentes para renderizar en grid (todos visibles por defecto)
    componentes = []
    
    # 1. Historia Clínica
    def render_hc():
        nonlocal busqueda_hc
        busqueda_hc = st.text_input("Historia Clínica", placeholder="Ej. 12345678", key="neo_hc")
        bloquear_caracteres(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑüÜ!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-— "), "text", 8, "Historia Clínica")
    componentes.append(render_hc)
    
    # 2. Nombre
    def render_nombre():
        nonlocal busqueda_nombre
        busqueda_nombre = st.text_input("Nombre del paciente", placeholder="Ej. Juan Pérez", key="neo_nom")
        bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"), "text", 40, "Nombre del paciente")
    componentes.append(render_nombre)
    
    # 3. Nombre Madre
    def render_madre():
        nonlocal busqueda_madre
        busqueda_madre = st.text_input("Nombre de la madre", placeholder="Ej. María García", key="neo_madre")
        bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"), "text", 40, "Nombre de la madre")
    componentes.append(render_madre)
    
    # 4. Semanas de Gestación
    def render_sem():
        nonlocal sem_sel
        v_sem = sorted(df["semanas_gestacion"].dropna().unique().tolist())
        sem_sel = st.selectbox("Semanas Gestación", options=["Todos"] + v_sem, key="neo_sem")
    componentes.append(render_sem)
    
    # 5. Edad
    def render_edad():
        nonlocal edad_sel
        v_e = sorted(df["edad"].dropna().astype(str).unique().tolist()) if "edad" in df.columns else []
        edad_sel = st.selectbox("Edad", options=["Todos"] + v_e, key="neo_edad_num")
    componentes.append(render_edad)

    # 6. Ordenar (siempre que haya peso o talla)
    tiene_peso, tiene_talla = "peso" in df.columns, "talla" in df.columns
    if tiene_peso or tiene_talla:
        def render_orden():
            nonlocal sort_elegido
            opciones_orden = ["Sin orden"]
            if tiene_peso: opciones_orden += ["Peso: Menor a mayor ↑", "Peso: Mayor a menor ↓"]
            if tiene_talla: opciones_orden += ["Talla: Menor a mayor ↑", "Talla: Mayor a menor ↓"]
            sort_elegido = st.selectbox("Ordenar por", opciones_orden, key="ord_neo")
        componentes.append(render_orden)

    # Renderizar en grid de 3 columnas
    for i in range(0, len(componentes), 3):
        chunk = componentes[i:i+3]
        cols = st.columns(3)
        for j, render_func in enumerate(chunk):
            with cols[j]:
                render_func()


    df_f = df.copy()
    def norm(t): return ''.join(c for c in unicodedata.normalize('NFKD', str(t).lower()) if unicodedata.category(c) != 'Mn')
    
    if busqueda_hc: df_f = df_f[df_f["historia_clinica"].astype(str).str.contains(busqueda_hc, na=False)]
    if busqueda_nombre: df_f = df_f[df_f["nombres_apellidos"].astype(str).apply(norm).str.contains(norm(busqueda_nombre), na=False)]
    if busqueda_madre: df_f = df_f[df_f["nombre_madre"].astype(str).apply(norm).str.contains(norm(busqueda_madre), na=False)]
    if edad_sel != "Todos": df_f = df_f[df_f["edad"].astype(str) == str(edad_sel)]
    # Filtro de tiempo eliminado
    if sem_sel != "Todos": df_f = df_f[df_f["semanas_gestacion"] == sem_sel]

    if sort_elegido != "Sin orden" and not df_f.empty:
        col = "peso" if sort_elegido.startswith("Peso") else "talla"
        df_f["_s"] = pd.to_numeric(df_f[col], errors="coerce")
        df_f = df_f.sort_values("_s", ascending="Menor" in sort_elegido).drop(columns=["_s"])
    
    st.divider()
    return df_f

def filtro_muerte_infantil(df):
    """
    Filtro avanzado para Muerte Infantil.
    Tags: Historia Clínica, Nombre, Nombre Madre, Peso, Talla, Edad.
    """
    if df.empty: return df
    st.markdown("**:material/manage_search: Filtros por Categoría — Muerte Infantil**")

    # Inicialización de variables de búsqueda
    busqueda_hc, busqueda_nombre, busqueda_madre, edad_sel = "", "", "", "Todos"
    sort_elegido = "Sin orden"

    # Lista de componentes para renderizar en grid
    componentes = []
    
    def render_hc():
        nonlocal busqueda_hc
        busqueda_hc = st.text_input("Historia Clínica", placeholder="Ej. 12345678", key="inf_hc")
        bloquear_caracteres(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑüÜ!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-— "), "text", 8, "Historia Clínica")
    componentes.append(render_hc)
    
    def render_nombre():
        nonlocal busqueda_nombre
        busqueda_nombre = st.text_input("Nombre del paciente", placeholder="Ej. Juan Pérez", key="inf_nom")
        bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"), "text", 40, "Nombre del paciente")
    componentes.append(render_nombre)
    
    def render_madre():
        nonlocal busqueda_madre
        busqueda_madre = st.text_input("Nombre de la madre", placeholder="Ej. María García", key="inf_madre")
        bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"), "text", 40, "Nombre de la madre")
    componentes.append(render_madre)
    
    def render_edad():
        nonlocal edad_sel
        v_e = sorted(df["edad"].dropna().astype(str).unique().tolist()) if "edad" in df.columns else []
        edad_sel = st.selectbox("Edad", options=["Todos"] + v_e, key="inf_edad_num")
    componentes.append(render_edad)

    # Ordenar (siempre que haya peso o talla)
    tiene_peso, tiene_talla = "peso" in df.columns, "talla" in df.columns
    if tiene_peso or tiene_talla:
        def render_orden():
            nonlocal sort_elegido
            opciones_orden = ["Sin orden"]
            if tiene_peso: opciones_orden += ["Peso: Menor a mayor ↑", "Peso: Mayor a menor ↓"]
            if tiene_talla: opciones_orden += ["Talla: Menor a mayor ↑", "Talla: Mayor a menor ↓"]
            sort_elegido = st.selectbox("Ordenar por", opciones_orden, key="ord_inf")
        componentes.append(render_orden)

    # Renderizar en grid
    # Fila 1: HC, Nombre, Madre
    col1, col2, col3 = st.columns(3)
    with col1: render_hc()
    with col2: render_nombre()
    with col3: render_madre()

    # Fila 2: Ordenar y Edad (Edad al medio)
    col_b1, col_b2, col_b3 = st.columns(3)
    if tiene_peso or tiene_talla:
        with col_b1: render_orden()
    with col_b2: render_edad()

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
    
    st.divider()
    return df_f



def filtro_muerte_materna(df):
    """
    Filtro avanzado para Muerte Materna.
    Tags disponibles: Historia Clínica, Nombre, Nombre Madre, Diagnóstico, Edad.
    """
    if df.empty:
        return df

    st.markdown("**:material/manage_search: Filtros por Categoría — Muerte Materna**")

    # Inicialización de variables de búsqueda
    busqueda_hc, busqueda_nombre, busqueda_madre = "", "", ""
    busqueda_dx_ing, busqueda_dx_def, edad_sel = "", "", "Todos"

    # Lista de componentes para renderizar en grid
    componentes = []
    
    def render_hc():
        nonlocal busqueda_hc
        busqueda_hc = st.text_input("Historia Clínica", placeholder="Ej. 12345678", key="mat_hc")
        bloquear_caracteres(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑüÜ!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-— "), "text", 8, "Historia Clínica")
    componentes.append(render_hc)
    
    def render_nombre():
        nonlocal busqueda_nombre
        busqueda_nombre = st.text_input("Nombre del paciente", placeholder="Ej. Ana García", key="mat_nom")
        bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"), "text", 40, "Nombre del paciente")
    componentes.append(render_nombre)
    
    def render_madre():
        nonlocal busqueda_madre
        busqueda_madre = st.text_input("Nombre de la madre", placeholder="Ej. María López", key="mat_madre")
        bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"), "text", 40, "Nombre de la madre")
    componentes.append(render_madre)
    
    def render_dx_ing():
        nonlocal busqueda_dx_ing
        busqueda_dx_ing = st.text_input("Diagnóstico de ingreso", placeholder="Ej. I10", key="mat_dx_ing")
        bloquear_caracteres(list("!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"), "text", 20, "Diagnóstico de ingreso")
    componentes.append(render_dx_ing)
    
    def render_dx_def():
        nonlocal busqueda_dx_def
        busqueda_dx_def = st.text_input("Diagnóstico de defunción", placeholder="Ej. I21", key="mat_dx_def")
        bloquear_caracteres(list("!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"), "text", 20, "Diagnóstico de defunción")
    componentes.append(render_dx_def)
    
    def render_edad():
        nonlocal edad_sel
        valores_e = sorted(df["edad"].dropna().astype(str).unique().tolist()) if "edad" in df.columns else []
        edad_sel  = st.selectbox("Edad (en años)", ["Todos"] + valores_e, key="mat_edad_num")
    componentes.append(render_edad)

    # Renderizar en grid de 3 columnas
    for i in range(0, len(componentes), 3):
        chunk = componentes[i:i+3]
        cols  = st.columns(3)
        for j, render_func in enumerate(chunk):
            with cols[j]:
                render_func()

    # ─── Aplicar filtros ─────────────────────────────────────────
    df_filtrado = df.copy()

    def nrm(txt):
        if not isinstance(txt, str): return ""
        return ''.join(c for c in unicodedata.normalize('NFKD', txt.lower()) if unicodedata.category(c) != 'Mn')

    if busqueda_hc and "historia_clinica" in df_filtrado.columns:
        df_filtrado = df_filtrado[df_filtrado["historia_clinica"].astype(str).str.contains(busqueda_hc, na=False)]
    if busqueda_nombre and "nombres_apellidos" in df_filtrado.columns:
        bn = nrm(busqueda_nombre)
        df_filtrado = df_filtrado[df_filtrado["nombres_apellidos"].astype(str).apply(nrm).str.contains(bn, na=False)]
    if busqueda_madre and "nombre_madre" in df_filtrado.columns:
        bm = nrm(busqueda_madre)
        df_filtrado = df_filtrado[df_filtrado["nombre_madre"].astype(str).apply(nrm).str.contains(bm, na=False)]
    if busqueda_dx_ing and "idx_ingreso" in df_filtrado.columns:
        bdi = nrm(busqueda_dx_ing)
        df_filtrado = df_filtrado[df_filtrado["idx_ingreso"].astype(str).apply(nrm).str.contains(bdi, na=False)]
    if busqueda_dx_def and "idx_defuncion" in df_filtrado.columns:
        bdd = nrm(busqueda_dx_def)
        df_filtrado = df_filtrado[df_filtrado["idx_defuncion"].astype(str).apply(nrm).str.contains(bdd, na=False)]
    if "edad" in df_filtrado.columns and edad_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["edad"].astype(str) == str(edad_sel)]

    st.divider()
    return df_filtrado
