import streamlit as st
import altair as alt
import pandas as pd
import numpy as np

# ESTE ES EL RELLENO TEMPORAL, REEMPLAZAR POR LOS DATOS REALES
def grafica_lineas():
        # 1. Crear los datos
        # Un Bump Chart requiere datos en un formato específico:
        # 'año' o 'periodo', 'equipo' o 'categoría', y 'ranking' o 'posición'
        data = pd.DataFrame({
            'year': [2020, 2020, 2020, 2020, 2020,
                    2021, 2021, 2021, 2021, 2021,
                    2022, 2022, 2022, 2022, 2022],
            'team': ['A', 'B', 'C', 'D', 'E',
                    'A', 'B', 'C', 'D', 'E',
                    'A', 'B', 'C', 'D', 'E'],
            'rank': [1, 2, 3, 4, 5,
                    3, 1, 2, 5, 4,
                    2, 3, 1, 4, 5]
        })

        # 2. Crear el gráfico base
        # Definimos las variables para los ejes X e Y y el color de las líneas.
        base = alt.Chart(data).encode(
            x=alt.X('year:O', title='Año'), # 'O' para datos ordinales
            y=alt.Y('rank:Q', title='Posición (Rank)', sort="descending"), # 'Q' para datos cuantitativos
            color=alt.Color('team:N', title='Equipo'), # 'N' para datos nominales
            tooltip=['year', 'team', 'rank']
        )

        # 3. Crear las líneas que conectan los puntos
        # Usamos 'mark_line' para dibujar las líneas del gráfico.
        lines = base.mark_line(point=True).encode(
            size=alt.value(3)
        )

        # 4. Crear el texto para las etiquetas de los puntos
        # Mostramos la posición (rank) al lado de cada punto.
        text = base.mark_text(
            align='left',
            baseline='middle',
            dx=10 # Mueve el texto 10 píxeles a la derecha del punto
        ).encode(
            text=alt.Text('rank:Q')
        )

        # 5. Combinar los gráficos
        chart = (lines + text).interactive()

        # 6. Mostrar el gráfico en Streamlit
        st.altair_chart(chart, use_container_width=True)

# LO MISMO AQUI ES RELLENO TEMPORAL
def grafica_pie():
        # 1. Crear los datos
        # Generamos 5 puntos de datos aleatorios para el ejemplo.
        data = pd.DataFrame({
            'category': ['A', 'B', 'C', 'D', 'E'],
            'value': np.random.randint(10, 100, 5) # Valores aleatorios entre 10 y 100
        })

        # 2. Crear el gráfico base con Altair
        # El uso de 'theta' y 'radius' es clave para los gráficos radiales.
        # 'theta' define el ángulo (similar a un slice de pastel)
        # 'radius' define la distancia desde el centro
        base = alt.Chart(data).encode(
            theta=alt.Theta("value:Q", stack=True)
        )

        # 3. Crear el gráfico de barras radial (Arc)
        # Usamos 'mark_arc' para crear las secciones del gráfico
        # El 'outerRadius' controla el tamaño del gráfico
        arc = base.mark_arc(outerRadius=120).encode(
            color=alt.Color("category:N"),
            order=alt.Order("value:Q", sort="descending"),
            tooltip=["category", "value"]
        )

        # 4. Crear el texto para las etiquetas
        # Esto es opcional, pero ayuda a leer los valores.
        text = base.mark_text(radius=140).encode(
            text=alt.Text("value:Q"),
            order=alt.Order("value:Q", sort="descending"),
            color=alt.value("black")
        )

        # 5. Combinar los gráficos
        chart = arc + text

        # 6. Mostrar el gráfico en Streamlit
        st.altair_chart(chart, use_container_width=True)


def global_stats():
    col_60, col_40 = st.columns([6, 4])
    with col_60:
        st.header(":material/groups: Estadísticas Globales", anchor=False)
        grafica_lineas()

    with col_40:
        st.header(":material/pie_chart: Estadísticas Globales", anchor=False)
        grafica_pie()
