import sys
import os
import subprocess
import time
import socket
import shutil
import webbrowser
import sqlite3
import stat

# streamlit CLI (solo en modo hijo si se usa stcli)
try:
    import streamlit.web.cli as stcli
except Exception:
    stcli = None

# dotenv opcional
try:
    from dotenv import load_dotenv
except Exception:
    load_dotenv = None

def resource_path(rel_path: str) -> str:
    """Ruta absoluta para archivos empaquetados (PyInstaller _MEIPASS) o locales."""
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    else:
        base = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base, rel_path)
    print(f"Resolviendo ruta para {rel_path}: {full_path}")  # Depuración
    return full_path

def wait_for_port(host: str, port: int, timeout: int = 60) -> bool:
    """Espera hasta que un socket responda en host:port."""
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False

def make_writable(path: str):
    """Quita atributo de solo lectura y asegura escritura en el archivo."""
    try:
        # Quitar flag de solo lectura en Python
        os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
        # Quitar flag en Windows con attrib (por si acaso)
        if os.name == "nt":
            subprocess.call(["attrib", "-R", path])
        print(f"[OK] Archivo listo para escritura: {path}")
    except Exception as e:
        print(f"[WARN] No se pudo ajustar permisos en {path}: {e}")

def prepare_writable_db():
    """
    Asegura que la base de datos hospital.db exista en %LOCALAPPDATA%\Epi
    - Si ya está allí, la usa y la deja escribible.
    - Si no, copia hospital.db desde el launcher.
    """
    user_data_dir = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "Epi")
    os.makedirs(user_data_dir, exist_ok=True)

    # Ruta final en el equipo del usuario
    db_user_path = os.path.join(user_data_dir, "hospital.db")

    # Ruta al hospital.db que está junto al launcher
    db_bundled = resource_path("hospital.db")  # ahora buscamos hospital.db directamente

    if not os.path.exists(db_bundled):
        raise RuntimeError(f"No se encontró la base de datos {db_bundled} junto al launcher.")

    # Copiar solo si no existe en la carpeta del usuario
    if not os.path.exists(db_user_path):
        try:
            shutil.copy(db_bundled, db_user_path)
            print(f"Base de datos copiada a {db_user_path}")
        except Exception as e:
            raise RuntimeError(f"No se pudo copiar la BD a {db_user_path}: {e}")

    # Quitar solo lectura cada vez
    make_writable(db_user_path)

    return db_user_path

# -----------------------
# MODO HIJO: ejecutar Streamlit
# -----------------------
def child_run_streamlit():
    env_path = resource_path("myenv")
    if os.path.exists(env_path) and load_dotenv:
        load_dotenv(env_path)

    db_path = prepare_writable_db()
    if not os.path.exists(db_path):
        sys.exit(f"Error: La base de datos {db_path} no existe o no es accesible")
    os.environ["DB_PATH"] = db_path  # Cambiado de AUTH_DB_PATH a hospital.db
    os.environ["AUTH_PEPPER"] = os.getenv("AUTH_PEPPER", "pepper_inseguro_cambiar")
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"

    main_app = resource_path("src/main.py")
    if not os.path.exists(main_app):
        sys.exit(f"Error: No se encontró el archivo {main_app}")

    sys.argv = [
        "streamlit",
        "run",
        main_app,
        "--server.port",
        "8501",
        "--server.headless",
        "true",
        "--global.developmentMode",
        "false",
    ]

    if stcli is not None:
        stcli.main()
    else:
        import runpy
        runpy.run_module("streamlit", run_name="__main__")

# -----------------------
# MODO PADRE: lanzar hijo y abrir navegador local
# -----------------------
def parent_launch_local():
    env_path = resource_path("myenv")
    if os.path.exists(env_path) and load_dotenv:
        load_dotenv(env_path)

    db_path = prepare_writable_db()
    if not os.path.exists(db_path):
        print(f"Error: La base de datos {db_path} no existe o no es accesible")
        return

    os.environ["DB_PATH"] = db_path  # Cambiado de AUTH_DB_PATH a hospital.db
    os.environ["AUTH_PEPPER"] = os.getenv("AUTH_PEPPER", "pepper_inseguro_cambiar")

    exe = sys.executable
    script = sys.argv[0]
    cmd = [exe, script, "--run-child"]

    try:
        proc = subprocess.Popen(cmd)
    except Exception as e:
        print(f"Error al iniciar el proceso hijo: {e}")
        return

    if not wait_for_port("localhost", 8501, timeout=60):
        try:
            proc.terminate()
        except Exception:
            pass
        print("Error: No se pudo conectar al servidor Streamlit en localhost:8501")
        return

    url = "http://localhost:8501"
    webbrowser.open(url)

# -----------------------
# ENTRADA PRINCIPAL
# -----------------------
if __name__ == "__main__":
    if "--run-child" in sys.argv:
        child_run_streamlit()
        sys.exit(0)

    parent_launch_local()
