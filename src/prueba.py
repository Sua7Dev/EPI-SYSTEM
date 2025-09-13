import streamlit as st
import pandas as pd
import re


# DataFrame de ejemplo
df = pd.DataFrame({
    "Nombre": ["Ana", "Luis", "Pedro", "Lucía", "Carlos", "María", "Jorge", "Sofía"],
    "Ciudad": ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", "Granada", "Zaragoza", "Málaga"],
    "Sexo": ["Femenino", "Masculino", "Masculino", "Femenino", "Masculino", "Femenino", "Masculino", "Femenino"],
    "Fecha": [
        "2024-06-01", "2023-12-15", "2022-08-10", "2021-03-22",
        "2020-11-05", "2019-07-19", "2018-02-28", "2017-09-13"
    ]
})

df["Fecha"] = pd.to_datetime(df["Fecha"])

# Barra de búsqueda personalizada
search_query = st.text_input("Buscar en la tabla", "")

# Opciones de filtrado, "Sin Filtro" es la opción por defecto
filter_option = st.selectbox(
    "Opciones de filtro",
    [
        "Sin Filtro",
        "A-Z (Nombre)",
        "Z-A (Nombre)",
        "Más reciente a más viejo (Fecha)",
        "Más viejo a más reciente (Fecha)",
        "Solo Masculino",
        "Solo Femenino"
    ],
    index=0
)

# Lógica de filtrado y ordenamiento en tiempo real
filtered_df = df.copy()

# Filtrado por búsqueda en tiempo real
if search_query:
    keywords = re.split(r'[,\s]+', search_query)
    mask = filtered_df.apply(lambda row: all(
        any(keyword.lower() in str(cell).lower() for cell in row)
        for keyword in keywords if keyword
    ), axis=1)
    filtered_df = filtered_df[mask]

# Aplicar opción de filtro seleccionada
if filter_option == "A-Z (Nombre)":
    filtered_df = filtered_df.sort_values("Nombre", ascending=True)
elif filter_option == "Z-A (Nombre)":
    filtered_df = filtered_df.sort_values("Nombre", ascending=False)
elif filter_option == "Más reciente a más viejo (Fecha)":
    filtered_df = filtered_df.sort_values("Fecha", ascending=False)
elif filter_option == "Más viejo a más reciente (Fecha)":
    filtered_df = filtered_df.sort_values("Fecha", ascending=True)
elif filter_option == "Solo Masculino":
    filtered_df = filtered_df[filtered_df["Sexo"] == "Masculino"]
elif filter_option == "Solo Femenino":
    filtered_df = filtered_df[filtered_df["Sexo"] == "Femenino"]
# Si es "Sin Filtro", no se aplica ningún filtro adicional

st.dataframe(filtered_df, use_container_width=True)


# FUNCION DE FILTRO ADAPTABLE ( EN PROCESO )
import re
import pandas as pd
import streamlit as st


def universal_filter(df: pd.DataFrame,
                     search_label: str = "Buscar en la tabla",
                     select_label: str = "Opciones de filtro",
                     key_prefix: str = "",
                     max_categorical_unique: int = 10) -> pd.DataFrame:
    """
    Barra de búsqueda + selectbox universal para filtrar/ordenar cualquier DataFrame.
    - df: DataFrame de entrada (no se modifica el original).
    - key_prefix: prefijo para las keys de Streamlit (evita colisión si hay varias tablas).
    - max_categorical_unique: máximo de valores únicos para generar filtros 'Solo X (col)'.
    Retorna el DataFrame filtrado/ordenado.
    """
    if df is None or df.empty:
        return df

    df2 = df.copy()

    # detectar tipos de columna
    datetime_cols = [c for c in df2.columns if pd.api.types.is_datetime64_any_dtype(df2[c])]
    numeric_cols = [c for c in df2.columns if pd.api.types.is_numeric_dtype(df2[c])]
    object_cols = [c for c in df2.columns if df2[c].dtype == object or pd.api.types.is_categorical_dtype(df2[c])]

    # columnas candidatas a "categóricas" para generar filtros "Solo X"
    categorical_candidates = []
    for c in df2.columns:
        nunq = df2[c].nunique(dropna=True)
        if 0 < nunq <= max_categorical_unique:
            categorical_candidates.append(c)

    # construir opciones y mapa de acciones
    options = ["Sin Filtro"]
    actions = {"Sin Filtro": ("none", None)}

    # ordenar columnas de texto (A-Z / Z-A)
    for c in object_cols:
        display = f"A-Z ({c})"
        options.append(display)
        actions[display] = ("sort", c, True)
        display = f"Z-A ({c})"
        options.append(display)
        actions[display] = ("sort", c, False)

    # ordenar columnas datetime
    for c in datetime_cols:
        display = f"Más reciente a más viejo ({c})"
        options.append(display)
        actions[display] = ("sort", c, False)  # desc
        display = f"Más viejo a más reciente ({c})"
        options.append(display)
        actions[display] = ("sort", c, True)  # asc

    # ordenar columnas numéricas
    for c in numeric_cols:
        display = f"Mayor a menor ({c})"
        options.append(display)
        actions[display] = ("sort", c, False)
        display = f"Menor a mayor ({c})"
        options.append(display)
        actions[display] = ("sort", c, True)

    # filtros por valor (solo para columnas con pocos valores únicos)
    for c in categorical_candidates:
        uniques = df2[c].dropna().unique().tolist()
        for u in uniques:
            display = f"Solo {u} ({c})"
            options.append(display)
            actions[display] = ("filter", c, u)

    # UI: búsqueda y selectbox
    search_key = f"{key_prefix}_search" if key_prefix else "universal_search"
    select_key = f"{key_prefix}_filter" if key_prefix else "universal_select"

    search_query = st.text_input(search_label, value="", key=search_key)
    filter_option = st.selectbox(select_label, options, index=0, key=select_key)

    # aplicar búsqueda (busca en todas las columnas, AND entre palabras, OR dentro de fila)
    filtered = df2
    if search_query:
        keywords = re.split(r'[,\s]+', search_query.strip())
        # mantener filas que contienen cada keyword en alguna celda
        mask = filtered.apply(lambda row: all(
            any(keyword.lower() in ("" if pd.isna(cell) else str(cell)).lower() for cell in row)
            for keyword in keywords if keyword
        ), axis=1)
        filtered = filtered[mask]

    # aplicar acción seleccionada
    action = actions.get(filter_option, ("none", None))
    if action[0] == "sort":
        col = action[1]
        asc = action[2]
        # si columna no existe en df filtrado (por alguna razón), no hacer nada
        if col in filtered.columns:
            try:
                # sort_values manejará tipos mixtos; na_position al final
                filtered = filtered.sort_values(by=col, ascending=asc, na_position="last")
            except Exception:
                # fallback: sort by string representation
                filtered = filtered.reindex(filtered.assign(_sort_key=filtered[col].astype(str)).sort_values("_sort_key", ascending=asc).index).drop(columns=["_sort_key"], errors="ignore")
    elif action[0] == "filter":
        col, val = action[1], action[2]
        if col in filtered.columns:
            filtered = filtered[filtered[col] == val]

    return filtered