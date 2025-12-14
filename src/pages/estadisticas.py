import streamlit as st
from pages.menu import menu
from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez, copyright_footer_dos
from utils.base_64 import img_a_base64
from stats.mortalidad_stats import mortalidad_stats
from stats.natalidad_stats import natalidad_stats
from stats.morbilidad_stats import morbilidad_stats
from utils.verificaciones import obtener_info_usuario
from pathlib import Path
configurar_pagina_espanol()
import sys


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
# lo que se ve
def mostrar_stats():
    logo(tamano="100%")
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a esta area.", icon=":material/error:")
        return
    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)
    if not info_usuario:
        st.error("Usuario no encontrado. Por favor, inicia sesión nuevamente.", icon=":material/error:")
        return

    st.subheader(":material/category_search: Estadísticas por sección", anchor=False) # hola more
    tabs = st.tabs([
        #"| :material/communities: Global |",
        "| :material/skull: Mortalidad |",
        "| :material/pregnant_woman: Natalidad |",
        "| :material/personal_injury: Morbilidad |",
    ])    #, width=500
    #with tabs[0]:
        #global_stats()
    with tabs[0]:
        mortalidad_stats()
        pass
    with tabs[1]:
        natalidad_stats()
        pass
    with tabs[2]:
        morbilidad_stats()
        pass
    copyright_footer_dos("Equipo Investigador", bottom="-200px")

# ejecucion principal
def estadisticas():
    logo_bandera = ASSETS_DIR / "imagebanderanueva2.png"
    logo_base64 = img_a_base64(logo_bandera)
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) # Llama a la función para recargar la página una vez.
    mostrar_stats()
    

estadisticas()