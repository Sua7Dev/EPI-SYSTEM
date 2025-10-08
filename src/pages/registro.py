import streamlit as st
import datetime
import time
import os
import sys
from pathlib import Path

from utils.contra import borro_cassette
from utils.verificaciones import guardar_usuario
from utils.validaciones import validar_texto, validar_nombre_usuario, val_mail, val_solo_numeros, validar_contraseña, mayor_de_edad, validar_cinco_espacios
from utils.base_64 import img_a_base64
from utils.limpieza import limpiar_campos_registro_usuario
from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez, copyright_al_final

import sqlite3

# ------------------- Configuración -------------------
configurar_pagina_espanol()

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
DB_PATH = os.getenv("hospital.db", "hospital.db")

# ------------------- Formulario de registro -------------------
def registro_formulario():
    try:
        st.header(':material/group_add: Registro De Usuarios', divider='gray', anchor=False)
        with st.form(key='registro_form'):
            # Primera fila
            col_nombre, col_sexo = st.columns(2)
            with col_nombre:
                nombre = st.text_input('Nombres y Apellidos:', 
                                       max_chars=40, 
                                       placeholder='Ejemplo: Juan Pérez', 
                                       key="nombre", icon=":material/person:")
            with col_sexo:
                sexo = st.selectbox("⚥ Sexo", ["Masculino", "Femenino"], key="sexo")
            
            # Segunda fila
            col_nacimiento1, col_rol = st.columns(2)
            with col_nacimiento1:
                nacimiento = st.date_input(
                    ':material/calendar_month: Fecha de nacimiento:', format='DD-MM-YYYY',
                    min_value=datetime.date(1960, 1, 1), 
                    max_value=datetime.datetime.now(),
                     key="nacimiento"
                )
            with col_rol:
                rol = st.selectbox(":material/assignment_ind: Rol", ["Doctor (a)", "Secretario (a)"], key="rol")            
            
            # Tercera fila
            col_correo, col_usuario = st.columns(2)
            with col_correo:
                correo = st.text_input('Correo electrónico:', max_chars=35, 
                                       placeholder='Ejemplo: Juan@gmail.com', 
                                       key="correo", icon=":material/mail:")            
            with col_usuario:
                nombre_usuario = st.text_input('Nombre de usuario:', max_chars=16, 
                                               placeholder='Ejemplo: Juan33', 
                                               key="nombre_usuario", icon=":material/person_check:")
            
            # Cuarta fila
            col_ci, col_nacional = st.columns(2)
            with col_ci:
                ci = st.text_input("Cédula de identidad", max_chars=8, 
                                   placeholder="Ejemplo: 12345678", 
                                   key="ci", icon=":material/contact_mail:")
            with col_nacional:
                nacionalidad = st.selectbox(":material/south_america: Nacionalidad", ["Venezolano (a)", "Extranjero (a)"], key="nacionalidad")
            
            # Quinta fila
            col_contra, col_confirmar = st.columns(2)
            with col_contra:
                contrasena = st.text_input('Contraseña:', max_chars=16, 
                                           type='password', 
                                           key="contra_usuario", icon=":material/visibility_lock:")
            with col_confirmar:
                confirmar_contra = st.text_input('Confirmar Contraseña:', max_chars=16, 
                                                 type='password', 
                                                 key="confirmar_contra", icon=":material/preview_off:")
            st.info('La contraseña debe tener entre 8 y 16 caracteres, una letra minúscula, una mayúscula y al menos un número.', icon=":material/info:")    
            
            # Botones
            col_registro, col_volver, col_nuevo = st.columns(3)
            with col_registro:
                registrar_btn = st.form_submit_button(label="Registrar", type="primary", width="stretch", icon=":material/person_add:")
            with col_volver:
                volver_btn = st.form_submit_button(label="Volver atrás", type="secondary", width="stretch", icon=":material/arrow_back:",
                                                   help="Vuelve a la página de configuración")
            with col_nuevo:
                nuesvo_registro_btn = st.form_submit_button(label="Nuevo registro", type="secondary", width="stretch", icon=":material/new_label:", 
                                                            on_click=limpiar_campos_registro_usuario,
                                                            help="Limpia todos los campos del formulario.")

            # ------------------- Lógica de validaciones y guardado -------------------
            if registrar_btn:
                if not all([nombre, sexo, nacimiento, nombre_usuario, correo, ci, nacionalidad, contrasena, confirmar_contra, rol]):
                    st.error("Todos los campos son obligatorios. Por favor, completa todos los campos.", icon=":material/error:")
                elif not validar_texto(nombre, "El", "nombre"):
                    return
                elif not validar_cinco_espacios(nombre, "El", "nombre"):
                    return
                elif not mayor_de_edad(nacimiento):
                    return
                elif not validar_nombre_usuario(nombre_usuario):
                    return
                elif not val_mail(correo):
                    return
                elif not val_solo_numeros(ci, "La", "cédula de identidad"):
                    return
                elif contrasena != confirmar_contra:
                    st.error("Las contraseñas no coinciden.", icon=":material/error:")
                elif not validar_contraseña(contrasena):
                    return
                else:
                    contrasena_hasheada = borro_cassette(contrasena) # hasheamos antes de guardar
                    exito = guardar_usuario(
                        nombre=nombre,
                        sexo=sexo,
                        nacimiento=nacimiento,
                        nombre_usuario=nombre_usuario,
                        correo=correo,
                        ci=ci,
                        nacionalidad=nacionalidad,
                        contrasena_hasheada=contrasena_hasheada,
                        rol=rol,
                        DB_PATH=DB_PATH
                    )
                    if exito:
                        st.success("Usuario registrado exitosamente.", icon=":material/check_circle:")
                        time.sleep(1)
                        st.rerun()

            if volver_btn:
                st.switch_page("pages/configuracion.py")
                st.rerun()

    except sqlite3.IntegrityError as e:
        error_message = str(e).lower()
        if 'usuarios.nombre_usuario' in error_message:
            st.error("El nombre de usuario ya está registrado. Por favor, elige otro.", icon=":material/error:")
        elif 'usuarios.correo' in error_message:
            st.error("El correo electrónico ya está registrado. Por favor, utiliza otro.", icon=":material/error:")
        elif 'usuarios.ci' in error_message:
            st.error("La cédula de identidad ya está registrada con otro usuario.", icon=":material/error:")
        else:
            st.error(f"Error de integridad de datos: {e}", icon=":material/error:")
        return

# ------------------- Ejecución principal -------------------
def registro():
    logo_bandera  = ASSETS_DIR / "imagebanderanueva2.png"
    logo_base64 = img_a_base64(logo_bandera)
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__)
    logo(tamano="70%")
    _, col_centro, _ = st.columns([3, 6, 3])
    with col_centro:    
        registro_formulario()
    copyright_al_final("SAMUEL URBANO & GUSTAVO HEREDIA")

registro()
