import pandas as pd
import os
import streamlit as st
from io import BytesIO
from utils.pdfbanners import CustomPDF

DB_PATH = os.getenv("hospital.db", "hospital.db")
DATE_FORMAT = 'DD/MM/YYYY'

# Canonical order of ALL numeric columns (pre-PEH rename)
ALL_NUM_COLS = ["partos", "cesareas", "varones", "hembras", "gemelar", "mto", "partos_extrahospitalarios"]

# Label map (after PEH rename)
LABEL_MAP = {
    "fecha":    "Fecha",
    "partos":   "Partos",
    "cesareas": "Cesareas",
    "varones":  "Varones",
    "hembras":  "Hembras",
    "gemelar":  "Gemelar",
    "mto":      "MTO",
    "PEH":      "PEH",
}

SEX_COLS  = {"varones", "hembras"}
TIPO_COLS = {"partos", "cesareas", "gemelar", "mto", "PEH"}


def _safe(text):
    """Sanitize string so it can be encoded as latin-1 by fpdf."""
    return text.encode("latin-1", errors="replace").decode("latin-1")


def _build_report_context(columnas_activas, filtros_label):
    """
    Returns (title, subtitle, table_num_cols, highlight_cols).
    table_num_cols uses post-rename names (PEH instead of partos_extrahospitalarios).
    highlight_cols is a set of post-rename column names that should be visually highlighted.
    """
    sexo_label = filtros_label.get("sexo", "Todos")
    tipo_label = filtros_label.get("tipo", "Todos")
    has_sexo   = sexo_label != "Todos"
    has_tipo   = tipo_label != "Todos"

    # Normalize to post-rename names
    active      = ["PEH" if c == "partos_extrahospitalarios" else c for c in columnas_activas]
    ALL_PEH     = ["partos", "cesareas", "varones", "hembras", "gemelar", "mto", "PEH"]

    if not has_sexo and not has_tipo:
        return ("REPORTE GENERAL DE NATALIDAD", None, ALL_PEH, set())

    if has_sexo and not has_tipo:
        sex_sel = [c for c in active if c in SEX_COLS]
        return (
            "REPORTE POR SEXO - NATALIDAD",
            _safe("Sexo destacado: " + sexo_label),
            ALL_PEH,
            set(sex_sel),
        )

    if not has_sexo and has_tipo:
        tipo_active = [c for c in active if c in TIPO_COLS]
        return (
            "REPORTE POR TIPO DE NACIMIENTO",
            _safe("Tipo filtrado: " + tipo_label),
            tipo_active,
            set(),
        )

    # Both
    tipo_sel = [c for c in active if c in TIPO_COLS]
    sex_sel  = [c for c in active if c in SEX_COLS]
    combined = [c for c in ["partos", "cesareas", "varones", "hembras", "gemelar", "mto", "PEH"]
                if c in tipo_sel or c in sex_sel]
    return (
        "REPORTE FILTRADO - NATALIDAD",
        _safe("Tipo: " + tipo_label + "  |  Sexo destacado: " + sexo_label),
        combined,
        set(sex_sel),
    )


def _exportar_pdf_natalidad(df, nombre_archivo):
    # Read filter context
    columnas_activas = st.session_state.get("nat_columnas_activas", None) or list(ALL_NUM_COLS)
    filtros_label    = st.session_state.get("nat_filtros_label", {"sexo": "Todos", "tipo": "Todos"})

    title, subtitle, pdf_num_cols, highlight_cols = _build_report_context(columnas_activas, filtros_label)

    # Empty guard
    if df.empty:
        pdf = CustomPDF(orientation='P', unit='mm', format='A4')
        pdf.add_page()
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(0, 10, "No hay datos disponibles para generar el reporte", ln=1, align='J')
        buf = BytesIO()
        buf.write(pdf.output(dest='S').encode('latin1'))
        buf.seek(0)
        return buf

    # Prepare df
    df_filtered = df.copy()
    for col in ALL_NUM_COLS:
        if col not in df_filtered.columns:
            df_filtered[col] = 0

    cols_to_exclude = ['id', ' ', 'fecha_registro_formulario', 'id_doctor', 'registrado_por']
    df_filtered = df_filtered[[c for c in df_filtered.columns if c not in cols_to_exclude]]

    df_filtered['fecha_dt'] = pd.to_datetime(df_filtered['fecha'], dayfirst=True, errors='coerce')
    df_filtered['fecha']    = df_filtered['fecha_dt'].dt.strftime('%d/%m/%Y').fillna('Sin fecha')

    if 'partos_extrahospitalarios' in df_filtered.columns:
        df_filtered = df_filtered.rename(columns={'partos_extrahospitalarios': 'PEH'})

    for col in df_filtered.columns:
        if col not in ('fecha', 'fecha_dt'):
            df_filtered[col] = pd.to_numeric(df_filtered[col], errors='coerce').fillna(0).astype(int)

    df_filtered = df_filtered.sort_values(by='fecha_dt')
    df_filtered['iso_year'] = df_filtered['fecha_dt'].dt.isocalendar().year
    df_filtered['iso_week'] = df_filtered['fecha_dt'].dt.isocalendar().week

    # PDF setup
    pdf = CustomPDF(orientation='P', unit='mm', format='Letter')
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_left_margin(12.7)
    pdf.set_right_margin(12.7)
    page_width = pdf.w - 25.4

    # Title
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 10, _safe(title), ln=1, align='C')
    pdf.ln(1)

    if subtitle:
        pdf.set_font("Arial", 'I', 10)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 7, _safe(subtitle), ln=1, align='C')
        pdf.ln(1)

    if highlight_cols:
        highlighted_names = " / ".join(LABEL_MAP.get(c, c) for c in sorted(highlight_cols))
        pdf.set_font("Arial", 'B', 9)
        pdf.set_text_color(0, 100, 0)
        pdf.ln(1)

    pdf.set_text_color(0, 0, 0)

    # ── Summary box ──────────────────────────────────────────────────────────────
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 8, "RESUMEN ESTADISTICO", border=0, ln=1, align='L')

    def _col_val(col):
        return int(df_filtered[col].sum()) if col in df_filtered.columns else 0

    display_map = {
        "partos":   ("Partos",   _col_val("partos")),
        "cesareas": ("Cesareas", _col_val("cesareas")),
        "varones":  ("Varones",  _col_val("varones")),
        "hembras":  ("Hembras",  _col_val("hembras")),
        "gemelar":  ("Gemelar",  _col_val("gemelar")),
        "mto":      ("MTO",      _col_val("mto")),
        "PEH":      ("PEH",      _col_val("PEH")),
    }
    active_summary = [(lbl, val, col) for col, (lbl, val) in display_map.items() if col in pdf_num_cols]

    # Pre-compute total nacimientos
    sex_in_report = [c for c in ["varones", "hembras", "mto"] if c in pdf_num_cols]
    total_nac = sum(display_map[c][1] for c in sex_in_report) if sex_in_report else None

    pdf.set_font("Arial", '', 9)
    n_items = len(active_summary)

    if n_items > 0:
        per_row = min(n_items, 4)
        box_w   = page_width / per_row

        for idx, (lbl, val, col) in enumerate(active_summary):
            is_hl = col in highlight_cols
            if is_hl:
                pdf.set_fill_color(200, 240, 200)
                pdf.set_font("Arial", 'B', 9)
                pdf.cell(box_w, 10, _safe(">> " + lbl + ": " + str(val) + " <<"), border=1, align='C', fill=True)
                pdf.set_font("Arial", '', 9)
            else:
                pdf.set_fill_color(255, 255, 255)
                pdf.cell(box_w, 10, _safe(lbl + ": " + str(val)), border=1, align='C')
            if (idx + 1) % per_row == 0:
                pdf.ln(10)

        remainder = n_items % per_row  # 0 = last row was full

        if total_nac is not None:
            if remainder == 0:
                # Full last row -> TOTAL as a full-width bordered cell below
                pdf.set_fill_color(220, 220, 220)
                pdf.set_font("Arial", 'B', 9)
                pdf.cell(page_width, 10, "TOTAL NACIMIENTOS: " + str(total_nac), border=1, align='C', fill=True)
                pdf.ln(10)
            else:
                # Fill empty slots then put TOTAL in the trailing space
                empty_slots = per_row - remainder - 1
                for _ in range(empty_slots):
                    pdf.set_fill_color(250, 250, 250)
                    pdf.cell(box_w, 10, "", border=1)
                total_w = box_w * (empty_slots + 1)
                pdf.set_fill_color(220, 220, 220)
                pdf.set_font("Arial", 'B', 9)
                pdf.cell(total_w, 10, "TOTAL NACIMIENTOS: " + str(total_nac), border=1, align='C', fill=True)
                pdf.ln(10)
        else:
            if remainder != 0:
                pdf.ln(10)

    pdf.ln(5)

    # Table columns
    table_cols          = ["fecha"] + [c for c in pdf_num_cols if c in df_filtered.columns]
    col_headers_display = [LABEL_MAP.get(c, c) for c in table_cols]

    def _weight(c):
        if c == "fecha":         return 2.0
        if c in highlight_cols:  return 1.3
        return 1.0

    weights    = [_weight(c) for c in table_cols]
    col_widths = [w * page_width / sum(weights) for w in weights]

    # Weekly blocks
    def render_block(block_df, range_text):
        pdf.set_font("Arial", size=11, style='B')
        pdf.cell(0, 10, _safe(range_text), ln=1, align='L')
        pdf.ln(2)

        # Custom header with per-column color
        pdf.set_font("Arial", 'B', 9)
        for hdr, w, c in zip(col_headers_display, col_widths, table_cols):
            if c in highlight_cols:
                pdf.set_fill_color(0, 102, 51)
            else:
                pdf.set_fill_color(0, 51, 102)
            pdf.set_text_color(255, 255, 255)
            pdf.cell(w, 8, _safe(hdr), border=1, align='C', fill=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(8)

        pdf.set_font("Arial", size=9)
        fill = False
        for row in block_df.itertuples(index=False):
            for c, w in zip(table_cols, col_widths):
                v    = getattr(row, c, "-")
                text = str(v) if v is not None else "-"
                if c in highlight_cols:
                    pdf.set_fill_color(220, 255, 220)
                    pdf.set_font("Arial", 'B', 9)
                    pdf.cell(w, 7, _safe(text), border=1, align='C', fill=True)
                    pdf.set_font("Arial", '', 9)
                else:
                    bg = (242, 242, 242) if fill else (255, 255, 255)
                    pdf.set_fill_color(*bg)
                    pdf.cell(w, 7, _safe(text), border=1, align='C', fill=True)
            pdf.ln(7)
            fill = not fill

        # Week subtotal
        pdf.ln(2)
        pdf.set_font("Arial", 'B', 9)
        num_in_block = [c for c in pdf_num_cols if c in block_df.columns]
        if num_in_block:
            subtotals = block_df[num_in_block].sum()
            parts = []
            for c in num_in_block:
                marker = "(*)" if c in highlight_cols else ""
                parts.append(_safe(LABEL_MAP.get(c, c) + marker + ": " + str(int(subtotals[c]))))
            total_text = "TOTAL SEMANA: " + "  |  ".join(parts)
        else:
            total_text = "TOTAL SEMANA: -"

        pdf.set_fill_color(230, 230, 230)
        pdf.cell(page_width, 8, _safe(total_text), border=1, ln=1, align='C', fill=True)
        pdf.ln(10)

    grouped = df_filtered.groupby(['iso_year', 'iso_week'], sort=False)
    for (year, week), group_df in grouped:
        group_clean = group_df.drop(columns=['iso_year', 'iso_week', 'fecha_dt'], errors='ignore')
        min_date    = group_df['fecha_dt'].min()
        max_date    = group_df['fecha_dt'].max()
        range_text  = ("Semana " + str(week).zfill(2) + " (" + str(year) + ") - Del "
                       + min_date.strftime('%d/%m/%Y') + " al " + max_date.strftime('%d/%m/%Y'))
        render_block(group_clean, range_text)

    pdf.set_title(_safe(nombre_archivo))
    pdf.set_author("SEE")

    buffer = BytesIO()
    buffer.write(pdf.output(dest='S').encode('latin1'))
    buffer.seek(0)
    return buffer