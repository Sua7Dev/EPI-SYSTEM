import streamlit as st
import os
import pandas as pd
from io import BytesIO
import numpy as np
import re
import datetime
from utils.pdfbanners import CustomPDF
DB_PATH = os.environ.get("AUTH_DB_PATH", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'

def _exportar_pdf_epi14(df, nombre_archivo):
    if df.empty:
        pdf = CustomPDF(orientation='P', unit='mm', format='A4')
        pdf.set_margins(10, 30, 10)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font(family="Arial", size=14, style='B')
        pdf.cell(0, 10, "No hay datos disponibles para generar el reporte", ln=1, align='J')
        buffer = BytesIO()
        fecha_actual = datetime.datetime.now()
        fecha_str = fecha_actual.strftime("%d-%m-%Y")
        hora_str = fecha_actual.strftime("%I").lstrip("0")  
        minutos_seg = fecha_actual.strftime("%M-%S")
        meridiano = "PM" if fecha_actual.hour >= 12 else "AM"
        fecha_hora_str = f"{fecha_str}_{hora_str}-{minutos_seg}_{meridiano}"
        pdf.set_title(f"{nombre_archivo}_{fecha_hora_str}")
        pdf.set_author("EPI-SYSTEM")
        buffer.write(pdf.output(dest='S').encode('latin1'))
        buffer.seek(0)
        return buffer

    df_filtered = df.copy()
    required_columns = ['causa', 'numero', 'sexo_edad', 'total']
    for col in required_columns:
        if col not in df_filtered.columns:
            df_filtered[col] = 'Unknown' if col not in ['numero', 'total'] else 0

    columns_to_exclude = [' ', 'fecha_registro_formulario', 'Registrado_por']
    id_columns = [col for col in df_filtered.columns if 'id' in col.lower()]
    columns_to_exclude.extend(id_columns)
    df_filtered = df_filtered[[col for col in df_filtered.columns if col not in columns_to_exclude]]

    df_filtered['causa'] = df_filtered['causa'].astype(str)
    df_filtered['causa_upper'] = df_filtered['causa'].str.upper()
    if 'semana' in df_filtered.columns:
        df_filtered['semana'] = df_filtered['semana'].astype(str)
        extracted = df_filtered['semana'].str.extract(r'Semana (\d+)-(\d{4})')
        df_filtered['week'] = pd.to_numeric(extracted[0], errors='coerce').fillna(0)
        df_filtered['year'] = pd.to_numeric(extracted[1], errors='coerce').fillna(0)
        group_cols = ['week', 'year', 'causa_upper']
    else:
        group_cols = ['causa_upper']

    agg_dict = {
        'causa': 'first',
        'numero': 'sum',
        'sexo_edad': lambda x: ', '.join(x.astype(str)),
        'total': 'first' if 'total' in df_filtered.columns else lambda x: sum(x)
    }
    df_filtered = df_filtered.groupby(group_cols).agg(agg_dict).reset_index()

    if 'week' in df_filtered.columns:
        df_filtered = df_filtered.sort_values(['week', 'year', 'causa_upper'])
        df_filtered['total'] = df_filtered.groupby(['week', 'year'])['numero'].transform('sum')
        df_filtered['total'] = df_filtered.groupby(['week', 'year'])['total'].transform(
            lambda x: [x.iloc[0]] + [''] * (len(x) - 1)
        )
        df_filtered = df_filtered.drop(columns=['week', 'year', 'causa_upper'], errors='ignore')
    else:
        df_filtered['total'] = df_filtered['numero'].sum()
        df_filtered['total'] = [df_filtered['total'].iloc[0]] + [''] * (len(df_filtered) - 1)
        df_filtered = df_filtered.drop(columns=['causa_upper'], errors='ignore')

    for col in df_filtered.columns:
        if col in ['numero', 'total'] and df_filtered[col].dtype in [np.float64, np.int64]:
            df_filtered[col] = df_filtered[col].apply(lambda x: str(int(x)) if pd.notnull(x) else "")

    date_columns = []
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4}')
    for col in df_filtered.columns:
        first_non_null = df_filtered[col].dropna().iloc[0] if not df_filtered[col].dropna().empty else ""
        if isinstance(first_non_null, str) and date_pattern.match(str(first_non_null)):
            date_columns.append(col)

    range_text = "(Semana no disponible)"
    if 'semana' in df.columns and not df['semana'].dropna().empty:
        try:
            semana_values = df['semana'].dropna().unique()
            weeks = []
            years = []
            for val in semana_values:
                match = re.match(r'Semana (\d+)-(\d{4})', str(val))
                if match:
                    weeks.append(int(match.group(1)))
                    years.append(int(match.group(2)))
            if weeks:
                min_week, max_week = min(weeks), max(weeks)
                min_year, max_year = min(years), max(years)
                range_text = (f"(Semana {min_week}-{min_year})" if min_week == max_week and min_year == max_year
                              else f"(Semanas {min_week}-{min_year} a {max_week}-{max_year})")
        except:
            pass

    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(10, 30, 10)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font(family="Arial", size=14, style='B')
    pdf.cell(0, 10, f"Epi 14 Semanal {range_text}", ln=1, align='J')
    pdf.ln(8)

    pdf.set_font(family="Arial", size=10, style='')
    line_height = pdf.font_size * 2.5
    page_width = pdf.w - 20
    num_cols = len(df_filtered.columns)
    date_col_width = 50
    non_date_col_width = (page_width - len(date_columns) * date_col_width) / (num_cols - len(date_columns)) if num_cols > len(date_columns) else page_width / num_cols
    col_widths = [date_col_width if col in date_columns else non_date_col_width for col in df_filtered.columns]

    total_width = sum(col_widths)
    if total_width > page_width:
        scale_factor = page_width / total_width
        col_widths = [w * scale_factor for w in col_widths]

    col_headers = [str(col).title() for col in df_filtered.columns]
    max_header_lines = max(len(pdf.multi_cell(w, line_height, txt, border=0, align='L', split_only=True)) for txt, w in zip(col_headers, col_widths))
    max_header_height = max_header_lines * line_height

    start_y = pdf.get_y()

    pdf.set_fill_color(158, 185, 212)
    pdf.rect(10, start_y, page_width, max_header_height, style='F')

    pdf.set_text_color(0, 0, 0)
    start_x = 10
    for txt, width in zip(col_headers, col_widths):
        pdf.set_xy(start_x, start_y)
        pdf.multi_cell(width, line_height, txt, border=0, align='L')
        start_x += width

    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.3)
    pdf.rect(10, start_y, page_width, max_header_height)
    current_x = 10
    for width in col_widths:
        pdf.line(current_x, start_y, current_x, start_y + max_header_height)
        current_x += width
    pdf.line(10, start_y + max_header_height, 10 + page_width, start_y + max_header_height)
    pdf.set_xy(10, start_y + max_header_height)

    numeric_cols = ['numero', 'total']
    row_index = 0
    for _, row in df_filtered.iterrows():
        cell_texts = [str(row[col]) if row[col] is not None else "" for col in df_filtered.columns]
        max_lines = max(len(pdf.multi_cell(w, line_height, t, border=0, align='L' if col not in numeric_cols else 'J', split_only=True)) for t, w, col in zip(cell_texts, col_widths, df_filtered.columns))
        row_height = max_lines * line_height

        start_y = pdf.get_y()

        start_x = 10
        for text, width, col in zip(cell_texts, col_widths, df_filtered.columns):
            pdf.set_xy(start_x, start_y)
            align = 'J' if col in numeric_cols else 'L'
            pdf.multi_cell(width, line_height, text, border=0, align=align)
            start_x += width

        pdf.rect(10, start_y, page_width, row_height)
        current_x = 10
        for width in col_widths:
            pdf.line(current_x, start_y, current_x, start_y + row_height)
            current_x += width
        pdf.line(10, start_y + row_height, 10 + page_width, start_y + row_height)
        pdf.set_xy(10, start_y + row_height)
        row_index += 1

    pdf.ln(20)
    pdf.set_font(family="Arial", size=12, style='')
    pdf.cell(100, 10, ln=0, align='L')
    pdf.cell(0, 10, ln=1, align='J')

    pdf.set_title(nombre_archivo)
    pdf.set_author("EPI-SYSTEM")
    buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_output)
    buffer.seek(0)
    return buffer