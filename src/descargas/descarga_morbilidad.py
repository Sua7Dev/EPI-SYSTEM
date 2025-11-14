import streamlit as st
import pandas as pd
import datetime
import os
from io import BytesIO
from utils.pdfbanners import CustomPDF

DB_PATH = os.getenv("hospital.db", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'

def limpiar_dato(valor):
    """Filtra valores no válidos (No disponible, NaN, vacíos, None)."""
    if pd.isna(valor):
        return None
    if isinstance(valor, str):
        if valor.strip().lower() in ["", "nan", "none", "no disponible", "No disponible"]:
            return None
    return str(valor).strip()

def exportar_pdf_morbilidad_extensa(df, nombre_archivo):
    if df.empty:
        pdf = CustomPDF(orientation='P', unit='mm', format='A4')
        pdf.set_margins(15, 30, 15)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "MORBILIDAD EXTENSA", ln=1, align='J')
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 6, "NO HUBO CASOS", ln=1, align='J')
        buffer = BytesIO()
        pdf.set_title(nombre_archivo)
        pdf.set_author("EPI-SYSTEM")
        buffer.write(pdf.output(dest='S').encode('latin1'))
        buffer.seek(0)
        return buffer

    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(15, 30, 15)
    pdf.set_auto_page_break(auto=True, margin=15)

    for _, row in df.iterrows():
        pdf.add_page()

        # Título principal
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "MORBILIDAD EXTENSA", ln=1, align='J')
        pdf.ln(2)

        # Datos paciente
        data = {
            "Diagnóstico": limpiar_dato(row.get('diagnostico')),
            "Nombres y Apellidos": limpiar_dato(row.get('nombres_apellidos')),
            "Sexo": limpiar_dato(row.get('sexo')),
            "Estado Civil": limpiar_dato(row.get('estado_civil')),
            "Teléfono": limpiar_dato(row.get('telefono')),
            "Cédula": limpiar_dato(row.get('cedula')),
            "Historia Clínica": limpiar_dato(row.get('HC')),
            "Edad": f"{int(row.get('edad'))} años" if pd.notnull(row.get('edad')) else None,
            "Fecha de Registro": pd.to_datetime(row.get('fecha_registro_formulario'), errors='coerce').strftime('%d/%m/%Y') if pd.notnull(row.get('fecha_registro_formulario')) else None,
            "Fecha de Nacimiento": pd.to_datetime(row.get('fecha_nacimiento'), errors='coerce').strftime('%d/%m/%Y') if pd.notnull(row.get('fecha_nacimiento')) else None,
            "Dirección del Hogar": limpiar_dato(row.get('direccion_hogar')),
            "Lugar de Nacimiento": limpiar_dato(row.get('direccion_nacimiento'))
        }

        # Procesar direcciones para eliminar "No disponible" y componentes vacíos
        for key in ["Dirección del Hogar", "Lugar de Nacimiento"]:
            if data[key]:
                componentes = [comp.strip() for comp in data[key].split(',')]
                componentes_validos = [comp for comp in componentes if comp and comp != "No disponible"]
                data[key] = ", ".join(componentes_validos) if componentes_validos else None

        # Filtrar datos nulos o vacíos
        data = {k: v for k, v in data.items() if v}

        # Mostrar en dos columnas (excepto Dirección y Lugar de Nacimiento)
        items = [(k, v) for k, v in data.items() if k not in ["Dirección del Hogar", "Lugar de Nacimiento"]]
        col1_width = 45
        col2_width = 55
        col_total = col1_width + col2_width

        for i in range(0, len(items), 2):
            campo1, valor1 = items[i]
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(col1_width, 6, f"{campo1}:", ln=0)
            pdf.set_font("Arial", '', 10)
            pdf.multi_cell(col2_width, 6, valor1)

            if i + 1 < len(items):
                campo2, valor2 = items[i + 1]
                y_actual = pdf.get_y() - 6
                pdf.set_xy(15 + col_total, y_actual)
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(col1_width, 6, f"{campo2}:", ln=0)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(col2_width, 6, valor2)
            else:
                pdf.ln(6)

        pdf.ln(5)

        # Dirección de nacimiento y hogar
        pdf.set_font("Arial", "", 10)
        direccion_nac = data.get("Lugar de Nacimiento")
        if direccion_nac:
            pdf.set_font("Arial", "B", 10)
            pdf.cell(50, 8, "Lugar de Nacimiento: ", ln=0)
            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(0, 8, direccion_nac)
            pdf.ln(2)

        direccion_hogar = data.get("Dirección del Hogar")
        if direccion_hogar:
            pdf.set_font("Arial", "B", 10)
            pdf.cell(50, 8, "Dirección del Hogar: ", ln=0)
            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(0, 8, direccion_hogar)
            pdf.ln(2)

    # Exportación
    pdf.set_title(nombre_archivo)
    pdf.set_author("EPI-SYSTEM")
    buffer = BytesIO()
    buffer.write(pdf.output(dest='S').encode('latin1'))
    buffer.seek(0)
    return buffer

def exportar_pdf_morbilidad_simp(df, nombre_archivo):
    """Versión resumida"""
    if df.empty:
        pdf = CustomPDF(orientation='P', unit='mm', format='A4')
        pdf.set_margins(15, 30, 15)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "MORBILIDAD SIMPLIFICADA", ln=1, align='J')
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 6, "NO HUBO CASOS", ln=1, align='J')
        buffer = BytesIO()
        pdf.set_title(nombre_archivo)
        pdf.set_author("EPI-SYSTEM")
        buffer.write(pdf.output(dest='S').encode('latin1'))
        buffer.seek(0)
        return buffer

    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(15, 30, 15)
    pdf.set_auto_page_break(auto=True, margin=15)

    for _, row in df.iterrows():
        pdf.add_page()

        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "MORBILIDAD SIMPLIFICADA", ln=1, align='J')
        pdf.ln(2)

        data = {
            "Diagnóstico": limpiar_dato(row.get('diagnostico')),
            "Nombres y Apellidos": limpiar_dato(row.get('nombres_apellidos')),
            "Sexo": limpiar_dato(row.get('sexo')),
            "Edad": f"{int(row.get('edad'))} años" if pd.notnull(row.get('edad')) else None,
            "Fecha de Registro": pd.to_datetime(row.get('fecha_registro_formulario'), errors='coerce').strftime('%Y-%m-%d') if pd.notnull(row.get('fecha_registro_formulario')) else None,
            "Fecha de Nacimiento": pd.to_datetime(row.get('fecha_nacimiento'), errors='coerce').strftime('%d/%m/%Y') if pd.notnull(row.get('fecha_nacimiento')) else None
        }

        data = {k: v for k, v in data.items() if v}

        col1_width = 45
        col2_width = 55
        col_total = col1_width + col2_width
        items = list(data.items())

        for i in range(0, len(items), 2):
            campo1, valor1 = items[i]
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(col1_width, 6, f"{campo1}:", ln=0)
            pdf.set_font("Arial", '', 10)
            pdf.multi_cell(col2_width, 6, valor1)

            if i + 1 < len(items):
                campo2, valor2 = items[i + 1]
                y_actual = pdf.get_y() - 6
                pdf.set_xy(15 + col_total, y_actual)
                pdf.set_font("Arial", 'B', 10)
                pdf.cell(col1_width, 6, f"{campo2}:", ln=0)
                pdf.set_font("Arial", '', 10)
                pdf.multi_cell(col2_width, 6, valor2)
            else:
                pdf.ln(6)

        pdf.ln(5)

    # Exportación
    pdf.set_title(nombre_archivo)
    pdf.set_author("EPI-SYSTEM")
    buffer = BytesIO()
    buffer.write(pdf.output(dest='S').encode('latin1'))
    buffer.seek(0)
    return buffer