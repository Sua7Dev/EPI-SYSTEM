import pandas as pd
import sqlite3
import datetime
from io import BytesIO
from descargas.descarga_reg_diario import _exportar_pdf
from utils.pdfbanners import CustomPDF
import os
DB_PATH = os.environ.get("DB_PATH", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'

def exportar_pdf_registro_diario(year=None, week=None, specific_date=None, start_date=None, end_date=None):
    # Expresión para convertir fd (DD/MM/YYYY) -> YYYY-MM-DD dentro de SQLite
    iso_fd = "substr(fd,7,4)||'-'||substr(fd,4,2)||'-'||substr(fd,1,2)"
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # Usamos la MISMA lógica que en "cargar": TRIM(semana) + año de fecha_registro_formulario
            base_query = f"""
                SELECT
                    TRIM(semana) || '-' || strftime('%Y', fecha_registro_formulario) AS semana,
                    fd, edad_sexo, mr, mo, so, cb, cd, gett, nc, peso, talla, autopsia,
                    fecha_registro_formulario
                FROM registro_diario
                {{where_clause}}
                ORDER BY semana, {iso_fd}
            """

            where_clause = ""
            params = []

            # Filtro por Semana + Año
            if year and week:
                where_clause = "WHERE (TRIM(semana) || '-' || strftime('%Y', fecha_registro_formulario)) = ?"
                params = [f"Semana {int(week)}-{int(year)}"]

            # Filtro por Fecha específica (comparando fd como ISO)
            elif specific_date:
                if isinstance(specific_date, datetime.date):
                    specific_iso = specific_date.strftime('%Y-%m-%d')
                else:
                    # En caso de que te llegue string 'YYYY-MM-DD' o datepicker
                    try:
                        specific_iso = pd.to_datetime(specific_date, dayfirst=False).strftime('%Y-%m-%d')
                    except Exception:
                        specific_iso = str(specific_date)
                where_clause = f"WHERE {iso_fd} = ?"
                params = [specific_iso]

            # Filtro por Rango de fechas (comparando fd como ISO)
            elif start_date and end_date:
                if isinstance(start_date, datetime.date):
                    start_iso = start_date.strftime('%Y-%m-%d')
                else:
                    start_iso = pd.to_datetime(start_date, dayfirst=False).strftime('%Y-%m-%d')
                if isinstance(end_date, datetime.date):
                    end_iso = end_date.strftime('%Y-%m-%d')
                else:
                    end_iso = pd.to_datetime(end_date, dayfirst=False).strftime('%Y-%m-%d')
                where_clause = f"WHERE {iso_fd} BETWEEN ? AND ?"
                params = [start_iso, end_iso]

            query = base_query.format(where_clause=where_clause)
            df = pd.read_sql_query(query, conn, params=params)

            # Mostrar 'fd' en DD/MM/YYYY en el PDF
            if not df.empty and "fd" in df.columns:
                # Si en BD 'fd' ya está en DD/MM/YYYY, esto solo normaliza; si viniera nulo, previene NaT
                df["fd"] = pd.to_datetime(df["fd"], format='%d/%m/%Y', errors="coerce").dt.strftime('%d/%m/%Y')

    except sqlite3.Error:
        df = pd.DataFrame()

    # Si no hay datos, devuelve PDF con "NO HUBO CASOS"
    if df.empty:
        pdf = CustomPDF(orientation='P', unit='mm', format='A4')
        pdf.set_margins(left=15, top=30, right=15)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 6, "NO HUBO CASOS", ln=1, align='J')
        pdf.set_title(f"Reporte_Registro_Diario_{datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}")
        pdf.set_author("EPI-SYSTEM")
        buffer = BytesIO()
        pdf_output = pdf.output(dest='S').encode('latin1')
        buffer.write(pdf_output)
        buffer.seek(0)
        return buffer

    # Orden y título
    df_sorted = df.sort_values(['semana', 'fd'])

    # Semana para el título del PDF
    if year and week:
        semana_val = f"Semana {int(week)}-{int(year)}"
    elif "semana" in df_sorted.columns and not df_sorted["semana"].dropna().empty:
        semana_val = str(df_sorted["semana"].iloc[0])
    else:
        semana_val = "Semana no disponible"

    return _exportar_pdf(
        df_sorted,
        f"Reporte_Registro_Diario_{datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}",
        semana=semana_val
    )
