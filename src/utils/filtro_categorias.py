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
    
    opciones = ["Todas"] + list(categorias_map.keys())
    
    categorias_seleccionadas = st.multiselect(
        "Seleccione las categorías",
        options=opciones,
        default=st.session_state.get("nat_categorias", ["Todas"]),
        key="nat_categorias",
        on_change=_on_change_cats
    )

    df_filtrado = df.copy()

    if "Todas" not in categorias_seleccionadas and categorias_seleccionadas:
        for i in range(0, len(categorias_seleccionadas), 3):
            chunk = categorias_seleccionadas[i:i+3]
            cols = st.columns(3)
            for j, cat_nombre in enumerate(chunk):
                columna_df = categorias_map[cat_nombre]
                
                # Obtener valores unicos numéricos disponibles
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
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        busqueda_nombre = st.text_input("Nombres y Apellidos", placeholder="Ej. Juan Pérez", max_chars=40, key="filtro_morb_nombre")
        bloquear_caracteres(
            caracteres=list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"),
            tipo_de_input="text",
            max_chars=40,
            label="Nombres y Apellidos"
        )
        
    with col2:
        if pd.api.types.is_numeric_dtype(df["edad"]) and not df.empty:
            valores_edad = sorted([int(x) for x in df["edad"].dropna().unique()])
        else:
            valores_edad = sorted(df["edad"].dropna().unique().tolist())
            
        edad_sel = st.selectbox(
            "Edad",
            options=["Todos"] + valores_edad,
            key="filtro_morb_edad"
        )
        
    with col3:
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

    if "neo_categorias" not in st.session_state: st.session_state["neo_categorias"] = ["Todas"]
    if "prev_neo_categorias" not in st.session_state: st.session_state["prev_neo_categorias"] = ["Todas"]

    def _on_change_neo():
        actual = st.session_state.get("neo_categorias", [])
        prev = st.session_state.get("prev_neo_categorias", ["Todas"])
        if "Todas" in actual and "Todas" not in prev:
            st.session_state["neo_categorias"] = ["Todas"]
            st.session_state["prev_neo_categorias"] = ["Todas"]
            return
        if "Todas" in prev and "Todas" in actual and len(actual) > 1:
            new = [c for c in actual if c != "Todas"]
            st.session_state["neo_categorias"] = new
            st.session_state["prev_neo_categorias"] = new
            return
        if len(actual) == 0:
            st.session_state["neo_categorias"] = ["Todas"]
            st.session_state["prev_neo_categorias"] = ["Todas"]
            return
        st.session_state["prev_neo_categorias"] = actual

    opciones_todas = {
        "Historia Clínica": "historia_clinica",
        "Nombre": "nombres_apellidos",
        "Nombre Madre": "nombre_madre",
        "Semanas de Gestación": "semanas_gestacion",
        "Peso": "peso",
        "Talla": "talla",
        "Edad": "edad",
    }
    opciones_validas = {k: v for k, v in opciones_todas.items() if v in df.columns}
    if "tiempo" in df.columns: opciones_validas["Edad"] = "edad"

    categorias_sel = st.multiselect(
        "Seleccione qué filtros utilizar",
        options=["Todas"] + list(opciones_validas.keys()),
        default=st.session_state.get("neo_categorias", ["Todas"]),
        key="neo_categorias",
        on_change=_on_change_neo
    )

    filtros_activos = list(opciones_validas.keys()) if "Todas" in categorias_sel else [
        f for f in categorias_sel if f in opciones_validas
    ]

    busqueda_hc, busqueda_nombre, busqueda_madre, edad_sel, tiempo_sel, sem_sel = "", "", "", "Todos", "Todos", "Todos"
    sort_elegido = "Sin orden"

    if not filtros_activos:
        st.divider()
        return df.copy()

    FILTROS_SIMPLES = ["Historia Clínica", "Nombre", "Nombre Madre", "Semanas de Gestación"]
    simples_activos = [f for f in filtros_activos if f in FILTROS_SIMPLES]

    for i in range(0, len(simples_activos), 3):
        chunk = simples_activos[i:i+3]
        cols = st.columns(len(chunk))
        for j, tag in enumerate(chunk):
            with cols[j]:
                if tag == "Historia Clínica":
                    busqueda_hc = st.text_input("Historia Clínica", placeholder="Ej. 12345678", key="neo_hc")
                    bloquear_caracteres(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑüÜ!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-— "), "text", 8, "Historia Clínica")
                elif tag == "Nombre":
                    busqueda_nombre = st.text_input("Nombre del paciente", placeholder="Ej. Juan Pérez", key="neo_nom")
                    bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"), "text", 40, "Nombre del paciente")
                elif tag == "Nombre Madre":
                    busqueda_madre = st.text_input("Nombre de la madre", placeholder="Ej. María García", key="neo_madre")
                    bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"), "text", 40, "Nombre de la madre")
                elif tag == "Semanas de Gestación":
                    v_sem = sorted(df["semanas_gestacion"].dropna().unique().tolist())
                    sem_sel = st.selectbox("Semanas Gestación", options=["Todos"] + v_sem, key="neo_sem")

    opciones_orden = ["Sin orden"]
    tiene_peso, tiene_talla = "Peso" in filtros_activos and "peso" in df.columns, "Talla" in filtros_activos and "talla" in df.columns
    if tiene_peso: opciones_orden += ["Peso: Menor a mayor ↑", "Peso: Mayor a menor ↓"]
    if tiene_talla: opciones_orden += ["Talla: Menor a mayor ↑", "Talla: Mayor a menor ↓"]
    if tiene_peso or tiene_talla:
        sort_elegido = st.selectbox("Ordenar registros por", opciones_orden, key="ord_neo")

    if "Edad" in filtros_activos:
        _, col_num, _pad = st.columns([1.2, 3.0, 2.8])
        with col_num:
            v_e = sorted(df["edad"].dropna().astype(str).unique().tolist()) if "edad" in df.columns else []
            edad_sel = st.selectbox("Edad", options=["Todos"] + v_e, key="neo_edad_num")
        # Unidad eliminada por petición del usuario

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

    if "inf_categorias" not in st.session_state: st.session_state["inf_categorias"] = ["Todas"]
    if "prev_inf_categorias" not in st.session_state: st.session_state["prev_inf_categorias"] = ["Todas"]

    def _on_change_inf():
        actual = st.session_state.get("inf_categorias", [])
        prev = st.session_state.get("prev_inf_categorias", ["Todas"])
        if "Todas" in actual and "Todas" not in prev:
            st.session_state["inf_categorias"] = ["Todas"]; st.session_state["prev_inf_categorias"] = ["Todas"]
            return
        if "Todas" in prev and "Todas" in actual and len(actual) > 1:
            new = [c for c in actual if c != "Todas"]
            st.session_state["inf_categorias"] = new; st.session_state["prev_inf_categorias"] = new
            return
        if len(actual) == 0:
            st.session_state["inf_categorias"] = ["Todas"]; st.session_state["prev_inf_categorias"] = ["Todas"]
            return
        st.session_state["prev_inf_categorias"] = actual

    opciones_todas = {"Historia Clínica": "historia_clinica", "Nombre": "nombres_apellidos", "Nombre Madre": "nombre_madre", "Peso": "peso", "Talla": "talla", "Edad": "edad"}
    opciones_validas = {k: v for k, v in opciones_todas.items() if v in df.columns}
    if "tiempo" in df.columns: opciones_validas["Edad"] = "edad"

    categorias_sel = st.multiselect(
        "Seleccione qué filtros utilizar",
        options=["Todas"] + list(opciones_validas.keys()),
        default=st.session_state.get("inf_categorias", ["Todas"]),
        key="inf_categorias",
        on_change=_on_change_inf
    )

    filtros_activos = list(opciones_validas.keys()) if "Todas" in categorias_sel else [f for f in categorias_sel if f in opciones_validas]

    busqueda_hc, busqueda_nombre, busqueda_madre, edad_sel, tiempo_sel = "", "", "", "Todos", "Todos"
    sort_elegido = "Sin orden"

    if not filtros_activos:
        st.divider(); return df.copy()

    FILTROS_SIMPLES = ["Historia Clínica", "Nombre", "Nombre Madre"]
    simples_activos = [f for f in filtros_activos if f in FILTROS_SIMPLES]

    for i in range(0, len(simples_activos), 3):
        chunk = simples_activos[i:i+3]
        cols = st.columns(len(chunk))
        for j, tag in enumerate(chunk):
            with cols[j]:
                if tag == "Historia Clínica":
                    busqueda_hc = st.text_input("Historia Clínica", placeholder="Ej. 12345678", key="inf_hc")
                    bloquear_caracteres(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑüÜ!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-— "), "text", 8, "Historia Clínica")
                elif tag == "Nombre":
                    busqueda_nombre = st.text_input("Nombre del paciente", placeholder="Ej. Juan Pérez", key="inf_nom")
                    bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"), "text", 40, "Nombre del paciente")
                elif tag == "Nombre Madre":
                    busqueda_madre = st.text_input("Nombre de la madre", placeholder="Ej. María García", key="inf_madre")
                    bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"), "text", 40, "Nombre de la madre")

    opciones_orden = ["Sin orden"]
    tiene_peso, tiene_talla = "Peso" in filtros_activos and "peso" in df.columns, "Talla" in filtros_activos and "talla" in df.columns
    if tiene_peso: opciones_orden += ["Peso: Menor a mayor ↑", "Peso: Mayor a menor ↓"]
    if tiene_talla: opciones_orden += ["Talla: Menor a mayor ↑", "Talla: Mayor a menor ↓"]
    if tiene_peso or tiene_talla:
        sort_elegido = st.selectbox("Ordenar registros por", opciones_orden, key="ord_inf")

    if "Edad" in filtros_activos:
        _, col_num, _pad = st.columns([1.2, 3.0, 2.8])
        with col_num:
            v_e = sorted(df["edad"].dropna().astype(str).unique().tolist()) if "edad" in df.columns else []
            edad_sel = st.selectbox("Edad", options=["Todos"] + v_e, key="inf_edad_num")
        # Unidad eliminada por petición del usuario

    df_f = df.copy()
    def norm(t): return ''.join(c for c in unicodedata.normalize('NFKD', str(t).lower()) if unicodedata.category(c) != 'Mn')
    
    if busqueda_hc: df_f = df_f[df_f["historia_clinica"].astype(str).str.contains(busqueda_hc, na=False)]
    if busqueda_nombre: df_f = df_f[df_f["nombres_apellidos"].astype(str).apply(norm).str.contains(norm(busqueda_nombre), na=False)]
    if busqueda_madre: df_f = df_f[df_f["nombre_madre"].astype(str).apply(norm).str.contains(norm(busqueda_madre), na=False)]
    if edad_sel != "Todos": df_f = df_f[df_f["edad"].astype(str) == str(edad_sel)]
    # Filtro de tiempo eliminado

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

    if "mat_categorias" not in st.session_state:
        st.session_state["mat_categorias"] = ["Todas"]
    if "prev_mat_categorias" not in st.session_state:
        st.session_state["prev_mat_categorias"] = ["Todas"]

    def _on_change():
        actual = st.session_state.get("mat_categorias", [])
        prev   = st.session_state.get("prev_mat_categorias", ["Todas"])
        if "Todas" in actual and "Todas" not in prev:
            st.session_state["mat_categorias"] = ["Todas"]
            st.session_state["prev_mat_categorias"] = ["Todas"]
            return
        if "Todas" in prev and "Todas" in actual and len(actual) > 1:
            new = [c for c in actual if c != "Todas"]
            st.session_state["mat_categorias"] = new
            st.session_state["prev_mat_categorias"] = new
            return
        if len(actual) == 0:
            st.session_state["mat_categorias"] = ["Todas"]
            st.session_state["prev_mat_categorias"] = ["Todas"]
            return
        st.session_state["prev_mat_categorias"] = actual

    opciones_todas = {
        "Historia Clínica": "historia_clinica",
        "Nombre":           "nombres_apellidos",
        "Nombre Madre":     "nombre_madre",
        "Diagnóstico (Ingreso)":   "idx_ingreso",
        "Diagnóstico (Defunción)": "idx_defuncion",
        "Edad":             "edad",
    }
    opciones_validas = {k: v for k, v in opciones_todas.items() if v in df.columns}
    if "tiempo" in df.columns:
        opciones_validas["Edad"] = "edad"

    opts = ["Todas"] + list(opciones_validas.keys())
    categorias_sel = st.multiselect(
        "Seleccione qué filtros utilizar",
        options=opts,
        default=st.session_state.get("mat_categorias", ["Todas"]),
        key="mat_categorias",
        on_change=_on_change
    )

    filtros_activos = list(opciones_validas.keys()) if "Todas" in categorias_sel else [
        f for f in categorias_sel if f in opciones_validas
    ]

    # ─── valores por defecto ─────────────────────────────────────
    busqueda_hc      = ""
    busqueda_nombre  = ""
    busqueda_madre   = ""
    busqueda_dx_ing  = ""
    busqueda_dx_def  = ""
    edad_sel         = "Todos"
    tiempo_sel       = "Todos"

    if not filtros_activos:
        st.divider()
        return df.copy()

    # ─── Filtros de texto en grid dinámico ───────────────────────
    SIMPLES = ["Historia Clínica", "Nombre", "Nombre Madre",
               "Diagnóstico (Ingreso)", "Diagnóstico (Defunción)"]
    simples_activos = [f for f in filtros_activos if f in SIMPLES]

    for i in range(0, len(simples_activos), 3):
        chunk = simples_activos[i:i+3]
        cols  = st.columns(len(chunk))
        for j, tag in enumerate(chunk):
            with cols[j]:
                if tag == "Historia Clínica":
                    busqueda_hc = st.text_input("Historia Clínica", placeholder="Ej. 12345678", key="mat_hc")
                    bloquear_caracteres(list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑüÜ!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-— "), "text", 8, "Historia Clínica")
                elif tag == "Nombre":
                    busqueda_nombre = st.text_input("Nombre del paciente", placeholder="Ej. Ana García", key="mat_nom")
                    bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"), "text", 40, "Nombre del paciente")
                elif tag == "Nombre Madre":
                    busqueda_madre = st.text_input("Nombre de la madre", placeholder="Ej. María López", key="mat_madre")
                    bloquear_caracteres(list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"), "text", 40, "Nombre de la madre")
                elif tag == "Diagnóstico (Ingreso)":
                    busqueda_dx_ing = st.text_input("Diagnóstico de ingreso", placeholder="Ej. I10", key="mat_dx_ing")
                    bloquear_caracteres(list("!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"), "text", 20, "Diagnóstico de ingreso")
                elif tag == "Diagnóstico (Defunción)":
                    busqueda_dx_def = st.text_input("Diagnóstico de defunción", placeholder="Ej. I21", key="mat_dx_def")
                    bloquear_caracteres(list("!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"), "text", 20, "Diagnóstico de defunción")

    # ─── Edad: fila dedicada ─────────────────────────────────────
    if "Edad" in filtros_activos:
        _, col_num, _pad = st.columns([1.2, 3.0, 2.8])
        with col_num:
            valores_e = sorted(df["edad"].dropna().astype(str).unique().tolist()) if "edad" in df.columns else []
            edad_sel  = st.selectbox("Edad (en años)", ["Todos"] + valores_e, key="mat_edad_num")
        # Quitamos selectbox de unidad por petición del usuario (se asume años)

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
    if "tiempo" in df_filtrado.columns and tiempo_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["tiempo"].str.contains(tiempo_sel, case=False, na=False)]

    st.divider()
    return df_filtrado
