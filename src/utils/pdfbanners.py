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
    def header(self):
        logo_path = ASSETS_DIR / "facil.png"
        if logo_path.exists():
            page_width = self.w  
            logo_width = 180    
            x = (page_width - logo_width) / 2  
            self.image(str(logo_path), x=x, y=8, w=logo_width)
        self.ln(30)

    def footer(self):
        self.set_y(-20)
        self.set_font("Arial", "B", 9)

        ahora = datetime.now()
        hora_str = ahora.strftime("%I:%M")  
        meridiano = "PM" if ahora.hour >= 12 else "AM"
        fecha_str = ahora.strftime("%d/%m/%Y")

        fecha_hora = f"{fecha_str} {hora_str} {meridiano}"
        version = "v1.0"
        anio_programa = "2025"

        self.cell(
            0, 10,
            f"Generado por: EPI-SYSTEM {version} {anio_programa} | Fecha y hora: {fecha_hora}",
            0, 0, "C"
        )