import streamlit as st
from datetime import datetime
import time
from utils.base_64 import img_a_base64
from pathlib import Path

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

def logo(tamano):
    logo_path = img_a_base64(ASSETS_DIR / "cc1.png")
    html_code = f'''
    <div class="logo-centro">
        <img src="data:image/png;base64,{logo_path}" width={tamano}/> <!-- 30% para paginas, 55 para el inicio sesion -->
    </div>
    '''
    st.markdown(
    """
    <style>
    body, .main, .block-container {
        overflow-x: hidden !important;
    }
    .block-container {
        padding-top: 0.5rem !important; /* Reduce el espacio superior general */
    }
    .logo-centro {
        display: flex;
        justify-content: center;
        align-items: flex-start;
        margin-top: 0;
        margin-bottom: 0.1rem;
    }
    </style>
    """,
    unsafe_allow_html=True)
    st.markdown(html_code, unsafe_allow_html=True)

@st.fragment(run_every=1)  # Actualiza cada 1 segundo
def reloj():
    # Obtiene la hora actual
    hora_actual = datetime.now()

    # Formatea la hora en formato de 12 horas sin AM/PM
    hora_str = hora_actual.strftime("%I:%M:%S")

    # Determina si es AM o PM
    if hora_actual.hour >= 12:
        meridiano = "PM"
    else:
        meridiano = "AM"
    
    # Combina la hora y el meridiano
    hora_completa = f"{hora_str} {meridiano}"
    
    st.subheader(f":material/schedule: Hora actual: {hora_completa}", anchor=False)

def notificacion_cambios():
    msg = st.toast('Preparando cambios...', icon=":material/hourglass_top:") # ":material/hourglass_top:"
    time.sleep(1)
    msg.toast('Guardando cambios...', icon=":material/hourglass_bottom:")
    time.sleep(1)
    msg.toast(":green[Cambios guardados correctamente.]", icon =":material/cloud_done:")
    time.sleep(1)


# Grafico de barras de progreso
# mostrada en el registro de usuario y cuando inicias sesion
def mostrar_progreso():
    progreso_texto = "Cargando... Por favor espera."
    barra_progreso = st.progress(0, text=progreso_texto)
    for porcentaje in range(100):
        time.sleep(0.01)
        barra_progreso.progress(porcentaje + 1, text=progreso_texto)
    time.sleep(1)
    barra_progreso.empty()

def cargando(mensaje, icono=":hourglass:"):
    msg = st.toast('Preparando...', icon=":material/hourglass_top:") # ":material/hourglass_top:"
    time.sleep(1)
    msg.toast('Ya casi...', icon=":material/hourglass_bottom:")
    time.sleep(1)
    msg.toast(f":green[{mensaje}]", icon=icono)

def configurar_pagina_espanol():
    """
    Inyecta un script a través de st.markdown para establecer el idioma de la página en español ('es')
    y añade lógica global para evitar multiclicks en botones críticos.
    Se debe llamar al principio de cada página de la aplicación.
    """
    js_code = """
    <script>
    // 1. Establecer idioma
    document.querySelector('html').lang = 'es';
    </script>
    """
    st.markdown(js_code, unsafe_allow_html=True)

def recargar_una_vez(caller_file, delay=0.01):
    """
    Ejecuta st.rerun() una sola vez cuando se entra en una página.

    Utiliza el `session_state` para controlar que la recarga se haga una única vez
    por página, usando el nombre del archivo que llama a la función para crear una
    clave de sesión única.

    Args:
        caller_file (str): Debe ser `__file__` desde el script que llama a la función.
        delay (float): Tiempo de espera en segundos antes de ejecutar st.rerun().
    """
    session_key = f"rerun_done_{Path(caller_file).stem}"
    if not st.session_state.get(session_key, False):
        st.session_state[session_key] = True
        time.sleep(delay)
        st.rerun()

def copyright_footer(autor_o_empresa):
    """
    Muestra un footer fijo en la parte inferior de la aplicación Streamlit.
    NOTA: Esto usa HTML/CSS inseguro para forzar el footer.
    """
    # 1. CSS y HTML inyectados
    footer_html = f"""
    <style>
        /* Asegura que el footer se fije en la parte inferior de la ventana 
        y no solo del contenido. Se usa 'position: fixed' para esto.
        */
        .footer {{
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f2f2f2; /* Color de fondo */
            color: #555;
            text-align: center;
            padding: 10px 0;
            font-size: 0.85em;
            border-top: 1px solid #ccc;
            z-index: 100; /* Asegura que esté por encima de otros elementos */
        }}
        .footer a {{
            color: #007bff; /* Color de enlace */
            text-decoration: none;
        }}
        .footer a:hover {{
            text-decoration: underline;
        }}
    </style>
    
    <div class="footer">
        &copy; 2025 {autor_o_empresa}. Copyright.
        <a href="" target="_blank"></a>
    </div>
    """
    
    # 2. Inyectar en Streamlit, permitiendo HTML inseguro
    st.markdown(footer_html, unsafe_allow_html=True)


def copyright_footer_dos(autor_o_empresa, left="-83px", bottom="-160px", margin_right="260px"):
    """
    Muestra un footer fijo en la parte inferior de la aplicación Streamlit.
    NOTA: Esto usa HTML/CSS inseguro para forzar el footer.
    """
    # 1. CSS y HTML inyectados
    footer_html = f"""
    <style>
        /* Asegura que el footer se fije en la parte inferior de la ventana 
        y no solo del contenido. Se usa 'position: fixed' para esto.
        */
        .footer {{
            position: absolute;        
            left: {left};
            bottom: {bottom};
            width: 100vw;
            background-color: #f2f2f2; /* Color de fondo */
            color: #555;
            text-align: center;
            padding: 10px 0;
            font-size: 0.85em;
            border-top: 10px; /*  solid #ccc */
            z-index: 100; /* Asegura que esté por encima de otros elementos */
        }}
        .footer a {{
            color: #007bff; /* Color de enlace */
            text-decoration: none;
            margin-right: {margin_right};
        }}
        .footer a:hover {{
            text-decoration: underline;
        }}
    </style>
    
    <div class="footer">
        &copy; 2025 {autor_o_empresa}. Copyright.
        <a href="" target="_blank"></a>
    </div>
    """
    
    # 2. Inyectar en Streamlit, permitiendo HTML inseguro
    st.markdown(footer_html, unsafe_allow_html=True)

def markdown_sin_link():
    hide_anchor_link_css = """
    <style>
    /* CLAVE: Selecciona todos los enlaces de anclaje generados automáticamente 
              por los encabezados (h1, h2, h3, etc.) y los oculta. */
    h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {
        display: none !important; 
    }
    </style>
    """
    
    # Inyecta el CSS en la aplicación
    st.markdown(hide_anchor_link_css, unsafe_allow_html=True)

    # Ahora, tus encabezados ya no mostrarán el ícono de enlace
    # este de abajo es para probar
   # st.markdown("## Título de la Sección Sin Link") 