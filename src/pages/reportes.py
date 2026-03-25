import streamlit as st
from utils.verificaciones import obtener_info_usuario
from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez, copyright_footer_dos
from pages.menu import menu
from utils.base_64 import img_a_base64
from pathlib import Path
from utils.recargar_retroceso import reload_on_back
from utils.reportes import formulario_reporte_general
from reportes.morbilidad_gen import formulario_reporte_general_morbilidad
from reportes.natalidad_general import formulario_reporte_general_natalidad

configurar_pagina_espanol()
if "previous_page" not in st.session_state:
    st.session_state["previous_page"] = "pages/inicio.py"
st.session_state["previous_page"] = "pages/reportes.py"
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

def secciones_reportes():
    tab_morta, tab_nata, tab_morbi = st.tabs([
        "| :material/skull: Mortalidad |",
        "| :material/pregnant_woman: Natalidad |",
        "| :material/personal_injury: Morbilidad |",
    ]) 
    with tab_morta:
        #st.subheader(":material/arrow_circle_down: Descargas de reportes", anchor=False, divider="gray")
        col_izq, col_centro, col_der = st.columns([3.35, 4, 2.65])
        with col_centro:
            formulario_reporte_general()
        #st.markdown("")
    with tab_nata:
        #st.subheader(":material/arrow_circle_down: Descargas de reportes", anchor=False, divider="gray")
        col_izq, col_centro, col_der = st.columns([3.35, 4, 2.65])
        with col_centro:
            formulario_reporte_general_natalidad()
        #st.markdown("")
    with tab_morbi:
        #st.subheader(":material/arrow_circle_down: Descargas de reportes", anchor=False, divider="gray")
        col_izq, col_centro, col_der = st.columns([3.35, 4, 2.65])
        with col_centro:
            formulario_reporte_general_morbilidad()
        #st.markdown("")

def reportes():
    logo_bandera  = ASSETS_DIR / "imagebanderanueva2.png"
    logo_base64 = img_a_base64(logo_bandera)
    
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) # Llama a la función para recargar la página una vez.
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a esta area.", icon=":material/error:")
        return   
    logo(tamano="100%")
    st.header(":material/docs: Reportes del sistema", divider="gray", anchor=False)
    secciones_reportes()
    #st.markdown('## ')

    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)

    if not info_usuario:
        st.error("Usuario no encontrado. Por favor, inicia sesión nuevamente.", icon=":material/error:")
        return
    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)


    copyright_footer_dos("Equipo Investigador", bottom="-335px")#
    

reportes()
reload_on_back()

