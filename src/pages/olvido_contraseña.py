import streamlit as st
from pathlib import Path
import os
import time
from utils.verificaciones import (
    verificar_usuario_cedula,
    obtener_contrasena_actual,
    cambiar_contrasena,
    verificar_preg_res_seg,
    obtener_preguntas_usuario
)
from utils.base_64 import img_a_base64
from utils.validaciones import val_solo_numeros, validar_contraseña, validar_texto, validar_nombre_usuario
from utils.visuales import cargando, configurar_pagina_espanol, logo, recargar_una_vez, copyright_footer_dos
from utils.contra import borro_cassette, verifi_contra_hasheada
import sys

# Initialize session state
if "olvido_usuario_id" not in st.session_state:
    st.session_state["olvido_usuario_id"] = None
if "pagina_actual" not in st.session_state:
    st.session_state["pagina_actual"] = "verificacion"

# ------------------- Rutas y configuración -------------------
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

# Ruta global de la base de datos
DB_PATH = os.path.abspath(os.getenv("hospital.db", "hospital.db"))  # Ensure absolute path
configurar_pagina_espanol()

# ------------------- Fragmentos de Streamlit -------------------
@st.fragment
def nueva_contra():
    st.markdown("")
    st.header(":material/lock_reset: Actualiza tu contraseña", anchor=False)
    
    with st.form(key="form_nueva_contra"):
        nueva_contra = st.text_input(
            "Ingresa tu nueva contraseña",
            key="nueva_contra",
            type="password",
            max_chars=16,
            icon=":material/visibility_lock:"
        )
        confirmar_contra = st.text_input(
            "Confirma tu nueva contraseña",
            key="confirmar_contra",
            type="password",
            max_chars=16,
            icon=":material/preview_off:"
        )
        st.info(
            'La contraseña debe tener entre 8 y 16 caracteres, una letra minúscula, una mayúscula y al menos un número.',
            icon=":material/info:"
        )
        col_verificar, col_cancelar = st.columns(2)
        with col_verificar:
            btn_verificar = st.form_submit_button(
                "Cambiar contraseña", type="primary", width="stretch", icon=":material/verified_user:"
            )
        with col_cancelar:
            btn_cancelar = st.form_submit_button(
                "Cancelar", type="secondary", width="stretch", icon=":material/cancel:",
                help="Vuelves a la Verificación de Usuario y Cédula."
            )

        if btn_verificar:
            if not nueva_contra or not confirmar_contra:
                st.error("Ambos campos son obligatorios.", icon=":material/error:")
            elif nueva_contra != confirmar_contra:
                st.error("Las contraseñas no coinciden.", icon=":material/error:")
            elif not validar_contraseña(nueva_contra):
                return
            else:
                usuario = st.session_state.get("olvido_usuario_id")
                if not usuario:
                    st.error("Sesión inválida. Regresa a verificación.", icon=":material/error:")
                    if st.button("Regresar a Verificación", key="btn_regresar_olvido"):
                        st.session_state["pagina_actual"] = "verificacion"
                        st.session_state["olvido_usuario_id"] = None
                        st.rerun()
                    return
                
                contrasena_actual = obtener_contrasena_actual(usuario, DB_PATH)
                if contrasena_actual is None:
                    return

                if verifi_contra_hasheada(nueva_contra, contrasena_actual):
                    st.error("La contraseña es igual a la actual.", icon=":material/error:")
                    return

                nueva_contra_hash = borro_cassette(nueva_contra)
                exito = cambiar_contrasena(nueva_contra_hash, usuario, DB_PATH)

                if exito:
                    st.success("Contraseña actualizada correctamente.", icon=":material/check_circle:")
                    time.sleep(1)
                    st.success("Volviendo a inicio de sesión...", icon=":material/check_circle:")
                    time.sleep(1)
                    st.session_state["olvido_usuario_id"] = None
                    st.session_state["pagina_actual"] = "verificacion"
                    st.switch_page("pages/inicio_sesion.py")
                else:
                    st.error("Error al actualizar la contraseña en la base de datos.", icon=":material/error:")

    if btn_cancelar:
        st.session_state["olvido_usuario_id"] = None
        st.session_state["pagina_actual"] = "verificacion"
        st.rerun()

@st.fragment
def P_Seguridad():
    st.header(":material/question_exchange: Verificación de Preguntas", anchor=False)
    usuario = st.session_state.get("olvido_usuario_id")
    preguntas = st.session_state.get("olvido_preguntas") or (obtener_preguntas_usuario(usuario, DB_PATH) if usuario else None)

    if not preguntas:
        st.error("Este usuario no tiene preguntas de seguridad registradas. Vuelve al inicio.", icon=":material/error:")
        if st.button("Volver", key="btn_volver_sin_preg"):
            st.session_state["pagina_actual"] = "verificacion"
            st.session_state["olvido_usuario_id"] = None
            st.rerun()
        return

    pregunta_uno, pregunta_dos, pregunta_tres = preguntas

    with st.form(key="form_P_Seguridad"):
        #st.markdown()
        respuesta_uno = st.text_input(f"**Pregunta 1:** {pregunta_uno}", type='password', key="respuesta_uno",
                                      icon=":material/security:", max_chars=18,)
        #st.markdown()
        respuesta_dos = st.text_input(f"**Pregunta 2:** {pregunta_dos}", type='password', key="respuesta_dos",
                                      icon=":material/security:", max_chars=18,)
        #st.markdown()
        respuesta_tres = st.text_input(f"**Pregunta 3:** {pregunta_tres}", type='password', key="respuesta_tres",
                                       icon=":material/security:", max_chars=18,)

        col_verificar, col_cancelar = st.columns(2)
        with col_verificar:
            btn_verificar = st.form_submit_button("Verificar", type="primary", width="stretch", icon=":material/verified_user:")
        with col_cancelar:
            btn_cancelar = st.form_submit_button("Cancelar", type="secondary", width="stretch", icon=":material/cancel:")

        if btn_verificar:
            if not all([respuesta_uno, respuesta_dos, respuesta_tres]):
                st.error("Todos los campos son obligatorios.", icon=":material/error:")
                return
            if not validar_texto(respuesta_uno, "La", "primera respuesta de seguridad"): return
            if not validar_texto(respuesta_dos, "La", "segunda respuesta de seguridad"): return
            if not validar_texto(respuesta_tres, "La", "tercera respuesta de seguridad"): return

            ok, _ = verificar_preg_res_seg(
                respuesta_uno, pregunta_uno,
                respuesta_dos, pregunta_dos,
                respuesta_tres, pregunta_tres,
                usuario, DB_PATH
            )
            if ok:
                st.session_state["pagina_actual"] = "nueva_contra"
                st.rerun()

        if btn_cancelar:
            st.session_state["olvido_usuario_id"] = None
            st.session_state["pagina_actual"] = "verificacion"
            st.rerun()

# ------------------- Funciones auxiliares -------------------
def fotodos(tamano):
    ruta_imagen = ASSETS_DIR / "child.webp"
    img_b64 = img_a_base64(ruta_imagen)
    html_code = f'''
    <div class="logo-centro">
        <img src="data:image/png;base64,{img_b64}" width={tamano}/>
    </div>
    '''
    st.markdown(
    """
    <style>
    body, .main, .block-container {
        overflow-x: hidden !important;
    }
    .block-container {
        padding-top: 0.5rem !important;
    }
    .logo-centro {
        display: flex;
        justify-content: center;
        align-items: flex-start;
        margin-top: 0;
        margin-bottom: 0.1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(html_code, unsafe_allow_html=True)

def informacion():
    st.write("")
    _, col_centro = st.columns([0.2, 2.8])
    with col_centro:
        st.subheader(":material/sentiment_dissatisfied: ¿Has olvidado tu contraseña?", anchor=False)

    st.markdown("¡No te preocupes! **Sigue** estos sencillos pasos para recuperar el acceso a tu cuenta.")

    col_paso1, col_paso2 = st.columns([1.5, 2])
    with col_paso1:
        st.subheader(":material/looks_one: Identificación", anchor=False)
        st.markdown("Indica tu **nombre de usuario** y los **últimos 4 dígitos de tu cédula**.")
    with col_paso2:
        st.subheader(":material/looks_two: Preguntas de seguridad", anchor=False)
        st.markdown("Responde tus **3 preguntas de seguridad** registradas y verifica.")

    st.subheader(":material/looks_3: ¡Listo! Cambia tu contraseña", anchor=False)
    st.markdown("Establece una nueva contraseña. Recuerda **cumplir** con los siguientes parámetros:")
    col_fila1, col_fila2 = st.columns(2)
    with col_fila1:
        st.info(':material/done_outline: Entre 8 y 16 caracteres.')
        st.info(':material/done_outline: Debe incluir al menos una letra minúscula.')
    with col_fila2:
        st.info(':material/done_outline: Debe incluir al menos un número.')
        st.info(':material/done_outline: Debe incluir al menos una letra mayúscula.')
    st.warning("Si no puedes desbloquear tu cuenta, por favor contacta al administrador.", icon=":material/supervisor_account:")

@st.fragment
def formulario_verificacion():
    st.markdown("")
    st.header(":material/passkey: Verificación de Usuario y Cédula", anchor=False)

    st.components.v1.html("""
        <script>
        const setupLogic = () => {
            const doc = window.parent.document;
            const inputs = doc.querySelectorAll('input[type="number"]');
            
            inputs.forEach(input => {
                if (!input.dataset.listenerActive) {
                    // Bloqueo por teclado (Keydown)
                    input.addEventListener('keydown', (e) => {
                        const prohibidas = ['e', 'E', '+', '-', '.', ','];
                        const esControl = ['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab', "Enter"].includes(e.key);
                        
                        // 1. Bloquear caracteres especiales
                        if (prohibidas.includes(e.key)) {
                            e.preventDefault();
                        }
                        
                        // 2. Bloquear si supera 4 caracteres (y no es tecla de borrar/mover)
                        if (input.value.length >= 4 && !esControl) {
                            e.preventDefault();
                        }
                    });
                    // Bloqueo por pegado o arrastre (Input event)
                    input.addEventListener('input', (e) => {
                        if (input.value.length > 4) {
                            input.value = input.value.slice(0, 4);
                        }
                    });
                    input.dataset.listenerActive = "true";
                }
            });
        };
        setupLogic();
        setInterval(setupLogic, 700);
        </script>
        """, height=0)

    with st.form(key='formulario_verificacion'):
        st.markdown("""
            <style>
            /* Ocultar los botones de + y - de todos los st.number_input */
            button[data-testid="stNumberInputStepDown"], 
            button[data-testid="stNumberInputStepUp"] {
                display: none !important;
            }
            iframe {
                display: none !important;
                height: 0 !important;
                margin: 0 !important;
            }
            }
            </style>
                """, unsafe_allow_html=True)
        nombre_usuario = st.text_input("Nombre de Usuario", max_chars=16, icon=":material/person_check:", placeholder="Ejemplo: Juan33", help="Tiene que ser un usuario registrado en el sistema.")
        ci = st.number_input("Últimos 4 dígitos de la cédula",
                                    value=None, step=1,
                                    max_value=9999, min_value=1,
                                    placeholder="Ejemplo: 1234", 
                                    key="ci", icon=":material/contact_mail:", format= "%d",
                                    help="Tiene que ser de la cédula asociada al usuario.")
        col_verificar, col_volver = st.columns(2)
        with col_verificar:    
            verificar = st.form_submit_button("Verificar", type="primary", width="stretch", icon=":material/lock:")
        with col_volver:    
            volver = st.form_submit_button("Volver al inicio de sesión", type="secondary", width="stretch", icon=":material/arrow_back:")

    if verificar:
        if not nombre_usuario or not ci:
            st.warning("Por favor, completa todos los campos.", icon=":material/warning:")
            return
        elif not validar_nombre_usuario(nombre_usuario):
            return
        try:
            if verificar_usuario_cedula(nombre_usuario, ci, DB_PATH):
                preguntas = obtener_preguntas_usuario(nombre_usuario, DB_PATH)
                if not preguntas:
                    st.error("Este usuario no tiene preguntas de seguridad registradas.", icon=":material/error:")
                    #if st.button("Volver", key="volver_sin_preg"):
                    #    st.session_state["pagina_actual"] = "verificacion"
                    #    st.session_state["olvido_usuario_id"] = None
                    #    st.rerun()
                    return
                st.session_state["olvido_usuario_id"] = nombre_usuario
                st.session_state["olvido_preguntas"] = preguntas
                st.session_state["pagina_actual"] = "seguridad"
                st.rerun()
        except Exception as e:
            st.error(f"Error al verificar: {str(e)}. Contacta al admin.", icon=":material/error:")

    if volver:
        st.session_state["olvido_usuario_id"] = None
        st.session_state["pagina_actual"] = "verificacion"
        st.switch_page("pages/inicio_sesion.py")

# ------------------- Control principal -------------------
def mostrar_olvido():
    logo_bandera = ASSETS_DIR / "imagebanderanueva2.png"
    logo_base64 = img_a_base64(logo_bandera)
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__)
    logo(tamano="70%")
    
    colfoto, _, coltext = st.columns([3, 0.1, 3])
    with colfoto:
        if st.session_state["pagina_actual"] == "verificacion":
            formulario_verificacion()
        elif st.session_state["pagina_actual"] == "seguridad":
            P_Seguridad()
        elif st.session_state["pagina_actual"] == "nueva_contra":
            nueva_contra()

    with coltext:
        informacion()
    copyright_footer_dos("Equipo Investigador", margin_right="0px")

# ------------------- Ejecución -------------------
mostrar_olvido()