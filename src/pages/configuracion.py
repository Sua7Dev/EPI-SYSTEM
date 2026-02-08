import streamlit as st
from pages.historial import mostrar_historial_actividades
from utils.verificaciones import obtener_info_usuario
from utils.edicion_super import mostrar_modo_edicion, mostrar_modo_normal
from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez, copyright_footer_dos
from pages.menu import menu
from utils.base_64 import img_a_base64
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

def elementos():

    if 'edit_mode' not in st.session_state or not st.session_state['edit_mode']:
        mostrar_modo_normal()
        st.markdown("---")
        mostrar_historial_actividades()
    else:#aqui este bloque iria lo de las pag extras o capas de seguridad con su pedida de info o contrasenas para el super user
        mostrar_modo_edicion()

def configuracion():
    logo_bandera  = ASSETS_DIR / "imagebanderanueva2.png"
    logo_base64 = img_a_base64(logo_bandera)
    
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) # Llama a la función para recargar la página una vez.
    logo(tamano="100%")
    elementos()
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a esta area.", icon=":material/error:")
        return

    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)

    if not info_usuario:
        st.error("Usuario no encontrado. Por favor, inicia sesión nuevamente.", icon=":material/error:")
        return
    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)

    st.header(":material/admin_panel_settings: Configuración y extras del sistema", divider="gray", anchor=False)
    copyright_footer_dos("Equipo Investigador", bottom="-200px")#
    

configuracion()
    

