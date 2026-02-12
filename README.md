
![Logo](https://i.imgur.com/SAHxoGy.png)


# Sistema de Estadísticas Epidemiológicas (SEE) (before EPI-SYSTEM)

The developed system is a web-based epidemiological surveillance environment for the Dr. Felipe Guevara Rojas Hospital. Its purpose is to digitize and optimize the recording, analysis, and query of epidemiological data, replacing manual paper-based processes with an efficient, secure, and accessible technological tool.

The application, built in Python (Streamlit) and supported by a relational database (SQLite/MySQL), integrates mortality, morbidity, birth, and demographic modules, allowing the recording, validation, and query of clinical and statistical information. It also includes secure authentication, PDF report generation, and dynamic graphical visualization features, facilitating the interpretation of health trends by year, sex, and age group.

In short, it is a technological solution that strengthens hospital management and public health decision-making, ensuring the security, traceability, and accessibility of epidemiological data.

## Authors

- [@Sua7Dev](https://github.com/Sua7Dev)
- [@Gustav0H2O](https://github.com/Gustav0H2O)


## Deployment

To deploy this project:

### - step 1. Open a terminal and navigate to your project folder.
```bash
cd myproject
```
### - step 2. In your terminal, type to clone the repository:
```bash
git clone https://github.com/Sua7Dev/EPI-SYSTEM.git
```

### - step 3. creates a virtual environment:
```bash
python -m venv .venv
```

### - step 4. activate the virtual environment (this is for Windows PowerShell):
```bash
.venv\Scripts\Activate.ps1
```

### - step 5. installs the necessary libraries:
```bash
pip install -r requirements.txt
```

### - step 6. access the src folder:
```bash
cd src
```

### - step 7. we compile to .exe:
```bash
pyinstaller --clean --icon=../iconito.ico --onedir launcher.py --name EPI-SYSTEM --collect-all streamlit --collect-all streamlit_extras --add-data "../static;static" --add-data "../.streamlit;.streamlit" --add-data "hospital.db;." --add-data "main.py;." --add-data "launcher.py;." --add-data "utils;utils" --add-data "db.py;." --add-data "pages;pages" --add-data "reportes;reportes" --add-data "descargas;descargas" --add-data "stats;stats" --hidden-import=streamlit.web.cli --hidden-import=importlib.metadata --hidden-import=fpdf --hidden-import=db --hidden-import=utils.sql_control --hidden-import=pandas --hidden-import=numpy --hidden-import=pyarrow --hidden-import=snowflake.connector --hidden-import=streamlit_extras --noupx --noconsole
```



## Run Locally

To test the page locally before compiling to .exe, you can run
```bash
cd src
```
```bash
streamlit run main.py
```

## Screenshots
- home page
![App Screenshot](https://i.imgur.com/xkEl6EV.png)
- dashboard page
![App Screenshot](https://i.imgur.com/fFYzfB0.png)




## Documentation

User manuals (in Spanish)

[Admin](https://docs.google.com/document/d/1E493h8-7XwpHkWZRZZxG43KwKU4cTJ8Zkb3KiOXHFec/edit?usp=sharing)

[Doctor](https://docs.google.com/document/d/1SEgjlOTY88uGNEyolEECzOKYe6gAYwX2ukD0BNJ3tao/edit?usp=sharing)

[Secretaria](https://docs.google.com/document/d/1WJNMI8rx49F1U1FKIIaTP3K53h5kYPzYZaAn1-Vx-1Q/edit?usp=sharing )

## FAQ

#### 1. My PowerShell won't let me run scripts.

In the PowerShell window, type the following command and press Enter:
```bash
Set-ExecutionPolicy RemoteSigned
```
PowerShell will ask you to confirm the change. Type Y (or Y on some systems) and press Enter.

#### 2. error: Microsoft Visual C++ 14.0 or greater is required. Get it with "Microsoft C++ Build Tools"

- Go to the download page: https://visualstudio.microsoft.com/visual-cpp-build-tools/

- Download the installer.

- Run it and, when it asks you which components to install, make sure you select "Desktop Development with C++."

- Once installed, restart your terminal or code editor.

Try installing the packages again with pip install -r requirements.txt.
