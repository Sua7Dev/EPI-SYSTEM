import streamlit as st
from utils.verificaciones import obtener_info_usuario
from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez, copyright_footer_dos
from pages.menu import menu
from utils.base_64 import img_a_base64
from pathlib import Path
from utils.informaciones import nosotros, hospital, mision, vision, manual_de_uso, alcance_del_sistema, proposito_del_sistema
from utils.recargar_retroceso import reload_on_back

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

def orden_de_informaciones():
    with st.container(border=True):
        hospital()
        st.markdown("---")
        col_mision, col_vision = st.columns(2)
        with col_mision:
            mision()
        with col_vision:
            vision()
        
        st.markdown("---")
        col_alcance, col_proposito = st.columns(2)
        with col_alcance:
            alcance_del_sistema()
        with col_proposito:
            proposito_del_sistema()
        st.markdown("---")
        col_manual, col_nosotros = st.columns(2)
        with col_manual:
            manual_de_uso()        
        with col_nosotros:
            nosotros()
    st.markdown("# ")


def acerca_de():
    logo_bandera  = ASSETS_DIR / "imagebanderanueva2.png"
    logo_base64 = img_a_base64(logo_bandera)
    
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) # Llama a la función para recargar la página una vez.
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a esta area.", icon=":material/error:")
        return   
    logo(tamano="100%")
    st.header(":material/chat_info: Información del sistema", divider="gray", anchor=False)
    orden_de_informaciones()
    st.markdown('## ')

    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)

    if not info_usuario:
        st.error("Usuario no encontrado. Por favor, inicia sesión nuevamente.", icon=":material/error:")
        return
    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)


    copyright_footer_dos("Equipo Investigador", bottom="-335px")#
    

acerca_de()
reload_on_back()

