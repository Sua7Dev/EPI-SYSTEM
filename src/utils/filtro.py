import streamlit as st
import pandas as pd
import datetime
import os
from descargas.descarga_natalidad import _exportar_pdf_natalidad
from descargas.descarga_epi14 import _exportar_pdf_epi14
from descargas.descarga_morbilidad import exportar_pdf_morbilidad_extensa, exportar_pdf_morbilidad_simp
from descargas.descarga_mortalidad import _exportar_pdf_mortalidad, _exportar_pdf_mortalidad_mensual
from descargas.descarga_reg_diario import _exportar_pdf

DB_PATH = os.environ.get("AUTH_DB_PATH", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'

def filtrar_por_fechas(df, columna_fecha='fecha_registro_formulario'):

    if columna_fecha is None or columna_fecha not in df.columns:
        return df
    try:
        df[columna_fecha] = pd.to_datetime(df[columna_fecha], errors='coerce')
        if df[columna_fecha].isna().all():
            return df
        st.subheader(":material/calendar_clock: Filtrar por Fechas", anchor=False)
        
       
        fecha_min_datos = df[columna_fecha].min().date() if not df.empty else datetime.date(2000, 1, 1)
        fecha_max_datos = df[columna_fecha].max().date() if not df.empty else datetime.date(2050, 12, 31)
        fecha_min = datetime.date(2000, 1, 1)
        fecha_max = datetime.date(2050, 12, 31)
        
        col1, col2 = st.columns(2)
        with col1:
            fecha_inicio = st.date_input(
                ":material/date_range: Fecha de Inicio",
                value=fecha_min_datos,
                min_value=fecha_min,
                max_value=fecha_max,
                format=DATE_FORMAT,
                key=f"fecha_inicio_filtro_{columna_fecha}"
            )
        with col2:
            fecha_fin = st.date_input(
                ":material/date_range: Fecha de Fin",
                value=fecha_max_datos,
                min_value=fecha_min,
                max_value=fecha_max,
                format=DATE_FORMAT,
                key=f"fecha_fin_filtro_{columna_fecha}"
            )
        
        if fecha_inicio and fecha_fin:
            return df[
                (df[columna_fecha] >= pd.Timestamp(fecha_inicio)) &
                (df[columna_fecha] <= pd.Timestamp(fecha_fin) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))
            ]
        return df
    except Exception as e:
        st.error(f"Error al filtrar por fechas: {e}", icon=":material/error:")
        return df

### esta se queda aqui
def descargar_pdf(df, nombre_base="datos", label="Descargar PDF", disabled=False):
    fecha_actual = datetime.datetime.now()
    fecha_str = fecha_actual.strftime("%d-%m-%Y")
    hora_str = fecha_actual.strftime("%I-%M-%S")  
    meridiano = "PM" if fecha_actual.hour >= 12 else "AM"
    fecha_hora_str = f"{fecha_str}_{hora_str}_{meridiano}"

    output = None
    area_descargada = None

    if not df.empty:
        if nombre_base.lower() in ["epi14_semanal", "epi14_semanal_seleccionado"]:
            output = _exportar_pdf_epi14(df, nombre_base)
            area_descargada = "Epi14_Semanal"
        elif nombre_base.lower() in ["natalidad", "natalidad_seleccionado"]:
            output = _exportar_pdf_natalidad(df, nombre_base)
            area_descargada = "Natalidad"
        elif nombre_base.lower() in ["registro_diario", "registro_diario_seleccionado"]:
            output = _exportar_pdf(df, nombre_base)
            area_descargada = "Registro_Diario"
        elif nombre_base.lower() in ["morbilidad_extensa", "morbilidad_extensa_seleccionado"]:
            output = exportar_pdf_morbilidad_extensa(df, nombre_base)
            area_descargada = "Morbilidad_Extensa"
        elif nombre_base.lower() in ["morbilidad_simplificada", "morbilidad_simplificada_seleccionado"]:
            output = exportar_pdf_morbilidad_simp(df, nombre_base)
            area_descargada = "Morbilidad_Simplificada"
        elif nombre_base.lower() in ["mortalidad_neonatal", "mortalidad_neonatal_seleccionado"]:
            output = _exportar_pdf_mortalidad(df, nombre_base)
            area_descargada = "Mortalidad_Neonatal"
        elif nombre_base.lower() in ["mortalidad_infantil", "mortalidad_infantil_seleccionado"]:
            output = _exportar_pdf_mortalidad(df, nombre_base)
            area_descargada = "Mortalidad_Infantil"
        elif nombre_base.lower() in ["mortalidad_materna", "mortalidad_materna_seleccionado"]:
            output = _exportar_pdf_mortalidad(df, nombre_base)
            area_descargada = "Mortalidad_Materna"
        elif nombre_base.lower() in ["mortalidad_mensual_infatil", "mortalidad_mensual_infatil_seleccionado",
                                     "mortalidad_mensual_neonatal", "mortalidad_mensual_neonatal_seleccionado",
                                     "mortalidad_mensual_general", "mortalidad_mensual_general_seleccionado"]:
            output = _exportar_pdf_mortalidad_mensual(df, nombre_base)
            area_descargada = "Mortalidad_Mensual"

    if not area_descargada:
        area_descargada = nombre_base.capitalize()

    nombre_archivo = f"{area_descargada}_{fecha_hora_str}.pdf"

    st.download_button(
        label=label,
        data=output if output else b"",
        file_name=nombre_archivo,
        mime="application/pdf",
        icon=":material/download:",
        key=f"download{nombre_base}_{fecha_hora_str}",
        disabled=disabled,
        use_container_width=True
    )


def detectar_columna_id(df):
    posibles = [col for col in df.columns if (col.lower().startswith("id") or col.lower().endswith("_id") or col.lower() == "hc") and col != " "]
    if posibles:
        return next((col for col in posibles if col.lower() in ["id", "hc"]), posibles[0])
    for col in df.columns:
        if col != " " and pd.api.types.is_integer_dtype(df[col]) and df[col].is_unique:
            return col
    return None

def descargar_registros_seleccionados(df, tabla):
    if ' ' not in df.columns:
        return None
    id_col = detectar_columna_id(df)
    if not id_col:
        return None
    seleccionados = df[df[' '] == True]
    if seleccionados.empty:
        return None
    return seleccionados[id_col].tolist()
