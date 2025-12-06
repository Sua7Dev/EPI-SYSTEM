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

def _exportar_pdf_mortalidad_mensual(df, nombre_archivo):
    try:
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    except locale.Error:
        month_map = {
            'January': 'enero', 'February': 'febrero', 'March': 'marzo', 'April': 'abril',
            'May': 'mayo', 'June': 'junio', 'July': 'julio', 'August': 'agosto',
            'September': 'septiembre', 'October': 'octubre',
            'November': 'noviembre', 'December': 'diciembre'
        }

        def format_spanish_date(m):
            date_obj = datetime.datetime.strptime(m, '%Y-%m')
            english_month = date_obj.strftime('%B')
            spanish_month = month_map.get(english_month, english_month)
            return f"{spanish_month.capitalize()} {date_obj.year}"

    else:
        format_spanish_date = lambda m: datetime.datetime.strptime(
            m, '%Y-%m'
        ).strftime('%B %Y').capitalize()

    if nombre_archivo.lower() in ["mortalidad_mensual_infatil, mortalidad_mensual_infatil_seleccionado"]:
        title = "Datos de mortalidad mensual infantil"
    elif "mortalidad_mensual_neonatal_seleccionado" in nombre_archivo.lower():
        title = "Datos de mortalidad mensual neonatal"
    elif "mortalidad_mensual_general, mortalidad_mensual_general_seleccionado" in nombre_archivo.lower():
        title = "Datos de mortalidad mensual general"
    else:
        title = "Datos de mortalidad mensual"

    selected_columns = ['causas', 'n_casos', 'tasa', 'total', 'fecha_registro_formulario']
    tipo = "Mensual"

    columns_to_exclude = ['fecha_registro_formulario', ' ', 'semana', 'fecha_registro']
    id_columns = [col for col in df.columns if 'id' in col.lower()]
    columns_to_exclude.extend(id_columns)

    available_columns = [col for col in selected_columns if col in df.columns]
    df_filtered = df[available_columns].copy()

    for col in df_filtered.columns:
        if df_filtered[col].dtype == np.float64:
            df_filtered[col] = df_filtered[col].apply(
                lambda x: f"{x:.2f}" if pd.notnull(x) else ""
            )

    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(left=10, top=30, right=10)
    pdf.add_page()

    pdf.set_font("Arial", size=14)
    pdf.cell(0, 12, title, ln=1, align='C')
    pdf.ln(8)

    if df_filtered.empty:
        pdf.set_font("Arial", size=14)
        pdf.multi_cell(0, 8, f"{tipo}: No hubo casos.", align='J')

    else:
        if 'fecha_registro_formulario' in df_filtered.columns:
            df_filtered['mes'] = pd.to_datetime(
                df_filtered['fecha_registro_formulario']
            ).dt.strftime('%Y-%m')

            unique_months = sorted(df_filtered['mes'].unique())
            selected_dates = ", ".join([format_spanish_date(m) for m in unique_months])

        else:
            unique_months = [datetime.datetime.now().strftime('%Y-%m')]
            selected_dates = format_spanish_date(unique_months[0])
            df_filtered['mes'] = unique_months[0]

        df_grouped = df_filtered.groupby(
            ['mes', df_filtered['causas'].str.lower()]
        ).agg({
            'causas': 'first',
            'n_casos': 'sum',
            'tasa': 'first',
            'total': 'first'
        }).reset_index(level=1, drop=True).reset_index()

        for mes in unique_months:
            pdf.set_font("Arial", 'B', size=13)
            pdf.cell(0, 10, format_spanish_date(mes), ln=1, align='L')
            pdf.ln(4)

            df_mes = df_grouped[df_grouped['mes'] == mes][
                ['causas', 'n_casos', 'tasa', 'total']
            ]

            if df_mes.empty:
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 8, "No hubo casos.", align='J')

            else:
                # Usar todo el ancho imprimible para que la tabla quede más estirada y centrada
                pdf.set_font("Arial", 'B', size=12)
                printable_width = pdf.w - pdf.l_margin - pdf.r_margin
                # proporciones: causas (65%), casos (17.5%), tasa (17.5%)
                w_causas = printable_width * 0.65
                w_casos = printable_width * 0.175
                w_tasa = printable_width - (w_causas + w_casos)

                start_x = pdf.l_margin
                pdf.set_x(start_x)
                pdf.cell(w_causas, 8, LABELS["causas"], 1, 0, 'C')
                pdf.cell(w_casos, 8, LABELS["n_casos"], 1, 0, 'C')
                pdf.cell(w_tasa, 8, LABELS["tasa"], 1, 1, 'C')

                pdf.set_font("Arial", size=12)
                for _, row in df_mes.iterrows():
                    x_before = start_x
                    y_before = pdf.get_y()

                    # columna 'causas' justificada y con multi_cell dentro del ancho calculado
                    pdf.set_x(x_before)
                    pdf.multi_cell(w_causas, 6, str(row['causas']), border=1, align='J')

                    # las siguientes celdas alineadas con la línea de inicio del registro
                    pdf.set_xy(x_before + w_causas, y_before)
                    pdf.multi_cell(w_casos, 6, str(row['n_casos']), border=1, align='C')

                    pdf.set_xy(x_before + w_causas + w_casos, y_before)
                    pdf.multi_cell(w_tasa, 6, str(row['tasa']), border=1, align='C')

                    # mover el cursor al inicio de la siguiente fila
                    pdf.set_xy(pdf.l_margin, max(pdf.get_y(), y_before + 6))

                total = df_mes['total'].iloc[0] if not df_mes['total'].empty else 0

                pdf.set_font("Arial", 'B', size=12)
                # ajustar anchura total de la fila Total para mantener centrado
                pdf.cell(w_causas, 8, LABELS["total"], 1, 0, 'C')
                pdf.cell(w_casos + w_tasa, 8, str(total), 1, 1, 'C')

            pdf.ln(8)

    pdf.set_title(nombre_archivo)
    pdf.set_author("EPI-SYSTEM")

    buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_output)
    buffer.seek(0)
    return buffer