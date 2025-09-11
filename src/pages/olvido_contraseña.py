import streamlit as st
from pathlib import Path
from utils.verificaciones import verificar_usuario_cedula
from utils.base_64 import img_a_base64
from utils.validaciones import val_solo_numeros, validar_contraseña, validar_texto, validar_nombre_usuario, val_mail
from utils.visuales import cargando, configurar_pagina_espanol, logo, recargar_una_vez
from utils.verificaciones import obtener_contrasena_actual, cambiar_contrasena, verificar_preg_res_seg, verificar_correo_cedula, obtener_nombre_usuario
from utils.contra import borro_cassette, verifi_contra_hasheada
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
configurar_pagina_espanol()

@st.fragment
def nueva_contra():
    #logo(tamano="100%")
    st.markdown("")
    #fotodos(tamano="100%")
    st.header(":material/lock_reset: Actualiza tu contraseña", anchor=False)
    with st.form(key="form_nueva_contra"):
        nueva_contra = st.text_input("Ingresa tu nueva contraseña", key="nueva_contra", 
                                     type="password", max_chars=16, icon=":material/visibility_lock:")
        confirmar_contra = st.text_input("Confirma tu nueva contraseña", key="confirmar_contra", 
                                         type="password", max_chars=16, icon=":material/preview_off:")
        st.info('La contraseña debe tener entre 8 y 16 caracteres, una letra minúscula, una mayúscula y al menos un número.', icon=":material/info:")
        col_verificar, col_cancelar = st.columns(2)
        with col_verificar:
            btn_verificar = st.form_submit_button("Cambiar contraseña", type="primary", width="stretch", icon=":material/verified_user:")
        with col_cancelar:
            btn_cancelar = st.form_submit_button("Cancelar", type="secondary", width="stretch", icon=":material/cancel:",
                                                 help="Vuelves a la Verificación de Usuario y Cédula.")
    if btn_verificar:
            if not nueva_contra or not confirmar_contra:
                st.error("Ambos campos son obligatorios.", icon=":material/error:")
            elif nueva_contra != confirmar_contra:
                st.error("Las contraseñas no coinciden.", icon=":material/error:")
            elif not validar_contraseña(nueva_contra):
                return 
            else:
                usuario = st.session_state.get("usuario")

                # aqui fallas
            # Obtener la contraseña actual del usuario (hash)
                contrasena_actual = obtener_contrasena_actual(usuario)
                #if contrasena_actual is None:
                #    st.error("No se pudo obtener la contraseña actual del usuario. Verifica que el usuario esté correctamente seleccionado.", icon=":material/error:")
                #    return

            # Verificar si la nueva contraseña es igual a la actual usando la función específica
            # verifi_contra_hasheada compara una contraseña en texto plano con un hash
                if verifi_contra_hasheada(nueva_contra, contrasena_actual):
                    st.error("La contraseña es igual a la actual.", icon=":material/error:")
                    return
            
            # Si llegamos aquí, es porque las contraseñas son diferentes
            # Hashear la nueva contraseña para guardarla
                nueva_contra_hash = borro_cassette(nueva_contra)
                exito = cambiar_contrasena(nueva_contra_hash, usuario)
            # Se procede a cambiar la contraseña, pasando la pregunta seleccionada y la cédula

                if exito:
                    cargando("Contraseña actualizada correctamente.", icono=":material/cloud_upload:")
                # cambiar la pagina a inicio
                    st.session_state["pagina_actual"] = "verificacion"
                    st.rerun()

    if btn_cancelar:
        st.session_state["pagina_actual"] = "verificacion"
        st.rerun()

@st.fragment
def P_Seguridad():
    #logo(tamano="100%")
    st.markdown("")
    #fotodos(tamano="100%")
    st.header(":material/question_exchange: Verificación de Preguntas", anchor=False)
    with st.form(key="form_P_Seguridad"):
        
        col_preguntas, col_respuestas = st.columns(2)
        with col_preguntas:
            pregunta_uno =  st.selectbox(":material/looks_one: Selecciona tu pregunta de seguridad", 
                                        ["¿Cuál es el segundo nombre de tu madre?", 
                                        "¿Cuál es tu pelicula favorita?",
                                        "¿Cuál es el nombre de tu primer mejor amigo/a?",
                                        "¿Cuál es tu comida favorita?",
                                        "¿Cuál era el nombre de tu primera mascota?",
                                        "¿Cuál es el segundo nombre de tu abuelo paterno?",
                                        "¿En qué calle vivías cuando tenías 10 años?"], 
                                        key="pregunta_uno_contra")
            pregunta_dos =  st.selectbox(":material/looks_two: Selecciona tu pregunta de seguridad", 
                                        ["¿Cuál es el segundo nombre de tu madre?", 
                                        "¿Cuál es tu pelicula favorita?",
                                        "¿Cuál es el nombre de tu primer mejor amigo/a?",
                                        "¿Cuál es tu comida favorita?",
                                        "¿Cuál era el nombre de tu primera mascota?",
                                        "¿Cuál es el segundo nombre de tu abuelo paterno?",
                                        "¿En qué calle vivías cuando tenías 10 años?"], 
                                        key="pregunta_dos_contra")
            pregunta_tres =  st.selectbox(":material/looks_3: Selecciona tu pregunta de seguridad", 
                                        ["¿Cuál es el segundo nombre de tu madre?", 
                                        "¿Cuál es tu pelicula favorita?",
                                        "¿Cuál es el nombre de tu primer mejor amigo/a?",
                                        "¿Cuál es tu comida favorita?",
                                        "¿Cuál era el nombre de tu primera mascota?",
                                        "¿Cuál es el segundo nombre de tu abuelo paterno?",
                                        "¿En qué calle vivías cuando tenías 10 años?"], 
                                        key="pregunta_tres_contra")
        with col_respuestas:
            respuesta_uno = st.text_input("Indica la respuesta:", type='password', 
                                icon=":material/health_and_safety:", max_chars=18, key="respuesta_uno")
            respuesta_dos = st.text_input("Indica la respuesta:", type='password', 
                                icon=":material/health_and_safety:", max_chars=18, key="respuesta_dos")
            respuesta_tres = st.text_input("Indica la respuesta:", type='password', 
                                icon=":material/health_and_safety:", max_chars=18, key="respuesta_tres")
        col_verificar, col_cancelar = st.columns(2)
        with col_verificar:
            btn_verificar = st.form_submit_button("Verificar", type="primary", width="stretch", icon=":material/verified_user:")
        with col_cancelar:
            btn_cancelar = st.form_submit_button("Cancelar", type="secondary", width="stretch", icon=":material/cancel:",
                                                 help="Vuelves a la Verificación de Usuario y Cédula.")
    if btn_verificar:
        if not all([respuesta_uno, respuesta_dos, respuesta_tres]):
            st.error("Todos los campos son obligatorios.", icon=":material/error:")
        elif pregunta_uno == pregunta_dos or pregunta_uno == pregunta_tres or pregunta_dos == pregunta_tres:
            st.error("Las preguntas de seguridad no pueden ser iguales.", icon=":material/error:")  
        elif not validar_texto(respuesta_uno, "La", "primera respuesta de seguridad"):
            return
        elif not validar_texto(respuesta_dos, "La", "segunda respuesta de seguridad"):
            return
        elif not validar_texto(respuesta_tres, "La", "tercera respuesta de seguridad"):
            return
        else:
            usuario = st.session_state.get("usuario")
            # Verifica las tres preguntas y respuestas en un solo llamado
            ok, _ = verificar_preg_res_seg(
                respuesta_uno, pregunta_uno,
                respuesta_dos, pregunta_dos,
                respuesta_tres, pregunta_tres,
                usuario
            )
            if ok:
                st.session_state["pagina_actual"] = "nueva_contra"
                st.rerun()

    if btn_cancelar:
        st.session_state["pagina_actual"] = "verificacion"
        st.rerun()

def fotodos(tamano):
    ruta_imagen = ASSETS_DIR / "child.webp"
    img_b64 = img_a_base64(ruta_imagen)
    html_code = f'''
    <div class="logo-centro">
        <img src="data:image/png;base64,{img_b64}" width={tamano}/> <!-- 30% para paginas, 55 para el inicio sesion -->
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


def informacion():
    st.write("") # lo use para bajar un pixel el contenido
    _, col_centro = st.columns([0.2, 2.8]) # centrado
    with col_centro:
        st.subheader(":material/sentiment_dissatisfied: ¿Has olvidado tu contraseña?", anchor=False)

    st.markdown("¡No te preocupes! **Sigue** estos sencillos pasos para recuperar el acceso a tu cuenta.")
    
    col_paso1, col_paso2 = st.columns([1.5, 2])
    with col_paso1:
        st.subheader(":material/looks_one: Identificación", anchor=False)
        st.markdown("""
        Indica tu **nombre de usuario** y los **últimos 4 dígitos de tu cédula**.
        """)
    with col_paso2:
        st.subheader(":material/looks_two: Preguntas de seguridad", anchor=False)
        st.markdown("""
        Selecciona tus **3 preguntas de seguridad** registradas y escribe sus respuestas.
        """)

    st.subheader(":material/looks_3: ¡Listo! Cambia tu contraseña", anchor=False)
    st.markdown("""
    Establece una nueva contraseña. Recuerda **cumplir** con los siguientes parámetros:
    """)
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
    #logo(tamano="100%")
    st.markdown("")
    #fotodos(tamano="30%")
    st.header(":material/passkey: Verificación de Usuario y Cédula", anchor=False)# :material/lock_person:

    # Se crea el formulario para la entrada de datos
    with st.form(key='formulario_verificacion'):
        nombre_usuario = st.text_input("Nombre de Usuario", max_chars=16, icon=":material/person_check:",
                                       placeholder="Ejemplo: Juan33", help="Tiene que ser un usuario registrado en el sistema.")
        ci = st.text_input("Últimos 4 dígitos de la cédula", max_chars=4, type="password", icon=":material/contact_mail:",
                           placeholder="Ejemplo: 1234", help="Tiene que ser de la cédula asociada al usuario.")
        col_verificar, col_volver = st.columns(2)
        with col_verificar:    
            verificar = st.form_submit_button("Verificar", type="primary", width="stretch", icon=":material/lock:")
        with col_volver:    
            volver = st.form_submit_button("Volver al inicio de sesión", type="secondary", width="stretch", icon=":material/arrow_back:")

    if verificar:
        # Validación básica de los campos
        if not nombre_usuario or not ci:
            st.warning("Por favor, completa todos los campos.", icon=":material/warning:")
            return
        elif not validar_nombre_usuario(nombre_usuario):
            return
        elif not val_solo_numeros(ci, "Los", "digitos de la cédula de identidad"):
            return
        # Llama a la función de verificación
        if verificar_usuario_cedula(nombre_usuario, ci):
            #st.success("✅ ¡Verificación exitosa! El usuario y la cédula coinciden.")
            st.session_state["usuario"] = nombre_usuario
            #cargando("Usuario verificado correctamente.", icono=":material/cloud_upload:")
            st.session_state["pagina_actual"] = "seguridad"
            st.rerun()
        #else:
        #    st.error("Error de verificación. El nombre de usuario o los últimos 4 dígitos de la cédula son incorrectos.", icon=":material/error:")
    if volver:
        st.switch_page("pages/inicio_sesion.py")
        st.rerun()

def mostrar_olvido():
    logo_bandera  = ASSETS_DIR / "imagebanderanueva2.png"
    logo_base64 = img_a_base64(logo_bandera)
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) # Llama a la función para recargar la página una vez.
    logo(tamano="70%")
    colfoto, _, coltext = st.columns([3, 0.1, 3])    
    with colfoto:
        with st.container():
                # Inicializa la clave si no existe
            if "pagina_actual" not in st.session_state:
                st.session_state["pagina_actual"] = "verificacion"
            # Este es el controlador principal que decide qué fragmento mostrar
            if st.session_state["pagina_actual"] == "verificacion":
                formulario_verificacion()
            elif st.session_state["pagina_actual"] == "seguridad":
                P_Seguridad()
            elif st.session_state["pagina_actual"] == "nueva_contra":
                nueva_contra()
            #formulario_verificacion()
    with coltext:
        with st.container():
            informacion()

mostrar_olvido()