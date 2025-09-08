import streamlit as st
import pandas as pd

# Datos de ejemplo
df = pd.DataFrame({
    "Nombre": ["Ana", "Luis", "María", "Juan"],
    "Edad": [23, 34, 29, 41],
    "Seleccionar": [False, False, False, False],  # Columna para seleccionar filas
})

# Mostrar el editor de datos con la columna de selección como checkbox
edited_df = st.data_editor(
    df,
    column_config={
        "Seleccionar": st.column_config.CheckboxColumn("Seleccionar"),
    },
    hide_index=True,
)

# Botón para eliminar filas seleccionadas
if st.button("Eliminar"):
    # Filtrar las filas donde 'Seleccionar' es False
    df_filtrado = edited_df[~edited_df["Seleccionar"]]
    st.write("Tabla actualizada:")
    st.dataframe(df_filtrado)
else:
    st.write("Tabla original o editada:")
    st.dataframe(edited_df)