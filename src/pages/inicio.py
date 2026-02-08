import streamlit as st
import os
from stats.dash_stats import obtener_totales, obtener_top_areas_registro, obtener_totales_por_anio
from pages.menu import menu
from utils.base_64 import img_a_base64
from utils.visuales import reloj, logo, configurar_pagina_espanol, recargar_una_vez, copyright_footer_dos
import altair as alt
import pandas as pd
import numpy as npv
from utils.verificaciones import obtener_info_usuario
from utils.informaciones import mostrar_usuario_activo, usuario_activo_fixed
from pathlib import Path
DB_PATH = os.getenv("hospital.db", "hospital.db")

configurar_pagina_espanol()
import sys
import os
from pathlib import Path


def get_project_root() -> Path:
    """Devuelve la raíz del proyecto, incluso empaquetado con PyInstaller."""
    if getattr(sys, "frozen", False):  # Si está empaquetado
        # Carpeta base del ejecutable
        return Path(sys._MEIPASS)
    else:
        # Carpeta base del código fuente
        return Path(__file__).resolve().parent.parent.parent

PROJECT_ROOT = get_project_root()
ASSETS_DIR = PROJECT_ROOT / "static" / "assets" / "imagenes"

menu()


def contenedores_totales():
    _, col_total = st.columns([1.5, 2.8])
    with col_total:
        st.header(":material/health_metrics: Casos totales", anchor=False)
    totales = obtener_totales()
    col_total, col_morta, col_nata, col_morb = st.columns(4)
    with col_total:
        st.subheader(":material/trending_up: Registros", anchor=False)
        st.metric(":material/arrow_right: Total", f"{totales['total_general']}", border=True)

    with col_morta:
        st.subheader(":material/trending_up: Mortalidad", anchor=False)
        st.metric(":material/arrow_right: Total", f"{totales['total_mortalidad']}", border=True)

    with col_nata:
        st.subheader(":material/trending_up: Natalidad", anchor=False)
        st.metric(":material/arrow_right: Total", f"{totales['total_natalidad']}", border=True)

    with col_morb:
        st.subheader(":material/trending_up: Morbilidad", anchor=False)
        st.metric(":material/arrow_right: Total", f"{totales['total_morbilidad']}", border=True)

import threading
DB_LOCK = threading.Lock()

def boton_eliminar_base_datos():

    st.warning("Esta acción eliminará TODA la base de datos. No se puede deshacer.", icon=":material/warning:")

    if st.button(" Eliminar Base de Datos"):
        with DB_LOCK:
            try:
                if os.path.exists(DB_PATH):
                    os.remove(DB_PATH)
                    st.success("Base de datos eliminada correctamente.", icon=":material/check_circle:")
                else:
                    st.info("La base de datos no existe.", icon=":material/info:")
            except Exception as e:
                st.error(f"Error al eliminar la base de datos: {e}", icon=":material/error:")
                
#boton_eliminar_base_datos()
import shutil
def boton_descargar_bd(db_path=DB_PATH):
    """
    Muestra un botón en Streamlit para descargar la base de datos completa.
    """
    st.subheader("Descargar Base de Datos")

    if st.button("Descargar BD completa"):
        db_file = Path(db_path)
        if db_file.exists():
            # Crear una copia temporal para la descarga
            tmp_file = db_file.with_name("backup_bd.db")
            shutil.copy(db_file, tmp_file)

            with open(tmp_file, "rb") as f:
                st.download_button(
                    label="Haz clic aquí para descargar la base de datos",
                    data=f,
                    file_name="base_de_datos.db",
                    mime="application/x-sqlite3"
                )
            st.success("Listo, puedes descargar la BD.")
        else:
            st.error("No se encontró la base de datos.", icon=":warning:")
            
#boton_descargar_bd()

def graficas_dashboard():
    """
    Display a dashboard with a line chart for yearly totals across categories and a donut chart for top 3 areas.
    Uses specific date fields and formats for each category and shows the top 3 areas by total records.
    """
    col_70, col_30 = st.columns([7, 3])

    with col_70:
        st.subheader(":material/query_stats: Todas las categorías", divider="gray", anchor=False)

        df_totales = obtener_totales_por_anio()
        if df_totales.empty:
            st.info("No hay datos para mostrar.", icon=":material/warning:")
        else:
            # Renombrar columna para que se vea bonito en la gráfica
            df_totales = df_totales.rename(columns={'anio': 'Año'})

            # Transformar a formato largo para Altair
            data = df_totales.melt(
                id_vars='Año',
                value_vars=[
                    'total_mortalidad',
                    'total_natalidad',
                    'total_morbilidad',
                ],
                var_name='categoria',
                value_name='total'
            )
            categoria_map = {
                'total_mortalidad': 'Mortalidad',
                'total_natalidad': 'Natalidad',
                'total_morbilidad': 'Morbilidad',
            }
            data['categoria'] = data['categoria'].map(categoria_map)

            # Crear gráfica de líneas
            chart = alt.Chart(data).mark_line(point=True).encode(
                x=alt.X('Año:O', title='Año'),
                y=alt.Y('total:Q', title='Cantidad de Registros'),
                color=alt.Color('categoria:N', title='Categoría'),
                tooltip=['Año', 'categoria', 'total']
            ).properties(
                title='Cantidad de Registros por Categoría y Año'
            )

            st.altair_chart(chart, use_container_width=True)

    with col_30:
        st.subheader(":material/data_exploration: Top 3 áreas", divider="gray", anchor=False)
        top_areas = obtener_top_areas_registro(3)

        # Convertir a DataFrame y filtrar valores > 0
        data = pd.DataFrame({
            'category': [a['area'] for a in top_areas],
            'value': [a['total'] for a in top_areas]
        })

        data = data[data['value'] > 0]

        if data.empty:
            st.info("No hay datos para mostrar.", icon=":material/warning:")
        else:
            base = alt.Chart(data).encode(theta=alt.Theta("value:Q", stack=True))
            donut = base.mark_arc(outerRadius=120).encode(
                color=alt.Color("category:N", legend=None),
                order=alt.Order("value:Q", sort="descending"),
                tooltip=["category", "value"]
            )
            text = base.mark_text(radius=140).encode(
                text="category:N",
                order=alt.Order("value:Q", sort="descending"),
                color=alt.value("black")
            )
            st.altair_chart(donut + text, use_container_width=True)

def dashboard():
    logo(tamano="100%")
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a esta area.", icon=":material/error:")
        return

    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)

    if not info_usuario:
        st.error("Usuario no encontrado. Por favor, inicia sesión nuevamente.", icon=":material/error:")
        return
    _, col_reloj = st.columns([1.5, 2.8])
    with col_reloj:
        reloj()
    # parte visual graficas/textos
    st.header(":material/dashboard: Panel General - Departamento de Epidemiología", divider="gray", anchor=False) 
    # contenedores principales
    contenedores_totales()
    # graficas
    graficas_dashboard()
    copyright_footer_dos("Equipo Investigador")

 
def inicio():
    
    logo_bandera  = ASSETS_DIR / "imagebanderanueva2.png"

    logo_base64 = img_a_base64(logo_bandera)
    
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) # Llama a la función para recargar la página una vez.
    

    dashboard()
# Aquí va el contenido que quieres mostrar después de que termine el "cargando"
inicio()





