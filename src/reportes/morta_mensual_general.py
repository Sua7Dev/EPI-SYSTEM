import streamlit as st
import pandas as pd
import sqlite3
import datetime
from io import BytesIO
import locale
from utils.pdfbanners import CustomPDF


def exportar_pdf_mortalidad_mensual_general(year=None, month=None, specific_date=None, start_date=None, end_date=None):
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

    try:
        with sqlite3.connect('hospital.db') as conn:
            query = """
                SELECT m.id_mortaM AS id, m.causas, m.n_casos, m.tasa, m.total, m.fecha_registro_formulario
                FROM mortalidad_mensual m
                WHERE NOT EXISTS (
                    SELECT 1 FROM mortalidad_mensual_infantil t1 WHERE t1.id_mortaM = m.id_mortaM
                    UNION
                    SELECT 1 FROM mortalidad_mensual_neonatal t2 WHERE t2.id_mortaM = m.id_mortaM
                )
                {where_clause}
            """
            params = []
            where_clause = ""
            if year and month:
                where_clause = "AND strftime('%Y-%m', m.fecha_registro_formulario) = ?"
                params = [f"{year}-{month:02d}"]
            elif specific_date:
                where_clause = "AND m.fecha_registro_formulario = ?"
                params = [specific_date]
            elif start_date and end_date:
                where_clause = "AND m.fecha_registro_formulario BETWEEN ? AND ?"
                params = [start_date, end_date]

            query = query.format(where_clause=where_clause)
            df = pd.read_sql_query(query, conn, params=params)
    except sqlite3.Error:
        df = pd.DataFrame()

    time_frame = "Mensual General"
    if year and month:
        time_frame = f"{format_spanish_date(f'{year}-{month:02d}')}"
    elif specific_date:
        time_frame = f"Fecha {specific_date.strftime('%d/%m/%Y')}"
    elif start_date and end_date:
        time_frame = f"Desde {start_date.strftime('%d/%m/%Y')} hasta {end_date.strftime('%d/%m/%Y')}"

    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(left=15, top=30, right=15)
    pdf.add_page()

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, f"Reporte de Mortalidad Mensual General - {time_frame}", ln=1, align='J')
    pdf.ln(6)

    if df.empty:
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 6, "NO HUBO CASOS", ln=1, align='J')
    else:
        df['mes'] = pd.to_datetime(df['fecha_registro_formulario']).dt.strftime('%Y-%m')
        unique_months = sorted(df['mes'].unique())
        selected_dates = ", ".join([format_spanish_date(m) for m in unique_months])

        df_grouped = df.groupby(['mes', df['causas'].str.lower()]).agg({
            'causas': 'first',
            'n_casos': 'sum',
            'tasa': 'first',
            'total': 'first'
        }).reset_index(level=1, drop=True).reset_index()

        for mes in unique_months:
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(0, 6, format_spanish_date(mes), ln=1, align='L')
            pdf.ln(3)

            df_mes = df_grouped[df_grouped['mes'] == mes][['causas', 'n_casos', 'tasa', 'total']]
            
            if df_mes.empty:
                pdf.set_font("Arial", size=9)
                pdf.cell(0, 5, "No hubo casos", ln=1, align='L')
            else:
                table_width = 160
                col_widths = [90, 35, 35]
                pdf.set_x((210 - table_width) / 2)
                pdf.set_font("Arial", 'B', 9)
                pdf.cell(col_widths[0], 6, "Causas", 1, 0, 'J')
                pdf.cell(col_widths[1], 6, "N. Casos", 1, 0, 'J')
                pdf.cell(col_widths[2], 6, "Tasa (%)", 1, 1, 'J')
                
                pdf.set_font("Arial", size=8)
                for _, row in df_mes.iterrows():
                    pdf.set_x((210 - table_width) / 2)
                    pdf.cell(col_widths[0], 6, row['causas'][:50], 1, 0, 'L')
                    pdf.cell(col_widths[1], 6, str(row['n_casos']), 1, 0, 'J')
                    pdf.cell(col_widths[2], 6, row['tasa'], 1, 1, 'J')
                
                total = df_mes['total'].iloc[0] if not df_mes['total'].empty else 0
                pdf.set_x((210 - table_width) / 2)
                pdf.set_font("Arial", 'B', 9)
                pdf.cell(col_widths[0], 6, "Total", 1, 0, 'J')
                pdf.cell(col_widths[1] + col_widths[2], 6, str(total), 1, 1, 'J')
            
            pdf.ln(5)

    pdf.set_title(f"Reporte_Mortalidad_Mensual_General_{datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}")
    pdf.set_author("EPI-SYSTEM")
    buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_output)
    buffer.seek(0)
    return buffer