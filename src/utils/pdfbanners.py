from pathlib import Path
from fpdf import FPDF
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
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