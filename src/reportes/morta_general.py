
import pandas as pd
import sqlite3
import datetime
from fpdf import FPDF
from io import BytesIO
import locale
from utils.pdfbanners import CustomPDF
import os
DB_PATH = os.environ.get("DB_PATH", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'

def limpiar_dato(valor):
    if pd.isna(valor) or valor is None:
        return ""
    return str(valor).strip()

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

    try:
        with sqlite3.connect(DB_PATH) as conn:
            base_query = """
                SELECT m.historia_clinica, m.nombres_apellidos, pp.edad, m.fecha_nacimiento,
                       m.fecha_defuncion, m.hora_defuncion, mn.nombre_madre, mn.hora_nacimiento,
                       mn.semanas_gestacion, mn.peso, mn.talla, m.idx_ingreso, m.idx_defuncion,
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
            where_clause = ""
            if year:
                where_clause = "WHERE strftime('%Y', m.fecha_registro_formulario) = ?"
                params = [str(year)] * 3
            elif specific_date:
                where_clause = "WHERE m.fecha_registro_formulario = ?"
                params = [specific_date] * 3
            elif start_date and end_date:
                where_clause = "WHERE m.fecha_registro_formulario BETWEEN ? AND ?"
                params = [start_date, end_date] * 3

            query = base_query.format(where_clause=where_clause)
            df = pd.read_sql_query(query, conn, params=params)

    except sqlite3.Error:
        df = pd.DataFrame()

    time_frame = "General"
    if year:
        time_frame = f"Año {year}"
    elif specific_date:
        time_frame = f"Fecha {specific_date.strftime('%d/%m/%Y')}"
    elif start_date and end_date:
        time_frame = f"Desde {start_date.strftime('%d/%m/%Y')} hasta {end_date.strftime('%d/%m/%Y')}"

    pdf = CustomPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(left=15, top=30, right=15)
    pdf.add_page()

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 8, f"Reporte General de Mortalidad ({time_frame})", ln=1, align='J')
    pdf.ln(6)

    pdf.set_font("Arial", '', 12)
    line_height = pdf.font_size * 1.3

    tipos = [('Neonatal', 'Muerte Neonatal'), ('Infantil', 'Muerte Infantil'), ('Materna', 'Muerte Materna')]
    for tipo_db, tipo_nombre in tipos:
        sub_df = df[df['tipo'] == tipo_db]
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 6, f"--- {tipo_nombre} ---", ln=1, align='J')
        pdf.set_font("Arial", '', 12)

        if sub_df.empty:
            pdf.multi_cell(0, line_height, "NO HUBO CASOS", align='J')
            pdf.ln(line_height * 0.5)
        else:
            for idx, row in sub_df.iterrows():
                fields = [
                    f"Historia: {limpiar_dato(row['historia_clinica'])}",
                    f"Nombre: {limpiar_dato(row['nombres_apellidos'])}",
                    f"Edad: {limpiar_dato(row['edad'])}",
                    f"Fecha Nac.: {limpiar_dato(row['fecha_nacimiento'])}",
                    f"Fecha Def.: {limpiar_dato(row['fecha_defuncion'])}",
                    f"Hora Def.: {limpiar_dato(row['hora_defuncion'])}",
                    f"IDX Ingreso: {limpiar_dato(row['idx_ingreso'])}",
                    f"IDX Defunción: {limpiar_dato(row['idx_defuncion'])}"
                ]
                if tipo_db == 'Neonatal':
                    if pd.notnull(row['hora_nacimiento']):
                        fields.append(f"Hora Nac.: {limpiar_dato(row['hora_nacimiento'])}")
                    if pd.notnull(row['nombre_madre']):
                        fields.append(f"Nombre Madre: {limpiar_dato(row['nombre_madre'])}")
                    if pd.notnull(row['semanas_gestacion']):
                        fields.append(f"Sem. Gest.: {limpiar_dato(row['semanas_gestacion'])}")
                    if pd.notnull(row['peso']):
                        fields.append(f"Peso: {limpiar_dato(row['peso'])} kg")
                    if pd.notnull(row['talla']):
                        fields.append(f"Talla: {limpiar_dato(row['talla'])} cm")
                elif tipo_db == 'Infantil':
                    if pd.notnull(row['nombre_madre']):
                        fields.append(f"Nombre Madre: {limpiar_dato(row['nombre_madre'])}")

                # Procesar dirección para eliminar "No disponible" y componentes vacíos
                direccion = limpiar_dato(row['direccion'])
                if direccion:
                    # Dividir la dirección por comas y limpiar cada componente
                    componentes = [comp.strip() for comp in direccion.split(',')]
                    # Filtrar componentes vacíos o "No disponible"
                    componentes_validos = [comp for comp in componentes if comp and comp != "No disponible"]
                    # Volver a concatenar con comas
                    direccion_limpia = ", ".join(componentes_validos) if componentes_validos else None
                    if direccion_limpia:
                        fields.append(f"Dirección: {direccion_limpia}")

                text = ", ".join([f for f in fields if f])
                pdf.multi_cell(0, line_height, text, align='J')
                pdf.ln(line_height * 0.5)

        pdf.ln(line_height)

    pdf.set_title(f"Reporte_Mortalidad_General_{datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}")
    pdf.set_author("EPI-SYSTEM")
    buffer = BytesIO()
    pdf_output = pdf.output(dest='S').encode('latin1')
    buffer.write(pdf_output)
    buffer.seek(0)
    return buffer