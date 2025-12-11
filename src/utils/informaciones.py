import streamlit as st
import sqlite3
import os
from utils.base_64 import img_a_base64
from pathlib import Path
from utils.sql_control import mostrar_descripcion_departamento, mostrar_descripcion_hospital
from pathlib import Path

DB_PATH = os.getenv("hospital.db", "hospital.db")
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

# rutas iconos para el identificadoe
RUTA_ADMIN_SVG = ASSETS_DIR / "admin.svg"
RUTA_DOCTOR_SVG = ASSETS_DIR / "doctor.svg"
RUTA_SECRETARIA_SVG = ASSETS_DIR / "secretaria.svg"

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
    col_hospital, col_depa = st.columns(2, gap="medium")
    with col_hospital:
        st.subheader(":material/home_health: Sobre el Hospital...", anchor=False, divider="gray")
        mostrar_descripcion_hospital()
    with col_depa:
        st.subheader(":material/local_hospital: Sobre el Departamento...", anchor=False, divider="gray")
        mostrar_descripcion_departamento()
    # aqui la informacion del personal

def mision():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT mision FROM departamento WHERE nombre = 'Epidemiología'")
        row = cursor.fetchone()
        conn.close()
        
        texto = (row[0] if row and row[0] else "Misión no definida aún.")
        
        with st.popover("Misión", icon=":material/target:", width="stretch"):
            st.header(":material/target: Misión", divider="gray", anchor=False)
            st.markdown(f"<div style='text-align: justify; margin: 10px 0;'>{texto}</div>", unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error al cargar la misión: {e}", icon=":material/error:")
        

def vision():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT vision FROM departamento WHERE nombre = 'Epidemiología'")
        row = cursor.fetchone()
        conn.close()
        
        texto = (row[0] if row and row[0] else "Visión no definida aún.")
        
        with st.popover("Visión", icon=":material/emoji_objects:", width="stretch"):
            st.header(":material/emoji_objects: Visión", divider="gray", anchor=False)
            st.markdown(f"<div style='text-align: justify; margin: 10px 0;'>{texto}</div>", unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error al cargar la visión: {e}", icon=":material/error:")
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

def mostrar_usuario_activo():
    if "autenticado_usuario" not in st.session_state:
        st.sidebar.error("Debes iniciar sesión.", icon=":material/error:")
        return
    nombre_usuario = st.session_state["autenticado_usuario"]
    from utils.verificaciones import obtener_info_usuario
    info_usuario = obtener_info_usuario(nombre_usuario)
    if not info_usuario:
        st.sidebar.error("Usuario no encontrado.", icon=":material/error:")
        return
    rol_usuario = info_usuario["rol"]

    st.sidebar.markdown(
        f"""
        <div style="
        .usuario-fixed {{
            position: fixed;
            top: 20px;
            right: 30px;
            z-index: 9999;
            background: linear-gradient(90deg, #e0eafc 0%, #cfdef3 100%);
            border-radius: 12px;
            padding: 5px 10px; 
            margin-top: 18px;
            margin-bottom: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
            text-align: center;
        ">
        }}
            <span style="
                font-size: 22px; 
                font-weight: 700; 
                color: #1a237e;
                display: block;
                margin-bottom: 2px;
            ">
                {nombre_usuario}
            </span>
            </span>
            <span style="font-size: 16px; font-weight: 500; color: #3949ab;">
                {rol_usuario} 
            </span>
        </div>
        """,
        # Asegúrate de que este parámetro esté siempre presente para HTML
        unsafe_allow_html=True
    )

def usuario_activo_fixed():
    # iconos a base64
    svg_base64_admin = img_a_base64(RUTA_ADMIN_SVG)
    svg_base64_doctor = img_a_base64(RUTA_DOCTOR_SVG)
    svg_base64_secretaria = img_a_base64(RUTA_SECRETARIA_SVG)
    if "autenticado_usuario" not in st.session_state:
        return

    nombre_usuario = st.session_state["autenticado_usuario"]
    from utils.verificaciones import obtener_info_usuario
    info_usuario = obtener_info_usuario(nombre_usuario)
    if not info_usuario:
        return

    rol_usuario = info_usuario["rol"]
    nombre_apellido = info_usuario.get("nombre_apellido", nombre_usuario)

    # Selecciona el icono según el rol
    iconos_base64 = {
        "Administrador (a)": svg_base64_admin,
        "Doctor (a)": svg_base64_doctor,
        "Secretario (a)": svg_base64_secretaria,
    }
    icon_base64 = iconos_base64.get(rol_usuario)

    html_content = f"""
    <style>
    .usuario-fixed {{
        position: fixed;
        top: 14px;
        right: 20px;
        z-index: 9999;
        background: #9EB9D4;
        border-radius: 12px;
        padding: 10px 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.10);
        display: flex;
        align-items: center;
        gap: 12px;
        font-family: 'Roboto', sans-serif;
        min-width: 120px;
    }}
    .icon-circle {{
        padding: 6px;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #fff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.10);
        overflow: hidden;
    }}
    .nombre {{
        font-size: 19px;
        font-weight: 700;
        color: #1a237e;
        line-height: 1.2;
    }}
    .rol {{
        font-size: 17px;
        font-weight: 600;
        color: #3949ab;
    }}
    </style>
    <div class="usuario-fixed">
        <div class="icon-circle">
            {"<img src='data:image/svg+xml;base64," + icon_base64 + "' width='32' height='32'/>" if icon_base64 else ""}
        </div>
        <div>
            <div class="nombre">{nombre_apellido}</div>
            <div class="rol">{rol_usuario}</div>
        </div>
    </div>
    """

    st.markdown(html_content, unsafe_allow_html=True)