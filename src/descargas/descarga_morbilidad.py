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
    # Formato Carta (Carta) P: ~216x279mm. Útil: ~190mm
    pdf = CustomPDF(orientation='P', unit='mm', format='Letter')
    pdf.alias_nb_pages()
    pdf.set_margins(15, 20, 15)
    page_width = pdf.w - 30

    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, "REPORTE DE DENUNCIAS OBLIGATORIAS (MORBILIDAD)", ln=1, align='C')
    pdf.ln(2)
    pdf.set_text_color(0, 0, 0)

    if df.empty:
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, "NO SE ENCONTRARON REGISTROS", ln=1, align='C')
        buffer = BytesIO()
        pdf.set_title(nombre_archivo)
        pdf.output(buffer)
        buffer.seek(0)
        return buffer

    # --- RESUMEN ESTADÍSTICO ---
    total_casos = len(df)
    # Contar diagnósticos más comunes
    top_diag = df['diagnostico'].value_counts().head(3)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 8, "RESUMEN ESTADÍSTICO", border=0, ln=1, align='L')
    
    box_w = pdf.w - 2 * pdf.l_margin

    pdf.set_font("Arial", '', 9)
    # Ahora la celda ocupará todo el ancho disponible
    pdf.cell(box_w, 10, f"Total de Casos: {total_casos}", border=1, align='C')

    pdf.ln(15)

    from utils.validaciones import parse_fecha_robusta
    df = df.copy()
    df['fecha_dt'] = df['fecha_registro_formulario'].apply(parse_fecha_robusta)
    df['fecha_str'] = df['fecha_dt'].dt.strftime('%d/%m/%Y').fillna('Sin fecha')

    headers = ['#', 'Enfermedad / Diagnóstico', 'Nombres y Apellidos', 'Edad', 'Dirección de Hogar']
    pct = [0.08, 0.28, 0.28, 0.08, 0.28]
    col_widths = [usable_width * p for usable_width, p in zip([page_width]*5, pct)]

    def clean_direccion(text):
        if not text: return "No disponible"
        componentes = [comp.strip() for comp in str(text).split(',') if comp.strip() and comp.strip().lower() != "no disponible"]
        return ", ".join(componentes) if componentes else "No disponible"

    df['_id_num'] = pd.to_numeric(df.get('id', pd.Series(dtype='float')), errors='coerce').fillna(0).astype(int)
    df = df.sort_values(by=['fecha_dt', '_id_num'], ascending=[True, True]).reset_index(drop=True)

    def print_group_header(fecha):
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 8, f"Fecha de Registro: {fecha}", ln=1, align='L')
        pdf.ln(2)
        pdf.draw_table_header(headers, col_widths)
        pdf.set_font("Arial", '', 9)

    first_group = True
    for fecha, df_fecha in df.groupby('fecha_str', sort=False):
        if not first_group:
            pdf.ln(5)

        print_group_header(fecha)

        fill = False
        for seq, (_, row) in enumerate(df_fecha.reset_index(drop=True).iterrows(), start=1):
            diagnostico = str(row.get('diagnostico', '') or '')
            nombres = str(row.get('nombres_apellidos', '') or '')
            edad = f"{int(row.get('edad'))}" if pd.notnull(row.get('edad')) else ''
            direccion = clean_direccion(row.get('direccion_hogar', ''))
            
            cells = [str(seq), diagnostico, nombres, edad, direccion]
            
            res = pdf.draw_tabular_row(cells, col_widths, fill=fill)
            if not res:
                print_group_header(fecha)
                pdf.draw_tabular_row(cells, col_widths, fill=fill)
            
            fill = not fill

        first_group = False

    buffer = BytesIO()
    pdf.set_title(nombre_archivo)
    pdf.set_author("SEE")
    buffer.write(pdf.output(dest='S').encode('latin1'))
    buffer.seek(0)
    return buffer