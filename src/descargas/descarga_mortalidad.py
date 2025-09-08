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

DB_PATH = os.environ.get("AUTH_DB_PATH", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'


def _exportar_pdf_mortalidad(df, nombre_archivo):
    if "neonatal" in nombre_archivo.lower():
        title = "Datos de Muerte Neonatal"
        selected_columns = [
            'historia_clinica', 'nombres_apellidos', 'edad', 'fecha_nacimiento',
            'hora_nacimiento', 'fecha_defuncion', 'hora_defuncion',
            'nombre_madre', 'semanas_gestacion', 'peso', 'talla',
            'idx_ingreso', 'idx_defuncion', 'direccion'
        ]
        tipo = "Neonatal"
    elif "infantil" in nombre_archivo.lower():
        title = "Datos de Muerte Infantil"
        selected_columns = [
            'historia_clinica', 'nombres_apellidos', 'edad', 'fecha_nacimiento',
            'fecha_defuncion', 'hora_defuncion', 'nombre_madre',
            'idx_ingreso', 'idx_defuncion', 'direccion'
        ]
        tipo = "Infantil"
    elif "materna" in nombre_archivo.lower():
        title = "Datos de Muerte Materna"
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
        ).dt.strftime("%Y-%m-%d")

    for col in df_filtered.columns:
        if df_filtered[col].dtype == np.float64:
            df_filtered[col] = df_filtered[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "")

    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(left=10, top=30, right=10)

    if df_filtered.empty:
        pdf.add_page()
        pdf.set_font("Arial", 'B', size=16)
        pdf.cell(0, 12, title, ln=1, align='J')
        pdf.ln(12)
        pdf.set_font("Arial", size=14)
        pdf.cell(0, 10, f"{tipo}: NO HUBO CASOS", ln=1, align='L')
    else:
        column_width = 95
        line_height = 10
        columns = 2

        for idx, (_, row) in enumerate(df_filtered.iterrows(), start=1):
            pdf.add_page()
            pdf.set_font("Arial", 'B', size=16)
            pdf.cell(0, 12, title, ln=1, align='J')
            pdf.ln(12)
            pdf.set_font("Arial", size=14)

            fields = []
            for col in df_filtered.columns:
                value = str(row[col]) if pd.notnull(row[col]) else ""
                if col == 'direccion':
                    if value == "No disponible":
                        continue
                    cleaned_value = re.sub(r'\bNo disponible\b(?:,\s*|$)', '', value).strip(', ')
                    if not cleaned_value:
                        continue
                    value = cleaned_value
                if value:
                    label = col.replace('_', ' ').title() + ":"
                    fields.append(f"{label} {value}")

            if fields:
                fields_per_column = (len(fields) + columns - 1) // columns
                col1_fields = fields[:fields_per_column]
                col2_fields = fields[fields_per_column:]

                start_y = pdf.get_y()

                pdf.set_x(10)
                for field in col1_fields:
                    pdf.multi_cell(column_width, line_height, field, align='L')
                    pdf.set_x(10)

                if col2_fields:
                    pdf.set_xy(10 + column_width, start_y)
                    for field in col2_fields:
                        pdf.multi_cell(column_width, line_height, field, align='L')
                        pdf.set_xy(10 + column_width, pdf.get_y())

                pdf.ln(12)

    pdf.set_title(nombre_archivo)
    pdf.set_author("EPI-SYSTEM")

    buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_output)
    buffer.seek(0)
    return buffer

def _exportar_pdf_mortalidad_mensual(df, nombre_archivo):
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except locale.Error:
        month_map = {
            'January': 'Enero', 'February': 'Febrero', 'March': 'Marzo', 'April': 'Abril',
            'May': 'Mayo', 'June': 'Junio', 'July': 'Julio', 'August': 'Agosto',
            'September': 'Septiembre', 'October': 'Octubre', 'November': 'Noviembre', 'December': 'Diciembre'
        }
        def format_spanish_date(m):
            date_obj = datetime.datetime.strptime(m, '%Y-%m')
            english_month = date_obj.strftime('%B')
            spanish_month = month_map.get(english_month, english_month)
            return f"{spanish_month} {date_obj.year}"
    else:
        format_spanish_date = lambda m: datetime.datetime.strptime(m, '%Y-%m').strftime('%B %Y')

    if nombre_archivo.lower() in ["mortalidad_mensual_infatil, mortalidad_mensual_infatil_seleccionado"]:
        title = "Datos de Mortalidad Mensual Infantil"
    elif "mortalidad_mensual_neonatal_seleccionado" in nombre_archivo.lower():
        title = "Datos de Mortalidad Mensual Neonatal"
    elif "mortalidad_mensual_general, mortalidad_mensual_general_seleccionado" in nombre_archivo.lower():
        title = "Datos de Mortalidad Mensual General"
    else:
        title = "Datos de Mortalidad Mensual"
    selected_columns = ['causas', 'n_casos', 'tasa', 'total', 'fecha_registro_formulario']
    tipo = "Mensual"

    columns_to_exclude = ['fecha_registro_formulario', ' ', 'semana', 'fecha_registro']
    id_columns = [col for col in df.columns if 'id' in col.lower()]
    columns_to_exclude.extend(id_columns)
    available_columns = [col for col in selected_columns if col in df.columns]
    df_filtered = df[available_columns]

    for col in df_filtered.columns:
        if df_filtered[col].dtype == np.float64:
            df_filtered[col] = df_filtered[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "")

    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(left=10, top=30, right=10)
    pdf.add_page()

    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(0, 12, title, ln=1, align='J')
    pdf.ln(12)

    if df_filtered.empty:
        pdf.set_font("Arial", size=14)
        pdf.cell(0, 10, f"{tipo}: NO HUBO CASOS", ln=1, align='L')
    else:
        if 'fecha_registro_formulario' in df_filtered.columns:
            df_filtered['mes'] = pd.to_datetime(df_filtered['fecha_registro_formulario']).dt.strftime('%Y-%m')
            unique_months = sorted(df_filtered['mes'].unique())
            selected_dates = ", ".join([format_spanish_date(m) for m in unique_months])
        else:
            unique_months = [datetime.datetime.now().strftime('%Y-%m')]
            selected_dates = format_spanish_date(unique_months[0])
            df_filtered['mes'] = unique_months[0]

        pdf.set_font("Arial", size=14)
        pdf.cell(0, 10, f"Fecha(s) Elegida(s): {selected_dates}", ln=1, align='L')
        pdf.ln(10)

        df_grouped = df_filtered.groupby(['mes', df_filtered['causas'].str.lower()]).agg({
            'causas': 'first',
            'n_casos': 'sum',
            'tasa': 'first',
            'total': 'first'
        }).reset_index(level=1, drop=True).reset_index()

        for mes in unique_months:
            pdf.set_font("Arial", 'B', size=14)
            pdf.cell(0, 10, format_spanish_date(mes), ln=1, align='L')
            pdf.ln(5)

            df_mes = df_grouped[df_grouped['mes'] == mes][['causas', 'n_casos', 'tasa', 'total']]
            
            if df_mes.empty:
                pdf.set_font("Arial", size=12)
                pdf.cell(0, 10, "No hubo casos", ln=1, align='L')
            else:
                pdf.set_font("Arial", 'B', size=12)
                pdf.cell(100, 10, "Causas", 1, 0, 'J')
                pdf.cell(30, 10, "N. Casos", 1, 0, 'J')
                pdf.cell(30, 10, "Tasa (%)", 1, 1, 'J')
                
                pdf.set_font("Arial", size=12)
                for _, row in df_mes.iterrows():
                    pdf.cell(100, 10, row['causas'], 1, 0, 'L')
                    pdf.cell(30, 10, str(row['n_casos']), 1, 0, 'J')
                    pdf.cell(30, 10, row['tasa'], 1, 1, 'J')
                
                total = df_mes['total'].iloc[0] if not df_mes['total'].empty else 0
                pdf.set_font("Arial", 'B', size=12)
                pdf.cell(100, 10, "Total", 1, 0, 'J')
                pdf.cell(60, 10, str(total), 1, 1, 'J')
            
            pdf.ln(10)

    pdf.set_title(nombre_archivo)
    pdf.set_author("EPI-SYSTEM")
    buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_output)
    buffer.seek(0)
    return buffer