import streamlit as st
import datetime
from pathlib import Path
from utils.sql_control import operaciones_sql_natalidad, eliminar_registros_natalidad
from dateutil.relativedelta import relativedelta
from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez
from utils.filtro import filtrar_por_fechas, descargar_pdf, descargar_registros_seleccionados
from utils.verificaciones import obtener_info_usuario
from pages.menu import menu
import time
from utils.base_64 import img_a_base64
from utils.limpieza import limpiar_campos_natalidad
from utils.botones import confirmar_eliminar, guadar_btn
from utils.guardar_cambios import procesar_guardado_cambios_natalidad
configurar_pagina_espanol()
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

def data_editor_natalidad(df, rol_usuario):
    if " " not in df.columns:
        df.insert(0, " ", False)

    columns_to_display = [col for col in df.columns if col not in [" ", "id"]]
    columns_to_show = [" "] + columns_to_display + (["id"] if "id" in df.columns else [])
    df = df[columns_to_show]
    

    column_config = {
        " ": st.column_config.CheckboxColumn(" ", default=False, disabled=False),
        "fecha_registro_formulario": st.column_config.DateColumn("Fecha registro formulario", format='DD/MM/YYYY', disabled=True),
        "fecha": st.column_config.DateColumn("Fechas",format='DD/MM/YYYY', disabled=(rol_usuario == "Secretario (a)")),
        "partos": st.column_config.NumberColumn("Partos", min_value=0, step=1, disabled=(rol_usuario == "Secretario (a)")),
        "cesareas": st.column_config.NumberColumn("Cesáreas", min_value=0, step=1, disabled=(rol_usuario == "Secretario (a)")),
        "varones": st.column_config.NumberColumn("Varones", min_value=0, step=1, disabled=(rol_usuario == "Secretario (a)")),
        "hembras": st.column_config.NumberColumn("Hembras", min_value=0, step=1, disabled=(rol_usuario == "Secretario (a)")),
        "gemelar": st.column_config.NumberColumn("Gemelar", min_value=0, step=1, disabled=True),
        "mto": st.column_config.NumberColumn("Muertos (MTO)", min_value=0, step=1, disabled=(rol_usuario == "Secretario (a)")),
        "partos_extrahospitalarios": st.column_config.NumberColumn("Partos extrahospitalarios", min_value=0, step=1, disabled=(rol_usuario == "Secretario (a)")),
        "sexo_gemelar": st.column_config.SelectboxColumn("Sexo de los gemelos", options=["No aplica", "Varones", "Hembras", "Mixto"], disabled=(rol_usuario == "Secretario (a)")),
        "id": st.column_config.TextColumn("ID", disabled=True),
        "id_doctor": st.column_config.TextColumn("ID_Doctor", disabled=True),
        "registrado_por": st.column_config.TextColumn("Registrado por", disabled=True),
    }


    for col in columns_to_show:
        if col not in column_config and col != " ":
            column_config[col] = st.column_config.TextColumn(col, disabled=True)

    edited_df = st.data_editor(
        df,
        hide_index=True,
        column_config=column_config,
        key="editor_natalidad"
    )
    return edited_df


@st.fragment
def formulario_natalidad():
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
    id_administrador = info_usuario["id_administrador"]

    st.header(":material/pediatrics: Datos De Natalidad", divider="gray", anchor=False)

    df = operaciones_sql_natalidad("cargar")
    if df is None:
        return

    if df.empty:
        st.info("No hay registros disponibles.", icon=":material/info:")
    else:
        mostrar_editor = st.toggle("Mostrar datos de registros", value=False, key="toggle_editor_natalidad")

        if mostrar_editor:
            df[' '] = False
            df_filtrado = filtrar_por_fechas(df, 'fecha')
            edited_df = data_editor_natalidad(df_filtrado, rol_usuario)

            if not df_filtrado.empty:
                col1, col3 = st.columns(2)
                has_selection = edited_df[' '].any()
                col_guadar, col_descargar_todo, col_des_seleccionado, col_eliminar = st.columns(4)

                if rol_usuario == "Secretario (a)":
                    with col1:
                        descargar_pdf(edited_df, "natalidad", label="Descargar PDF")
                    with col3:
                        df_sel = edited_df[edited_df[' '] == True]
                        descargar_registros_seleccionados(edited_df, "natalidad")
                        descargar_pdf(df_sel, "natalidad_seleccionado", label="Descarga selección", disabled=not has_selection)
                else:
                    with col_guadar:
                        guadar_btn(procesar_guardado_cambios_natalidad, edited_df)                
                    with col_descargar_todo:
                            descargar_pdf(edited_df, "natalidad")                
                    with col_des_seleccionado:
                        df_sel = edited_df[edited_df[' '] == True]
                        descargar_registros_seleccionados(edited_df, "natalidad")
                        descargar_pdf(df_sel, "natalidad_seleccionado", label="Descarga selección", disabled=not has_selection)
                    with col_eliminar:
                        btn_eliminar = st.button("Eliminar", icon=":material/delete:", key="delete_natalidad", 
                                                disabled=not has_selection, width="stretch",
                                                help="Eliminar registros seleccionados.")
                        if btn_eliminar:
                            confirmar_eliminar(eliminar_registros_natalidad, edited_df)
                        #  eliminar_registros_natalidad(edited_df)
                    
    if rol_usuario != "Secretario (a)":
        st.subheader(":material/new_label: Registrar Natalidad", anchor=False)
        with st.form("form_natalidad"):
            col_fecha, col_partos, col_hembras, col_varones = st.columns(4)
            with col_fecha:
                fecha_minima = datetime.datetime.now().date() - relativedelta(months=1)
                fecha_maxima = datetime.date.today() + relativedelta(months=1)
                fecha = st.date_input("Fecha", format="DD/MM/YYYY",
                                    min_value=fecha_minima,
                                    max_value=fecha_maxima, key="fecha_natalidad")
            with col_partos:
                partos = st.number_input("Partos", min_value=0, step=1, key="partos_natalidad")
            with col_hembras:
                hembras = st.number_input("Hembras", min_value=0, step=1, key="hembras_natalidad")
            with col_varones:
                varones = st.number_input("Varones", min_value=0, step=1, key="varones_natalidad")

            col_sexo_gem, col_gemelar = st.columns(2)
            with col_sexo_gem:
                sexo_gemelar = st.selectbox("Sexo de los gemelos", options=["No aplica", "Varones", "Hembras", "Mixto"], key="sexo_gemelar_natalidad")
            with col_gemelar:
                gemelar = st.number_input("Gemelar", min_value=0, step=1, key="gemelar_natalidad")

            col_cesareas, col_mto = st.columns(2)
            with col_cesareas:
                cesareas = st.number_input("Cesáreas", min_value=0, step=1, key="cesareas_natalidad")
            with col_mto:
                mto = st.number_input("Muertos (MTO)", min_value=0, step=1, key="mto_natalidad")

            partos_extrahospitalarios = st.number_input("Partos extrahospitalarios", min_value=0, step=1, key="partos_extra_natalidad")

            col_reg, col_limp = st.columns([30, 1])
            with col_reg:
                registrar = st.form_submit_button("Registrar", icon=":material/save:", type="primary")
            with col_limp:
                limpiar = st.form_submit_button("", icon=":material/cleaning_services:",
                                                on_click=limpiar_campos_natalidad, type="tertiary",
                                                help="Limpia todos los campos del formulario.")      
            if registrar:
                fecha_formateada_nacimiento = fecha.strftime("%d/%m/%Y")

                varones_ajustado = varones
                hembras_ajustado = hembras
                if sexo_gemelar == "Varones":
                    varones_ajustado += gemelar * 2
                elif sexo_gemelar == "Hembras":
                    hembras_ajustado += gemelar * 2
                elif sexo_gemelar == "Mixto":
                    varones_ajustado += gemelar
                    hembras_ajustado += gemelar

                datos_registro = (
                    fecha_formateada_nacimiento, partos, cesareas, varones_ajustado, hembras_ajustado,
                    gemelar, mto, partos_extrahospitalarios, id_doctor, id_administrador, rol_usuario
                )
                if operaciones_sql_natalidad("registrar", datos_registro=datos_registro):
                    st.success("Registro guardado correctamente.", icon=":material/check_circle:")
                    st.rerun()

def mostrar_nata():
    logo_bandera = ASSETS_DIR / "imagebanderanueva2.png"
    logo_base64 = img_a_base64(logo_bandera)
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) # Llama a la función para recargar la página una vez.
    logo(tamano="100%")
    formulario_natalidad()

mostrar_nata()