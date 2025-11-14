import streamlit as st
import os
from utils.sql_control import operaciones_sql_morb_extenso, operaciones_sql_morb_simplifica, eliminar_registros_morb_extenso, eliminar_registros_morb_simplifica
from pathlib import Path
import datetime
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

    df[' '] = False


    columns_to_display = [col for col in df.columns if col not in [' ', 'id']]
    columns_to_show = [' '] + columns_to_display + (['id'] if 'id' in df.columns else [])
    df = df[columns_to_show]


    column_config = {
        " ": st.column_config.CheckboxColumn(" ", default=False, disabled=False),
        "HC": st.column_config.TextColumn("HC", disabled=True),
        "nombres_apellidos": st.column_config.TextColumn("Nombres y apellidos", disabled=False),
        "diagnostico": st.column_config.TextColumn("Diagnóstico", disabled=False),
        "edad": st.column_config.NumberColumn("Edad", min_value=0, step=1, disabled=False),
        "sexo": st.column_config.SelectboxColumn("Sexo", options=["Masculino", "Femenino"], disabled=False),
        "estado_civil": st.column_config.SelectboxColumn(
            "Estado Civil",
            options=["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a"],
            disabled=False
        ),
        "fecha_nacimiento": st.column_config.TextColumn("Fecha De Nacimiento", disabled=False),
        "cedula": st.column_config.TextColumn("Cédula", disabled=False),
        "telefono": st.column_config.TextColumn("Teléfono", disabled=False),
        "direccion_hogar": st.column_config.TextColumn("Direccion Hogar", disabled=True),
        "direccion_nacimiento": st.column_config.TextColumn("Direccion Nacimiento", disabled=True),
        "id": st.column_config.TextColumn("id", disabled=True), 
        "fecha_registro_formulario": st.column_config.DateColumn("Registro De Formulario", disabled=True),
    }

    edited_df = st.data_editor(
        df,
        hide_index=True,
        column_config=column_config,
        key="editor_morb_extenso"
    )
    return edited_df


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

    st.subheader(":material/table: Datos de Morbilidad Extensa", anchor=False)
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
                guadar_btn(procesar_guardado_morb_extenso, edited_df)
            with col_descargar:
                descargar_pdf(edited_df, "morbilidad_extensa")        
            with col_descargar_seleccionado:
                df_sel = edited_df[edited_df[' '] == True]
                descargar_registros_seleccionados(edited_df, "morbilidad_extensa")
                descargar_pdf(df_sel, "morbilidad_extensa_seleccionado", label="Descarga selección", disabled=not has_selection)
            with col_eliminar:
                btn_eliminar = st.button("Eliminar", icon=":material/delete:", key="delete_morbilidad_extensa", 
                                        disabled=not has_selection, width="stretch",
                                        help="Eliminar registros seleccionados.")
                if btn_eliminar:
                    confirmar_eliminar(eliminar_registros_morb_extenso, edited_df)

    st.subheader(":material/new_label: Registrar Morbilidad Extensa", anchor=False)
    with st.form("form_morb_extenso"):
        fecha_minima = datetime.date.today() - relativedelta(months=1)
        fecha_maxima = datetime.date.today() + relativedelta(months=1)
        fecha_maxima_hoy = datetime.date.today()
        fecha_minimi_1935 = datetime.date(1935, 1, 1)
        col_hc, col_nombre = st.columns(2)
        with col_hc:
            hc = st.text_input("Historia clínica", max_chars=8, key="hc_morb_extenso", placeholder="Ej. 12345678")
        with col_nombre:
            nombres_apellidos = st.text_input("Nombres y apellidos", max_chars=40, key="nombres_apellidos_morb_extenso", placeholder="Ej. Juan Pérez")
        col_cedula, col_tlf = st.columns(2)
        with col_cedula:
            cedula = st.text_input("Cédula", max_chars=10, key="cedula_morb_extenso", placeholder="Ej. V12345678")
        with col_tlf:
            telefono = st.text_input("Teléfono", max_chars=15, key="telefono_morb_extenso", placeholder="Ej. +58412-1234567")
        diagnostico = st.text_area("Diagnóstico", max_chars=150, key="diagnostico_morb_extenso", placeholder="Descripción del diagnóstico")
        col_edad, col_sexo = st.columns(2)
        with col_edad:
            edad = st.number_input("Edad", min_value=0, step=1, key="edad_morb_extenso")
        with col_sexo:
            sexo = st.selectbox("Sexo", ["Masculino", "Femenino"], key="sexo_morb_extenso")
        col_fecha_nac, col_estado_civil = st.columns(2)
        with col_fecha_nac:
            fecha_nacimiento = st.date_input("Fecha de Nacimiento", min_value=fecha_minimi_1935, 
                                             max_value=fecha_maxima_hoy, 
                                             key="fecha_nacimiento_morb_extenso", format=DATE_FORMAT)
        with col_estado_civil:
            estado_civil = st.selectbox("Estado Civil", ["Soltero/a", "Casado/a", "Divorciado/a", "Viudo/a"], key="estado_civil_morb_extenso")
        st.markdown("**Dirección de Hogar**")
        col_pais, col_estado, col_muni = st.columns(3)
        with col_pais:
            pais_hogar = st.text_input("País (Opcional)", max_chars=56, key="pais_hogar_morb_extenso", placeholder="Venezuela")
        with col_estado:
            estado_hogar = st.text_input("Estado (Opcional)", max_chars=56, key="estado_hogar_morb_extenso", placeholder="Anzoátegui")
        with col_muni:
            municipio_hogar = st.text_input("Municipio (Opcional)", max_chars=56, key="municipio_hogar_morb_extenso", placeholder="Simón Rodríguez")
        col_parroquia, col_city = st.columns(2)
        with col_parroquia:
            parroquia_hogar = st.text_input("Parroquia", max_chars=56, key="parroquia_hogar_morb_extenso", placeholder="Edmundo Barrios (zona norte)")
        with col_city:
            ciudad_hogar = st.text_input("Ciudad", max_chars=56, key="cuidad_hogar_morb_extenso", placeholder="El Tigre")
        direccion_exacta_hogar = st.text_area("Dirección Exacta", max_chars=150, key="direccion_exacta_hogar_morb_extenso", placeholder="Pueblo Nuevo Norte, 3ra Carrera Norte, Número 26")
        st.markdown("**Dirección de Nacimiento**")
        col_pais_2, col_estado_2, col_muni_2 = st.columns(3)
        with col_pais_2:
            pais_nacimiento = st.text_input("País (Opcional)", max_chars=56, key="pais_nacimiento_morb_extenso", placeholder="Venezuela")
        with col_estado_2:
            estado_nacimiento = st.text_input("Estado (Opcional)", max_chars=56, key="estado_nacimiento_morb_extenso", placeholder="Anzoátegui")
        with col_muni_2:
            municipio_nacimiento = st.text_input("Municipio (Opcional)", max_chars=56, key="municipio_nacimiento_morb_extenso", placeholder="Simón Rodríguez")
        col_city_2, col_parroquia_2 = st.columns(2)
        with col_parroquia_2:
            parroquia_nacimiento = st.text_input("Parroquia (Opcional)", max_chars=56, key="parroquia_nacimiento_morb_extenso", placeholder="Edmundo Barrios")
        with col_city_2:
            ciudad_nacimiento = st.text_input("Ciudad", max_chars=56, key="cuidad_nacimiento_morb_extenso", placeholder="El Tigre")
        direccion_exacta_nacimiento = st.text_area("Dirección Exacta (Opcional)", max_chars=150, key="direccion_exacta_nacimiento_morb_extenso", placeholder="Pueblo Nuevo Norte, 3ra Carrera Norte, Número 26")
        col_reg, col_limp = st.columns([30, 1])
        with col_reg:
            registrar = st.form_submit_button("Registrar", icon=":material/save:", type="primary")
        with col_limp:
            limpiar = st.form_submit_button("", icon=":material/cleaning_services:", on_click=limpiar_campos_morb_extenso, 
                                            type="tertiary", help="Limpia todos los campos del formulario.")
        if registrar:
            if not all([hc, nombres_apellidos, diagnostico, ciudad_nacimiento, parroquia_hogar, ciudad_hogar, 
                        direccion_exacta_hogar, cedula, telefono, fecha_nacimiento, estado_civil]):
                st.error("Por favor completa todos los campos obligatorios", icon=":material/error:")
                return
            elif not val_num_espacios(hc, "La", "historia clínica"):
                return
            elif not validar_texto(nombres_apellidos, "Los", "nombres y apellidos"): 
                return     
            elif not validar_cinco_espacios(nombres_apellidos, "Los", "nombres y apellidos"):
                return
            elif not val_solo_numeros(cedula, "La", "cedula de identidad"): #
                return     
            elif not val_num_espacios(telefono, "El", "telefono"): #
                return     
            elif not val_texynum(diagnostico, "El", "diagnóstico"): 
                return
            elif not validar_pais(pais_hogar, "El", "país del hogar"): 
                return     
            elif not validar_pais(estado_hogar, "El", "estado del hogar"): 
                return     
            elif not validar_pais(municipio_hogar, "El", "municipio del hogar"): 
                return     
            elif not validar_pais(parroquia_hogar, "La", "parroquia del hogar"): 
                return     
            elif not validar_pais(ciudad_hogar, "La", "ciudad del hogar"): 
                return     
            elif not val_notas(direccion_exacta_hogar, "La", "dirección del hogar"): 
                return     
            elif not validar_pais(pais_nacimiento, "El", "país de nacimiento"): 
                return     
            elif not validar_pais(estado_nacimiento, "El", "estado de nacimiento"): 
                return     
            elif not validar_pais(municipio_nacimiento, "El", "municipio de nacimiento"): 
                return     
            elif not validar_pais(parroquia_nacimiento, "La", "parroquia de nacimiento"): 
                return     
            elif not validar_pais(ciudad_nacimiento, "La", "ciudad de nacimiento"): 
                return     
            elif not val_notas(direccion_exacta_nacimiento, "La", "dirección de nacimiento"): 
                return     
            else:
                fecha_formateada_nacimiento = fecha_nacimiento.strftime("%d/%m/%Y")
                datos_registro = (
                    hc, nombres_apellidos, diagnostico, edad, sexo, 
                    pais_hogar, estado_hogar, municipio_hogar, parroquia_hogar, ciudad_hogar, direccion_exacta_hogar,
                    pais_nacimiento, estado_nacimiento, municipio_nacimiento, parroquia_nacimiento, ciudad_nacimiento, direccion_exacta_nacimiento,
                    fecha_formateada_nacimiento, estado_civil, cedula, telefono,
                    id_doctor, id_administrador, id_secretaria, rol_usuario
                )
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
    recargar_una_vez(__file__) # Llama a la función para recargar la página una vez.
    logo(tamano="100%")
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a este formulario.", icon=":material/error:")
        return
    tipo_morb = st.selectbox(
        ":material/gesture_select: Selecciona el tipo de registro:",
        options=["Morbilidad Extensa", "Morbilidad Simplificada"],
        key="tipo_morb"
    )
    formularios_morb = {
        "Morbilidad Extensa": formulario_morb_extenso,
        "Morbilidad Simplificada": formulario_morb_simplifica
    }
    func_morb = formularios_morb.get(tipo_morb)
    if func_morb:
        func_morb()
    copyright_footer_dos("Equipo Investigador")

mostrar_morb()
