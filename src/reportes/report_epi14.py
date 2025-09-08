import pandas as pd
import sqlite3
import datetime
from io import BytesIO
import locale
from utils.pdfbanners import CustomPDF
import os
DB_PATH = os.environ.get("AUTH_DB_PATH", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'

def exportar_pdf_epi14_semanal(year=None, week=None, specific_date=None, start_date=None, end_date=None):
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
        with sqlite3.connect(DB_PATH) as conn:
            query = """
                SELECT es.semana || '-' || strftime('%Y', es.fecha_registro_formulario) AS semana, 
                       es.causa, es.numero, es.sexo_edad,
                       SUM(es.numero) OVER (PARTITION BY es.semana || '-' || strftime('%Y', es.fecha_registro_formulario)) AS total,
                       es.fecha_registro_formulario
                FROM epi14_semanal es
                {where_clause}
            """
            params = []
            where_clause = ""
            if year and week:
                where_clause = "WHERE es.semana || '-' || strftime('%Y', es.fecha_registro_formulario) = ?"
                params = [f"Semana {week}-{year}"]
            elif specific_date:
                where_clause = "WHERE es.fecha_registro_formulario = ?"
                params = [specific_date]
            elif start_date and end_date:
                where_clause = "WHERE es.fecha_registro_formulario BETWEEN ? AND ?"
                params = [start_date, end_date]

            query = query.format(where_clause=where_clause)
            df = pd.read_sql_query(query, conn, params=params)
    except sqlite3.Error:
        df = pd.DataFrame()

    time_frame = "Semanal"
    if year and week:
        time_frame = f"Semana {week}-{year}"
    elif specific_date:
        time_frame = f"Fecha {specific_date.strftime('%d/%m/%Y')}"
    elif start_date and end_date:
        time_frame = f"Desde {start_date.strftime('%d/%m/%Y')} hasta {end_date.strftime('%d/%m/%Y')}"

    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(left=15, top=30, right=15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Encabezado
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 6, f"Reporte EPI-14 Semanal ({time_frame})", ln=1, align='J')
    pdf.ln(4)

    if df.empty:
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 6, "NO HUBO CASOS", ln=1, align='J')
    else:
        # Extraer semana y año en columnas separadas
        extracted = df['semana'].str.extract(r'Semana (\d+)-(\d{4})')
        df['week'] = pd.to_numeric(extracted[0], errors='coerce').fillna(0)
        df['year'] = pd.to_numeric(extracted[1], errors='coerce').fillna(0)
        
        df['causa_norm'] = df['causa'].str.strip().str.lower()

        # Agrupar datos
        df_grouped = (
            df.groupby(['week', 'year', 'causa_norm'])
            .agg({
                'numero': 'sum',
                'sexo_edad': lambda x: ', '.join(x.astype(str)),
                'total': 'first',
                'causa': 'first'  # conservar una escritura original de la causa
            })
            .reset_index()
            .drop(columns=['causa_norm'])
            .sort_values(['year', 'week', 'causa'])
        )

        unique_weeks = sorted(df_grouped[['week', 'year']].drop_duplicates().values, key=lambda x: (x[1], x[0]))
        selected_weeks = ", ".join([f"Semana {int(w)}-{int(y)}" for w, y in unique_weeks])

        for week, year in unique_weeks:
            pdf.set_font("Arial", 'B', 9)
            pdf.cell(0, 5, f"Semana {int(week)}-{int(year)}", ln=1, align='L')
            pdf.ln(2)

            df_week = df_grouped[(df_grouped['week'] == week) & (df_grouped['year'] == year)][['causa', 'numero', 'sexo_edad']]

            if df_week.empty:
                pdf.set_font("Arial", size=8)
                pdf.cell(0, 5, "No hubo casos", ln=1, align='L')
            else:
                table_width = 180  # Adjusted for portrait A4 (210 mm - 15 mm left - 15 mm right)
                col_widths = [90, 45, 45]  # Adjusted proportionally to fit within 180 mm
                pdf.set_x((210 - table_width) / 2)  # Centrar tabla
                pdf.set_font("Arial", 'B', 8)
                pdf.cell(col_widths[0], 6, "Causa", 1, 0, 'J')
                pdf.cell(col_widths[1], 6, "N. Casos", 1, 0, 'J')
                pdf.cell(col_widths[2], 6, "Sexo/Edad", 1, 1, 'J')
                
                pdf.set_font("Arial", size=7)
                for _, row in df_week.iterrows():
                    pdf.set_x((210 - table_width) / 2)
                    pdf.cell(col_widths[0], 6, str(row['causa'])[:50], 1, 0, 'L')  # Truncar para ajustar
                    pdf.cell(col_widths[1], 6, str(int(row['numero'])) if pd.notnull(row['numero']) else "", 1, 0, 'J')
                    pdf.cell(col_widths[2], 6, str(row['sexo_edad'])[:60], 1, 1, 'L')  # Truncar para ajustar
                
                # Mostrar un solo total por semana
                total = int(df_grouped[(df_grouped['week'] == week) & (df_grouped['year'] == year)]['total'].iloc[0]) if not df_grouped[(df_grouped['week'] == week) & (df_grouped['year'] == year)].empty else 0
                pdf.set_x((210 - table_width) / 2)
                pdf.set_font("Arial", 'B', 8)
                pdf.cell(sum(col_widths) - col_widths[1], 6, "Total", 1, 0, 'J')
                pdf.cell(col_widths[1], 6, str(total), 1, 1, 'J')
            
            pdf.ln(3)

    fecha_actual = datetime.datetime.now()
    fecha_str = fecha_actual.strftime("%d-%m-%Y")
    hora_str = fecha_actual.strftime("%I-%M-%S")
    meridiano = "PM" if fecha_actual.hour >= 12 else "AM"
    fecha_hora_str = f"{fecha_str}_{hora_str}_{meridiano}"

    pdf.set_title(f"Reporte_EPI14_Semanal_{fecha_hora_str}")
    pdf.set_author("EPI-SYSTEM")
    buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_output)
    buffer.seek(0)
    return buffer