import streamlit as st
import pandas as pd
import datetime
import time
import os
import base64
from descargas.descarga_natalidad import _exportar_pdf_natalidad
from descargas.descarga_morbilidad import exportar_pdf_morbilidad_extensa
from descargas.descarga_mortalidad import _exportar_pdf_mortalidad
from pages.historial import registrar_actividad_duradera

DB_PATH = os.getenv("hospital.db", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'

MESES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

def filtrar_por_fechas(df, columna_fecha='fecha_registro_formulario'):
    if columna_fecha is None or columna_fecha not in df.columns:
        return df
    try:
        # Pre-procesar fechas
        df[columna_fecha] = pd.to_datetime(df[columna_fecha], dayfirst=True, errors='coerce')
        if df[columna_fecha].isna().all():
            return df
        
        # Obtener años y fechas límites
        min_f = df[columna_fecha].min().date()
        max_f = df[columna_fecha].max().date()
        anios_disponibles = sorted(df[columna_fecha].dt.year.dropna().unique().astype(int).tolist(), reverse=True)
        
        if not anios_disponibles:
            return df

        modo = st.selectbox(
            ":material/calendar_view_month: Seleccionar período",
            ["Todo", "Año", "Mes y Año", "Fecha Específica", "Rango de Fechas"],
            index=0,
            key=f"modo_filtro_{columna_fecha}"
        )

        if modo == "Todo":
            return df

        elif modo == "Año":
            anio_sel = st.selectbox(":material/calendar_today: Año", options=anios_disponibles, key=f"anio_solo_{columna_fecha}")
            return df[df[columna_fecha].dt.year == anio_sel]

        elif modo == "Mes y Año":
            col1, col2 = st.columns(2)
            with col1:
                anio_sel = st.selectbox(":material/calendar_today: Año", options=anios_disponibles, key=f"anio_mes_{columna_fecha}")
            
            df_anio = df[df[columna_fecha].dt.year == anio_sel]
            meses_dis_num = sorted(df_anio[columna_fecha].dt.month.dropna().unique().astype(int).tolist())
            meses_opt = [MESES_ES[m] for m in meses_dis_num]
            
            with col2:
                meses_sel = st.multiselect(":material/calendar_month: Mes(es)", options=meses_opt, placeholder="Todos los meses", key=f"meses_sel_{columna_fecha}")
            
            if meses_sel:
                m_nums = [k for k, v in MESES_ES.items() if v in meses_sel]
                return df_anio[df_anio[columna_fecha].dt.month.isin(m_nums)]
            return df_anio

        elif modo == "Fecha Específica":
            f_esp = st.date_input(":material/event: Fecha", value=max_f, min_value=min_f, max_value=max_f, format="DD/MM/YYYY", key=f"f_esp_{columna_fecha}")
            return df[df[columna_fecha].dt.date == f_esp]

        elif modo == "Rango de Fechas":
            c1, c2 = st.columns(2)
            with c1:
                f_ini = st.date_input(":material/date_range: Fecha Inicio", value=min_f, min_value=min_f, max_value=max_f, format="DD/MM/YYYY", key=f"f_ini_{columna_fecha}")
            with c2:
                f_fin = st.date_input(":material/date_range: Fecha Fin", value=max_f, min_value=min_f, max_value=max_f, format="DD/MM/YYYY", key=f"f_fin_{columna_fecha}")
            
            if f_fin < f_ini:
                st.error("La fecha fin debe ser posterior a la inicio.")
                return df
            
            return df[
                (df[columna_fecha].dt.date >= f_ini) & 
                (df[columna_fecha].dt.date <= f_fin)
            ]

        return df

    except Exception as e:
        st.error(f"Error al filtrar por fechas: {e}", icon=":material/error:")
        return df

from utils.filtro_categorias import (
    filtro_categorias_natalidad, 
    filtro_muerte_neonatal, 
    filtro_muerte_infantil, 
    filtro_muerte_materna, 
    filtro_morbilidad
)

def filtrar_datos_completos(df, tipo_reporte, columna_fecha='fecha_registro_formulario'):
    """
    Función unificada que maneja filtros por fecha (Año/Mes) y filtros por categoría (cascading).
    """
    if df.empty:
        if tipo_reporte == 'natalidad':
             return df, []
        return df

    # 1. Filtro por Fecha (Contenedor principal)
    with st.container():
        df_fechas = filtrar_por_fechas(df, columna_fecha)
        
        # 2. Filtro por Categorías (usando el resultado de las fechas para cascading)
        if tipo_reporte == 'natalidad':
            return filtro_categorias_natalidad(df_fechas)
        elif tipo_reporte == 'mortalidad_neonatal':
            return filtro_muerte_neonatal(df_fechas)
        elif tipo_reporte == 'mortalidad_infantil':
            return filtro_muerte_infantil(df_fechas)
        elif tipo_reporte == 'mortalidad_materna':
            return filtro_muerte_materna(df_fechas)
        elif tipo_reporte == 'morbilidad_extensa':
            return filtro_morbilidad(df_fechas)
        else:
            return df_fechas

def obtener_area(nombre_base):
    if nombre_base.lower() in ["natalidad", "natalidad_seleccionado"]:
        return "Natalidad"
    elif nombre_base.lower() in ["morbilidad_extensa", "morbilidad_extensa_seleccionado"]:
        return "Denuncias Obligatorias"
    elif nombre_base.lower().startswith("mortalidad_neonatal"):
        return "Mortalidad Neonatal"
    elif nombre_base.lower().startswith("mortalidad_infantil"):
        return "Mortalidad Infantil"
    elif nombre_base.lower().startswith("mortalidad_materna"):
        return "Mortalidad Materna"
    return nombre_base.capitalize()

def generar_pdf_segun_tipo(df, nombre_base):
    if df.empty: return None
    
    nm_lower = nombre_base.lower()
    if nm_lower in ["natalidad", "natalidad_seleccionado", "natalidad_general"]:
        from descargas.descarga_natalidad import _exportar_pdf_natalidad
        return _exportar_pdf_natalidad(df, nombre_base)
    elif nm_lower in ["morbilidad_extensa", "morbilidad_extensa_seleccionado", "morbilidad"]:
        from descargas.descarga_morbilidad import exportar_pdf_morbilidad_extensa
        return exportar_pdf_morbilidad_extensa(df, "denuncias obligatorias" if "extensa" in nm_lower else "Morbilidad")
    elif "mortalidad_neonatal" in nm_lower:
        from descargas.descarga_mortalidad import _exportar_pdf_mortalidad
        return _exportar_pdf_mortalidad(df, nombre_base)
    elif "mortalidad_infantil" in nm_lower:
        from descargas.descarga_mortalidad import _exportar_pdf_mortalidad
        return _exportar_pdf_mortalidad(df, nombre_base)
    elif "mortalidad_materna" in nm_lower:
        from descargas.descarga_mortalidad import _exportar_pdf_mortalidad
        return _exportar_pdf_mortalidad(df, nombre_base)
    elif nm_lower == "mortalidad_general":
        from reportes.morta_general import exportar_pdf_mortalidad_general_df
        return exportar_pdf_mortalidad_general_df(df)
    return None

def descargar_pdf(df, nombre_base="datos", label="Descargar PDF", disabled=False):
    # from utils.botones import bloquear_botones

    
    key = f"btn_descarga_{nombre_base}_{abs(hash(str(df.index)))}"
    
    # Combinar el estado de deshabilitado pasado
    is_disabled = disabled or df.empty
    
    btn = st.button(label=label, icon=":material/download:", 
                    disabled=is_disabled, 
                    use_container_width=True, key=key, 
                    type="primary" if label == "Descargar Reporte" else "secondary")
    
def generar_nombre_archivo_pdf(nombre_base):
    area_descargada = obtener_area(nombre_base)
    fecha_actual = datetime.datetime.now()
    fecha_str = fecha_actual.strftime("%Y-%m-%d")
    hora_str = fecha_actual.strftime("%I-%M-%S")
    meridiano = "PM" if fecha_actual.hour >= 12 else "AM"
    return f"{area_descargada}_{fecha_str}_{hora_str}_{meridiano}.pdf"

def ejecutar_descarga_pdf(content, nombre_archivo, area_descargada):
    b64 = base64.b64encode(content).decode()
    js = f"""
        <script>
        const link = window.parent.document.createElement('a');
        link.href = 'data:application/pdf;base64,{b64}';
        link.download = '{nombre_archivo}';
        link.click();
        </script>
    """
    st.components.v1.html(js, height=0)
    registrar_actividad_duradera("DESCARGA PDF", f"Reportes {area_descargada}")
    time.sleep(1)
    st.rerun()

def descargar_pdf_desde_buffer(content, nombre_base, label="Descargar PDF", key=None):
    if not content:
        st.error("No hay contenido para descargar.")
        return

    if st.button(label=label, icon=":material/download:", use_container_width=True, key=key, type="primary"):
        nombre_archivo = generar_nombre_archivo_pdf(nombre_base)
        area_descargada = obtener_area(nombre_base)
        ejecutar_descarga_pdf(content, nombre_archivo, area_descargada)

def descargar_pdf(df, nombre_base="datos", label="Descargar PDF", disabled=False):
    key = f"btn_descarga_{nombre_base}_{abs(hash(str(df.index)))}"
    is_disabled = disabled or df.empty
    
    if st.button(label=label, icon=":material/download:", 
                    disabled=is_disabled, 
                    use_container_width=True, key=key, 
                    type="primary" if label == "Descargar Reporte" else "secondary"):
        
        output = generar_pdf_segun_tipo(df, nombre_base)
        if output:
            content = output.getvalue() if hasattr(output, "getvalue") else output
            nombre_archivo = generar_nombre_archivo_pdf(nombre_base)
            area_descargada = obtener_area(nombre_base)
            ejecutar_descarga_pdf(content, nombre_archivo, area_descargada)
        else:
            st.error("No se pudo generar el PDF.")
            st.rerun()

def ver_pdf(df, nombre_base="datos", key_btn=None, disabled=False):
    # from utils.botones import bloquear_botones
    
    key = key_btn if key_btn else f"btn_ver_{nombre_base}_{abs(hash(str(df.index)))}"
    is_disabled = disabled or df.empty
    
    btn = st.button("Ver reporte", icon=":material/visibility:", width="stretch", 
                    type="primary", key=key, 
                    disabled=is_disabled)
    
    if btn:
            output = generar_pdf_segun_tipo(df, nombre_base)
            
            if output:
                content = output.getvalue() if hasattr(output, "getvalue") else output
                st.session_state["pdf_buffer"] = content
                st.session_state["pdf_nombre_base"] = nombre_base
                st.switch_page("pages/ver_reportes.py")
            else:
                st.error("No se pudo generar el reporte.")
                st.rerun()  # Reactivar botón si falla

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
