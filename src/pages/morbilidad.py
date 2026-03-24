import streamlit as st
import os
import time
from utils.sql_control import operaciones_sql_morb_extenso, eliminar_registros_morb_extenso
from pathlib import Path
import pandas as pd 
from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez, copyright_footer_dos
from utils.verificaciones import obtener_info_usuario
from pages.menu import menu
from dateutil.relativedelta import relativedelta
from utils.filtro import filtrar_por_fechas, descargar_pdf, descargar_registros_seleccionados, ver_pdf
from utils.base_64 import img_a_base64
from utils.limpieza import limpiar_campos_morb_extenso
from utils.validaciones import val_diagnostico, validar_texto, val_texynum, val_notas, val_num_espacios, val_solo_numeros, validar_cinco_espacios, validar_pais
from utils.botones import confirmar_eliminar, guadar_btn, ver_btn
from utils.guardar_cambios import procesar_guardado_morb_extenso
from reportes.morbilidad_gen import formulario_reporte_general_morbilidad
from utils.recargar_retroceso import reload_on_back
configurar_pagina_espanol()
if "previous_page" not in st.session_state:
    st.session_state["previous_page"] = "pages/inicio.py"
st.session_state["previous_page"] = "pages/morbilidad.py"

DB_PATH = os.getenv("hospital.db", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'

import sys
from utils.validaciones import bloquear_caracteres

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

menu()

def data_editor_morb_extenso(df):

    # Columna de selección
    if " " not in df.columns:
        df.insert(0, " ", False)

    # Mostrar TODO excepto ids internos, pero dejar id AL FINAL
    columns_to_display = [
        col for col in df.columns
        if col not in [" ", "id_paciente", "id_direccion_hogar"]
    ]

    # Asegurar id al final
    if "id" in columns_to_display:
        columns_to_display.remove("id")
        columns_to_display.append("id")

    columns_to_show = [" "] + columns_to_display
    df = df[columns_to_show]

    # Configuración de columnas
    column_config = {
        " ": st.column_config.CheckboxColumn(" ", default=False),
        "nombres_apellidos": st.column_config.TextColumn("Nombres y Apellidos"),
        "edad": st.column_config.NumberColumn("Edad", min_value=0, step=1),
        "diagnostico": st.column_config.TextColumn("Diagnóstico"),
        "fecha_registro_formulario": st.column_config.DateColumn(
            "Fecha registro", format="DD/MM/YYYY", disabled=True
        ),
        "direccion_hogar": st.column_config.TextColumn(
            "Dirección del hogar", disabled=True), #
        "id": st.column_config.NumberColumn("ID", disabled=True),
    }

    # El resto solo lectura
    for col in columns_to_show:
        if col not in column_config and col != " ":
            column_config[col] = st.column_config.TextColumn(col, disabled=True)

    edited_df = st.data_editor(
        df,
        hide_index=True,
        column_config=column_config,
        key="editor_morb_extenso"
    )

    return edited_df


@st.fragment
def formulario_morb_extenso(db=DB_PATH):

    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a esta area.", icon=":material/error:")
        return

    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)

    if not info_usuario:
        st.error("Usuario no encontrado. Por favor, inicia sesión nuevamente.", icon=":material/error:")
        return

    rol_usuario = info_usuario["rol"]
    id_doctor = info_usuario["id_doctor"]
    id_secretaria = info_usuario["id_secretaria"]
    id_administrador = info_usuario["id_administrador"]

    st.subheader(":material/table: Datos de Morbilidad", anchor=False)

    df = operaciones_sql_morb_extenso("cargar")
    if df is None:
        return

    if df.empty:
        st.info("No hay datos para mostrar.", icon=":material/info:")
    else:
        mostrar_editor = st.toggle(
            "Mostrar datos de registros", 
            value=st.session_state.get("toggle_editor_morbilidadex", False),
            key="toggle_editor_morbilidadex"
        )
        if mostrar_editor:
            df = filtrar_por_fechas(df, 'fecha_registro_formulario')
            edited_df = data_editor_morb_extenso(df)

            col_ver, col_guardar, col_descargar, col_eliminar = st.columns(4)
            has_selection = edited_df[' '].any()
            df_sel = edited_df[edited_df[' '] == True] if has_selection else None
            df_to_use = df_sel if has_selection else edited_df

            with col_ver:
                ver_pdf(df_to_use, "morbilidad_extensa", key_btn="ver_btn_morbilidad")

            with col_guardar:
                guardar = st.button("Guardar cambios", icon=":material/save:", width="stretch", 
                                    type="primary")   

            with col_descargar:
                label_descarga = "Descargar Selección" if has_selection else "Descargar PDF"
                descargar_pdf(df_to_use, "morbilidad_extensa", label=label_descarga)

            with col_eliminar:
                btn_eliminar = st.button(
                    "Eliminar",
                    icon=":material/delete:",
                    key="delete_morbilidad_extensa",
                    disabled=not has_selection,
                    width="stretch",
                    help="Eliminar registros seleccionados."
                )
                if btn_eliminar:
                    confirmar_eliminar(eliminar_registros_morb_extenso, edited_df)
            if guardar:
                procesar_guardado_morb_extenso(edited_df)
                time.sleep(1)
                st.rerun()

    st.subheader(":material/new_label: Registrar Morbilidad", anchor=False)
    st.components.v1.html("""
                <script>
                const setupLogic = () => {
                    const doc = window.parent.document;
                    // Buscamos todos los contenedores de number_input
                    const widgets = doc.querySelectorAll('[data-testid="stNumberInput"]');
                    
                    widgets.forEach(widget => {
                        const labelText = widget.querySelector('label')?.innerText;
                        const input = widget.querySelector('input');
                        const buttons = widget.querySelectorAll('button');
                        
                        // CONFIGURACIÓN PARA EL INPUT RESTRINGIDO (DNI / ID / etc)
                        // si queremps varios input asi: if (labelText === "ID" || labelText === "Teléfono" || labelText === "Código") { ... }
                        // Aquí pones el nombre exacto de la etiqueta que quieres restringir
                        if (labelText === "Historia clínica" || labelText === "Edad") {
                            
                            // 1. Ocultar botones solo para este input
                            buttons.forEach(btn => btn.style.display = 'none');
                            
                            if (!input.dataset.listenerActive) {
                                input.addEventListener('keydown', (e) => {
                                    const prohibidas = ['e', 'E', '+', '-', '.', ','];
                                    const esControl = ['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab', "Enter"].includes(e.key);
                                    
                                    if (prohibidas.includes(e.key)) e.preventDefault();
                                    if (input.value.length >= 8 && !esControl) e.preventDefault();
                                });

                                input.addEventListener('input', (e) => {
                                    if (input.value.length > 8) input.value = input.value.slice(0, 8);
                                });
                                input.dataset.listenerActive = "true";
                            }
                        }
                        
                        // CONFIGURACIÓN PARA INPUT FLOAT (Precio / Peso / etc)
                        // --- CASO 2: FLOAT LIMPIO (Sin e, sin signos) ---
                                    if (labelText === "Peso (kg)" || labelText === "Talla (cm)" || labelText === "Semanas de gestación" || labelText === "Edad") {
                                        // AQUÍ NO OCULTAMOS LOS BOTONES (se quedan los + y - de Streamlit)
                                        
                                        if (!input.dataset.listenerActive) {
                                            input.addEventListener('keydown', (e) => {
                                                // Bloqueamos e, E y los signos, pero PERMITIMOS el punto y la coma
                                                const prohibidas = ['e', 'E', '+', '-'];
                                                if (prohibidas.includes(e.key)) e.preventDefault();
                                            });
                                            input.dataset.listenerActive = "true";
                                        }
                                    }
                                });
                            };

                            setupLogic();
                            setInterval(setupLogic, 500);
                            </script>
                            """, height=0)
    with st.form("form_morb_extenso"):
        st.markdown("""
            <style>
            /* Quitar flechas por defecto del navegador (spinners) */
            input::-webkit-outer-spin-button,
            input::-webkit-inner-spin-button {
            -webkit-appearance: none;
            margin: 0;
            }
            input[type=number] {
            -moz-appearance: textfield;
            }
            iframe {
                display: none !important;
                height: 0 !important;
                margin: 0 !important;
            
            /* Ocultamos el contenedor del script para que no deje hueco */
            [data-testid="stHtml"] {
                display: none !important;
            }
            </style>
            """, unsafe_allow_html=True)
        # Primeras filas del formulario
        col_nombre, col_edad = st.columns(2)
        with col_nombre:
            nombres_apellidos = st.text_input(
                "Nombres y apellidos", max_chars=40,
                key="nombres_apellidos_morb_extenso",
                placeholder="Ej. Juan Pérez"
            )
            bloquear_caracteres(
                caracteres=list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"),
                tipo_de_input="text",
                max_chars=40,
                label="Nombres y apellidos"
            )
        with col_edad:
            edad = st.text_input("Edad (años)", key="edad_morb_extenso",
                placeholder="Ej. 25", max_chars=3)
            bloquear_caracteres(
                caracteres=list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZáéíóúÁÉÍÓÚñÑüÜ!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-— "),
                tipo_de_input="text",
                max_chars=3,
                label="Edad (años)"
            )
        diagnostico = st.text_area(
            "Diagnóstico", max_chars=150,
            key="diagnostico_morb_extenso",
            placeholder="Descripción del diagnóstico"
        )
        bloquear_caracteres(
            caracteres=list("!@#$%¨&*_=+[]{}:;\"\\|<>?`~^°¡¿§±←→•#"),
            tipo_de_input="textarea",
            max_chars=150,
            label="Diagnóstico"
        )

        st.markdown("**Dirección de Hogar**")
        col_pais, col_estado, col_muni = st.columns(3)
        with col_pais:
            pais_hogar = st.text_input("País (Opcional)", max_chars=56, key="pais_hogar_morb_extenso", placeholder="Venezuela")
            bloquear_caracteres(
                caracteres=list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"),
                tipo_de_input="text",
                max_chars=40,
                label="País"
            )
        with col_estado:
            estado_hogar = st.text_input("Estado (Opcional)", max_chars=56, key="estado_hogar_morb_extenso", placeholder="Anzoátegui")
            bloquear_caracteres(
                caracteres=list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"),
                tipo_de_input="text",
                max_chars=40,
                label="Estado (Opcional)"
            )    
        with col_muni:
            municipio_hogar = st.text_input("Municipio (Opcional)", max_chars=56, key="municipio_hogar_morb_extenso", placeholder="Simón Rodríguez")
            bloquear_caracteres(
                caracteres=list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"),
                tipo_de_input="text",
                max_chars=40,
                label="Municipio (Opcional)"
            )
        col_parroquia, col_ciudad = st.columns(2)
        with col_parroquia:
            parroquia_hogar = st.text_input("Parroquia (Opcional)", max_chars=56, key="parroquia_hogar_morb_extenso", placeholder="Edmundo Barrios (zona norte)")
            bloquear_caracteres(
                caracteres=list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"),
                tipo_de_input="text",
                max_chars=40,
                label="Parroquia (Opcional)"
            )
        with col_ciudad:
            ciudad_hogar = st.text_input("Ciudad (Opcional)", max_chars=56, key="cuidad_hogar_morb_extenso", placeholder="El Tigre")
            bloquear_caracteres(
                caracteres=list("0123456789!@#$%¨&*()_+=[]{};:'\"\\|<>,.?/`~-—^"),
                tipo_de_input="text",
                max_chars=40,
                label="Ciudad (Opcional)"
            )
        direccion_exacta_hogar = st.text_area("Dirección", max_chars=150, key="direccion_exacta_hogar_morb_extenso", placeholder="Pueblo Nuevo Norte, 3ra Carrera Norte, Número 26")
        bloquear_caracteres(
            caracteres=list("!@%¨&*()_+=[]{}:;\"\\|<>?`~^°¡¿§±←→•^"),  # caracteres prohibidos (excluye ' / - . , #)
            tipo_de_input="textarea",
            max_chars=150,
            label="Dirección"
        )
        col_reg, col_limp = st.columns([30, 1])
        with col_reg:
            registrar = st.form_submit_button("Registrar", icon=":material/save:", type="primary")
        with col_limp:
            limpiar = st.form_submit_button("", icon=":material/cleaning_services:", on_click=limpiar_campos_morb_extenso, type="tertiary", help="Limpia todos los campos del formulario.")

        if registrar:
            # Validaciones básicas
            if not all([nombres_apellidos, diagnostico, direccion_exacta_hogar]):
                st.error("Por favor completa todos los campos obligatorios", icon=":material/error:")
                return
            if not validar_texto(nombres_apellidos, "Los", "nombres y apellidos"): 
                return
            if not validar_cinco_espacios(nombres_apellidos, "Los", "nombres y apellidos"): 
                return
            if edad > 120:
                st.error("La edad no puede ser mayor a 120 años", icon=":material/error:")
                return
            if not val_diagnostico(diagnostico, "El", "diagnóstico"): 
                return

            datos_registro = {
                "rol_usuario": rol_usuario,
                "nombres_apellidos": nombres_apellidos,
                "edad": edad,
                "diagnostico": diagnostico,
                "direccion": {
                    "pais": pais_hogar,
                    "estado": estado_hogar,
                    "municipio": municipio_hogar,
                    "parroquia": parroquia_hogar,
                    "ciudad": ciudad_hogar,
                    "direccion_exacta": direccion_exacta_hogar
                },
                "id_doctor": id_doctor,
                "id_secretaria": id_secretaria,
                "id_administrador": id_administrador
            }

            if operaciones_sql_morb_extenso("registrar", datos_registro=datos_registro):
                st.success("Registro guardado.", icon=":material/check_circle:")
                st.rerun()


def mostrar_morb():
    logo_bandera = ASSETS_DIR / "imagebanderanueva2.png"
    
    logo_base64 = img_a_base64(logo_bandera)
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) 
    logo(tamano="100%")
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a esta area.", icon=":material/error:")
        return

    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)

    if not info_usuario:
        st.error("Usuario no encontrado. Por favor, inicia sesión nuevamente.", icon=":material/error:")
        return
    tab1, tab2 = st.tabs(["| :material/personal_injury: Morbilidad |", 
                                "| :material/article_shortcut: Reporte General |"])
    with tab1:
        formulario_morb_extenso()
    with tab2:
        st.subheader(":material/arrow_circle_down: Descargas de reportes", anchor=False, divider="gray")
        col_izq, col_centro, col_der = st.columns([3.35, 4, 2.65])

        with col_centro:
            formulario_reporte_general_morbilidad()

        st.markdown("")
    copyright_footer_dos("Equipo Investigador")

mostrar_morb()
reload_on_back()