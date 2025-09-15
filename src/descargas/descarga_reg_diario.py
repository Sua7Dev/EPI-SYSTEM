import pandas as pd
import os
from io import BytesIO
import numpy as np
import re
from utils.pdfbanners import CustomPDF

DB_PATH = os.getenv("hospital.db", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'

def _exportar_pdf(df, nombre_archivo, semana=None):
    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(left=15, top=30, right=15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    if df.empty:
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 6, "NO HUBO CASOS", ln=1, align='J')
        pdf.set_title(nombre_archivo)
        pdf.set_author("EPI-SYSTEM")
        buffer = BytesIO()
        pdf_output = pdf.output(dest='S').encode('latin1')
        buffer.write(pdf_output)
        buffer.seek(0)
        return buffer

    columns_to_exclude = ['fecha_registro_formulario', ' ', 'semana']
    id_columns = [col for col in df.columns if 'id' in col.lower()]
    columns_to_exclude.extend(id_columns)
    df_filtered = df[[col for col in df.columns if col not in columns_to_exclude]].copy()

    # Diccionario de reemplazo personalizado para encabezados
    custom_headers = {
        'fd': 'FO',
        'gett': 'Get',
        'edad_sexo': 'Edad/Sexo'
    }

    # Generar encabezados aplicando reemplazos
    col_headers = [
        custom_headers[col] if col in custom_headers else str(col).title()
        for col in df_filtered.columns
    ]

    # Formatear columna 'fd' como fecha DD/MM/YYYY
    if 'fd' in df_filtered.columns:
        df_filtered['fd'] = pd.to_datetime(
            df_filtered['fd'], errors='coerce', format='%d/%m/%Y', exact=False
        ).dt.strftime('%d/%m/%Y')

    # Formatear floats con dos decimales
    for col in df_filtered.columns:
        if df_filtered[col].dtype == np.float64:
            df_filtered[col] = df_filtered[col].apply(lambda x: f"{x:.2f}" if pd.notnull(x) else "")

    # Detectar columnas de fechas
    date_columns = []
    date_pattern = re.compile(r'^\d{2}/\d{2}/\d{4}$|^\d{4}-\d{2}-\d{2}$')
    for col in df_filtered.columns:
        if pd.api.types.is_datetime64_any_dtype(df_filtered[col]):
            date_columns.append(col)
        else:
            first_non_null = df_filtered[col].dropna().iloc[0] if not df_filtered[col].dropna().empty else ""
            if isinstance(first_non_null, str) and date_pattern.match(str(first_non_null)):
                date_columns.append(col)

    # Determinar semana
    week_display = None
    if semana:
        week_display = semana
    elif 'semana' in df.columns and not df['semana'].dropna().empty:
        week_display = str(df['semana'].dropna().iloc[0])
    if not week_display:
        week_display = "Semana no disponible"

    pdf.set_font("Arial", 'B', size=12)
    title = "Epi 14 Semanal" if "epi14_semanal" in nombre_archivo.lower() else f"Registro Diario ({week_display})"
    pdf.cell(0, 10, title, ln=1, align='J')
    pdf.ln(8)

    pdf.set_font("Arial", size=8)
    line_height = pdf.font_size * 2.5
    page_width = pdf.w - 30
    num_cols = len(df_filtered.columns)
    date_col_width = 25
    non_date_col_width = (page_width - len(date_columns) * date_col_width) / (num_cols - len(date_columns)) if num_cols > len(date_columns) else page_width / num_cols
    col_widths = [date_col_width if col in date_columns else non_date_col_width for col in df_filtered.columns]

    # Ajustar ancho si se excede
    total_width = sum(col_widths)
    if total_width > page_width:
        scale_factor = page_width / total_width
        col_widths = [w * scale_factor for w in col_widths]

    # Dibujar encabezados
    pdf.set_fill_color(158, 185, 212)
    max_header_height = 0
    for col, width in zip(col_headers, col_widths):
        nb_lines = pdf.multi_cell(width, line_height, col, border=0, align='J', split_only=True)
        header_height = line_height * len(nb_lines)
        max_header_height = max(max_header_height, header_height)

    start_y = pdf.get_y()
    pdf.rect(15, start_y, page_width, max_header_height, style='F')
    start_x = 15
    for col, width in zip(col_headers, col_widths):
        pdf.set_xy(start_x, start_y)
        pdf.multi_cell(width, line_height, col, border=1, align='J', fill=True)
        start_x += width

    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.3)
    pdf.rect(15, start_y, page_width, max_header_height)
    current_x = 15
    for width in col_widths:
        pdf.line(current_x, start_y, current_x, start_y + max_header_height)
        current_x += width
    pdf.line(15, start_y + max_header_height, 15 + page_width, start_y + max_header_height)
    pdf.set_xy(15, start_y + max_header_height)

    # Dibujar filas
    for _, row in df_filtered.iterrows():
        cell_texts = [str(row[col]) if row[col] is not None else "" for col in df_filtered.columns]
        row_height = 0
        for text, width in zip(cell_texts, col_widths):
            nb_lines = pdf.multi_cell(width, line_height, text, border=0, align='L', split_only=True)
            row_height = max(row_height, line_height * len(nb_lines))

        start_y = pdf.get_y()
        start_x = 15
        for text, width in zip(cell_texts, col_widths):
            pdf.set_xy(start_x, start_y)
            pdf.multi_cell(width, line_height, text, border=1, align='L')
            start_x += width

        pdf.rect(15, start_y, page_width, row_height)
        current_x = 15
        for width in col_widths:
            pdf.line(current_x, start_y, current_x, start_y + row_height)
            current_x += width
        pdf.line(15, start_y + row_height, 15 + page_width, start_y + row_height)
        pdf.set_xy(15, start_y + row_height)

    pdf.ln(20)
    pdf.set_font("Arial", size=12)
    pdf.cell(100, 10, ln=0, align='L')
    pdf.cell(0, 10, ln=1, align='J')

    pdf.set_title(nombre_archivo)
    pdf.set_author("EPI-SYSTEM")
    buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_output)
    buffer.seek(0)
    return buffer
