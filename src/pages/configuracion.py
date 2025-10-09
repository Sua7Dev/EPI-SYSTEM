import streamlit as st
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
    logo(tamano="100%")
    st.header(":material/admin_panel_settings: Configuración y extras del sistema", divider="gray", anchor=False)
    if 'edit_mode' not in st.session_state or not st.session_state['edit_mode']:
        mostrar_modo_normal()
    else:#aqui este bloque iria lo de las pag extras o capas de seguridad con su pedida de info o contrasenas para el super user
        mostrar_modo_edicion()

def configuracion():
    logo_bandera  = ASSETS_DIR / "imagebanderanueva2.png"
    logo_base64 = img_a_base64(logo_bandera)
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) # Llama a la función para recargar la página una vez.
    elementos()
    copyright_footer_dos("SAMUEL URBANO & GUSTAVO HEREDIA", bottom="-200px")#
    

configuracion()
    

