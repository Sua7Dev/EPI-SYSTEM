import pandas as pd
import os
from io import BytesIO
from utils.pdfbanners import CustomPDF

DB_PATH = os.getenv("hospital.db", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'

def _exportar_pdf_natalidad(df, nombre_archivo):
    if df.empty:
        pdf = CustomPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font(family="Arial", size=14, style='B')
        pdf.cell(0, 10, "No hay datos disponibles para generar el reporte", ln=1, align='J')
        buffer = BytesIO()
        pdf_output = pdf.output(dest='S').encode('latin1')
        buffer.write(pdf_output)
        buffer.seek(0)
        return buffer

    df_filtered = df.copy()
    required_columns = ['fecha', 'partos', 'cesareas', 'varones', 'hembras', 'gemelar', 'mto', 'partos_extrahospitalarios']
    for col in required_columns:
        if col not in df_filtered.columns:
            df_filtered[col] = 'Unknown' if col == 'fecha' else 0

    # Excluir columnas no necesarias
    columns_to_exclude = ['id', ' ', 'fecha_registro_formulario', 'id_doctor']
    df_filtered = df_filtered[[col for col in df_filtered.columns if col not in columns_to_exclude]]

    # Convertir fecha al formato YYYY-MM-DD
    df_filtered['fecha'] = pd.to_datetime(df_filtered['fecha'], errors='coerce').dt.strftime('%Y-%m-%d')

    # Asegurar que los valores numéricos estén bien definidos
    for col in ['partos', 'cesareas', 'varones', 'hembras', 'gemelar', 'mto', 'partos_extrahospitalarios']:
        df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce').fillna(0).astype(int)

    # Renombrar la columna "partos_extrahospitalarios" a "PEH"
    if 'partos_extrahospitalarios' in df_filtered.columns:
        df_filtered = df_filtered.rename(columns={'partos_extrahospitalarios': 'PEH'})

    # Ordenar por fecha
    df_filtered = df_filtered.sort_values(by='fecha')

    # Texto del rango de fechas
    range_text = "(Semana no disponible)"
    if 'fecha' in df_filtered.columns and not df_filtered['fecha'].dropna().empty:
        try:
            dates = pd.to_datetime(df_filtered['fecha'].dropna())
            min_date = dates.min()
            max_date = dates.max()
            min_date_str = min_date.strftime('%Y-%m-%d')
            max_date_str = max_date.strftime('%Y-%m-%d')
            range_text = f"Semana desde {min_date_str} a {max_date_str}"
        except:
            pass

    # Subtotales y totales
    subtotals = {
        'partos': df_filtered['partos'].sum(),
        'cesareas': df_filtered['cesareas'].sum(),
        'varones': df_filtered['varones'].sum(),
        'hembras': df_filtered['hembras'].sum(),
        'gemelar': df_filtered['gemelar'].sum(),
        'mto': df_filtered['mto'].sum(),
        'PEH': df_filtered['PEH'].sum()
    }
    totals = {
        'partos_cesareas': subtotals['partos'] + subtotals['cesareas'],
        'varones_hembras': subtotals['varones'] + subtotals['hembras']
    }

    # Construcción del PDF
    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    pdf.set_font(family="Arial", size=14, style='B')
    pdf.cell(0, 10, range_text, ln=1, align='J')
    pdf.ln(10)

    pdf.set_font(family="Arial", size=10, style='')
    line_height = pdf.font_size * 1.5
    page_width = pdf.w - 20
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    num_cols = len(df_filtered.columns)
    col_width = page_width / num_cols
    col_widths = [col_width * 1.5] + [col_width * 0.85 for _ in range(num_cols - 1)]
    col_widths = [w * (page_width / sum(col_widths)) for w in col_widths]

    # Encabezados de columnas
    col_headers = [str(col).title() for col in df_filtered.columns]
    max_header_lines = max(len(pdf.multi_cell(w, line_height, txt, border=0, align='J', split_only=True)) 
                           for txt, w in zip(col_headers, col_widths))
    max_header_height = max_header_lines * line_height

    start_y = pdf.get_y()

    pdf.set_fill_color(158, 185, 212)
    pdf.rect(10, start_y, page_width, max_header_height, style='F')

    pdf.set_text_color(0, 0, 0)
    start_x = 10
    for txt, width in zip(col_headers, col_widths):
        pdf.set_xy(start_x, start_y)
        pdf.multi_cell(width, line_height, txt, border=0, align='J')
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

    # Filas de datos
    row_index = 0
    for _, row in df_filtered.iterrows():
        cell_texts = [str(row[col]) if row[col] is not None else "" for col in df_filtered.columns]
        max_lines = max(len(pdf.multi_cell(w, line_height, t, border=0, align='J', split_only=True)) 
                        for t, w in zip(cell_texts, col_widths))
        row_height = max_lines * line_height

        start_y = pdf.get_y()
        pdf.set_fill_color(240, 240, 240) if row_index % 2 == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.rect(10, start_y, page_width, row_height, style='F')

        start_x = 10
        for text, width in zip(cell_texts, col_widths):
            pdf.set_xy(start_x, start_y)
            pdf.multi_cell(width, line_height, text, border=0, align='J')
            start_x += width

        pdf.rect(10, start_y, page_width, row_height)
        current_x = 10
        for width in col_widths:
            pdf.line(current_x, start_y, current_x, start_y + row_height)
            current_x += width
        pdf.line(10, start_y + row_height, 10 + page_width, start_y + row_height)
        pdf.set_xy(10, start_y + row_height)
        row_index += 1

    # Subtotales
    pdf.set_font(family="Arial", size=10, style='B')
    subtotal_texts = [
        'Subtotal',
        str(subtotals['partos']),
        str(subtotals['cesareas']),
        str(subtotals['varones']),
        str(subtotals['hembras']),
        str(subtotals['gemelar']),
        str(subtotals['mto']),
        str(subtotals['PEH'])
    ]
    max_sub_lines = max(len(pdf.multi_cell(w, line_height, t, border=0, align='J', split_only=True)) 
                        for t, w in zip(subtotal_texts, col_widths))
    sub_row_height = max_sub_lines * line_height

    start_y = pdf.get_y()
    pdf.set_fill_color(200, 220, 240)
    pdf.rect(10, start_y, page_width, sub_row_height, style='F')

    start_x = 10
    for text, width in zip(subtotal_texts, col_widths):
        pdf.set_xy(start_x, start_y)
        pdf.multi_cell(width, line_height, text, border=0, align='J')
        start_x += width

    pdf.rect(10, start_y, page_width, sub_row_height)
    current_x = 10
    for width in col_widths:
        pdf.line(current_x, start_y, current_x, start_y + sub_row_height)
        current_x += width
    pdf.line(10, start_y + sub_row_height, 10 + page_width, start_y + sub_row_height)
    pdf.set_xy(10, start_y + sub_row_height)

    # Totales
    merged_widths = [col_widths[0], col_widths[1] + col_widths[2], col_widths[3] + col_widths[4], col_widths[5], col_widths[6], col_widths[7]]
    total_texts = [
        'Total',
        str(totals['partos_cesareas']),
        str(totals['varones_hembras']),
        str(subtotals['gemelar']),
        str(subtotals['mto']),
        str(subtotals['PEH'])
    ]
    max_total_lines = max(len(pdf.multi_cell(w, line_height, t, border=0, align='J', split_only=True)) 
                          for t, w in zip(total_texts, merged_widths))
    total_row_height = max_total_lines * line_height

    start_y = pdf.get_y()
    pdf.set_fill_color(180, 200, 220)
    pdf.rect(10, start_y, page_width, total_row_height, style='F')

    start_x = 10
    for text, width in zip(total_texts, merged_widths):
        pdf.set_xy(start_x, start_y)
        pdf.multi_cell(width, line_height, text, border=0, align='J')
        start_x += width
    pdf.rect(10, start_y, page_width, total_row_height)
    current_x = 10
    for width in merged_widths:
        pdf.line(current_x, start_y, current_x, start_y + total_row_height)
        current_x += width
    pdf.line(10, start_y + total_row_height, 10 + page_width, start_y + total_row_height)
    pdf.set_xy(10, start_y + total_row_height)

    # Final
    pdf.ln(15)
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
