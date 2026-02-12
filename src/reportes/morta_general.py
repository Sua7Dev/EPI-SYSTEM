import pandas as pd
import sqlite3
import datetime
from fpdf import FPDF
from io import BytesIO
import locale
from utils.pdfbanners import CustomPDF
import os

DB_PATH = os.getenv("hospital.db", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'


def limpiar_dato(valor):
    if pd.isna(valor) or valor is None:
        return ""
    return str(valor).strip()


def obtener_rango_fechas_mortalidad():
    """Devuelve la fecha mínima y máxima de registros de mortalidad."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            df = pd.read_sql_query("""
                SELECT fecha_registro_formulario
                FROM mortalidad
                WHERE fecha_registro_formulario IS NOT NULL
            """, conn)
        if df.empty:
            return datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()
        df['fecha_iso'] = pd.to_datetime(df['fecha_registro_formulario'], dayfirst=True, errors='coerce')
        # Filtrar fechas futuras inválidas que podrían venir de errores de parseo previos
        df = df[df['fecha_iso'] <= pd.Timestamp.now()]
        
        if df.empty:
            return datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()
            
        min_fecha = df['fecha_iso'].min().date()
        max_fecha = df['fecha_iso'].max().date()
        return min_fecha, max_fecha
    except Exception:
        return datetime.date.today() - datetime.timedelta(days=30), datetime.date.today()


def exportar_pdf_mortalidad_general(year=None, specific_date=None, start_date=None, end_date=None):
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

def consultar_mortalidad_general(year=None, specific_date=None, start_date=None, end_date=None):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            base_query = """
                SELECT m.historia_clinica, m.nombres_apellidos, pp.edad, m.fecha_nacimiento,
                       m.fecha_defuncion, m.hora_defuncion, mn.nombre_madre, mn.hora_nacimiento,
                       mn.semanas_gestacion, mn.peso, mn.talla, m.idx_ingreso, m.idx_defuncion,
                       m.fecha_registro_formulario,
                       COALESCE(p.nombre || ', ', '') || 
                       COALESCE(e.nombre || ', ', '') || 
                       COALESCE(c.nombre || ', ', '') || 
                       COALESCE(mu.nombre || ', ', '') || 
                       COALESCE(par.nombre || ', ', '') || 
                       d.descripcion AS direccion, 'Neonatal' AS tipo
                FROM mortalidad_neonatal mn
                JOIN mortalidad m ON mn.id_m = m.id_m
                JOIN persona_paciente pp ON m.id_paciente = pp.id_paciente
                LEFT JOIN direccion d ON m.id_direccion = d.id_direccion
                LEFT JOIN parroquia par ON d.id_parroquia = par.id_parroquia
                LEFT JOIN municipio mu ON par.id_municipio = mu.id_municipio
                LEFT JOIN ciudad c ON mu.id_ciudad = c.id_ciudad
                LEFT JOIN estado e ON c.id_estado = e.id_estado
                LEFT JOIN pais p ON e.id_pais = p.id_pais
                {where_clause}
                UNION
                SELECT m.historia_clinica, m.nombres_apellidos, pp.edad, m.fecha_nacimiento,
                       m.fecha_defuncion, m.hora_defuncion, mi.nombre_madre, NULL AS hora_nacimiento,
                       NULL AS semanas_gestacion, NULL AS peso, NULL AS talla,
                       m.idx_ingreso, m.idx_defuncion,
                       m.fecha_registro_formulario,
                       COALESCE(p.nombre || ', ', '') || 
                       COALESCE(e.nombre || ', ', '') || 
                       COALESCE(c.nombre || ', ', '') || 
                       COALESCE(mu.nombre || ', ', '') || 
                       COALESCE(par.nombre || ', ', '') || 
                       d.descripcion AS direccion, 'Infantil' AS tipo
                FROM mortalidad_infantil mi
                JOIN mortalidad m ON mi.id_m = m.id_m
                JOIN persona_paciente pp ON m.id_paciente = pp.id_paciente
                LEFT JOIN direccion d ON m.id_direccion = d.id_direccion
                LEFT JOIN parroquia par ON d.id_parroquia = par.id_parroquia
                LEFT JOIN municipio mu ON par.id_municipio = mu.id_municipio
                LEFT JOIN ciudad c ON mu.id_ciudad = c.id_ciudad
                LEFT JOIN estado e ON c.id_estado = e.id_estado
                LEFT JOIN pais p ON e.id_pais = p.id_pais
                {where_clause}
                UNION
                SELECT m.historia_clinica, m.nombres_apellidos, pp.edad, m.fecha_nacimiento,
                       m.fecha_defuncion, m.hora_defuncion, NULL AS nombre_madre, NULL AS hora_nacimiento,
                       NULL AS semanas_gestacion, NULL AS peso, NULL AS talla,
                       m.idx_ingreso, m.idx_defuncion,
                       m.fecha_registro_formulario,
                       COALESCE(p.nombre || ', ', '') || 
                       COALESCE(e.nombre || ', ', '') || 
                       COALESCE(c.nombre || ', ', '') || 
                       COALESCE(mu.nombre || ', ', '') || 
                       COALESCE(par.nombre || ', ', '') || 
                       d.descripcion AS direccion, 'Materna' AS tipo
                FROM mortalidad_materna mm
                JOIN mortalidad m ON mm.id_m = m.id_m
                JOIN persona_paciente pp ON m.id_paciente = pp.id_paciente
                LEFT JOIN direccion d ON m.id_direccion = d.id_direccion
                LEFT JOIN parroquia par ON d.id_parroquia = par.id_parroquia
                LEFT JOIN municipio mu ON par.id_municipio = mu.id_municipio
                LEFT JOIN ciudad c ON mu.id_ciudad = c.id_ciudad
                LEFT JOIN estado e ON c.id_estado = e.id_estado
                LEFT JOIN pais p ON e.id_pais = p.id_pais
                {where_clause}
            """

            params = []
            # Traemos todo y filtramos en Pandas para evitar problemas con formatos de fecha en SQLite
            df = pd.read_sql_query(base_query.format(where_clause=""), conn)

            if df.empty:
                return df
                
            # Convertir a datetime
            df['fecha_iso'] = pd.to_datetime(df['fecha_defuncion'], dayfirst=True, errors='coerce')

            if year:
                df = df[df['fecha_iso'].dt.year == int(year)]
            elif specific_date:
                df = df[df['fecha_iso'].dt.date == specific_date]
            elif start_date and end_date:
                df = df[(df['fecha_iso'].dt.date >= start_date) & 
                        (df['fecha_iso'].dt.date <= end_date)]
            
            return df
    except sqlite3.Error:
        return pd.DataFrame()

def exportar_pdf_mortalidad_general_df(df, year=None, specific_date=None, start_date=None, end_date=None):
    time_frame = "General"
    if year:
        time_frame = f"Año {year}"
    elif specific_date:
        if isinstance(specific_date, datetime.date):
             time_frame = f"Fecha {specific_date.strftime('%d/%m/%Y')}"
        else:
             time_frame = f"Fecha {specific_date}"
    elif start_date and end_date:
        time_frame = f"Desde {start_date.strftime('%d/%m/%Y')} hasta {end_date.strftime('%d/%m/%Y')}"

    # Letter Portrait: ~215.9mm x 279.4mm. Útil: ~190mm
    pdf = CustomPDF(orientation='P', unit='mm', format='Letter')
    pdf.alias_nb_pages()
    pdf.set_margins(left=12.7, top=15, right=12.7)
    pdf.add_page()
    page_width = pdf.w - 25.4

    # --- TÍTULO ---
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, f"REPORTE GENERAL DE MORTALIDAD", ln=1, align='C')
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 8, f"Período: {time_frame}", ln=1, align='C')
    pdf.ln(2)
    pdf.set_text_color(0, 0, 0)

    # --- RESUMEN (Uniforme) ---
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 8, "RESUMEN ESTADÍSTICO", border=0, ln=1, align='L')
    
    counts = df['tipo'].value_counts()
    neonatal_count = counts.get('Neonatal', 0)
    infantil_count = counts.get('Infantil', 0)
    materna_count = counts.get('Materna', 0)
    total_count = len(df)

    box_w = page_width / 4
    pdf.set_font("Arial", '', 9)
    pdf.cell(box_w, 10, f"Neonatal: {neonatal_count}", border=1, align='C')
    pdf.cell(box_w, 10, f"Infantil: {infantil_count}", border=1, align='C')
    pdf.cell(box_w, 10, f"Materna: {materna_count}", border=1, align='C')
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(box_w, 10, f"TOTAL: {total_count}", border=1, align='C')
    pdf.ln(15)

    # --- DATOS DETALLADOS ---
    tipos = [('Neonatal', 'MORTALIDAD NEONATAL'), ('Infantil', 'MORTALIDAD INFANTIL'), ('Materna', 'MORTALIDAD MATERNA')]
    
    for tipo_db, tipo_nombre in tipos:
        sub_df = df[df['tipo'] == tipo_db]
        if sub_df.empty:
            continue
            
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(0, 51, 102)
        pdf.cell(0, 10, f"{tipo_nombre}", ln=1)
        pdf.set_text_color(0, 0, 0)
        
        # Diseño consolidado para no perder info en Portrait
        if tipo_db == 'Neonatal':
            headers = ["PACIENTE / NACIMIENTO", "DATOS MATERNOS/CLÍN.", "DEFUNCIÓN / DIAGNÓSTICOS", "DIRECCIÓN"]
            widths = [48, 45, 50, 47] # Ajuste de anchos para Portrait Letter (Total ~190)
        elif tipo_db == 'Infantil':
            headers = ["PACIENTE / NACIMIENTO", "DATOS MATERNOS", "DEFUNCIÓN / DIAGNÓSTICOS", "DIRECCIÓN"]
            widths = [48, 45, 50, 47]
        else: # Materna
            headers = ["PACIENTE / NACIMIENTO", "DEFUNCIÓN / DIAGNÓSTICOS", "DIRECCIÓN"]
            widths = [55, 70, 65]

        pdf.draw_table_header(headers, widths)
        
        pdf.set_font("Arial", '', 8.5)
        fill = False
        for _, row in sub_df.iterrows():
            if tipo_db == 'Neonatal':
                col1 = f"Historia Clínica: {row['historia_clinica']}\nNombre: {row['nombres_apellidos']}\nEdad: {row['edad']} días\nNacimiento: {row['fecha_nacimiento']} ({row['hora_nacimiento']})"
                col2 = f"Madre: {row['nombre_madre']}\nSemanas Gest.: {row['semanas_gestacion']}\nPeso: {row['peso']} kg\nTalla: {row['talla']} cm"
                col3 = f"Defunción: {row['fecha_defuncion']} ({row['hora_defuncion']})\nDiag. Ingreso: {row['idx_ingreso']}\nDiag. Defunción: {row['idx_defuncion']}"
                col4 = f"Dirección:\n{row['direccion']}"
                vals = [col1, col2, col3, col4]
            elif tipo_db == 'Infantil':
                col1 = f"Historia Clínica: {row['historia_clinica']}\nNombre: {row['nombres_apellidos']}\nEdad: {row['edad']} meses\nNacimiento: {row['fecha_nacimiento']}"
                col2 = f"Madre: {row['nombre_madre']}"
                col3 = f"Defunción: {row['fecha_defuncion']} ({row['hora_defuncion']})\nDiag. Ingreso: {row['idx_ingreso']}\nDiag. Defunción: {row['idx_defuncion']}"
                col4 = f"Dirección:\n{row['direccion']}"
                vals = [col1, col2, col3, col4]
            else: # Materna
                col1 = f"Historia Clínica: {row['historia_clinica']}\nNombre: {row['nombres_apellidos']}\nEdad: {row['edad']} años\nNacimiento: {row['fecha_nacimiento']}"
                col2 = f"Defunción: {row['fecha_defuncion']} ({row['hora_defuncion']})\nDiag. Ingreso: {row['idx_ingreso']}\nDiag. Defunción: {row['idx_defuncion']}"
                col3 = f"Dirección:\n{row['direccion']}"
                vals = [col1, col2, col3]
            
            res = pdf.draw_tabular_row([limpiar_dato(v) for v in vals], widths, fill=fill)
            
            if not res:
                pdf.draw_table_header(headers, widths)
                pdf.draw_tabular_row([limpiar_dato(v) for v in vals], widths, fill=fill)
            
            fill = not fill
            
        pdf.ln(10)

    pdf.set_title(f"Reporte_Mortalidad_{datetime.datetime.now().strftime('%d-%m-%Y')}")
    pdf.set_author("EPI-SYSTEM")
    
    buffer = BytesIO()
    # fpdf2 uses output(dest='S') or output() returns bytes depending on version
    # Here we use the standard way for this codebase
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_bytes)
    buffer.seek(0)
    return buffer
