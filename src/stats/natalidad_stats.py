import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from utils.sql_control import operaciones_sql_natalidad


import pandas as pd
import altair as alt

def total_casos_por_ano():
    df = operaciones_sql_natalidad("cargar")
    if df is None or df.empty:
        st.info("No hay datos de natalidad disponibles.", icon=":material/warning:")
        return
    
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['year'] = df['fecha'].dt.year

    years = sorted(df['year'].dropna().unique().tolist())
    if not years:
        st.info("No hay años disponibles para mostrar.", icon=":material/warning:")
        return

    selected_year = st.selectbox("Seleccione un año", years, index=len(years)-1,
                                 key="selectbox_total_casos_por_ano")

    # Filtrar por año seleccionado
    df = df[df['year'] == selected_year]

    # Crear un DataFrame con todos los meses del año
    meses_num = range(1, 13)
    meses_abrev = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
                   'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
    df_total = pd.DataFrame({'mes_num': list(meses_num), 'mes_label': list(meses_abrev)})

    # Agrupar los datos reales por mes
    df['mes_num'] = df['fecha'].dt.month
    total_data = df.groupby('mes_num')[['varones', 'hembras']].sum().reset_index()
    total_data['total'] = total_data['varones'] + total_data['hembras']

    # Unir con todos los meses para incluir meses sin datos
    df_final = pd.merge(df_total, total_data, how='left', left_on='mes_num', right_on='mes_num')
    df_final[['varones', 'hembras', 'total']] = df_final[['varones', 'hembras', 'total']].fillna(0)

    chart = alt.Chart(df_final).mark_area(
        line={'color': '#2ca02c'},
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='white', offset=0),
                alt.GradientStop(color='#2ca02c', offset=1)
            ],
            x1=1, x2=1, y1=1, y2=0
        )
    ).encode(
        x=alt.X('mes_label:O', title='Mes', sort=list(meses_abrev)),
        y=alt.Y('total:Q', title='Total de Nacimientos'),
        tooltip=['mes_label', 'varones', 'hembras', 'total']
    ).properties(
        title=f"Total de Nacimientos por Mes - {selected_year}"
    )
    
    st.altair_chart(chart, use_container_width=True)


def comparacion_partos():
    df = operaciones_sql_natalidad("cargar")
    if df is None or df.empty:
        st.info("No hay datos de natalidad disponibles.", icon=":material/warning:")
        return

    data = pd.DataFrame({
        'tipo': ['Partos', 'Cesáreas', 'Partos Extrahospitalarios'],
        'count': [
            df['partos'].sum(),
            df['cesareas'].sum(),
            df['partos_extrahospitalarios'].sum()
        ]
    })

    base = alt.Chart(data).encode(
        x=alt.X('count:Q', title='Cantidad Total'),
        y=alt.Y('tipo:O', sort='-x', title=''),   
        text=alt.Text('count:Q', format='.0f')
    )

    bars = base.mark_bar(
        tooltip=alt.expr("luminance(scale('color', datum.count))")
    ).encode(
        color='count:Q'
    )

    text = base.mark_text(
        align='right',
        dx=-3,
        color=alt.expr("luminance(scale('color', datum.count)) > 0.5 ? 'black' : 'white'")
    )

    chart = (bars + text).properties(
        title='Comparación de Totales de Partos, Cesáreas y Partos Extrahospitalarios'
    )

    st.altair_chart(chart, use_container_width=True)

def comparacion_varones_hembras():
    df = operaciones_sql_natalidad("cargar")
    if df is None or df.empty:
        st.info("No hay datos de natalidad disponibles.", icon=":material/warning:")
        return

    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['year'] = df['fecha'].dt.year

    bar_data = df.groupby('year')[['varones', 'hembras']].sum().reset_index()
    bar_data_male = bar_data[['year', 'varones']].rename(columns={'varones': 'count'})
    bar_data_male['sex'] = 1
    bar_data_female = bar_data[['year', 'hembras']].rename(columns={'hembras': 'count'})
    bar_data_female['sex'] = 2
    bar_data = pd.concat([bar_data_male, bar_data_female], ignore_index=True)

    years = sorted(bar_data['year'].unique().tolist())
    if not years:
        st.info("No hay años disponibles para mostrar.", icon=":material/warning:")
        return

    selected_year = st.selectbox("Seleccione un año", years, index=len(years)-1, key="natalidad_stast")

    bar_data = bar_data[bar_data['year'] == selected_year]

    bar_data['gender'] = bar_data['sex'].map({1: 'Male', 2: 'Female'})

    base = alt.Chart(bar_data).properties(
        width=250
    )

    color_scale = alt.Scale(domain=['Male', 'Female'],
                            range=['#1f77b4', '#e377c2'])

    female_chart = base.transform_filter(
        alt.datum.gender == 'Female'
    ).encode(
        y=alt.Y('year:O', axis=None),
        x=alt.X('sum(count):Q', title='Hembras', sort='descending'),
        color=alt.Color('gender:N', scale=color_scale, legend=None)
    ).mark_bar().properties(title='Hembras')

    middle = base.encode(
        y=alt.Y('year:O', axis=None),
        text=alt.Text('year:Q')
    ).mark_text().properties(width=20)

    male_chart = base.transform_filter(
        alt.datum.gender == 'Male'
    ).encode(
        y=alt.Y('year:O', axis=None),
        x=alt.X('sum(count):Q', title='Varones'),
        color=alt.Color('gender:N', scale=color_scale, legend=None)
    ).mark_bar().properties(title='Varones')

    chart = alt.hconcat(
        female_chart,
        middle,
        male_chart
    ).resolve_scale(y='shared').properties(
        title=f"Nacimientos en {selected_year}"
    )

    st.altair_chart(chart, use_container_width=True)



def natalidad_stats():
    st.header(":material/baby_changing_station: Partos/Cesáreas/Peh", anchor=False, divider="gray")
    comparacion_partos()    
  
    col_izq, _, col_der = st.columns([5, 0.1, 5])
    with col_izq:
        st.header("⚥ Nacimientos hembras/varones", anchor=False, divider="gray")
        comparacion_varones_hembras()  

    with col_der:
        st.header(":material/event_note: Total de nacimientos", anchor=False, divider="gray")
        total_casos_por_ano()

     
