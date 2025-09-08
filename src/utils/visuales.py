import streamlit as st
from datetime import datetime
import time
from utils.base_64 import img_a_base64
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
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
    Inyecta un script a través de st.markdown para establecer el idioma de la página en español ('es').
    Esto evita que el navegador muestre el pop-up de "Traducir página".
    Se debe llamar al principio de cada página de la aplicación.
    """
    st.markdown(
        """<script>document.querySelector('html').lang = 'es';</script>""",
        unsafe_allow_html=True
    )

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
