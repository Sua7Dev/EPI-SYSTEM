import streamlit as st
from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez, copyright_footer_dos
from utils.base_64 import img_a_base64
from streamlit_extras.pdf_viewer import pdf_viewer
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
PDF_DIR = PROJECT_ROOT / "static" / "assets" / "pdf"

def boton_volver():
    # TODO hacer que te devuelva a la pagina que viniste
    volver_btn = st.button(label="Volver atras", type="primary", icon=":material/arrow_back:")
    if volver_btn:
        st.switch_page(st.session_state.get("previous_page", "pages/inicio.py"))
        st.rerun()
    
def mostrar_pdf():
    pdf_buffer = st.session_state.get("pdf_buffer")

    if pdf_buffer:
        pdf_viewer(pdf_buffer)
    else:
        st.error("No se encontró el reporte para mostrar.", icon=":material/error:")

def ver_reportes():
    logo_bandera = ASSETS_DIR / "imagebanderanueva2.png"
    logo_base64 = img_a_base64(logo_bandera)
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) # Llama a la función para recargar la página una vez.
    logo(tamano="70%")
    mostrar_pdf()
    boton_volver()
    st.markdown("######")
    st.markdown("######")
    copyright_footer_dos("Equipo Investigador", margin_right="0px")

ver_reportes()