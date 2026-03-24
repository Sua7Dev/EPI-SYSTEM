import streamlit as st
from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez, copyright_footer_dos
from utils.base_64 import img_a_base64
from streamlit_extras.pdf_viewer import pdf_viewer
from utils.verificaciones import obtener_info_usuario
from utils.recargar_retroceso import reload_on_back
from pathlib import Path
configurar_pagina_espanol()
import sys
import datetime


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
    volver_btn = st.button(label="Volver atras", type="primary", icon=":material/arrow_back:", use_container_width=True)
    if volver_btn:
        st.switch_page(st.session_state.get("previous_page", "pages/inicio.py"))
        st.rerun()
    
def mostrar_pdf():
    pdf_buffer = st.session_state.get("pdf_buffer")
    nombre_base = st.session_state.get("pdf_nombre_base", "Reporte")

    if pdf_buffer:
        pdf_viewer(pdf_buffer)
        
        
        col_volver, col_descargar = st.columns([1, 1])
        with col_volver:
            boton_volver()
        with col_descargar:
            from utils.filtro import descargar_pdf_desde_buffer
            descargar_pdf_desde_buffer(pdf_buffer, nombre_base, label="Descargar PDF", key="descargar_ver_reporte")
            
    else:
        st.error("No se encontró el reporte para mostrar.", icon=":material/error:")
        boton_volver()

def ver_reportes():
    logo_bandera = ASSETS_DIR / "imagebanderanueva2.png"
    logo_base64 = img_a_base64(logo_bandera)
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) 
    logo(tamano="70%")
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a esta area.", icon=":material/error:")
        salir = st.button("Volver a inicio de sesión", icon=":material/arrow_back:", type="primary",
                  )
        if salir: st.switch_page("pages/inicio_sesion.py")
        return
    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)
    if not info_usuario:
        st.error("Usuario no encontrado. Por favor, inicia sesión nuevamente.", icon=":material/error:")
        return
    mostrar_pdf()
    
    st.markdown("######")
    st.markdown("######")
    copyright_footer_dos("Equipo Investigador", margin_right="0px")
    recargar_una_vez(__file__) 

ver_reportes()
reload_on_back()