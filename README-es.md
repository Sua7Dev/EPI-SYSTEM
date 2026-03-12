![SEE](https://i.imgur.com/GBdD7mx.png)
![Logo](https://i.imgur.com/SAHxoGy.png)


# Sistema de Estadísticas Epidemiológicas (SEE) (antes EPI-SYSTEM)

El sistema desarrollado es un entorno web de vigilancia epidemiológica orientada al Hospital Dr. Felipe Guevara Rojas. Su propósito es digitalizar y optimizar el registro, análisis y consulta de datos epidemiológicos, sustituyendo los procesos manuales en papel por una herramienta tecnológica eficiente, segura y accesible.

La aplicación, construida en Python (Streamlit) y respaldada por una base de datos relacional (SQLite/MySQL), integra los módulos de mortalidad, morbilidad, natalidad y demografía, permitiendo el registro, validación y consulta de información clínica y estadística. Además, incluye funcionalidades de autenticación segura, generación de reportes en PDF y visualización gráfica dinámica, facilitando la interpretación de tendencias de salud por año, sexo y grupos etarios.

En síntesis, se trata de una solución tecnológica que fortalece la gestión hospitalaria y la toma de decisiones en salud pública, garantizando seguridad, trazabilidad y accesibilidad de los datos epidemiológicos.

## Autores

- [@Sua7Dev](https://github.com/Sua7Dev)
- [@Gustav0H2O](https://github.com/Gustav0H2O)


## Implementación

Para implementar este proyecto:

### - Paso 1. Abra una terminal y navegue a la carpeta de su proyecto.
```bash
cd myproject
```
### - Paso 2. En tu terminal, escribe para clonar el repositorio:
```bash
git clone https://github.com/Sua7Dev/EPI-SYSTEM.git
```

### - Paso 3. crea un entorno virtual:
```bash
python -m venv .venv
```

### - Paso 4. Activar el entorno virtual (esto es para Windows PowerShell):
```bash
.venv\Scripts\Activate.ps1
```

### - Paso 5. instala las librerías necesarias:
```bash
pip install -r requirements.txt
```

### - Paso 6. Acceda a la carpeta src:
```bash
cd src
```

### - Paso 7. compilamos a .exe:
```bash
pyinstaller --clean --icon=../iconito.ico --onedir launcher.py --name SEE --collect-all streamlit --collect-all streamlit_extras --add-data "../static;static" --add-data "../.streamlit;.streamlit" --add-data "hospital.db;." --add-data "main.py;." --add-data "launcher.py;." --add-data "utils;utils" --add-data "db.py;." --add-data "pages;pages" --add-data "reportes;reportes" --add-data "descargas;descargas" --add-data "stats;stats" --hidden-import=streamlit.web.cli --hidden-import=importlib.metadata --hidden-import=fpdf --hidden-import=db --hidden-import=utils.sql_control --hidden-import=pandas --hidden-import=numpy --hidden-import=pyarrow --hidden-import=snowflake.connector --hidden-import=streamlit_extras --noupx --noconsole
```



## Ejecutar localmente

Para probar la página localmente antes de compilarla en .exe, puede ejecutar
```bash
cd src
```
```bash
streamlit run main.py
```

## Capturas de pantalla
- página de inicio
![iniciosesion](https://i.imgur.com/iq2mEc7.png)
- página de dashboard
![dashboard](https://i.imgur.com/cf0mlHg.png)



## Documentación

Manuales de usuario (en español)

[Admin](https://docs.google.com/document/d/1E493h8-7XwpHkWZRZZxG43KwKU4cTJ8Zkb3KiOXHFec/edit?usp=sharing)

[Doctor](https://docs.google.com/document/d/1SEgjlOTY88uGNEyolEECzOKYe6gAYwX2ukD0BNJ3tao/edit?usp=sharing)

[Secretaria](https://docs.google.com/document/d/1WJNMI8rx49F1U1FKIIaTP3K53h5kYPzYZaAn1-Vx-1Q/edit?usp=sharing )

## FAQ

#### 1. Mi PowerShell no me permite ejecutar scripts.

En la ventana de PowerShell, escriba el siguiente comando y presione Entrar:
```bash
Set-ExecutionPolicy RemoteSigned
```
PowerShell le pedirá que confirme el cambio. Escriba Y (o Y en algunos sistemas) y presione Enter.

#### 2. error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools"

- Ve a la página de descarga: https://visualstudio.microsoft.com/visual-cpp-build-tools/

- Descarga el instalador.

- Ejecútalo y, cuando te pregunte qué componentes instalar, asegúrate de seleccionar "Desarrollo para el escritorio con C++".

- Una vez instalado, reinicia tu terminal o editor de código.

Vuelve a intentar instalar los paquetes con pip install -r requirements.txt.
