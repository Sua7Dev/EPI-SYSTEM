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
        pdf.set_font(family="Arial", size=12, style='B')
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

    # Normalizar fecha a datetime y formato para impresión
    df_filtered['fecha_dt'] = pd.to_datetime(df_filtered['fecha'], errors='coerce')
    df_filtered['fecha'] = df_filtered['fecha_dt'].dt.strftime('%d/%m/%Y')

    for col in ['partos', 'cesareas', 'varones', 'hembras', 'gemelar', 'mto', 'partos_extrahospitalarios']:
        df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce').fillna(0).astype(int)

    if 'partos_extrahospitalarios' in df_filtered.columns:
        df_filtered = df_filtered.rename(columns={'partos_extrahospitalarios': 'PEH'})

    df_filtered = df_filtered.sort_values(by='fecha_dt')

    # Agrupar por semana ISO (año + semana) para generar un bloque por semana
    df_filtered['iso_year'] = df_filtered['fecha_dt'].dt.isocalendar().year
    df_filtered['iso_week'] = df_filtered['fecha_dt'].dt.isocalendar().week

    # Precalcular subtotales/totales por todo el conjunto si los necesitas (opcional)
    # Se generarán subtotales por bloque más abajo.

    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    page_width = pdf.w - 20
    pdf.set_font(family="Arial", size=10, style='')

    line_height = pdf.font_size * 1.5

    # helper para verificar espacio en la página y añadir nueva página si falta espacio
    def ensure_space(required_mm=60):
        if pdf.get_y() + required_mm > pdf.h - pdf.b_margin:
            pdf.add_page()

    # helper que dibuja la tabla para un df de bloque
    def render_block(block_df, range_text):
        # Header (margen superior y texto centrado)
        pdf.set_font(family="Arial", size=12, style='')
        pdf.ln(4)
        ensure_space(40)
        pdf.cell(0, 10, range_text, ln=1, align='C')
        pdf.ln(6)

        # Preparar columnas y anchos
        cols = [c for c in block_df.columns if c not in ['fecha_dt', 'iso_year', 'iso_week']]
        num_cols = len(cols)
        col_width = page_width / num_cols if num_cols else page_width
        col_widths = [col_width * 1.5] + [col_width * 0.85 for _ in range(max(0, num_cols - 1))]
        col_widths = [w * (page_width / sum(col_widths)) for w in col_widths]

        # Cabecera
        col_headers = [str(col).title() for col in cols]
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

        # Filas
        row_index = 0
        for _, row in block_df.iterrows():
            cell_texts = [str(row[col]) if row[col] is not None else "" for col in cols]
            max_lines = max(len(pdf.multi_cell(w, line_height, t, border=0, align='J', split_only=True))
                            for t, w in zip(cell_texts, col_widths))
            row_height = max_lines * line_height

            # Si la fila no cabe, nueva página y volver a dibujar la cabecera del bloque
            if pdf.get_y() + row_height + 80 > pdf.h - pdf.b_margin:
                pdf.add_page()
                # redraw block title on new page
                pdf.set_font(family="Arial", size=14, style='')
                pdf.cell(0, 10, range_text + " (continuación)", ln=1, align='C')
                pdf.ln(6)
                # redraw header
                start_y = pdf.get_y()
                pdf.set_fill_color(158, 185, 212)
                pdf.rect(10, start_y, page_width, max_header_height, style='F')
                start_x = 10
                for txt, width in zip(col_headers, col_widths):
                    pdf.set_xy(start_x, start_y)
                    pdf.multi_cell(width, line_height, txt, border=0, align='J')
                    start_x += width
                pdf.rect(10, start_y, page_width, max_header_height)
                current_x = 10
                for width in col_widths:
                    pdf.line(current_x, start_y, current_x, start_y + max_header_height)
                    current_x += width
                pdf.line(10, start_y + max_header_height, 10 + page_width, start_y + max_header_height)
                pdf.set_xy(10, start_y + max_header_height)

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

        # Subtotales y totales del bloque
        subtotals = {
            'partos': block_df.get('partos', pd.Series(dtype=int)).sum(),
            'cesareas': block_df.get('cesareas', pd.Series(dtype=int)).sum(),
            'varones': block_df.get('varones', pd.Series(dtype=int)).sum(),
            'hembras': block_df.get('hembras', pd.Series(dtype=int)).sum(),
            'gemelar': block_df.get('gemelar', pd.Series(dtype=int)).sum(),
            'mto': block_df.get('mto', pd.Series(dtype=int)).sum(),
            'PEH': block_df.get('PEH', pd.Series(dtype=int)).sum()
        }
        totals = {
            'partos_cesareas': subtotals['partos'] + subtotals['cesareas'],
            'varones_hembras': subtotals['varones'] + subtotals['hembras']
        }

        pdf.set_font(family="Arial", size=12, style='')
        subtotal_texts = [
            'Subtotal'
        ] + [str(subtotals.get(k, 0)) for k in ['partos', 'cesareas', 'varones', 'hembras', 'gemelar', 'mto', 'PEH']]

        max_sub_lines = max(len(pdf.multi_cell(w, line_height, t, border=0, align='J', split_only=True))
                            for t, w in zip(subtotal_texts, col_widths))
        sub_row_height = max_sub_lines * line_height

        start_y = pdf.get_y()
        # Si no hay espacio para subtotales, nueva página
        if start_y + sub_row_height + 60 > pdf.h - pdf.b_margin:
            pdf.add_page()
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

        # Totales (simplificados en ancho)
        merged_widths = [col_widths[0]] + [sum(col_widths[1:3]) if len(col_widths) > 2 else col_widths[1]] + col_widths[3:]
        total_texts = [
            'Total',
            str(totals['partos_cesareas']),
            str(totals['varones_hembras'])
        ] + [str(subtotals.get(k, 0)) for k in ['gemelar', 'mto', 'PEH']]

        max_total_lines = max(len(pdf.multi_cell(w, line_height, t, border=0, align='J', split_only=True))
                              for t, w in zip(total_texts, merged_widths))
        total_row_height = max_total_lines * line_height

        start_y = pdf.get_y()
        if start_y + total_row_height + 40 > pdf.h - pdf.b_margin:
            pdf.add_page()
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

        pdf.ln(10)

    # Iterar por cada semana y renderizar su bloque (ordenado)
    grouped = df_filtered.groupby(['iso_year', 'iso_week'])
    for (y, w), group_df in grouped:
        # calculo min/max fecha del bloque para el header
        if not group_df['fecha_dt'].dropna().empty:
            min_date = group_df['fecha_dt'].min()
            max_date = group_df['fecha_dt'].max()
            min_date_str = min_date.strftime('%d/%m/%Y')
            max_date_str = max_date.strftime('%d/%m/%Y')
            range_text = f"Semana {w} de {y} - Desde {min_date_str} a {max_date_str}"
        else:
            range_text = f"Semana {w} de {y} - Fechas no disponibles"

        # quitar columnas auxiliares antes de pasar al render
        render_df = group_df.drop(columns=[c for c in ['fecha_dt', 'iso_year', 'iso_week'] if c in group_df.columns])
        render_block(render_df, range_text)

    # Final
    pdf.ln(8)
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