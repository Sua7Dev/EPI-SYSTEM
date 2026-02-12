import streamlit as st
import pandas as pd
import sqlite3
import os
import datetime
from fpdf import FPDF
from io import BytesIO
import numpy as np
import re
import locale
from utils.pdfbanners import CustomPDF

DB_PATH = os.getenv("hospital.db", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'

LABELS = {
    "historia_clinica": "Historia clínica",
    "nombres_apellidos": "Nombres y apellidos",
    "edad": "Edad",
    "fecha_nacimiento": "Fecha de nacimiento",
    "hora_nacimiento": "Hora de nacimiento",
    "fecha_defuncion": "Fecha de defunción",
    "hora_defuncion": "Hora de defunción",
    "nombre_madre": "Nombre de la madre",
    "semanas_gestacion": "Semanas de gestación",
    "peso": "Peso",
    "talla": "Talla",
    "idx_ingreso": "Diagnóstico de ingreso",
    "idx_defuncion": "Diagnóstico de defunción",
    "direccion": "Dirección",
    "causas": "Causas",
    "n_casos": "Casos",
    "tasa": "Tasa (%)",
    "total": "Total",
    "fecha_registro_formulario": "Fecha de registro"
}

def _exportar_pdf_mortalidad(df, nombre_archivo):
    if "neonatal" in nombre_archivo.lower():
        title = "Datos de mortalidad neonatal"
        selected_columns = [
            'historia_clinica', 'nombres_apellidos', 'edad', 'fecha_nacimiento',
            'hora_nacimiento', 'fecha_defuncion', 'hora_defuncion',
            'nombre_madre', 'semanas_gestacion', 'peso', 'talla',
            'idx_ingreso', 'idx_defuncion', 'direccion'
        ]
        tipo = "Neonatal"

    elif "infantil" in nombre_archivo.lower():
        title = "Datos de mortalidad infantil"
        selected_columns = [
            'historia_clinica', 'nombres_apellidos', 'edad', 'fecha_nacimiento',
            'fecha_defuncion', 'hora_defuncion', 'nombre_madre',
            'idx_ingreso', 'idx_defuncion', 'direccion'
        ]
        tipo = "Infantil"

    elif "materna" in nombre_archivo.lower():
        title = "Datos de mortalidad materna"
        selected_columns = [
            'historia_clinica', 'nombres_apellidos', 'edad', 'fecha_nacimiento',
            'fecha_defuncion', 'hora_defuncion',
            'idx_ingreso', 'idx_defuncion', 'direccion'
        ]
        tipo = "Materna"
    else:
        return None

    columns_to_exclude = ['fecha_registro_formulario', ' ', 'semana', 'fecha_registro']
    id_columns = [col for col in df.columns if 'id' in col.lower()]
    columns_to_exclude.extend(id_columns)

    available_columns = [col for col in selected_columns if col in df.columns]
    df_filtered = df[available_columns].copy()

    if "fecha_defuncion" in df_filtered.columns:
        df_filtered["fecha_defuncion"] = pd.to_datetime(
            df_filtered["fecha_defuncion"], errors="coerce"
        ).dt.strftime("%d/%m/%Y")

    for col in df_filtered.columns:
        if df_filtered[col].dtype == np.float64:
            df_filtered[col] = df_filtered[col].apply(
                lambda x: f"{x:.2f}" if pd.notnull(x) else ""
            )

    # Forzar Portrait Letter
    pdf = CustomPDF(orientation='P', unit='mm', format='Letter')
    pdf.alias_nb_pages()
    pdf.set_margins(left=12.7, top=15, right=12.7)
    page_width = pdf.w - 25.4

    if df_filtered.empty:
        pdf.add_page()
        pdf.set_font("Arial", 'B', size=14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 12, title.upper(), ln=1, align='C')
        pdf.ln(8)
        pdf.set_font("Arial", size=11)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(0, 8, f"{tipo}: No se encontraron casos registrados para este periodo.", align='C')

    else:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, title.upper(), ln=1, align='C')
        pdf.ln(2)
        pdf.set_text_color(0, 0, 0)

        # --- RESUMEN ---
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 8, "RESUMEN DEL REPORTE", border=0, ln=1, align='L')
        pdf.set_font("Arial", '', 9)
        pdf.cell(page_width, 10, f"Total de Registros de {tipo}: {len(df_filtered)}", border=1, ln=1, align='C')
        pdf.ln(10)

        # Determinar cabeceras segun tipo
        if "neonatal" in nombre_archivo.lower():
            headers = ["PACIENTE / NACIMIENTO", "DATOS MATERNOS/CLÍN.", "DEFUNCIÓN / DIAGNÓSTICOS", "DIRECCIÓN"]
            widths = [48, 45, 50, 47]
        elif "infantil" in nombre_archivo.lower():
            headers = ["PACIENTE / NACIMIENTO", "DATOS MATERNOS", "DEFUNCIÓN / DIAGNÓSTICOS", "DIRECCIÓN"]
            widths = [48, 45, 50, 47]
        else: # materna
            headers = ["PACIENTE / NACIMIENTO", "DEFUNCIÓN / DIAGNÓSTICOS", "DIRECCIÓN"]
            widths = [55, 70, 65]

        pdf.draw_table_header(headers, widths)
        pdf.set_font("Arial", '', 8.5)
        
        fill = False
        for _, row in df_filtered.iterrows():
            if "neonatal" in nombre_archivo.lower():
                col1 = f"Historia Clínica: {row.get('historia_clinica','')}\nNombre: {row.get('nombres_apellidos','')}\nEdad: {row.get('edad','')} días\nNacimiento: {row.get('fecha_nacimiento','')} ({row.get('hora_nacimiento','')})"
                col2 = f"Madre: {row.get('nombre_madre','')}\nSemanas Gest.: {row.get('semanas_gestacion','')}\nPeso: {row.get('peso','')} kg\nTalla: {row.get('talla','')} cm"
                col3 = f"Defunción: {row.get('fecha_defuncion','')} ({row.get('hora_defuncion','')})\nDiag. Ingreso: {row.get('idx_ingreso','')}\nDiag. Defunción: {row.get('idx_defuncion','')}"
                col4 = f"Dirección:\n{row.get('direccion','')}"
                vals = [col1, col2, col3, col4]
            elif "infantil" in nombre_archivo.lower():
                col1 = f"Historia Clínica: {row.get('historia_clinica','')}\nNombre: {row.get('nombres_apellidos','')}\nEdad: {row.get('edad','')} meses\nNacimiento: {row.get('fecha_nacimiento','')}"
                col2 = f"Madre: {row.get('nombre_madre','')}"
                col3 = f"Defunción: {row.get('fecha_defuncion','')} ({row.get('hora_defuncion','')})\nDiag. Ingreso: {row.get('idx_ingreso','')}\nDiag. Defunción: {row.get('idx_defuncion','')}"
                col4 = f"Dirección:\n{row.get('direccion','')}"
                vals = [col1, col2, col3, col4]
            else: # materna
                col1 = f"Historia Clínica: {row.get('historia_clinica','')}\nNombre: {row.get('nombres_apellidos','')}\nEdad: {row.get('edad','')} años\nNacimiento: {row.get('fecha_nacimiento','')}"
                col2 = f"Defunción: {row.get('fecha_defuncion','')} ({row.get('hora_defuncion','')})\nDiag. Ingreso: {row.get('idx_ingreso','')}\nDiag. Defunción: {row.get('idx_defuncion','')}"
                col3 = f"Dirección:\n{row.get('direccion','')}"
                vals = [col1, col2, col3]

            def limpiar_string(v): return str(v) if pd.notnull(v) else ""
            res = pdf.draw_tabular_row([limpiar_string(v) for v in vals], widths, fill=fill)
            if not res:
                pdf.draw_table_header(headers, widths)
                pdf.draw_tabular_row([limpiar_string(v) for v in vals], widths, fill=fill)
            fill = not fill

    pdf.set_title(nombre_archivo)
    pdf.set_author("EPI-SYSTEM")

    buffer = BytesIO()
    # fpdf2 compatible output
    pdf_bytes = pdf.output(dest='S')
    if isinstance(pdf_bytes, str):
        pdf_bytes = pdf_bytes.encode('latin1')
    buffer.write(pdf_bytes)
    buffer.seek(0)
    return buffer
