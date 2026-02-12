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

    # Letter format (215.9 x 279.4 mm)
    pdf = CustomPDF(orientation='P', unit='mm', format='Letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_left_margin(12.7) # 0.5 inch
    pdf.set_right_margin(12.7)
    page_width = pdf.w - 25.4

    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, "REPORTE GENERAL DE NATALIDAD", ln=1, align='C')
    pdf.ln(2)
    pdf.set_text_color(0, 0, 0)

    # --- RESUMEN ESTADÍSTICO ---
    total_partos = df_filtered['partos'].sum()
    total_cesareas = df_filtered['cesareas'].sum()
    total_varones = df_filtered['varones'].sum()
    total_hembras = df_filtered['hembras'].sum()
    total_nacimientos = total_varones + total_hembras + df_filtered['mto'].sum()  # Incluye varones, hembras y muertos (MTO)
    total_gemelares = df_filtered['gemelar'].sum()

    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 8, "RESUMEN ESTADÍSTICO", border=0, ln=1, align='L')
    
    box_w = page_width / 4
    pdf.set_font("Arial", '', 9)
    pdf.cell(box_w, 10, f"Partos: {total_partos}", border=1, align='C')
    pdf.cell(box_w, 10, f"Cesáreas: {total_cesareas}", border=1, align='C')
    pdf.cell(box_w, 10, f"Varones: {total_varones}", border=1, align='C')
    pdf.cell(box_w, 10, f"Hembras: {total_hembras}", border=1, align='C')
    pdf.ln(10)
    pdf.cell(box_w, 10, f"Gemelares: {total_gemelares}", border=1, align='C')
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(box_w * 3, 10, f"TOTAL NACIMIENTOS: {total_nacimientos}", border=1, align='C')
    pdf.ln(15)

    def render_block(block_df, range_text):
        pdf.set_font("Arial", size=11, style='B')
        pdf.cell(0, 10, range_text, ln=1, align='L')
        pdf.ln(2)

        cols = ['fecha', 'partos', 'cesareas', 'varones', 'hembras', 'gemelar', 'mto', 'PEH']
        col_headers = ['Fecha', 'Partos', 'Cesáreas', 'Varones', 'Hembras', 'Gemelar', 'MTO', 'PEH']

        # Al ser P (Letter), el ancho es ~190mm usable
        base_widths = [2.0] + [1.0] * 7
        total_weight = sum(base_widths)
        col_widths = [w * page_width / total_weight for w in base_widths]

        pdf.draw_table_header(col_headers, col_widths)
        
        pdf.set_font("Arial", size=10)
        fill = False
        for row in block_df.itertuples(index=False):
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
            
            res = pdf.draw_tabular_row(cell_texts, col_widths, fill=fill)
            if not res:
                pdf.draw_table_header(col_headers, col_widths)
                pdf.draw_tabular_row(cell_texts, col_widths, fill=fill)
            fill = not fill

        # Resumen de bloque (Semanas)
        pdf.ln(2)
        pdf.set_font("Arial", 'B', 10)
        subtotals = block_df[['partos', 'cesareas', 'varones', 'hembras', 'gemelar', 'mto', 'PEH']].sum()
        
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(page_width, 8, f"TOTAL SEMANA: Partos/Ces: {subtotals['partos']+subtotals['cesareas']} | Nacimientos: {subtotals['varones']+subtotals['hembras']+subtotals['mto']} | Gemelares: {subtotals['gemelar']} | PEH: {subtotals['PEH']}", border=1, ln=1, align='C', fill=True)
        pdf.ln(10)

    # Procesar cada semana
    grouped = df_filtered.groupby(['iso_year', 'iso_week'], sort=False)
    for (year, week), group_df in grouped:
        group_clean = group_df.drop(columns=['iso_year', 'iso_week', 'fecha_dt'], errors='ignore')
        min_date = group_df['fecha_dt'].min()
        max_date = group_df['fecha_dt'].max()
        range_text = f"Semana {week:02d} ({year}) - Del {min_date.strftime('%d/%m/%Y')} al {max_date.strftime('%d/%m/%Y')}"
        render_block(group_clean, range_text)

    pdf.set_title(nombre_archivo)
    pdf.set_author("EPI-SYSTEM")

    buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_output)
    buffer.seek(0)
    return buffer