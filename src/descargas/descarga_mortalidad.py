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

    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(left=10, top=30, right=10)

    if df_filtered.empty:
        pdf.add_page()
        pdf.set_font("Arial", 'B', size=14)
        pdf.cell(0, 12, title, ln=1, align='C')
        pdf.ln(8)
        pdf.set_font("Arial", size=14)
        pdf.multi_cell(0, 8, f"{tipo}: No hubo casos.", align='J')

    else:
        column_width = 95
        line_height = 8
        columns = 2

        for idx, (_, row) in enumerate(df_filtered.iterrows(), start=1):
            pdf.add_page()
            pdf.set_font("Arial", 'B', size=14)
            pdf.cell(0, 12, title, ln=1, align='C')
            pdf.ln(6)
            pdf.set_font("Arial", size=12)

            fields = []
            for col in df_filtered.columns:
                value = str(row[col]) if pd.notnull(row[col]) else ""

                if col == 'direccion':
                    if value.lower() in ["no disponible", "no disponible."]:
                        continue

                    cleaned_value = re.sub(
                        r'\bNo disponible\b(?:,\s*|$)',
                        '',
                        value,
                        flags=re.IGNORECASE
                    ).strip(', ').strip()

                    if not cleaned_value:
                        continue

                    value = cleaned_value

                if value:
                    label = LABELS.get(col, col.replace('_', ' ').title()) + ":"
                    fields.append(f"{label} {value}")

            if fields:
                fields_per_column = (len(fields) + columns - 1) // columns
                col1_fields = fields[:fields_per_column]
                col2_fields = fields[fields_per_column:]

                start_y = pdf.get_y()

                pdf.set_x(10)
                for field in col1_fields:
                    pdf.multi_cell(column_width, line_height, field, align='J')
                    pdf.set_x(10)

                if col2_fields:
                    pdf.set_xy(10 + column_width + 5, start_y)
                    for field in col2_fields:
                        pdf.multi_cell(column_width, line_height, field, align='J')
                        pdf.set_xy(10 + column_width + 5, pdf.get_y())

                pdf.ln(8)

    pdf.set_title(nombre_archivo)
    pdf.set_author("EPI-SYSTEM")

    buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_output)
    buffer.seek(0)
    return buffer
