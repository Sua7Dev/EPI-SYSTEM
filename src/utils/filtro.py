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

def filtrar_por_fechas(df, columna_fecha='fecha_registro_formulario'):

    if columna_fecha is None or columna_fecha not in df.columns:
        return df
    try:
        df[columna_fecha] = pd.to_datetime(df[columna_fecha], dayfirst=True, errors='coerce')
        if df[columna_fecha].isna().all():
            return df
        st.subheader(":material/calendar_clock: Filtrar por Fechas", anchor=False)
        
       
        fecha_min_datos = df[columna_fecha].min().date() if not df.empty else datetime.date.today()
        fecha_max_datos = df[columna_fecha].max().date() if not df.empty else datetime.date.today()
        fecha_min = datetime.date(2000, 1, 1)
        fecha_max = datetime.date.today()
        
        col1, col2 = st.columns(2)
        with col1:
            fecha_inicio = st.date_input(
                ":material/date_range: Fecha de Inicio",
                value=fecha_min_datos,
                min_value=fecha_min_datos,
                max_value=fecha_max,
                format=DATE_FORMAT,
                key=f"fecha_inicio_filtro_{columna_fecha}"
            )
        with col2:
            fecha_fin = st.date_input(
                ":material/date_range: Fecha de Fin",
                value=fecha_max_datos,
                min_value=fecha_min_datos,
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
    
    if btn:
            output = generar_pdf_segun_tipo(df, nombre_base)
            # Resetear estado después de generar
            
            if output:
                # Ensure we have raw bytes
                content = output.getvalue() if hasattr(output, "getvalue") else output
                
                area_descargada = obtener_area(nombre_base)
                fecha_actual = datetime.datetime.now()
                fecha_str = fecha_actual.strftime("%d-%m-%Y")
                hora_str = fecha_actual.strftime("%I-%M-%S")
                meridiano = "PM" if fecha_actual.hour >= 12 else "AM"
                nombre_archivo = f"{area_descargada}_{fecha_str}_{hora_str}_{meridiano}.pdf"
                
                b64 = base64.b64encode(content).decode()
                # JS trigger for download
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
                st.rerun()  # Reactivar botón después de descarga
                
            else:
                st.error("No se pudo generar el PDF.")
                st.rerun()  # Reactivar botón incluso si falla

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
