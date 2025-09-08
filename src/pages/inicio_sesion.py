import streamlit as st
from pathlib import Path
import time
try:
    from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez
    from utils.validaciones import val_solo_numeros, validar_contraseña, validar_texto, val_mail
    from utils.base_64 import img_a_base64
    from utils.verificaciones import verificar_usuario, obtener_info_usuario, guardar_preguntas_seguridad, verificar_preg_res_seg
    from utils.contra import borro_cassette
    from utils.bienvenida import bienvenida
    from utils.verificaciones import obtener_info_usuario, verificar_preguntas_guardadas, verificar_correo_cedula, obtener_nombre_usuario
except ValueError as e:
    st.error("xd")

configurar_pagina_espanol()
# --- CONFIGURACIÓN DE RUTAS ---
# Esto crea una ruta absoluta al directorio raíz del proyecto (V6)
# Path(__file__) -> .../V6/src/pages/inicio_sesion.py
# .parent -> .../V6/src/pages
# .parent -> .../V6/src
# .parent -> .../V6/
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = PROJECT_ROOT / "static" / "assets" / "imagenes"

@st.dialog(":material/data_loss_prevention: Recupera tu usuario")
def recuperar_usuario():
    with st.form(key='recuperar_usuario'):
        correo = st.text_input("Ingresa tu correo electrónico", max_chars=50, icon=":material/email:",
                               help="Tiene que ser un correo registrado en el sistema.", placeholder='Ejemplo: Juan@gmail.com')
        ci = st.text_input("Primeros 4 dígitos de la cédula", max_chars=4, type="password", icon=":material/contact_mail:",
                           placeholder="Ejemplo: 1234", help="Tiene que ser de la cédula asociada al correo.")
        colsi, colno = st.columns(2)
        with colno:    
            no = st.form_submit_button("Cancelar", icon=":material/cancel:", width="stretch")
        with colsi:    
            si = st.form_submit_button("Verificar", icon=":material/conditions:", width="stretch", type="primary")
        if no:
            st.rerun()               
        if si:
            if not correo or not ci:
                st.warning("Por favor, completa todos los campos.", icon=":material/warning:")
                return
            elif not val_mail(correo):
                return
            elif not val_solo_numeros(ci, "Los", "digitos de la cédula de identidad"):
                return
            else:
                if verificar_correo_cedula(correo, ci):
                    obtener_nombre_usuario(correo, ci)



def foto():
    img_b64 = img_a_base64(ASSETS_DIR / "medicina (1).webp")
    st.markdown(
        f"""
        <style>
        /* Oculta el encabezado predeterminado de Streamlit si existe */
        .stApp header {{
            display: none;
        }}

        /* Aplica la imagen de fondo directamente al elemento raíz de la aplicación Streamlit */
        /* Esto asegura que la imagen esté en el "fondo fondo" y no se mueva */
        .stApp {{
            background-image: url("data:image/jpeg;base64,{img_b64}");
            background-size: 50vw 100vh; /* La imagen cubre el 50% del ancho y 100% del alto del viewport */
            background-position: left top; /* La imagen se alinea a la izquierda y arriba */
            background-repeat: no-repeat; /* No repite la imagen */
            background-attachment: fixed; /* Mantiene la imagen fija al desplazarse */
        }}

        /* Asegura que el sidebar esté por encima del fondo y tenga un color sólido */
        .stApp [data-testid="stSidebar"] {{
            background-color: white; /* Color de fondo sólido para cubrir la imagen */
            z-index: 100; /* Asegura que el sidebar esté por encima de todo */
        }}

        /* Estilo para la columna izquierda (colfoto) para que sea transparente y muestre la imagen de fondo */
        /* Esta es la primera columna dentro del contenedor principal (.main) */
        .stApp > div:first-child > .main > div:nth-child(1) {{
            background-color: transparent !important; /* Asegura que sea transparente */
        }}

        /* Estilo para la columna derecha (coltext) donde está el formulario */
        /* Esta es la segunda columna dentro del contenedor principal (.main) */
        .stApp > div:first-child > .main > div:nth-child(2) {{
            background-color: rgba(255, 255, 255, 0.9); /* Fondo blanco semi-transparente para el formulario */
            height: 100vh; /* Asegura que cubra toda la altura de la ventana */
            overflow-y: auto; /* Permite desplazamiento si el contenido es largo */
            box-sizing: border-box; /* Incluye el padding en el cálculo del ancho/alto */
        }}

        /* Ajustes para el padding del block-container dentro de la columna derecha */
        /* Esto es para el padding interno del formulario */
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


# Formulario con todo y logos
def iniciar_sesion():

    with st.container():
        logo(tamano="100%") # helpppp
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
                                                width="stretch") #, on_click=click_prueba

            if iniciar_btn:# este es el bueno
                if nombre_usuario and contrasena:
                    if verificar_usuario(nombre_usuario, contrasena):
                        info_usuario = obtener_info_usuario(nombre_usuario)
                        if not info_usuario:
                            st.error("No se pudo obtener la información del usuario.", icon=":material/error:")
                            return            
                        if verificar_preguntas_guardadas(nombre_usuario):
                            st.switch_page("pages/inicio.py")
                        else:
                            if bienvenida(nombre_usuario):
                                st.switch_page("pages/inicio.py")
                    #else:
                    #    st.error("Usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.")
                else:
                    st.warning("Por favor, ingresa tu usuario y contraseña para iniciar sesión.")    

    _, col_olvido, col_olvido_usuario = st.columns([2.1, 4.5, 5], vertical_alignment="bottom", gap=None)
    # APARTIR DE AQUI PONER NUEVA LOGICA DE INICIO DE SESION
    with col_olvido:
        olvido_btn = st.button(":blue-background[¿Olvidaste tu contraseña?]", type="tertiary")
    with col_olvido_usuario:
        olvido_usuario = st.button(":blue-background[¿Olvidaste tu usuario?]", type="tertiary")
    
    if olvido_usuario:
        recuperar_usuario()
    if olvido_btn:
        st.switch_page("pages/olvido_contraseña.py")

# Ejecucion principal de toda la pagina
def login():
    logo_path = ASSETS_DIR / "imagebanderanueva2.png"
    st.set_page_config(layout="wide", page_icon=str(logo_path))
    recargar_una_vez(__file__) # Llama a la función para recargar la página una vez.
    colfoto, coltext = st.columns([3, 2.7])    
    with colfoto:
        with st.container():
            foto()
    with coltext:
        with st.container():
            
            iniciar_sesion()
    

login()