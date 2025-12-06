import streamlit as st
import datetime
import pandas as pd
from pathlib import Path
from utils.sql_control import operaciones_sql_neonatal, eliminar_registros_neonatal, operaciones_sql_infantil, eliminar_registros_infantil, operaciones_sql_materna, eliminar_registros_materna, operaciones_sql_mensual_infantil, eliminar_registros_mensual_infantil, operaciones_sql_mensual_neonatal, eliminar_registros_mensual_neonatal, operaciones_sql_mensual_general, eliminar_registros_mensual_general, calcular_tasa_por_ano, calcular_tasa_por_ano_infantil, calcular_tasa_por_ano_neonatal
from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez, copyright_footer_dos
from utils.verificaciones import obtener_info_usuario
from pages.menu import menu
from dateutil.relativedelta import relativedelta
from utils.filtro import filtrar_por_fechas, descargar_pdf, descargar_registros_seleccionados
from utils.base_64 import img_a_base64
from utils.limpieza import limpiar_campos_mensual_general, limpiar_campos_mensual_neonatal, limpiar_campos_mensual_infantil, limpiar_campos_materna, limpiar_campos_infantil, limpiar_campos_neonatal
from utils.validaciones import validar_texto, val_texynum, val_notas, val_num_espacios, validar_cinco_espacios, validar_pais
from utils.botones import confirmar_eliminar, guadar_btn
from utils.guardar_cambios import (procesar_guardado_cambios_mortalidad_neonatal,
                                   procesar_guardado_cambios_mortalidad_infantil, procesar_guardado_cambios_mortalidad_materna,
                                   procesar_guardado_cambios_mensual_neonatal, procesar_guardado_cambios_mensual_infantil,
                                   procesar_guardado_cambios_mensual_general)
from utils.reportes import formulario_reporte_general, formulario_reporte_mensual_combinado, formulario_reporte_mensual_general
import os
DB_PATH = os.getenv("hospital.db", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'
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


#NEONATAL
def data_editor_neonatal(df_filtrado, rol_usuario):
    if " " not in df_filtrado.columns:
        df_filtrado.insert(0, " ", False)


    columns_to_display = [col for col in df_filtrado.columns if col not in [" ", "id"]]
    columns_to_show = [" "] + columns_to_display + (["id"] if "id" in df_filtrado.columns else [])
    df_filtrado = df_filtrado[columns_to_show]


    column_config = {
        " ": st.column_config.CheckboxColumn(" ", default=False, disabled=False),
        "fecha_registro_formulario": st.column_config.DateColumn("Fecha registro", format='DD/MM/YYYY',disabled=True),
        "historia_clinica": st.column_config.TextColumn("Historia clínica", disabled=True),
        "nombres_apellidos": st.column_config.TextColumn("Nombres y Apellidos", disabled=(rol_usuario == "Secretario (a)")),
        "nombre_madre": st.column_config.TextColumn("Nombre de la madre", disabled=(rol_usuario == "Secretario (a)")),
        "fecha_nacimiento": st.column_config.TextColumn("Fecha de nacimiento", disabled=(rol_usuario == "Secretario (a)")),
        "hora_nacimiento": st.column_config.TextColumn("Hora de nacimiento", disabled=(rol_usuario == "Secretario (a)")),
        "fecha_ingreso": st.column_config.TextColumn("Fecha de ingreso", disabled=(rol_usuario == "Secretario (a)")),
        "hora_ingreso": st.column_config.TextColumn("Hora de ingreso", disabled=(rol_usuario == "Secretario (a)")),
        "fecha_defuncion": st.column_config.DateColumn("Fecha de defunción", format='DD/MM/YYYY',disabled=(rol_usuario == "Secretario (a)")),
        "hora_defuncion": st.column_config.TextColumn("Hora de defunción", disabled=(rol_usuario == "Secretario (a)")),
        "edad": st.column_config.TextColumn("Edad", disabled=(rol_usuario == "Secretario (a)")),
        "tiempo": st.column_config.TextColumn("Tiempo de edad", disabled=(rol_usuario == "Secretario (a)")),
        "idx_ingreso": st.column_config.TextColumn("IDX de ingreso", disabled=(rol_usuario == "Secretario (a)")),
        "idx_defuncion": st.column_config.TextColumn("IDX de defunción", disabled=(rol_usuario == "Secretario (a)")),
        "semanas_gestacion": st.column_config.NumberColumn("Semanas de gestación", min_value=0, step=1, disabled=(rol_usuario == "Secretario (a)")),
        "peso": st.column_config.NumberColumn("Peso (kg)", min_value=0.0, step=0.1, format="%.1f", disabled=(rol_usuario == "Secretario (a)")),
        "talla": st.column_config.NumberColumn("Talla (cm)", min_value=0.0, step=0.1, format="%.1f", disabled=(rol_usuario == "Secretario (a)")),
        "pais_hogar": st.column_config.TextColumn("País", disabled=(rol_usuario == "Secretario (a)")),
        "estado_hogar": st.column_config.TextColumn("Estado", disabled=(rol_usuario == "Secretario (a)")),
        "municipio_hogar": st.column_config.TextColumn("Municipio", disabled=(rol_usuario == "Secretario (a)")),
        "parroquia_hogar": st.column_config.TextColumn("Parroquia", disabled=(rol_usuario == "Secretario (a)")),
        "ciudad_hogar": st.column_config.TextColumn("Ciudad", disabled=(rol_usuario == "Secretario (a)")),
        "direccion": st.column_config.TextColumn("Dirección", disabled=True),
        "id": st.column_config.TextColumn("ID", disabled=True),
        "registrado_por": st.column_config.TextColumn("Registrado por", disabled=True),
    }

    for col in columns_to_show:
        if col not in column_config and col != " ":
            column_config[col] = st.column_config.TextColumn(col, disabled=True)

    edited_df = st.data_editor(
        df_filtrado,
        hide_index=True,
        column_config=column_config,
        key="editor_neonatal"
    )
    return edited_df

@st.fragment
def formulario_neonatal(db=DB_PATH):
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

    st.subheader(":material/table: Datos de Muerte Neonatal", anchor=False)
    df = operaciones_sql_neonatal("cargar")
    if df is None:
        return
    if rol_usuario == "Secretario (a)":
        if df.empty:
            st.info("No hay datos para mostrar.", icon=":material/info:")
            st.markdown("# ")
    elif rol_usuario != "Secretario (a)":
        if df.empty:
            st.info("No hay datos para mostrar.", icon=":material/info:")
        else:
            mostrar_editor = st.toggle("Mostrar datos de registros", value=False, key="toggle_editor_neonatal")

            if mostrar_editor:
                df_filtrado = filtrar_por_fechas(df, 'fecha_defuncion')
                edited_df = data_editor_neonatal(df_filtrado, rol_usuario)
                col1, col3 = st.columns(2)
                has_selection = edited_df[' '].any()
                col_guardar, col_descargar, col_descargar_seleccionado, col_eliminar = st.columns(4)
                
                if rol_usuario == "Secretario (a)":
                    with col1:
                        descargar_pdf(edited_df, "mortalidad_neonatal", label="Descargar PDF")
                    with col3:
                        df_sel = edited_df[edited_df[' '] == True]
                        descargar_registros_seleccionados(edited_df, "mortalidad_neonatal")
                        descargar_pdf(df_sel, "mortalidad_neonatal_seleccionado", label="Descarga selección", disabled=not has_selection)
                else:
                    with col_guardar:
                        guadar_btn(procesar_guardado_cambios_mortalidad_neonatal, edited_df) 
                    with col_descargar:
                        descargar_pdf(edited_df, "mortalidad_neonatal")                
                    with col_descargar_seleccionado:
                        df_sel = edited_df[edited_df[' '] == True]
                        descargar_registros_seleccionados(edited_df, "mortalidad_neonatal")
                        descargar_pdf(df_sel, "mortalidad_neonatal_seleccionado", label="Descarga selección", disabled=not has_selection)
                    with col_eliminar:
                        btn_eliminar = st.button("Eliminar", icon=":material/delete:", key="delete_mortalidad_neonatal", 
                                                disabled=not has_selection, width="stretch",
                                                help="Eliminar registros seleccionados.")
                        if btn_eliminar:
                            confirmar_eliminar(eliminar_registros_neonatal, edited_df)

    if rol_usuario != "Secretario (a)":
        st.subheader(":material/new_label: Registrar Muerte Neonatal", anchor=False)
        with st.form("form_neonatal"):
            # variables de rangos de fechas posibles
            fecha_minima = datetime.date.today() - relativedelta(months=1)
            fecha_maxima = datetime.date.today() + relativedelta(months=1)
            fecha_maxima_hoy = datetime.date.today()
            fecha_minimi_1935 = datetime.date(1935, 1, 1)

            # primera fila
            col_hc, col_nombres, col_madre = st.columns(3)
            with col_hc:
                historia_clinica = st.text_input("Historia clínica", max_chars=8, key="historia_clinica_neonatal", placeholder="Ej. 12345678")
            with col_nombres:
                nombres_apellidos = st.text_input("Nombres y apellidos", max_chars=40, key="nombres_apellidos_neonatal", placeholder="Ej. Juan Pérez")
            with col_madre:
                nombre_madre = st.text_input("Nombre de la madre", max_chars=40, key="nombre_madre_neonatal", placeholder="Ej. Maria Jimenez")
            
            col_fecha_nacimiento, col_hora_nacimiento, col_fecha_ingreso, col_hora_ingreso = st.columns(4)
            with col_fecha_nacimiento:
                fecha_nacimiento = st.date_input("Fecha de nacimiento", format=DATE_FORMAT, min_value=fecha_minimi_1935, 
                                                max_value=fecha_maxima_hoy, key="fecha_nacimiento_neonatal")
            with col_hora_nacimiento:
                hora_nacimiento = st.time_input("Hora de nacimiento", key="hora_nacimiento_neonatal", value="now")

            with col_fecha_ingreso:
                fecha_ingreso = st.date_input("Fecha de ingreso", format=DATE_FORMAT, min_value=fecha_minima, 
                                              max_value=fecha_maxima, key="fecha_ingreso_neonatal")
            with col_hora_ingreso:
                hora_ingreso = st.time_input("Hora de ingreso", key="hora_ingreso_neonatal", value="now")
            
            col_fecha_defuncion, col_hora_defuncion, col_edad, col_tiempo = st.columns(4)

            veintiocho_dias = fecha_nacimiento + relativedelta(days=28)
            # Limitar el selector a la ventana entre la fecha de nacimiento y 28 días después.
            max_defuncion = min(veintiocho_dias, fecha_maxima) if 'fecha_maxima' in locals() else veintiocho_dias
            with col_fecha_defuncion:
                fecha_defuncion = st.date_input("Fecha de defunción", format='DD/MM/YYYY', min_value=fecha_minimi_1935, 
                                                max_value=max_defuncion, key="fecha_defuncion_neonatal")
            with col_hora_defuncion:
                hora_defuncion = st.time_input("Hora de defunción", key="hora_defuncion_neonatal", value="now")
            with col_edad:
                edad = st.number_input("Edad", min_value=0, step=1, key="edad_neonatal")
            with col_tiempo:
                tiempo = st.selectbox("Tiempo de edad", ["Horas", "Meses", "Años"], key="tiempo_neonatal")
            edad_junto = f"{edad} {tiempo}"
            
            col_idx_ingreso, col_idx_defuncion = st.columns(2)
            with col_idx_ingreso:
                idx_ingreso = st.text_area("IDX de ingreso", max_chars=150, key="idx_ingreso_neonatal", placeholder="Descripción de la IDX de ingreso")
            with col_idx_defuncion:
                idx_defuncion = st.text_area("IDX de defunción", max_chars=150, key="idx_defuncion_neonatal", placeholder="Descripción de la IDX de defuncion")
            
            st.markdown("**Dirección**")
            col_pais, col_estado, col_muni = st.columns(3)
            with col_pais:
                pais_hogar = st.text_input("País", max_chars=56, key="pais_hogar_neonatal", placeholder="Venezuela")
            with col_estado:
                estado_hogar = st.text_input("Estado", max_chars=56, key="estado_hogar_neonatal", placeholder="Anzoátegui")
            with col_muni:
                municipio_hogar = st.text_input("Municipio (Opcional)", max_chars=56, key="municipio_hogar_neonatal", 
                                                placeholder="Simón Rodríguez")
            col_parroquia, col_city = st.columns(2)
            with col_parroquia:
                parroquia_hogar = st.text_input("Parroquia", max_chars=56, key="parroquia_hogar_neonatal", placeholder="Edmundo Barrios (zona norte)")
            with col_city:
                ciudad_hogar = st.text_input("Ciudad", max_chars=56, key="cuidad_hogar_neonatal", placeholder="El Tigre")
            direccion_exacta = st.text_area("Dirección Exacta", max_chars=150, key="direccion_exacta_neonatal", placeholder="Pueblo Nuevo Norte, 3ra Carrera Norte, Número 26")
            col_semanas, col_peso, col_talla = st.columns(3)
            with col_semanas:
                semanas_gestacion = st.number_input("Semanas de gestación", min_value=0, step=1, key="semanas_gestacion_neonatal")
            with col_peso:
                peso = st.number_input("Peso (kg)", min_value=0.0, step=0.25, format="%.1f", 
                                       key="peso_neonatal")
            with col_talla:
                talla = st.number_input("Talla (cm)", min_value=0.0, step=0.25, format="%.1f", 
                                        key="talla_neonatal")
            col_reg, col_limp = st.columns([30, 1])
            with col_reg:
                registrar = st.form_submit_button("Registrar", icon=":material/save:", type="primary")
            with col_limp:
                limpiar = st.form_submit_button("", icon=":material/cleaning_services:", on_click=limpiar_campos_neonatal, 
                                                type="tertiary", help="Limpia todos los campos del formulario.")
            if registrar:
                # guardar fechas formateadas y validar
                if fecha_defuncion < fecha_nacimiento or fecha_defuncion > fecha_nacimiento + relativedelta(days=28):
                    st.error("La defuncion tiene que estar entre los primeros 28 dias del nacimiento.", icon=":material/error:")
                    return

                fecha_formateada_nacimiento = fecha_nacimiento.strftime("%d/%m/%Y")
                fecha_formateada_ingreso = fecha_ingreso.strftime("%d/%m/%Y")
                fecha_formateada_defuncion = fecha_defuncion.strftime("%d/%m/%Y")
                hora_12_nacimiento = hora_ingreso.strftime("%I:%M %p")
                hora_12_ingreso = hora_ingreso.strftime("%I:%M %p")
                hora_12_defuncion = hora_defuncion.strftime("%I:%M %p")
                
                hora_nacimiento_str = hora_nacimiento.strftime("%H:%M:%S") if isinstance(hora_nacimiento, datetime.time) else str(hora_nacimiento) if hora_nacimiento else ""
                hora_ingreso_str = hora_ingreso.strftime("%H:%M:%S") if isinstance(hora_ingreso, datetime.time) else str(hora_ingreso) if hora_ingreso else ""
                hora_defuncion_str = hora_defuncion.strftime("%H:%M:%S") if isinstance(hora_defuncion, datetime.time) else str(hora_defuncion) if hora_defuncion else ""
                
                datos_registro = (
                    historia_clinica, nombres_apellidos, nombre_madre, fecha_formateada_nacimiento, hora_nacimiento_str,
                    fecha_formateada_ingreso, hora_ingreso_str, fecha_formateada_defuncion, hora_defuncion_str, edad_junto,
                    idx_ingreso, idx_defuncion, semanas_gestacion, peso, talla, pais_hogar,
                    estado_hogar, municipio_hogar, parroquia_hogar, ciudad_hogar, direccion_exacta,
                    id_doctor, id_administrador
                )
                if not all([historia_clinica, nombres_apellidos, nombre_madre, fecha_nacimiento, pais_hogar, 
                            estado_hogar, parroquia_hogar, ciudad_hogar, direccion_exacta]):
                    st.error("Por favor completa todos los campos", icon=":material/error:")
                    return
                elif not val_num_espacios(historia_clinica, "La", "historia clinica"):
                    return
                elif not validar_texto(nombres_apellidos, "Los", "nombres y apellidos"):
                    return
                elif not validar_cinco_espacios(nombres_apellidos, "Los", "nombres y apellidos"):
                    return
                elif not validar_texto(nombre_madre, "El", "nombre de la madre"):
                    return
                elif not validar_cinco_espacios(nombre_madre, "El", "nombre de la madre"):
                    return
                elif not val_notas(idx_ingreso, "La", "IDX de ingreso"):
                    return
                elif not val_notas(idx_defuncion, "La", "IDX de defuncion"):
                    return   
                elif not validar_pais(pais_hogar, "El", "pais del hogar"):
                    return
                elif not validar_pais(estado_hogar, "El", "estado del hogar"):
                    return
                elif not validar_pais(municipio_hogar, "El", "municipio del hogar"):
                    return
                elif not validar_pais(parroquia_hogar, "La", "parroquia del hogar"):
                    return
                elif not validar_pais(ciudad_hogar, "La", "cuidad del hogar"):
                    return
                elif not val_notas(direccion_exacta, "La", "direccion exacta del hogar"):
                    return
                elif peso == 0.0 or talla == 0.0:
                    st.error("Peso y talla deben ser mayores a 0 para los registros diarios.", icon=":material/error:")
                    return
                else:
                    if operaciones_sql_neonatal("registrar", datos_registro=datos_registro):
                        st.success("Registro guardado.", icon=":material/check_circle:")
                        st.rerun()


#INFANTIL 
def data_editor_infantil(df, rol_usuario):
    if " " not in df.columns:
        df.insert(0, " ", False)


    columns_to_display = [col for col in df.columns if col not in [" ", "id"]]
    columns_to_show = [" "] + columns_to_display + (["id"] if "id" in df.columns else [])
    df_filtrado = df[columns_to_show]


    column_config = {
        " ": st.column_config.CheckboxColumn(" ", default=False, disabled=False),
        "fecha_registro_formulario": st.column_config.DateColumn("Fecha registro", disabled=True),
        "historia_clinica": st.column_config.TextColumn("Historia clínica", disabled=True),
        "nombres_apellidos": st.column_config.TextColumn("Nombres y Apellidos", disabled=(rol_usuario == "Secretario (a)")),
        "nombre_madre": st.column_config.TextColumn("Nombre de la madre", disabled=(rol_usuario == "Secretario (a)")),
        "fecha_nacimiento": st.column_config.TextColumn("Fecha de nacimiento", disabled=(rol_usuario == "Secretario (a)")),
        "hora_nacimiento": st.column_config.TextColumn("Hora de nacimiento", disabled=(rol_usuario == "Secretario (a)")),
        "fecha_ingreso": st.column_config.TextColumn("Fecha de ingreso", disabled=(rol_usuario == "Secretario (a)")),
        "hora_ingreso": st.column_config.TextColumn("Hora de ingreso", disabled=(rol_usuario == "Secretario (a)")),
        "fecha_defuncion": st.column_config.DateColumn("Fecha de defunción", format='DD/MM/YYYY', disabled=(rol_usuario == "Secretario (a)")),
        "hora_defuncion": st.column_config.TextColumn("Hora de defunción", disabled=(rol_usuario == "Secretario (a)")),
        "edad": st.column_config.TextColumn("Edad", disabled=(rol_usuario == "Secretario (a)")),
        "tiempo": st.column_config.TextColumn("Tiempo de edad", disabled=(rol_usuario == "Secretario (a)")),
        "idx_ingreso": st.column_config.TextColumn("IDX de ingreso", disabled=(rol_usuario == "Secretario (a)")),
        "idx_defuncion": st.column_config.TextColumn("IDX de defunción", disabled=(rol_usuario == "Secretario (a)")),
        "semanas_gestacion": st.column_config.NumberColumn("Semanas de gestación", min_value=0, step=1, disabled=(rol_usuario == "Secretario (a)")),
        "peso": st.column_config.NumberColumn("Peso (kg)", min_value=0.0, step=0.1, format="%.1f", disabled=(rol_usuario == "Secretario (a)")),
        "talla": st.column_config.NumberColumn("Talla (cm)", min_value=0.0, step=0.1, format="%.1f", disabled=(rol_usuario == "Secretario (a)")),
        "pais_hogar": st.column_config.TextColumn("País", disabled=(rol_usuario == "Secretario (a)")),
        "estado_hogar": st.column_config.TextColumn("Estado", disabled=(rol_usuario == "Secretario (a)")),
        "municipio_hogar": st.column_config.TextColumn("Municipio", disabled=(rol_usuario == "Secretario (a)")),
        "parroquia_hogar": st.column_config.TextColumn("Parroquia", disabled=(rol_usuario == "Secretario (a)")),
        "ciudad_hogar": st.column_config.TextColumn("Ciudad", disabled=(rol_usuario == "Secretario (a)")),
        "direccion": st.column_config.TextColumn("Dirección", disabled=True),
        "id": st.column_config.TextColumn("ID", disabled=True),
        "registrado_por": st.column_config.TextColumn("Registrado por", disabled=True),
    }

    for col in columns_to_show:
        if col not in column_config and col != " ":
            column_config[col] = st.column_config.TextColumn(col, disabled=True)

    edited_df = st.data_editor(
        df_filtrado,
        hide_index=True,
        column_config=column_config,
        key="editor_infantil"
    )
    return edited_df

@st.fragment
def formulario_infantil(db=DB_PATH):
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

    st.subheader(":material/table: Datos de Muerte Infantil", anchor=False)
    df = operaciones_sql_infantil("cargar")
    if df is None:
        return

    if rol_usuario == "Secretario (a)":
        if df.empty:
            st.info("No hay datos para mostrar.", icon=":material/info:")
            st.markdown("# ")
    elif rol_usuario != "Secretario (a)":
        if df.empty:
            st.info("No hay datos para mostrar.", icon=":material/info:")
        else:
            mostrar_editor = st.toggle("Mostrar datos de registros", value=False, key="toggle_editor_infantil")

            if mostrar_editor:
                df_filtrado = filtrar_por_fechas(df, 'fecha_defuncion')
                edited_df = data_editor_infantil(df_filtrado, rol_usuario)
                col1, col3 = st.columns(2)
                has_selection = edited_df[' '].any()
                col_guardar, col_descargar, col_descargar_seleccionado, col_eliminar = st.columns(4)
                
                if rol_usuario == "Secretario (a)":
                    with col1:
                        descargar_pdf(edited_df, "mortalidad_infantil", label="Descargar PDF")
                    with col3:
                        df_sel = edited_df[edited_df[' '] == True]
                        descargar_registros_seleccionados(edited_df, "mortalidad_infantil")
                        descargar_pdf(df_sel, "mortalidad_infantil_seleccionado", label="Descarga selección", disabled=not has_selection)
                else:
                    with col_guardar:
                        guadar_btn(procesar_guardado_cambios_mortalidad_infantil, edited_df) 
                    with col_descargar:
                        descargar_pdf(edited_df, "mortalidad_infantil")            
                    with col_descargar_seleccionado:
                        df_sel = edited_df[edited_df[' '] == True]
                        descargar_registros_seleccionados(edited_df, "mortalidad_infantil")
                        descargar_pdf(df_sel, "mortalidad_infantil_seleccionado", label="Descarga selección", disabled=not has_selection)
                    with col_eliminar:
                        btn_eliminar = st.button("Eliminar", icon=":material/delete:", key="delete_mortalidad_infantil", 
                                                disabled=not has_selection, width="stretch",
                                                help="Eliminar registros seleccionados.")
                        if btn_eliminar:
                            confirmar_eliminar(eliminar_registros_infantil, edited_df)

    if rol_usuario != "Secretario (a)":
        st.subheader(":material/new_label: Registrar Muerte Infantil", anchor=False)
        with st.form("form_infantil"):
            fecha_minima = datetime.date.today() - relativedelta(months=1)
            fecha_maxima = datetime.date.today() + relativedelta(months=1)
            fecha_maxima_hoy = datetime.date.today()
            fecha_minimi_1935 = datetime.date(1935, 1, 1)
            col_hc, col_nombres, col_madre = st.columns(3)
            with col_hc:
                historia_clinica = st.text_input("Historia clínica", max_chars=8, key="historia_clinica_infantil", placeholder="Ej. 12345678")
            with col_nombres:
                nombres_apellidos = st.text_input("Nombres y apellidos", max_chars=40, key="nombres_apellidos_infantil", placeholder="Ej. Juan Pérez")
            with col_madre:
                nombre_madre = st.text_input("Nombre de la madre", max_chars=40, key="nombre_madre_infantil", placeholder="Ej. Maria Jimenez")
            col_fecha_nacimiento, col_fecha_ingreso, col_hora_ingreso, col_fecha_defuncion = st.columns(4)
            with col_fecha_nacimiento:
                fecha_nacimiento = st.date_input("Fecha de nacimiento", format=DATE_FORMAT, min_value=fecha_minimi_1935, 
                                                max_value=fecha_maxima_hoy, key="fecha_nacimiento_infantil")
            with col_fecha_ingreso:
                fecha_ingreso = st.date_input("Fecha de ingreso", format=DATE_FORMAT, min_value=fecha_minima, 
                                              max_value=fecha_maxima, key="fecha_ingreso_infantil")
            with col_hora_ingreso:
                hora_ingreso = st.time_input("Hora de ingreso", key="hora_ingreso_infantil", value=datetime.datetime.now().time())
            with col_fecha_defuncion:
                fecha_defuncion = st.date_input("Fecha de defunción", format='DD/MM/YYYY', min_value=fecha_minimi_1935, 
                                                max_value=fecha_maxima_hoy, key="fecha_defuncion_infantil")
            col_hora_defuncion, col_edad, col_tiempo = st.columns(3)
            with col_hora_defuncion:
                hora_defuncion = st.time_input("Hora de defunción", key="hora_defuncion_infantil", value=datetime.datetime.now().time())
            with col_edad:
                edad = st.number_input("Edad", min_value=0, step=1, key="edad_infantil")
            with col_tiempo:
                tiempo = st.selectbox("Tiempo de edad", ["Meses", "Años"], key="tiempo_infantil")
            edad_junto = f"{edad} {tiempo}"
            col1, col2 = st.columns(2)
            with col1:
                idx_ingreso = st.text_area("IDX de ingreso", max_chars=150, key="idx_ingreso_infantil", placeholder="Descripción de la IDX de ingreso")
            with col2:
                idx_defuncion = st.text_area("IDX de defunción", max_chars=150, key="idx_defuncion_infantil", placeholder="Descripción de la IDX de defuncion")
            st.markdown("**Dirección**")
            col_pais, col_estado, col_muni = st.columns(3)
            with col_pais:
                pais_hogar = st.text_input("País", max_chars=56, key="pais_hogar_infantil", placeholder="Venezuela")
            with col_estado:
                estado_hogar = st.text_input("Estado", max_chars=56, key="estado_hogar_infantil", placeholder="Anzoátegui")
            with col_muni:
                municipio_hogar = st.text_input("Municipio (Opcional)", max_chars=56, key="municipio_hogar_infantil", placeholder="Simón Rodríguez")
            col_parroquia, col_city = st.columns(2)
            with col_parroquia:
                parroquia_hogar = st.text_input("Parroquia", max_chars=56, key="parroquia_hogar_infantil", placeholder="Edmundo Barrios (zona norte)")
            with col_city:
                ciudad_hogar = st.text_input("Ciudad", max_chars=56, key="ciudad_hogar_infantil", placeholder="El Tigre")
            direccion_exacta_hogar = st.text_area("Dirección Exacta", max_chars=150, key="direccion_exacta_hogar_infantil", placeholder="Pueblo Nuevo Norte, 3ra Carrera Norte, Número 26")
            col_reg, col_limp = st.columns([30, 1])
            with col_reg:
                registrar = st.form_submit_button("Registrar", icon=":material/save:", type="primary")
            with col_limp:
                limpiar = st.form_submit_button("", icon=":material/cleaning_services:", on_click=limpiar_campos_infantil, 
                                                type="tertiary", help="Limpia todos los campos del formulario.")  
            if registrar:
                fecha_formateada_nacimiento = fecha_nacimiento.strftime("%d/%m/%Y")
                fecha_formateada_ingreso = fecha_ingreso.strftime("%d/%m/%Y")
                fecha_formateada_defuncion = fecha_defuncion.strftime("%d/%m/%Y")
                hora_ingreso_str = hora_ingreso.strftime("%H:%M:%S") if isinstance(hora_ingreso, datetime.time) else str(hora_ingreso) if hora_ingreso else ""
                hora_defuncion_str = hora_defuncion.strftime("%H:%M:%S") if isinstance(hora_defuncion, datetime.time) else str(hora_defuncion) if hora_defuncion else ""
                datos_registro = (
                    historia_clinica, nombres_apellidos, nombre_madre, fecha_formateada_nacimiento, fecha_formateada_ingreso, hora_ingreso_str,
                    fecha_formateada_defuncion, hora_defuncion_str, edad_junto, idx_ingreso, idx_defuncion,
                    pais_hogar, estado_hogar, municipio_hogar, parroquia_hogar, ciudad_hogar,
                    direccion_exacta_hogar, id_doctor, id_administrador
                )
                if not all([historia_clinica, nombres_apellidos, nombre_madre, fecha_nacimiento, pais_hogar, 
                            estado_hogar, parroquia_hogar, ciudad_hogar, direccion_exacta_hogar, 
                            idx_ingreso, idx_defuncion]):
                    st.error("Por favor completa todos los campos", icon=":material/error:")
                    return
                elif not val_num_espacios(historia_clinica, "La", "historia clinica"):
                    return
                elif not validar_texto(nombres_apellidos, "Los", "nombres y apellidos"):
                    return
                elif not validar_cinco_espacios(nombres_apellidos, "Los", "nombres y apellidos"):
                    return
                elif not validar_texto(nombre_madre, "El", "nombre de la madre"):
                    return
                elif not validar_cinco_espacios(nombre_madre, "El", "nombre de la madre"):
                    return
                elif not val_notas(idx_ingreso, "La", "IDX de ingreso"):
                    return
                elif not val_notas(idx_defuncion, "La", "IDX de defuncion"):
                    return                
                elif not validar_pais(pais_hogar, "El", "pais del hogar"):
                    return
                elif not validar_pais(estado_hogar, "El", "estado del hogar"):
                    return
                elif not validar_pais(municipio_hogar, "El", "municipio del hogar"):
                    return
                elif not validar_pais(parroquia_hogar, "La", "parroquia del hogar"):
                    return
                elif not validar_pais(ciudad_hogar, "La", "cuidad del hogar"):
                    return
                elif not val_notas(direccion_exacta_hogar, "La", "direccion exacta del hogar"):
                    return
                else:
                    if operaciones_sql_infantil("registrar", datos_registro=datos_registro):
                        st.success("Registro guardado.", icon=":material/check_circle:")
                        st.rerun()

#MATERNA
def data_editor_materna(df, rol_usuario):
    if " " not in df.columns:
        df.insert(0, " ", False)

    columns_to_display = [col for col in df.columns if col not in [" ", "id"]]
    columns_to_show = [" "] + columns_to_display + (["id"] if "id" in df.columns else [])
    df = df[columns_to_show]

    column_config = {
        " ": st.column_config.CheckboxColumn(" ", default=False, disabled=False),
        "fecha_registro_formulario": st.column_config.DateColumn("Fecha registro", disabled=True),
        "historia_clinica": st.column_config.TextColumn("Historia clínica", disabled=True),
        "nombres_apellidos": st.column_config.TextColumn("Nombres y Apellidos", disabled=(rol_usuario == "Secretario (a)")),
        "fecha_nacimiento": st.column_config.TextColumn("Fecha de nacimiento", disabled=(rol_usuario == "Secretario (a)")),
        "fecha_ingreso": st.column_config.TextColumn("Fecha de ingreso", disabled=(rol_usuario == "Secretario (a)")),
        "hora_ingreso": st.column_config.TextColumn("Hora de ingreso", disabled=(rol_usuario == "Secretario (a)")),
        "fecha_defuncion": st.column_config.DateColumn("Fecha de defunción",format="DD/MM/YYYY", disabled=(rol_usuario == "Secretario (a)")),
        "hora_defuncion": st.column_config.TextColumn("Hora de defunción", disabled=(rol_usuario == "Secretario (a)")),
        "edad": st.column_config.TextColumn("Edad", disabled=(rol_usuario == "Secretario (a)")),
        "tiempo": st.column_config.TextColumn("Tiempo de edad", disabled=(rol_usuario == "Secretario (a)")),
        "idx_ingreso": st.column_config.TextColumn("IDX de ingreso", disabled=(rol_usuario == "Secretario (a)")),
        "idx_defuncion": st.column_config.TextColumn("IDX de defunción", disabled=(rol_usuario == "Secretario (a)")),
        "pais_hogar": st.column_config.TextColumn("País", disabled=(rol_usuario == "Secretario (a)")),
        "estado_hogar": st.column_config.TextColumn("Estado", disabled=(rol_usuario == "Secretario (a)")),
        "municipio_hogar": st.column_config.TextColumn("Municipio", disabled=(rol_usuario == "Secretario (a)")),
        "parroquia_hogar": st.column_config.TextColumn("Parroquia", disabled=(rol_usuario == "Secretario (a)")),
        "ciudad_hogar": st.column_config.TextColumn("Ciudad", disabled=(rol_usuario == "Secretario (a)")),
        "direccion_exacta_hogar": st.column_config.TextColumn("Dirección Exacta", disabled=(rol_usuario == "Secretario (a)")),
        "id": st.column_config.TextColumn("ID", disabled=True),
        "registrado_por": st.column_config.TextColumn("Registrado por", disabled=True),
    }

    for col in columns_to_show:
        if col not in column_config and col != " ":
            column_config[col] = st.column_config.TextColumn(col, disabled=True)

    edited_df = st.data_editor(
        df,
        hide_index=True,
        column_config=column_config,
        key="editor_materna"
    )
    return edited_df


@st.fragment
def formulario_materna(db=DB_PATH):
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

    st.subheader(":material/table: Datos de Muerte Materna", anchor=False)
    df = operaciones_sql_materna("cargar")
    if df is None:
        return

    if rol_usuario == "Secretario (a)":
        if df.empty:
            st.info("No hay datos para mostrar.", icon=":material/info:")
            st.markdown("# ")
    elif rol_usuario != "Secretario (a)":
        if df.empty:
            st.info("No hay datos para mostrar.", icon=":material/info:")
        else:
            mostrar_editor = st.toggle("Mostrar datos de registros", value=False, key="toggle_editor_materna")

            if mostrar_editor:
                df_filtrado = filtrar_por_fechas(df, 'fecha_defuncion')
                edited_df = data_editor_materna(df_filtrado, rol_usuario)
                col1, col3 = st.columns(2)
                has_selection = edited_df[' '].any()
                col_guardar, col_descargar, col_descargar_seleccionado, col_eliminar = st.columns(4)
                if rol_usuario == "Secretario (a)":
                    with col1:
                        descargar_pdf(edited_df, "mortalidad_materna", label="Descargar PDF")
                    with col3:
                        df_sel = edited_df[edited_df[' '] == True]
                        descargar_registros_seleccionados(edited_df, "mortalidad_materna")
                        descargar_pdf(df_sel, "mortalidad_materna_seleccionado", label="Descarga selección", disabled=not has_selection)
                else:
                    with col_guardar:
                        guadar_btn(procesar_guardado_cambios_mortalidad_materna, edited_df) 
                    with col_descargar:
                        descargar_pdf(edited_df, "mortalidad_materna")                
                    with col_descargar_seleccionado:
                        df_sel = edited_df[edited_df[' '] == True]
                        descargar_registros_seleccionados(edited_df, "mortalidad_materna")
                        descargar_pdf(df_sel, "mortalidad_materna_seleccionado", label="Descarga selección", disabled=not has_selection)
                    with col_eliminar:
                        btn_eliminar = st.button("Eliminar", icon=":material/delete:", key="delete_mortalidad_materna", 
                                                disabled=not has_selection, width="stretch",
                                                help="Eliminar registros seleccionados.")
                        if btn_eliminar:
                            confirmar_eliminar(eliminar_registros_materna, edited_df)

    if rol_usuario != "Secretario (a)":
        st.subheader(":material/new_label: Registrar Muerte Materna", anchor=False)
        with st.form("form_materna"):
            fecha_minima = datetime.date.today() - relativedelta(months=1)
            fecha_maxima = datetime.date.today() + relativedelta(months=1)
            fecha_maxima_hoy = datetime.date.today()
            fecha_minimi_1935 = datetime.date(1935, 1, 1)
            col_hc, col_nombres = st.columns(2)
            with col_hc:
                historia_clinica = st.text_input("Historia clínica", max_chars=8, key="historia_clinica_materna", placeholder="Ej. 12345678")
            with col_nombres:
                nombres_apellidos = st.text_input("Nombres y apellidos", max_chars=40, key="nombres_apellidos_materna", placeholder="Ej. Juan Pérez")
            col_fecha_nacimiento, col_fecha_ingreso, col_hora_ingreso, col_fecha_defuncion = st.columns(4)
            with col_fecha_nacimiento:
                fecha_nacimiento = st.date_input("Fecha de nacimiento", format=DATE_FORMAT, min_value=fecha_minimi_1935, 
                                                max_value=fecha_maxima_hoy, key="fecha_nacimiento_materna")
            with col_fecha_ingreso:
                fecha_ingreso = st.date_input("Fecha de ingreso", format=DATE_FORMAT, min_value=fecha_minima, 
                                              max_value=fecha_maxima, key="fecha_ingreso_materna")
            with col_hora_ingreso:
                hora_ingreso = st.time_input("Hora de ingreso", key="hora_ingreso_materna", value=datetime.datetime.now().time())
            with col_fecha_defuncion:
                fecha_defuncion = st.date_input("Fecha de defunción", format="DD/MM/YYYY", min_value=fecha_minimi_1935, 
                                                max_value=fecha_maxima_hoy, key="fecha_defuncion_materna")
            col_hora_defuncion, col_edad, col_tiempo = st.columns(3)
            with col_hora_defuncion:
                hora_defuncion = st.time_input("Hora de defunción", key="hora_defuncion_materna", value=datetime.datetime.now().time())
            with col_edad:
                edad = st.number_input("Edad", min_value=0, step=1, key="edad_materna")
            with col_tiempo:
                tiempo = st.selectbox("Tiempo de edad", ["Años"], key="tiempo_materna")
            edad_junto = f"{edad} {tiempo}"
            col1, col2 = st.columns(2)
            with col1:
                idx_ingreso = st.text_area("IDX de ingreso", max_chars=150, key="idx_ingreso_materna", placeholder="Descripción de la IDX de ingreso")
            with col2:
                idx_defuncion = st.text_area("IDX de defunción", max_chars=150, key="idx_defuncion_materna", placeholder="Descripción de la IDX de defuncion")
            st.markdown("**Dirección**")
            col_pais, col_estado, col_muni = st.columns(3)
            with col_pais:
                pais_hogar = st.text_input("País", max_chars=56, key="pais_hogar_materna", placeholder="Venezuela")
            with col_estado:
                estado_hogar = st.text_input("Estado", max_chars=56, key="estado_hogar_materna", placeholder="Anzoátegui")
            with col_muni:
                municipio_hogar = st.text_input("Municipio (Opcional)", max_chars=56, key="municipio_hogar_materna", placeholder="Simón Rodríguez")
            col_parroquia, col_city = st.columns(2)
            with col_parroquia:
                parroquia_hogar = st.text_input("Parroquia", max_chars=56, key="parroquia_hogar_materna", placeholder="Edmundo Barrios (zona norte)")
            with col_city:
                ciudad_hogar = st.text_input("Ciudad", max_chars=56, key="ciudad_hogar_materna", placeholder="El Tigre")
            direccion_exacta_hogar = st.text_area("Dirección Exacta", max_chars=150, key="direccion_exacta_hogar_materna", placeholder="Pueblo Nuevo Norte, 3ra Carrera Norte, Número 26")
            col_reg, col_limp = st.columns([30, 1])
            with col_reg:
                registrar = st.form_submit_button("Registrar", icon=":material/save:", type="primary")
            with col_limp:
                limpiar = st.form_submit_button("", icon=":material/cleaning_services:", on_click=limpiar_campos_materna, 
                                                type="tertiary", help="Limpia todos los campos del formulario.")  
            if registrar:
                fecha_formateada_nacimiento = fecha_nacimiento.strftime("%d/%m/%Y")
                fecha_formateada_ingreso = fecha_ingreso.strftime("%d/%m/%Y")
                fecha_formateada_defuncion = fecha_defuncion.strftime("%d/%m/%Y")
                hora_ingreso_str = hora_ingreso.strftime("%H:%M:%S") if isinstance(hora_ingreso, datetime.time) else str(hora_ingreso) if hora_ingreso else ""
                hora_defuncion_str = hora_defuncion.strftime("%H:%M:%S") if isinstance(hora_defuncion, datetime.time) else str(hora_defuncion) if hora_defuncion else ""
                datos_registro = (
                    historia_clinica, nombres_apellidos, fecha_formateada_nacimiento, fecha_formateada_ingreso, hora_ingreso_str,
                    fecha_formateada_defuncion, hora_defuncion_str, edad_junto, idx_ingreso, idx_defuncion,
                    pais_hogar, estado_hogar, municipio_hogar, parroquia_hogar, ciudad_hogar,
                    direccion_exacta_hogar, id_doctor, id_administrador
                )
                if not all([historia_clinica, nombres_apellidos, fecha_nacimiento, pais_hogar, 
                            estado_hogar, parroquia_hogar, ciudad_hogar, direccion_exacta_hogar, 
                            idx_ingreso, idx_defuncion]):
                    st.error("Por favor completa todos los campos", icon=":material/error:")
                    return
                elif not val_num_espacios(historia_clinica, "La", "historia clinica"):
                    return
                elif not validar_texto(nombres_apellidos, "Los", "nombres y apellidos"):
                    return
                elif not validar_cinco_espacios(nombres_apellidos, "Los", "nombres y apellidos"):
                    return
                elif not val_notas(idx_ingreso, "La", "IDX de ingreso"):
                    return
                elif not val_notas(idx_defuncion, "La", "IDX de defuncion"):
                    return                
                elif not validar_pais(pais_hogar, "El", "pais del hogar"):
                    return
                elif not validar_pais(estado_hogar, "El", "estado del hogar"):
                    return
                elif not validar_pais(municipio_hogar, "El", "municipio del hogar"):
                    return
                elif not validar_pais(parroquia_hogar, "La", "parroquia del hogar"):
                    return
                elif not validar_pais(ciudad_hogar, "La", "cuidad del hogar"):
                    return
                elif not val_notas(direccion_exacta_hogar, "La", "direccion exacta del hogar"):
                    return
                else:
                    if operaciones_sql_materna("registrar", datos_registro=datos_registro):
                        st.success("Registro guardado.", icon=":material/check_circle:")
                        st.rerun()

def data_editor_mensual_infantil(df, rol_usuario):
    if " " not in df.columns:
        df.insert(0, " ", False)

    columnas_excluir = ["fecha_hora", "hora"]
    columns_to_display = [col for col in df.columns if col not in [" ", "id"] + columnas_excluir]

    columns_to_show = [" "] + columns_to_display + (["id"] if "id" in df.columns else [])
    df = df[columns_to_show]

    column_config = {
        " ": st.column_config.CheckboxColumn(" ", default=False, disabled=False),
        "fecha_registro_formulario": st.column_config.DateColumn("Fecha registro", format="DD/MM/YYYY", disabled=True),
        "total": st.column_config.NumberColumn("Total", disabled=True),
        "tasa": st.column_config.TextColumn("Tasa", disabled=True),
        "causas": st.column_config.TextColumn("Causas", disabled=True),
        "n_casos": st.column_config.NumberColumn("Número de casos", min_value=0, step=1, disabled=True),
        "id": st.column_config.TextColumn("ID", disabled=True),
    }

    for col in columns_to_show:
        if col not in column_config and col != " ":
            column_config[col] = st.column_config.TextColumn(col, disabled=True)

    edited_df = st.data_editor(
        df,
        hide_index=True,
        column_config=column_config,
        key="editor_mensual_infantil"
    )
    return edited_df

@st.fragment
def formulario_mensual_infantil(db=DB_PATH):
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

    st.subheader(":material/table: Datos de Mortalidad Mensual Infantil", anchor=False)
    df = operaciones_sql_mensual_infantil("cargar")
    if df is None:
        return

    if rol_usuario == "Secretario (a)":
        if df.empty:
            st.info("No hay datos para mostrar.", icon=":material/info:")
            st.markdown("# ")
    elif rol_usuario != "Secretario (a)":
        if df.empty:
            st.info("No hay datos para mostrar.", icon=":material/info:")
        else:
            mostrar_editor = st.toggle("Mostrar datos de registros", value=False, key="toggle_editor_im")

            if mostrar_editor:
                df_filtrado = filtrar_por_fechas(df, 'fecha_registro_formulario')
                edited_df = data_editor_mensual_infantil(df_filtrado, rol_usuario)
                col1, col3 = st.columns(2)
                has_selection = edited_df[' '].any()
                col_guardar, col_descargar, col_descargar_seleccionado, col_eliminar = st.columns(4)
                
                if rol_usuario == "Secretario (a)":
                    with col1:
                        descargar_pdf(edited_df, "mortalidad_mensual_infatil", label="Descargar PDF")
                    with col3:
                        df_sel = edited_df[edited_df[' '] == True]
                        descargar_registros_seleccionados(edited_df, "mortalidad_mensual_infatil")
                        descargar_pdf(df_sel, "mortalidad_mensual_infatil_seleccionado", label="Descarga selección", disabled=not has_selection)
                else:
                    with col_guardar:
                        guadar_btn(procesar_guardado_cambios_mensual_neonatal, edited_df, key_1="btn_guardar_morta_infantil_mensual") # completar_boton_aqui
                    with col_descargar:
                            descargar_pdf(edited_df, "mortalidad_mensual_infatil")               
                    with col_descargar_seleccionado:
                        df_sel = edited_df[edited_df[' '] == True]
                        descargar_registros_seleccionados(edited_df, "mortalidad_mensual_infatil")
                        descargar_pdf(df_sel, "mortalidad_mensual_infatil_seleccionado", label="Descarga selección", disabled=not has_selection)
                    with col_eliminar:
                        btn_eliminar = st.button("Eliminar", icon=":material/delete:", key="delete_mortalidad_mensual_infatil", 
                                                disabled=not has_selection, width="stretch",
                                                help="Eliminar registros seleccionados.")
                        if btn_eliminar:
                            confirmar_eliminar(eliminar_registros_mensual_infantil, edited_df)
                        #  eliminar_registros_mensual_infantil(edited_df)

    if rol_usuario != "Secretario (a)":
        col_izq, col_der = st.columns(2)
        with col_der:
            st.subheader(":material/percent: Tasa", anchor=False)

            # Obtener los años que tienen registros
            if not df.empty:
                df['anio'] = pd.to_datetime(df['fecha_registro_formulario']).dt.year
                years = sorted(df['anio'].unique())
            else:
                years = []

            if years:
                year_seleccionado = st.selectbox(
                    "Seleccionar año para tasa", 
                    options=years, 
                    index=len(years)-1, 
                    key="year_tasa_infantil"
                )
                tasa = calcular_tasa_por_ano_infantil(db, year_seleccionado)
                st.metric(label="Tasa de Registros", value=f"{tasa}%", delta=None)
            else:
                st.info("No hay años con registros para calcular tasas.", icon=":material/info:")      

        with col_izq:
            st.subheader(":material/new_label: Registrar Mortalidad Mensual Infantil", anchor=False)
            with st.form("form_mensual_infantil", width=531):
                causas = st.text_area("Causas", max_chars=150, key="causas_mensual_infantil", placeholder="Descripción de la causa")
                n_casos = st.number_input("Número de casos", min_value=0, step=1, key="n_casos_mensual_infantil")
                col_reg, col_limp = st.columns([14.5, 1])
                with col_reg:
                    registrar = st.form_submit_button("Registrar", icon=":material/save:", type="primary")
                with col_limp:
                    limpiar = st.form_submit_button("", icon=":material/cleaning_services:", 
                                                    on_click=limpiar_campos_mensual_infantil, type="tertiary",
                                                    help="Limpia todos los campos del formulario.")
                if registrar:
                    if not val_notas(causas, "La", "causa"):
                        return
                    elif n_casos == 0:
                        st.error("El número de casos debe ser mayor que cero.", icon=":material/error:")
                        return
                    else:
                        datos_registro = (causas, n_casos, id_doctor, id_administrador, rol_usuario)
                        if operaciones_sql_mensual_infantil("registrar", datos_registro=datos_registro):
                            st.success("Registro guardado.", icon=":material/check_circle:")
                            st.rerun()


def data_editor_mensual_neonatal(df, rol_usuario):
    if " " not in df.columns:
        df.insert(0, " ", False)

    columns_to_display = [col for col in df.columns if col not in [" ", "id"]]

    columns_to_show = [" "] + columns_to_display + (["id"] if "id" in df.columns else [])
    df = df[columns_to_show]

    column_config = {
        " ": st.column_config.CheckboxColumn(" ", default=False, disabled=False),
        "fecha_hora": st.column_config.DateColumn("Fecha registro", format="DD/MM/YYYY", disabled=True),
        "total": st.column_config.NumberColumn("Total", disabled=True),
        "tasa": st.column_config.TextColumn("Tasa", disabled=True),
        "causas": st.column_config.TextColumn("Causas", disabled=True),
        "n_casos": st.column_config.NumberColumn("Número de casos", min_value=0, step=1, disabled=True),
        "id": st.column_config.TextColumn("ID", disabled=True),
    }

    for col in columns_to_show:
        if col not in column_config and col != " ":
            column_config[col] = st.column_config.TextColumn(col, disabled=True)

    edited_df = st.data_editor(
        df,
        hide_index=True,
        column_config=column_config,
        key="editor_neonatal_mensual"
    )
    return edited_df

@st.fragment
def formulario_mensual_neonatal(db=DB_PATH):
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

    st.subheader(":material/table: Datos de Mortalidad Mensual Neonatal", anchor=False)
    df = operaciones_sql_mensual_neonatal("cargar")
    if df is None:
        return

    if rol_usuario == "Secretario (a)":
        if df.empty:
            st.info("No hay datos para mostrar.", icon=":material/info:")
            st.markdown("# ")
    elif rol_usuario != "Secretario (a)":
        if df.empty:
            st.info("No hay datos para mostrar.", icon=":material/info:")
        else:
            mostrar_editor = st.toggle("Mostrar datos de registros", value=False, key="toggle_editor_mn")

            if mostrar_editor:
                df_filtrado = filtrar_por_fechas(df, 'fecha_registro_formulario')
                edited_df = data_editor_mensual_neonatal(df_filtrado, rol_usuario)
                col1, col3 = st.columns(2)
                has_selection = edited_df[' '].any()
                col_guardar, col_descargar, col_descargar_seleccionado, col_eliminar = st.columns(4)
                if rol_usuario == "Secretario (a)":
                    with col1:
                        descargar_pdf(edited_df, "mortalidad_mensual_neonatal", label="Descargar PDF")
                    with col3:
                        df_sel = edited_df[edited_df[' '] == True]
                        descargar_registros_seleccionados(edited_df, "mortalidad_mensual_neonatal")
                        descargar_pdf(df_sel, "mortalidad_mensual_neonatal_seleccionado", label="Descarga selección", disabled=not has_selection)
                else:
                    with col_guardar:
                        guadar_btn(procesar_guardado_cambios_mensual_infantil, edited_df, key_1="btn_guardar_morta_neo_mensual") # completar_boton_aqui
                    with col_descargar:
                            descargar_pdf(edited_df, "mortalidad_mensual_neonatal")                
                    with col_descargar_seleccionado:
                        df_sel = edited_df[edited_df[' '] == True]
                        descargar_registros_seleccionados(edited_df, "mortalidad_mensual_neonatal")
                        descargar_pdf(df_sel, "mortalidad_mensual_neonatal_seleccionado", label="Descarga selección", disabled=not has_selection)
                    with col_eliminar:
                        btn_eliminar = st.button("Eliminar", icon=":material/delete:", key="mortalidad_mensual_neonatal", 
                                                disabled=not has_selection, width="stretch",
                                                help="Eliminar registros seleccionados.")
                        if btn_eliminar:
                            confirmar_eliminar(eliminar_registros_mensual_infantil, edited_df)
                        # eliminar_registros_mensual_infantil(edited_df)

    if rol_usuario != "Secretario (a)":
        col_izq, col_der = st.columns(2)
        with col_der:
            st.subheader(":material/percent: Tasa", anchor=False)

            # Obtener los años que realmente tienen registros
            if not df.empty:
                df['anio'] = pd.to_datetime(df['fecha_hora']).dt.year
                years = sorted(df['anio'].unique())
            else:
                years = []

            if years:
                year_seleccionado = st.selectbox(
                    "Seleccionar año para tasa",
                    options=years,
                    index=len(years)-1,
                    key="year_tasa_neonatal"
                )
                tasa = calcular_tasa_por_ano_neonatal(db, year_seleccionado)
                st.metric(label="Tasa de Registros", value=f"{tasa}%", delta=None)
            else:
                st.info("No hay años con registros para calcular tasas.", icon=":material/info:")
        
        with col_izq:
            st.subheader(":material/new_label: Registrar Mortalidad Mensual Neonatal", anchor=False)
            with st.form("form_mensual_neonatal", width=531):
                causas = st.text_area("Causas", max_chars=150, key="causas_mensual_neonatal", placeholder="Descripción de la causa")
                n_casos = st.number_input("Número de casos", min_value=0, step=1, key="n_casos_mensual_neonatal")
                col_reg, col_limp = st.columns([14.5, 1])
                with col_reg:
                    registrar = st.form_submit_button("Registrar", icon=":material/save:", type="primary")
                with col_limp:
                    limpiar = st.form_submit_button("", icon=":material/cleaning_services:", 
                                                    on_click=limpiar_campos_mensual_neonatal, type="tertiary",
                                                    help="Limpia todos los campos del formulario.")
                if registrar:
                    if not val_notas(causas, "La", "causa"):
                        return
                    elif n_casos == 0:
                        st.error("El número de casos debe ser mayor que cero.", icon=":material/error:")
                        return
                    else:
                        datos_registro = (causas, n_casos, id_doctor, id_administrador, rol_usuario)
                        if operaciones_sql_mensual_neonatal("registrar", datos_registro=datos_registro):
                            st.success("Registro guardado.", icon=":material/check_circle:")
                            st.rerun()

def data_editor_mensual_general(df, rol_usuario):
    if " " not in df.columns:
        df.insert(0, " ", False)

    columns_to_display = [col for col in df.columns if col not in [" ", "id"]]

    columns_to_show = [" "] + columns_to_display + (["id"] if "id" in df.columns else [])
    df = df[columns_to_show]

    column_config = {
        " ": st.column_config.CheckboxColumn(" ", default=False, disabled=False),
        "fecha_hora": st.column_config.DateColumn("Fecha registro", format="DD/MM/YYYY", disabled=True),
        "total": st.column_config.NumberColumn("Total", disabled=True),
        "tasa": st.column_config.TextColumn("Tasa", disabled=True),
        "causas": st.column_config.TextColumn("Causas", disabled=True),
        "n_casos": st.column_config.NumberColumn("Número de casos", min_value=0, step=1, disabled=True),
        "id": st.column_config.TextColumn("ID", disabled=True),
    }

    for col in columns_to_show:
        if col not in column_config and col != " ":
            column_config[col] = st.column_config.TextColumn(col, disabled=True)

    edited_df = st.data_editor(
        df,
        hide_index=True,
        column_config=column_config,
        key="editor_general_mensual"
    )
    return edited_df

@st.fragment
def formulario_mensual_general(db=DB_PATH):
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

    st.subheader(":material/table: Datos de Mortalidad Mensual General", anchor=False)
    df = operaciones_sql_mensual_general("cargar")
    if df is None:
        return

    if rol_usuario == "Secretario (a)":
        if df.empty:
            st.info("No hay datos para mostrar.", icon=":material/info:")
            st.markdown("# ")
    elif rol_usuario != "Secretario (a)":
        if df.empty:
            st.info("No hay datos para mostrar.", icon=":material/info:")
        else:
            mostrar_editor = st.toggle("Mostrar datos de registros", value=False, key="toggle_editor_mg")

            if mostrar_editor:
                df_filtrado = filtrar_por_fechas(df, 'fecha_hora' )
                edited_df = data_editor_mensual_general(df_filtrado, rol_usuario)
                col1, col3 = st.columns(2)
                has_selection = edited_df[' '].any()
                col_guardar, col_descargar, col_descargar_seleccionado, col_eliminar = st.columns(4)
                if rol_usuario == "Secretario (a)":
                    with col1:
                        descargar_pdf(edited_df, "mortalidad_mensual_general", label="Descargar PDF")
                    with col3:
                        df_sel = edited_df[edited_df[' '] == True]
                        descargar_registros_seleccionados(edited_df, "mortalidad_mensual_general")
                        descargar_pdf(df_sel, "mortalidad_mensual_general_seleccionado", label="Descarga selección", disabled=not has_selection)
                else:
                    with col_guardar:
                        guadar_btn(procesar_guardado_cambios_mensual_general, edited_df,key_1="btn_guardar_morta_gen_mensual") # completar_boton_aqui
                    with col_descargar:
                        descargar_pdf(edited_df, "mortalidad_mensual_general")                
                    with col_descargar_seleccionado:
                        df_sel = edited_df[edited_df[' '] == True]
                        descargar_registros_seleccionados(edited_df, "mortalidad_mensual_general")
                        descargar_pdf(df_sel, "mortalidad_mensual_general_seleccionado", label="Descarga selección", disabled=not has_selection)
                    with col_eliminar:
                        btn_eliminar = st.button("Eliminar", icon=":material/delete:", key="mortalidad_mensual_general", 
                                                disabled=not has_selection, width="stretch",
                                                help="Eliminar registros seleccionados.")
                        if btn_eliminar:
                            confirmar_eliminar(eliminar_registros_mensual_general, edited_df)
                            #eliminar_registros_mensual_general(edited_df)

    if rol_usuario != "Secretario (a)":
        col_izq, col_der = st.columns(2)
        with col_der:
            st.subheader(":material/percent: Tasa", anchor=False)

            if not df.empty:
                df['anio'] = pd.to_datetime(df['fecha_hora']).dt.year
                years = sorted(df['anio'].unique())
            else:
                years = []

            if years:
                year_seleccionado = st.selectbox(
                    "Seleccionar año para tasa",
                    options=years,
                    index=len(years) - 1,
                    key="year_tasa_neonatal"
                )
                tasa = calcular_tasa_por_ano_neonatal(db, year_seleccionado)
                st.metric(label="Tasa de Registros", value=f"{tasa}%", delta=None)
            else:
                st.info("No hay años con registros para calcular tasas.", icon=":material/info:")

        with col_izq:
            st.subheader(":material/new_label: Registrar Mortalidad Mensual General", anchor=False)
            with st.form("form_mensual_general", width=531):
                causas = st.text_area("Causas", max_chars=150, key="causas_mensual_general", placeholder="Descripción de la causa")
                n_casos = st.number_input("Número de casos", min_value=0, step=1, key="n_casos_mensual_general")
                col_reg, col_limp = st.columns([14.5, 1])
                with col_reg:
                    registrar = st.form_submit_button("Registrar", icon=":material/save:", type="primary")
                with col_limp:
                    limpiar = st.form_submit_button("", icon=":material/cleaning_services:", 
                                                    on_click=limpiar_campos_mensual_general, type="tertiary",
                                                    help="Limpia todos los campos del formulario.")
                if registrar:
                    if not val_notas(causas, "La", "causa"):
                        return
                    elif n_casos == 0:
                        st.error("El número de casos debe ser mayor que cero.", icon=":material/error:")
                        return
                    else:
                        datos_registro = (causas, n_casos, id_doctor, id_administrador, rol_usuario)
                        if operaciones_sql_mensual_general("registrar", datos_registro=datos_registro):
                            st.success("Registro guardado.", icon=":material/check_circle:")
                            st.rerun()
            

def mostrar_morta():
    logo_bandera = ASSETS_DIR / "imagebanderanueva2.png"
    logo_base64 = img_a_base64(logo_bandera)
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) 
    menu()
    logo(tamano="100%")
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a este formulario.", icon=":material/error:")
        return
    tab1, tab2, tab3 = st.tabs(["| :material/skull: Mortalidad |", 
                                "| :material/skull_list: Mortalidad Mensual |", 
                                "| :material/article_shortcut: Reporte General |"])
    with tab1:
        tipo_muerte = st.selectbox(
            ":material/gesture_select: Selecciona el tipo de registro:",
            options=["Muerte Neonatal", "Muerte Infantil", "Muerte Materna"],
            key="tipo_muerte_normal"
        )
        formularios_normales = {
            "Muerte Neonatal": formulario_neonatal,
            "Muerte Infantil": formulario_infantil,
            "Muerte Materna": formulario_materna
        }
        func_normal = formularios_normales.get(tipo_muerte)
        if func_normal:
            func_normal()
    with tab2:
        tipo_muerte_mensual = st.selectbox(
            ":material/gesture_select: Selecciona el tipo de registro:",
            options=["Mortalidad Mensual Infantil", "Mortalidad Mensual Neonatal", "Mortalidad Mensual General"],
            key="tipo_muerte_mensual"
        )
        formularios_mensuales = {
            "Mortalidad Mensual Infantil": formulario_mensual_infantil,
            "Mortalidad Mensual Neonatal": formulario_mensual_neonatal,
            "Mortalidad Mensual General": formulario_mensual_general
        }
        func_mensual = formularios_mensuales.get(tipo_muerte_mensual)
        if func_mensual:
            func_mensual()
    with tab3:
        st.subheader(":material/arrow_circle_down: Descargas de reportes", anchor=False, divider="gray")
        col_izq, col_centro, col_der = st.columns([3.35, 4, 2.65])
        with col_izq:
            formulario_reporte_general()
        #st.markdown("---")
        with col_centro:
            formulario_reporte_mensual_combinado()
        #st.markdown("---")
        with col_der:
            formulario_reporte_mensual_general()
        st.markdown("")
    copyright_footer_dos("Equipo Investigador", bottom="-200px")
        
mostrar_morta()