from pathlib import Path
from fpdf import FPDF
from datetime import datetime

import sys


def get_project_root() -> Path:
    """Devuelve la raíz del proyecto, incluso empaquetado con PyInstaller."""
    if getattr(sys, "frozen", False):  # Si está empaquetado
        # Carpeta base del ejecutable
        return Path(sys._MEIPASS)
    else:
        # Carpeta base del código fuente
        return Path(__file__).resolve().parent.parent.parent

PROJECT_ROOT = get_project_root()
ASSETS_DIR = PROJECT_ROOT / "static" / "assets" / "imagenes"

class CustomPDF(FPDF):
    def __init__(self, orientation='P', unit='mm', format='Letter'):
        # Forzar Letter Portrait por defecto
        super().__init__(orientation=orientation, unit=unit, format=format)
        # Colores institucionales
        self.color_header_bg = (0, 51, 102)     # Azul Marino
        self.color_header_text = (255, 255, 255) # Blanco
        self.color_row_alt = (245, 247, 250)      # Gris claro
        self.color_border = (180, 180, 180) 
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        # Asegurar fuente estándar al inicio de página para evitar negritas heredadas
        self.set_font("Arial", '', 10)
        logo_path = ASSETS_DIR / "facil.png"
        if logo_path.exists():
            page_width = self.w  
            logo_width = 190 # Tamaño fijo profesional para Letter P
            x = (page_width - logo_width) / 2  
            self.image(str(logo_path), x=x, y=8, w=logo_width)
        self.ln(35) # Más espacio para evitar que el banner se sobreponga

    def footer(self):
        self.set_y(-18)
        # Forzar fuente normal e itálica específica para el footer
        self.set_font("Arial", "I", 8) 
        self.set_text_color(120, 120, 120)

        ahora = datetime.now()
        fecha_hora = ahora.strftime("%d/%m/%Y %I:%M %p")
        version = "v1.2"

        self.cell(
            0, 10,
            f"S.E.E {version} | Generado: {fecha_hora} | Página {self.page_no()}/{{nb}}",
            0, 0, "C"
        )
        # Reset para que lo siguiente no sea itálica
        self.set_font("Arial", "", 10)

    def draw_table_header(self, headers, widths, height=9):
        """Dibuja el encabezado de la tabla con estilo uniforme."""
        self.set_font("Arial", "B", 9) # Fuente un poco más pequeña para Portrait
        self.set_fill_color(*self.color_header_bg)
        self.set_text_color(*self.color_header_text)
        self.set_draw_color(*self.color_header_bg)
        
        for i, header in enumerate(headers):
            self.cell(widths[i], height, header, border=1, align='C', fill=True)
        self.ln()
        self.set_font("Arial", "", 9) 
        self.set_text_color(0, 0, 0)

    def draw_tabular_row(self, data, widths, fill=False):
        """Dibuja una fila uniforme con soporte multilínea y espaciado de seguridad."""
        lh = 4.5 # Línea base más fina para evitar amontonamiento
        padding = 3 # Padding vertical total
        
        # 1. Calcular altura máxima necesaria
        max_lines = 1
        for i, val in enumerate(data):
            lines = self.multi_cell(widths[i], lh, str(val), split_only=True)
            max_lines = max(max_lines, len(lines))
        
        row_height = (max_lines * lh) + padding

        # 2. Salto de página
        if self.get_y() + row_height > self.h - self.b_margin:
            self.add_page()
            return False

        # 3. Dibujar
        x_start = self.get_x()
        y_start = self.get_y()
        self.set_draw_color(*self.color_border)
        self.set_font("Arial", "", 8.5) # Un poco más pequeña para dar aire
        
        for i, val in enumerate(data):
            x = x_start + sum(widths[:i])
            self.set_xy(x, y_start)
            
            # Fondo
            if fill:
                self.set_fill_color(*self.color_row_alt)
            else:
                self.set_fill_color(255, 255, 255)
            
            # Celda contenedora
            self.cell(widths[i], row_height, '', border=1, fill=True)
            
            # Texto centrado verticalmente
            text_lines = self.multi_cell(widths[i], lh, str(val), split_only=True)
            text_height = len(text_lines) * lh
            # Ajuste de Y para centrado vertical con el padding
            self.set_xy(x, y_start + (row_height - text_height) / 2)
            self.multi_cell(widths[i], lh, str(val), border=0, align='C')

        self.set_y(y_start + row_height)
        return True