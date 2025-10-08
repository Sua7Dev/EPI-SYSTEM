import streamlit as st
from pathlib import Path
import time
import os
import sys
from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez, copyright_footer
from utils.validaciones import val_solo_numeros, validar_contraseña, validar_texto, val_mail
from utils.base_64 import img_a_base64
from utils.verificaciones import verificar_usuario, obtener_info_usuario, guardar_preguntas_seguridad, verificar_preg_res_seg
from utils.contra import borro_cassette
from utils.bienvenida import bienvenida
from utils.verificaciones import obtener_info_usuario, verificar_preguntas_guardadas, verificar_correo_cedula, obtener_nombre_usuario


configurar_pagina_espanol()

# --- CONFIGURACIÓN DE RUTAS ---
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

# Ruta global de la base de datos, con respaldo de variable de entorno
DB_PATH = os.getenv("hospital.db", "hospital.db")

@st.dialog(":material/data_loss_prevention: Recupera tu usuario")
def recuperar_usuario():
    with st.form(key='recuperar_usuario'):
        correo = st.text_input("Ingresa tu correo electrónico", max_chars=50, icon=":material/email:",
                               help="Tiene que ser un correo registrado en el sistema.", placeholder='Ejemplo: Juan@gmail.com')
        ci = st.text_input("Primeros 4 dígitos de la cédula", max_chars=4, type="password", icon=":material/contact_mail:",
                           placeholder="Ejemplo: 1234", help="Tiene que ser de la cédula asociada al correo.")
        colsi, colno = st.columns(2)
        with colsi:    
            si = st.form_submit_button("Verificar", icon=":material/conditions:", width="stretch", type="primary")        
        with colno:    
            no = st.form_submit_button("Cancelar", icon=":material/cancel:", width="stretch")
        if si:
            if not correo or not ci:
                st.warning("Por favor, completa todos los campos.", icon=":material/warning:")
                return
            elif not val_mail(correo):
                return
            elif not val_solo_numeros(ci, "Los", "digitos de la cédula de identidad"):
                return
            else:
                if verificar_correo_cedula(correo, ci, DB_PATH=DB_PATH):
                    obtener_nombre_usuario(correo, ci, DB_PATH=DB_PATH)
        if no:
            st.rerun()               




def foto():
    img_b64 = img_a_base64(ASSETS_DIR / "medicina (1).webp")
    st.markdown(
        f"""
        <style>
        .stApp header {{
            display: none;
        }}
        .stApp {{
            background-image: url("data:image/jpeg;base64,{img_b64}");
            background-size: 50vw 100vh;
            background-position: left top;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp [data-testid="stSidebar"] {{
            background-color: white;
            z-index: 100;
        }}
        .stApp > div:first-child > .main > div:nth-child(1) {{
            background-color: transparent !important;
        }}
        .stApp > div:first-child > .main > div:nth-child(2) {{
            background-color: rgba(255, 255, 255, 0.9);
            height: 100vh;
            overflow-y: auto;
            box-sizing: border-box;
        }}
        .stApp > div:first-child > .main > div:nth-child(2) .block-container {{
            padding-top: 2rem;
            padding-right: 2rem;
            padding-left: 2rem;
            padding-bottom: 2rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def iniciar_sesion():
    with st.container():
        logo(tamano="100%")
        st.markdown("")
        st.header(":material/badge: Inicio de sesión", anchor=False, divider="gray")
        with st.form(key="inicio_sesion"):
            nombre_usuario = st.text_input("Nombre de usuario:", placeholder='Ejemplo: Juan33', 
                                           icon=":material/person_check:", max_chars=18, key="usuario",
                                           help="El nombre de usuario debe estar ya registrado en el sistema.")
            contrasena = st.text_input("Contraseña", type="password", max_chars=18, 
                                       icon=":material/security:", key="contra",
                                       help="La contraseña debe estar la asociada al usuario.")
            iniciar_btn = st.form_submit_button(label="Iniciar sesión", type="primary", 
                                                icon=":material/login:", 
                                                width="stretch")

            if iniciar_btn:
                if nombre_usuario and contrasena:
                    if verificar_usuario(nombre_usuario, contrasena, DB_PATH=DB_PATH):
                        info_usuario = obtener_info_usuario(nombre_usuario, DB_PATH=DB_PATH)
                        if not info_usuario:
                            st.error("No se pudo obtener la información del usuario.", icon=":material/error:")
                            return            
                        if verificar_preguntas_guardadas(nombre_usuario, DB_PATH=DB_PATH):
                            st.switch_page("pages/inicio.py")
                        else:
                            if bienvenida(nombre_usuario):
                                st.switch_page("pages/inicio.py")
                else:
                    st.warning("Por favor, ingresa tu usuario y contraseña para iniciar sesión.")    

    _, col_olvido, col_olvido_usuario = st.columns([2.1, 4.5, 5], vertical_alignment="bottom", gap=None)
    with col_olvido:
        olvido_btn = st.button(":blue-background[¿Olvidaste tu contraseña?]", type="tertiary")
    with col_olvido_usuario:
        olvido_usuario = st.button(":blue-background[¿Olvidaste tu usuario?]", type="tertiary")
    
    if olvido_usuario:
        recuperar_usuario()
    if olvido_btn:
        st.switch_page("pages/olvido_contraseña.py")


def login():
    logo_path = ASSETS_DIR / "imagebanderanueva2.png"
    st.set_page_config(layout="wide", page_icon=str(logo_path))
    recargar_una_vez(__file__)
    colfoto, coltext = st.columns([3, 2.7])    
    with colfoto:
        with st.container():
            foto()
    with coltext:
        with st.container():
            iniciar_sesion()
            copyright_footer("SAMUEL URBANO & GUSTAVO HEREDIA")
    

login()
