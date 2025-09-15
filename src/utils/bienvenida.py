import streamlit as st
import time
from utils.validaciones import val_solo_numeros, validar_contraseña, validar_texto
from utils.contra import borro_cassette
from utils.verificaciones import verificar_usuario, guardar_preguntas_seguridad, verificar_preg_res_seg

@st.dialog(f":material/waving_hand: !Bienvenido al sistema¡", width="large")
def bienvenida(nombre_usuario):
    st.header(f":material/encrypted_add: {nombre_usuario} Registra tus datos de seguridad.", anchor=False, divider="gray")
    with st.form(key="Bienvenida"):
        col_preguntas, col_respuestas = st.columns(2)
        with col_preguntas:
            pregunta_uno =  st.selectbox(":material/looks_one: Selecciona tu primera pregunta de seguridad", 
                                        ["¿Cuál es el segundo nombre de tu madre?", 
                                        "¿Cuál es tu pelicula favorita?",
                                        "¿Cuál es el nombre de tu primer mejor amigo/a?",
                                        "¿Cuál es tu comida favorita?",
                                        "¿Cuál era el nombre de tu primera mascota?",
                                        "¿Cuál es el segundo nombre de tu abuelo paterno?",
                                        "¿En qué calle vivías cuando tenías 10 años?"], 
                                        key="pregunta_uno")
            pregunta_dos =  st.selectbox(":material/looks_two: Selecciona tu segunda pregunta de seguridad", 
                                        ["¿Cuál es el segundo nombre de tu madre?", 
                                        "¿Cuál es tu pelicula favorita?",
                                        "¿Cuál es el nombre de tu primer mejor amigo/a?",
                                        "¿Cuál es tu comida favorita?",
                                        "¿Cuál era el nombre de tu primera mascota?",
                                        "¿Cuál es el segundo nombre de tu abuelo paterno?",
                                        "¿En qué calle vivías cuando tenías 10 años?"], 
                                        key="pregunta_dos")
            pregunta_tres =  st.selectbox(":material/looks_3: Selecciona tu tercera pregunta de seguridad", 
                                        ["¿Cuál es el segundo nombre de tu madre?", 
                                        "¿Cuál es tu pelicula favorita?",
                                        "¿Cuál es el nombre de tu primer mejor amigo/a?",
                                        "¿Cuál es tu comida favorita?",
                                        "¿Cuál era el nombre de tu primera mascota?",
                                        "¿Cuál es el segundo nombre de tu abuelo paterno?",
                                        "¿En qué calle vivías cuando tenías 10 años?"], 
                                        key="pregunta_tres")
        with col_respuestas:
            respuesta_uno = st.text_input("Indica la respuesta a la pregunta de seguridad:", type='password', 
                                icon=":material/security:", max_chars=18, key="respuesta_uno")
            respuesta_dos = st.text_input("Indica la respuesta a la pregunta de seguridad:", type='password', 
                                icon=":material/security:", max_chars=18, key="respuesta_dos")
            respuesta_tres = st.text_input("Indica la respuesta a la pregunta de seguridad:", type='password', 
                                icon=":material/security:", max_chars=18, key="respuesta_tres")
        btn_Guardar = st.form_submit_button("Guardar los datos", type="primary", width="stretch", icon=":material/save:")
    if btn_Guardar:
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
            # hasheamos antes de guardar
            respuesta_hasheada = borro_cassette(respuesta_uno)
            respuesta_hasheada_dos = borro_cassette(respuesta_dos)
            respuesta_hasheada_tres = borro_cassette(respuesta_tres)
            if guardar_preguntas_seguridad(nombre_usuario, pregunta_uno, respuesta_hasheada, pregunta_dos, respuesta_hasheada_dos, pregunta_tres, respuesta_hasheada_tres):
                st.success("Preguntas de seguridad guardadas exitosamente.", icon=":material/check_circle:")
                st.session_state["primera_vez"] = False
                time.sleep(1)
                st.switch_page("pages/inicio.py")              
            else:
                st.error("Error al guardar las preguntas de seguridad. Inténtalo de nuevo.", icon=":material/error:")