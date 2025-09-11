import streamlit as st
import sqlite3
import os
from utils.sql_control import mostrar_descripcion_departamento, mostrar_descripcion_hospital
from pathlib import Path

DB_PATH = os.environ.get("DB_PATH", "hospital.db")
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

# Rutas a los manuales de usuario en PDF
RUTA_PDF_ADMIN = PDF_DIR / "cuadropio.pdf"
RUTA_PDF_DOCTOR = PDF_DIR / "MANUAL PROYECTO  UPTJAA 2022.pdf"
RUTA_PDF_SECRETARIA = PDF_DIR / "METODOLOGIAS_ RUP, XP, SCRUM.pdf"

def nosotros():
    nosotros_sg = st.popover("Sobre Nosotros", icon=":material/contact_support:", width="stretch")
    with nosotros_sg:
        st.subheader(":material/contact_page: Contactanos al:", divider="gray", anchor=False)
        st.markdown(":green[Whatsapp:]")
        st.write("Samuel Urbano: +58 0424-8528064")
        st.markdown("Gustavo Heredia: +58 0414-7966434")
        st.markdown(":red[Gmail:]")
        st.markdown("Samuel Urbano: samuel.urbano.arana@gmail.com")
        st.markdown("Gustavo Heredia: newpersonal98@gmail.com")

def hospital():
    _, col_titulo = st.columns([1.29, 2.8])
    with col_titulo:
        st.subheader(":material/medical_information: Información de la institución", anchor=False)#, divider="gray"
    col_hospital, col_depa = st.columns(2)
    with col_hospital:
        st.subheader(":material/home_health: Sobre el Hospital...", anchor=False, divider="gray")
        mostrar_descripcion_hospital()
    with col_depa:
        st.subheader(":material/local_hospital: Sobre el Departamento...", anchor=False, divider="gray")
        mostrar_descripcion_departamento()
    # aqui la informacion del personal

def mision():
    try: # conexion a la bd
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT contenido FROM mision WHERE id_departamento = (SELECT id_departamento FROM departamento WHERE nombre = ?)", ('Epidemiología',))
        texto_mision = cursor.fetchone()[0]
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")

    try: # lo que se ve
        with st.popover("Misión", icon=":material/target:", width="stretch"):
            st.header(":material/target: Misión", divider="gray", anchor=False)
            st.markdown(texto_mision)
        conn.close()
    except Exception as e:
       st.error(f"Ocurrió un error: {e}")

def vision():
    try: # bd
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT contenido FROM vision WHERE id_departamento = (SELECT id_departamento FROM departamento WHERE nombre = ?)", ('Epidemiología',))
        texto_vision = cursor.fetchone()[0]
    except sqlite3.Error as e:
        conn.rollback()
        st.error(f"Error en la base de datos: {e}", icon=":material/error:")
    
    try: # lo q se ve
        with st.popover("Visión", icon=":material/emoji_objects:", width="stretch"):
            st.header(":material/emoji_objects: Visión", divider="gray", anchor=False)
            st.markdown(texto_vision)
        conn.close()
    except Exception as e:
       st.error(f"Ocurrió un error: {e}")

def manual_de_uso():
    try:
        with st.popover("Manual de usuario", icon=":material/developer_guide:", width="stretch"):
            st.subheader(":material/pageview: Ver manual de usuario", divider="gray", anchor=False)
            ver_manual = st.button("Ver PDF", icon=":material/export_notes:", width="stretch")
            if ver_manual:
                st.switch_page("pages/manual_usuario.py")
                st.rerun()
    except Exception as e:
       st.error(f"Ocurrió un error: {e}")
