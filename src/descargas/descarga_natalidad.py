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
        pdf.set_font("Arial", size=12, style='B')
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

    columns_to_exclude = ['id', ' ', 'fecha_registro_formulario', 'id_doctor']
    df_filtered = df_filtered[[col for col in df_filtered.columns if col not in columns_to_exclude]]

    # Normalizar fecha de forma segura
    df_filtered['fecha_dt'] = pd.to_datetime(df_filtered['fecha'], dayfirst=True, errors='coerce')
    df_filtered['fecha'] = df_filtered['fecha_dt'].dt.strftime('%d/%m/%Y')
    df_filtered['fecha'] = df_filtered['fecha'].fillna('Sin fecha')

    # Convertir columnas numéricas
    for col in ['partos', 'cesareas', 'varones', 'hembras', 'gemelar', 'mto', 'partos_extrahospitalarios']:
        df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce').fillna(0).astype(int)

    if 'partos_extrahospitalarios' in df_filtered.columns:
        df_filtered = df_filtered.rename(columns={'partos_extrahospitalarios': 'PEH'})

    df_filtered = df_filtered.sort_values(by='fecha_dt')

    # Agrupar por semana ISO
    df_filtered['iso_year'] = df_filtered['fecha_dt'].dt.isocalendar().year
    df_filtered['iso_week'] = df_filtered['fecha_dt'].dt.isocalendar().week

    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_left_margin(10)
    pdf.set_right_margin(10)
    page_width = pdf.w - 20

    pdf.set_font("Arial", size=12)
    line_height = pdf.font_size * 1.5

    # Líneas más finas
    pdf.set_line_width(0.2)

    def ensure_space(required_mm):
        if pdf.get_y() + required_mm > pdf.h - pdf.b_margin:
            pdf.add_page()

    def render_block(block_df, range_text):
        # Estimar altura aproximada que ocupará toda la tabla (sin subtotales/totales aún)
        num_rows = len(block_df)
        estimated_row_height = line_height * 1.2  # margen conservador
        estimated_table_height = 30 + (num_rows * estimated_row_height) + 50  # título + cabecera + filas + subtotales/totales + margen

        # Si no cabe completa en la página actual → nueva página antes de empezar
        if pdf.get_y() + estimated_table_height > pdf.h - pdf.b_margin:
            pdf.add_page()

        # Título de la semana (en negrita para destacar)
        pdf.set_font("Arial", size=12, style='B')
        pdf.ln(5)
        pdf.cell(0, 10, range_text, ln=1, align='C')
        pdf.ln(8)

        # Volver al tamaño 10 sin negrita para toda la tabla
        pdf.set_font("Arial", size=10)

        cols = ['fecha', 'partos', 'cesareas', 'varones', 'hembras', 'gemelar', 'mto', 'PEH']
        col_headers = ['Fecha', 'Partos', 'Cesáreas', 'Varones', 'Hembras', 'Gemelar', 'MTO', 'PEH']

        base_widths = [1.8] + [0.8] * 7
        total_weight = sum(base_widths)
        col_widths = [w * page_width / total_weight for w in base_widths]

        # Altura de cabecera
        max_header_lines = max(
            len(pdf.multi_cell(w, line_height, txt, border=0, align='C', split_only=True))
            for txt, w in zip(col_headers, col_widths)
        )
        header_height = max_header_lines * line_height

        def draw_header(y):
            pdf.set_fill_color(158, 185, 212)
            pdf.rect(10, y, page_width, header_height, 'F')
            pdf.set_text_color(0, 0, 0)
            x = 10
            for txt, w in zip(col_headers, col_widths):
                pdf.set_xy(x, y)
                pdf.multi_cell(w, line_height, txt, align='C')
                x += w
            pdf.set_draw_color(0, 0, 0)
            pdf.rect(10, y, page_width, header_height)
            x = 10
            for w in col_widths:
                pdf.line(x, y, x, y + header_height)
                x += w
            pdf.line(10, y + header_height, 10 + page_width, y + header_height)

        y = pdf.get_y()
        draw_header(y)
        pdf.set_y(y + header_height)

        # Filas de datos
        for i, row in enumerate(block_df.itertuples(index=False)):
            cell_texts = [
                getattr(row, 'fecha', 'Sin fecha'),
                str(getattr(row, 'partos', 0)),
                str(getattr(row, 'cesareas', 0)),
                str(getattr(row, 'varones', 0)),
                str(getattr(row, 'hembras', 0)),
                str(getattr(row, 'gemelar', 0)),
                str(getattr(row, 'mto', 0)),
                str(getattr(row, 'PEH', 0))
            ]

            max_lines = max(
                len(pdf.multi_cell(w, line_height, t, border=0, align='C', split_only=True))
                for t, w in zip(cell_texts, col_widths)
            )
            row_height = max_lines * line_height

            # Si una fila individual no cabe, pasamos a nueva página y repetimos cabecera
            if pdf.get_y() + row_height + 50 > pdf.h - pdf.b_margin:  # +50 para subtotales/totales
                pdf.add_page()
                y = pdf.get_y()
                draw_header(y)
                pdf.set_y(y + header_height)

            y = pdf.get_y()
            pdf.set_fill_color(240, 240, 240) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
            pdf.rect(10, y, page_width, row_height, 'F')

            x = 10
            for text, w in zip(cell_texts, col_widths):
                pdf.set_xy(x, y)
                pdf.multi_cell(w, line_height, text, align='C')
                x += w

            pdf.rect(10, y, page_width, row_height)
            x = 10
            for w in col_widths:
                pdf.line(x, y, x, y + row_height)
                x += w
            pdf.line(10, y + row_height, 10 + page_width, y + row_height)
            pdf.set_y(y + row_height)

        # Subtotal y Total (tamaño 10, sin negrita)
        subtotals = {
            'partos': block_df['partos'].sum(),
            'cesareas': block_df['cesareas'].sum(),
            'varones': block_df['varones'].sum(),
            'hembras': block_df['hembras'].sum(),
            'gemelar': block_df['gemelar'].sum(),
            'mto': block_df['mto'].sum(),
            'PEH': block_df['PEH'].sum(),
        }
        totals = {
            'partos_cesareas': subtotals['partos'] + subtotals['cesareas'],
            'varones_hembras': subtotals['varones'] + subtotals['hembras']
        }

        # Subtotal
        subtotal_texts = ['Subtotal'] + [str(subtotals[c]) for c in ['partos', 'cesareas', 'varones', 'hembras', 'gemelar', 'mto', 'PEH']]
        ensure_space(50)
        y = pdf.get_y()
        pdf.set_fill_color(200, 220, 240)
        pdf.rect(10, y, page_width, line_height * 2, 'F')
        x = 10
        for text, w in zip(subtotal_texts, col_widths):
            pdf.set_xy(x, y + 4)
            pdf.multi_cell(w, line_height, text, align='C')
            x += w
        pdf.rect(10, y, page_width, line_height * 2)
        x = 10
        for w in col_widths:
            pdf.line(x, y, x, y + line_height * 2)
            x += w
        pdf.line(10, y + line_height * 2, 10 + page_width, y + line_height * 2)
        pdf.set_y(y + line_height * 2)

        # Total
        merged_widths = [col_widths[0], sum(col_widths[1:3]), sum(col_widths[3:5])] + col_widths[5:]
        total_texts = ['Total', str(totals['partos_cesareas']), str(totals['varones_hembras'])] + [
            str(subtotals['gemelar']), str(subtotals['mto']), str(subtotals['PEH'])
        ]
        y = pdf.get_y()
        pdf.set_fill_color(180, 200, 220)
        pdf.rect(10, y, page_width, line_height * 2, 'F')
        x = 10
        for text, w in zip(total_texts, merged_widths):
            pdf.set_xy(x, y + 4)
            pdf.multi_cell(w, line_height, text, align='C')
            x += w
        pdf.rect(10, y, page_width, line_height * 2)
        x = 10
        for w in merged_widths:
            pdf.line(x, y, x, y + line_height * 2)
            x += w
        pdf.line(10, y + line_height * 2, 10 + page_width, y + line_height * 2)

        pdf.ln(15)  # Espacio entre semanas

    # Procesar cada semana
    grouped = df_filtered.groupby(['iso_year', 'iso_week'], sort=False)
    for (year, week), group_df in grouped:
        group_clean = group_df.drop(columns=['iso_year', 'iso_week', 'fecha_dt'], errors='ignore')

        min_date = group_df['fecha_dt'].min()
        max_date = group_df['fecha_dt'].max()
        if pd.notna(min_date) and pd.notna(max_date):
            range_text = f"Semana {week:02d} del {year} - {min_date.strftime('%d/%m/%Y')} al {max_date.strftime('%d/%m/%Y')}"
        else:
            range_text = f"Semana {week:02d} del {year} - Fechas no disponibles"

        render_block(group_clean, range_text)

    pdf.set_title(nombre_archivo)
    pdf.set_author("EPI-SYSTEM")

    buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_output)
    buffer.seek(0)
    return buffer