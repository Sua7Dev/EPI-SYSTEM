import streamlit as st
import pandas as pd
import math
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
    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(15, 30, 15)
    pdf.set_auto_page_break(auto=True, margin=20)

    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "DENUNCIAS OBLIGATORIAS", ln=1, align='C')
    pdf.ln(5)

    if df.empty:
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, "NO HUBO CASOS", ln=1, align='C')
        buffer = BytesIO()
        pdf.set_title(nombre_archivo)
        pdf.set_author("EPI-SYSTEM")
        buffer.write(pdf.output(dest='S').encode('latin1'))
        buffer.seek(0)
        return buffer

    df = df.copy()
    df['fecha_dt'] = pd.to_datetime(df['fecha_registro_formulario'], dayfirst=True, errors='coerce')
    df['fecha_str'] = df['fecha_dt'].dt.strftime('%d/%m/%Y').fillna('Sin fecha')

    usable_width = pdf.w - pdf.l_margin - pdf.r_margin
    pct = [0.04, 0.22, 0.30, 0.08, 0.36]
    col_widths = [max(10, int(usable_width * p)) for p in pct]
    headers = ['#', 'Enfermedad', 'Nombres y Apellidos', 'Edad', 'Dirección']

    def clean_direccion(text):
        if not text:
            return ""
        componentes = [comp.strip() for comp in str(text).split(',') if comp.strip() and comp.strip().lower() != "no disponible"]
        return ", ".join(componentes)

    def num_lines_for_text(txt, width):
        if txt is None or str(txt).strip() == "":
            return 1
        lines = 0
        for part in str(txt).splitlines():
            part = part.strip()
            if part == "":
                lines += 1
                continue
            text_width = pdf.get_string_width(part)
            effective_width = max(1, width - 2)
            lines += max(1, math.ceil(text_width / effective_width))
        return lines

    line_height = 5

    df['_id_num'] = pd.to_numeric(df.get('id', pd.Series(dtype='float')), errors='coerce').fillna(0).astype(int)
    df = df.sort_values(by=['fecha_dt', '_id_num'], ascending=[True, True]).reset_index(drop=True)

    def print_group_header(fecha):
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 8, fecha, ln=1, align='L')
        pdf.ln(2)
        pdf.set_font("Arial", 'B', 10)
        for i, header in enumerate(headers):
            pdf.cell(col_widths[i], 8, header, border=0, align='C')
        pdf.ln()
        pdf.set_font("Arial", '', 10)

    def ensure_space(needed_space, fecha):
        trigger = getattr(pdf, 'page_break_trigger', pdf.h - pdf.b_margin)
        if pdf.get_y() + needed_space > trigger:
            pdf.add_page()
            print_group_header(fecha)

    first_group = True
    for fecha, df_fecha in df.groupby('fecha_str', sort=False):
        if fecha == 'NaT' or df_fecha.empty:
            continue

        # si no es la primera agrupación, simplemente dejar pequeño espacio antes del siguiente grupo
        if not first_group:
            pdf.ln(3)

        print_group_header(fecha)

        # numerar secuencialmente dentro de la fecha (1..n)
        for seq, (_, row) in enumerate(df_fecha.reset_index(drop=True).iterrows(), start=1):
            diagnostico = str(row.get('diagnostico', '') or '')
            nombres = str(row.get('nombres_apellidos', '') or '')
            edad = f"{int(row.get('edad'))} años" if pd.notnull(row.get('edad')) else ''
            direccion = clean_direccion(row.get('direccion_hogar', ''))
            cells = [str(seq), diagnostico, nombres, edad, direccion]

            lines_per_cell = [num_lines_for_text(cells[i], col_widths[i]) for i in range(len(cells))]
            max_lines = max(lines_per_cell)
            row_height = max_lines * line_height

            # espacio necesario: altura de fila + una pequeña separación y margen para encabezado si se produce salto
            needed = row_height + 6

            ensure_space(needed, fecha)

            x_start = pdf.get_x()
            y_start = pdf.get_y()

            for i, item in enumerate(cells):
                x = x_start + sum(col_widths[:i])
                y = y_start
                pdf.set_xy(x, y)
                pdf.multi_cell(col_widths[i], line_height, str(item), border=0, align='L')
                pdf.rect(x, y, col_widths[i], row_height)

            pdf.set_xy(x_start, y_start + row_height)

        first_group = False

    buffer = BytesIO()
    pdf.set_title(nombre_archivo)
    pdf.set_author("EPI-SYSTEM")
    buffer.write(pdf.output(dest='S').encode('latin1'))
    buffer.seek(0)
    return buffer