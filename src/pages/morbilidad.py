import streamlit as st
import os
from utils.sql_control import operaciones_sql_morb_extenso, operaciones_sql_morb_simplifica, eliminar_registros_morb_extenso, eliminar_registros_morb_simplifica
from pathlib import Path
import pandas as pd 
from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez, copyright_footer_dos
from utils.verificaciones import obtener_info_usuario
from pages.menu import menu
from dateutil.relativedelta import relativedelta
from utils.filtro import filtrar_por_fechas, descargar_pdf, descargar_registros_seleccionados
from utils.base_64 import img_a_base64
from utils.limpieza import limpiar_campos_morb_extenso, limpiar_campos_morb_simplificado
from utils.validaciones import validar_texto, val_texynum, val_notas, val_num_espacios, val_solo_numeros, validar_cinco_espacios, validar_pais
from utils.botones import confirmar_eliminar, guadar_btn
from utils.guardar_cambios import procesar_guardado_morb_extenso, procesar_guardado_morb_simplificado
from reportes.morbilidad_gen import formulario_reporte_general_morbilidad
configurar_pagina_espanol()

DB_PATH = os.getenv("hospital.db", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'

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

menu()

def data_editor_morb_extenso(df):
    original_ids = df[['id', 'id_paciente', 'id_direccion_hogar']].reset_index(drop=True) if set(['id','id_paciente','id_direccion_hogar']).issubset(df.columns) else None
    df_display = df.reset_index(drop=True).copy()
    for c in ['id', 'id_paciente', 'id_direccion_hogar']:
        if c in df_display.columns:
            df_display.drop(columns=[c], inplace=True)
    if " " not in df_display.columns:
        df_display.insert(0, " ", False)
    ordered_cols = [" ", "nombres_apellidos", "edad", "diagnostico", "fecha_registro_formulario", "direccion_hogar"]
    rest = [c for c in df_display.columns if c not in ordered_cols]
    columns_to_show = [c for c in (ordered_cols + rest) if c in df_display.columns]
    df_display = df_display[columns_to_show]
    column_config = {
        " ": st.column_config.CheckboxColumn(" ", default=False, disabled=False),
        "nombres_apellidos": st.column_config.TextColumn("Nombres y Apellidos", disabled=False),
        "edad": st.column_config.NumberColumn("Edad", min_value=0, step=1, disabled=False),
        "diagnostico": st.column_config.TextColumn("Diagnóstico", disabled=False),
        "fecha_registro_formulario": st.column_config.DateColumn("Fecha registro", format='DD/MM/YYYY', disabled=True),
        "direccion_hogar": st.column_config.TextColumn("Dirección del hogar", disabled=True),
    }
    for col in df_display.columns:
        if col not in column_config and col != " ":
            column_config[col] = st.column_config.TextColumn(col, disabled=True)
    edited_df = st.data_editor(df_display, hide_index=True, column_config=column_config, key="editor_morb_extenso")
    if original_ids is not None:
        edited_df = edited_df.reset_index(drop=True)
        edited_df = pd.concat([edited_df, original_ids], axis=1)
    return edited_df

# deprecado
def data_editor_morb_simplifica(df_filtrado):
    df_filtrado[' '] = False


    columns_to_display = [col for col in df_filtrado.columns if col not in [' ', 'id']]
    columns_to_show = [' '] + columns_to_display + (['id'] if 'id' in df_filtrado.columns else [])
    df_filtrado = df_filtrado[columns_to_show]
    
    column_config = {
        " ": st.column_config.CheckboxColumn(" ", default=False, disabled=False),
        "fecha_registro_formulario": st.column_config.DateColumn("Registro De Formulario",format='DD/MM/YYYY', disabled=True),
        "diagnostico": st.column_config.TextColumn("Diagnóstico", disabled=False),
        "sexo": st.column_config.SelectboxColumn("Sexo", options=["Masculino", "Femenino"], disabled=False),
        "edad": st.column_config.NumberColumn("Edad", min_value=0, step=1, disabled=False),
        "id": st.column_config.TextColumn("ID", disabled=True),
    }
    for col in columns_to_show:
        if col not in column_config and col != ' ':
            column_config[col] = st.column_config.TextColumn(col, disabled=True)

    edited_df = st.data_editor(
        df_filtrado,
        hide_index=True,
        column_config=column_config,
        key="editor_morb_simplifica"
    )
    return edited_df


@st.fragment
def formulario_morb_extenso(db=DB_PATH):

    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a este formulario.", icon=":material/error:")
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
        mostrar_editor = st.toggle("Mostrar datos de registros", value=False, key="toggle_editor_morbilidadex")
        if mostrar_editor:
            df = filtrar_por_fechas(df, 'fecha_registro_formulario')
            edited_df = data_editor_morb_extenso(df)

            col_guardar, col_descargar, col_descargar_seleccionado, col_eliminar = st.columns(4)
            has_selection = edited_df[' '].any()

            with col_guardar:
                guardar = st.button("Guardar cambios", icon=":material/save:", width="stretch", type="primary")   
                #guadar_btn(procesar_guardado_morb_extenso, edited_df)

            with col_descargar:
                descargar_pdf(edited_df, "morbilidad_extensa")

            with col_descargar_seleccionado:
                df_sel = edited_df[edited_df[' '] == True]
                descargar_registros_seleccionados(edited_df, "morbilidad_extensa")
                descargar_pdf(df_sel, "morbilidad_extensa_seleccionado", label="Descarga selección", disabled=not has_selection)

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

    st.subheader(":material/new_label: Registrar Morbilidad", anchor=False)

    with st.form("form_morb_extenso"):

        # Primeras filas del formulario
        col_nombre, col_edad = st.columns(2)
        with col_nombre:
            nombres_apellidos = st.text_input(
                "Nombres y apellidos", max_chars=40,
                key="nombres_apellidos_morb_extenso",
                placeholder="Ej. Juan Pérez"
            )
        with col_edad:
            edad = st.number_input("Edad", min_value=0, step=1, key="edad_morb_extenso")

        diagnostico = st.text_area(
            "Diagnóstico", max_chars=150,
            key="diagnostico_morb_extenso",
            placeholder="Descripción del diagnóstico"
        )

        st.markdown("**Dirección de Hogar**")
        col_pais, col_estado, col_muni = st.columns(3)
        with col_pais:
            pais_hogar = st.text_input("País (Opcional)", max_chars=56, key="pais_hogar_morb_extenso", placeholder="Venezuela")
        with col_estado:
            estado_hogar = st.text_input("Estado (Opcional)", max_chars=56, key="estado_hogar_morb_extenso", placeholder="Anzoátegui")
        with col_muni:
            municipio_hogar = st.text_input("Municipio (Opcional)", max_chars=56, key="municipio_hogar_morb_extenso", placeholder="Simón Rodríguez")
        col_parroquia, col_ciudad = st.columns(2)
        with col_parroquia:
            parroquia_hogar = st.text_input("Parroquia", max_chars=56, key="parroquia_hogar_morb_extenso", placeholder="Edmundo Barrios (zona norte)")
        with col_ciudad:
            ciudad_hogar = st.text_input("Ciudad", max_chars=56, key="cuidad_hogar_morb_extenso", placeholder="El Tigre")
        direccion_exacta_hogar = st.text_area("Dirección Exacta", max_chars=150, key="direccion_exacta_hogar_morb_extenso", placeholder="Pueblo Nuevo Norte, 3ra Carrera Norte, Número 26")

        col_reg, col_limp = st.columns([30, 1])
        with col_reg:
            registrar = st.form_submit_button("Registrar", icon=":material/save:", type="primary")
        with col_limp:
            limpiar = st.form_submit_button("", icon=":material/cleaning_services:", on_click=limpiar_campos_morb_extenso, type="tertiary", help="Limpia todos los campos del formulario.")

        if registrar:
            # Validaciones básicas
            if not all([nombres_apellidos, diagnostico, parroquia_hogar, ciudad_hogar, direccion_exacta_hogar]):
                st.error("Por favor completa todos los campos obligatorios", icon=":material/error:")
                return
            if not validar_texto(nombres_apellidos, "Los", "nombres y apellidos"): return
            if not validar_cinco_espacios(nombres_apellidos, "Los", "nombres y apellidos"): return
            if not val_texynum(diagnostico, "El", "diagnóstico"): return

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


@st.fragment
def formulario_morb_simplifica(db=DB_PATH):
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a este formulario.", icon=":material/error:")
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

    st.subheader(":material/table: Datos de Morbilidad Simplificada", anchor=False)
    df = operaciones_sql_morb_simplifica("cargar")
    if df is None:
        return

    if df.empty:
        st.info("No hay datos para mostrar.", icon=":material/info:")
    else:
        mostrar_editor = st.toggle("Mostrar datos de registros", value=False, key="toggle_editor_morbsim")

        if mostrar_editor:
            df = filtrar_por_fechas(df, 'fecha_registro_formulario')
            edited_df = data_editor_morb_simplifica(df)
            has_selection = edited_df[' '].any()
            col_guardar, col_descargar, col_descargar_seleccionado, col_eliminar = st.columns(4)

            with col_descargar:
                descargar_pdf(edited_df, "morbilidad_simplificada")        
            with col_descargar_seleccionado:
                df_sel = edited_df[edited_df[' '] == True]
                descargar_registros_seleccionados(edited_df, "morbilidad_simplificada")
                descargar_pdf(df_sel, "morbilidad_simplificada_seleccionado", label="Descarga selección", disabled=not has_selection)
            with col_eliminar:
                btn_eliminar = st.button("Eliminar", icon=":material/delete:", key="delete_morbilidad_simplificada", 
                                        disabled=not has_selection, width="stretch",
                                        help="Eliminar registros seleccionados.")
                if btn_eliminar:
                    confirmar_eliminar(eliminar_registros_morb_simplifica, edited_df)
            with col_guardar:
                guadar_btn(procesar_guardado_morb_simplificado, edited_df)

    st.subheader(":material/new_label: Registrar Morbilidad Simplificada", anchor=False)
    with st.form("form_morb_simplifica"):
        col_izq, col_der = st.columns(2)
        with col_izq:
            diagnostico = st.text_area("Diagnóstico", max_chars=150, height=152, 
                                       key="diagnostico_morb_simplifica", placeholder="Descripción del diagnóstico")
        with col_der:
            edad = st.number_input("Edad", min_value=0, step=1, key="edad_morb_simplifica")
            sexo = st.selectbox("Sexo", ["Masculino", "Femenino"], key="sexo_morb_simplifica")
        col_reg, col_limp = st.columns([30, 1])
        with col_reg:
            registrar = st.form_submit_button("Registrar", icon=":material/save:", type="primary")
        with col_limp:
            limpiar = st.form_submit_button("", icon=":material/cleaning_services:", on_click=limpiar_campos_morb_simplificado, 
                                            type="tertiary", help="Limpia todos los campos del formulario.")
        if registrar:
            if not diagnostico:
                st.error("Por favor completa el diagnóstico", icon=":material/error:")
                return
            elif not val_notas(diagnostico, "El", "diagnostico"):
                return
            else:
                datos_registro = (diagnostico, edad, sexo, id_doctor, id_administrador, id_secretaria, rol_usuario)
                if operaciones_sql_morb_simplifica("registrar", datos_registro=datos_registro):
                    st.success("Registro guardado.", icon=":material/check_circle:")
                    st.rerun()

def mostrar_morb():
    logo_bandera = ASSETS_DIR / "imagebanderanueva2.png"
    
    logo_base64 = img_a_base64(logo_bandera)
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) 
    logo(tamano="100%")
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a este formulario.", icon=":material/error:")
        return
    tab1, tab2 = st.tabs(["| :material/personal_injury: Morbilidad |", 
                                "| :material/article_shortcut: Reporte General |"])
    with tab1:
        formulario_morb_extenso()
    with tab2:
        st.subheader(":material/arrow_circle_down: Descargas de reportes", anchor=False, divider="gray")
        col_izq, col_centro, col_der = st.columns([3.35, 4, 2.65])
        #with col_izq:
            #formulario_reporte_mensual_combinado()
        #st.markdown("---")
        with col_centro:
            formulario_reporte_general_morbilidad()
        #st.markdown("---")
        #with col_der:
            #formulario_reporte_mensual_general()
        st.markdown("")
    copyright_footer_dos("Equipo Investigador")

mostrar_morb()
