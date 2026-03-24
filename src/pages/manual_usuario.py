import streamlit as st
from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez, copyright_footer_dos
from utils.base_64 import img_a_base64
from streamlit_extras.pdf_viewer import pdf_viewer
from utils.verificaciones import obtener_info_usuario
from utils.recargar_retroceso import reload_on_back
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

# Mapeo de roles a sus respectivos manuales en PDF 
MANUALES_POR_ROL = {
    "Administrador (a)": PDF_DIR / "MANUAL ADMIN.pdf",
    "Doctor (a)": PDF_DIR / "MANUAL DOCTOR.pdf",
    "Secretario (a)": PDF_DIR / "MANUAL SECREATARIA.pdf"
}

def botones_manual():
    volver_btn = st.button(label="Volver atras", type="primary", icon=":material/arrow_back:")
    if volver_btn:
        st.switch_page("pages/configuracion.py")
        st.rerun()

def mostrar_pdf():
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a este apartado.", icon=":material/error:")
        return
    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)
    
    # Normalizamos el rol para que la primera letra sea mayúscula y coincida con las claves del diccionario.
    # Esto hace la búsqueda más robusta ante variaciones de mayúsculas/minúsculas.
    rol_usuario = info_usuario["rol"]#.capitalize()
    # esto no sirvio xd
    ruta_pdf = MANUALES_POR_ROL.get(rol_usuario)    
    
    if ruta_pdf: #and ruta_pdf.exists():
        # pdf_viewer puede manejar objetos Path directamente
        pdf_viewer(ruta_pdf)
    else:
        st.error("No se encontró el manual para tu rol o el archivo no existe.", icon=":material/error:")

def manual_usuario():
    logo_bandera = ASSETS_DIR / "imagebanderanueva2.png"
    logo_base64 = img_a_base64(logo_bandera)
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) # Llama a la función para recargar la página una vez.
    logo(tamano="70%")
    mostrar_pdf()
    botones_manual()
    st.markdown("######")
    st.markdown("######")
    copyright_footer_dos("Equipo Investigador", margin_right="0px")

manual_usuario()
reload_on_back()