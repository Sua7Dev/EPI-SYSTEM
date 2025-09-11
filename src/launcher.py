import sys
import os
import subprocess
import time
import socket
import shutil
import webbrowser
import sqlite3
import stat
import traceback

# streamlit CLI (solo en modo hijo si se usa stcli)
try:
    import streamlit.web.cli as stcli
except Exception as e:
    print(f"[DEBUG-IMPORT] No se pudo importar streamlit.web.cli: {e}")
    stcli = None

# dotenv opcional
try:
    from dotenv import load_dotenv
except Exception as e:
    print(f"[DEBUG-IMPORT] No se pudo importar dotenv: {e}")
    load_dotenv = None

# Importar funciones de inicialización de la base de datos
try:
    from db import create_all_tables
    from utils.sql_control import insertar_hospital_info, crear_superusuario
except ImportError as e:
    print(f"[DEBUG-IMPORT] No se pudieron importar las funciones de inicialización: {e}")
    traceback.print_exc()
    sys.exit(1)

def resource_path(rel_path: str) -> str:
    """Ruta absoluta para archivos empaquetados (PyInstaller _MEIPASS) o locales."""
    if getattr(sys, "frozen", False):
        base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
        possible_paths = [
            os.path.join(base, rel_path),  # Prioridad: ruta en la raíz del bundle
        ]
    else:
        base = os.path.dirname(os.path.abspath(__file__))
        possible_paths = [
            os.path.join(base, rel_path),  # Dentro de src
            os.path.join(base, "..", rel_path)  # Fuera de src (para static, .env, etc.)
        ]
    for path in possible_paths:
        if os.path.exists(path) and os.access(path, os.R_OK):
            print(f"[OK-RESOURCE] Ruta válida y legible: {path}")
            return path
        print(f"[ERROR-RESOURCE] Ruta no encontrada: {path}")
    return possible_paths[0]  # Retorna la última ruta intentada como fallback

def wait_for_port(host: str, port: int, timeout: int = 60) -> bool:
    """Espera hasta que un socket responda en host:port."""
    print(f"[DEBUG-PORT] Esperando conexión en {host}:{port} por {timeout} segundos")
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                print(f"[OK-PORT] Conexión exitosa a {host}:{port}")
                return True
        except OSError as e:
            print(f"[DEBUG-PORT] Intento de conexión fallido: {e}")
            time.sleep(0.5)
    print(f"[ERROR-PORT] Timeout: No se pudo conectar a {host}:{port}. Verifica si el puerto está en uso.")
    return False

def ensure_writable(path: str):
    """Asegura que el archivo sea escribible sin depender de permisos específicos."""
    print(f"[DEBUG-WRITE] Verificando permisos para: {path}")
    try:
        os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
        if os.name == "nt":
            subprocess.run(["attrib", "-R", path], check=False)
        print(f"[OK-WRITE] Archivo preparado para escritura: {path}")
    except Exception as e:
        print(f"[ERROR-WRITE] No se pudo ajustar permisos en {path}: {e}")

def is_database_initialized(db_path: str) -> bool:
    """Verifica si la base de datos ya está inicializada comprobando la existencia de una tabla."""
    print(f"[DEBUG-DB] Verificando inicialización de: {db_path}")
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='hospital_info'")
            initialized = cursor.fetchone() is not None
            print(f"[DEBUG-DB] Base de datos inicializada: {initialized}")
            return initialized
    except sqlite3.Error as e:
        print(f"[ERROR-DB] Error al verificar inicialización de {db_path}: {e}")
        return False

def initialize_database(db_path: str):
    """Ejecuta las funciones de inicialización de la base de datos si no está inicializada."""
    print(f"[DEBUG-DB] Inicializando base de datos en: {db_path}")
    if not is_database_initialized(db_path):
        try:
            create_all_tables()
            insertar_hospital_info()
            crear_superusuario()
            print(f"[OK-DB] Base de datos inicializada correctamente")
        except Exception as e:
            print(f"[ERROR-DB] No se pudo inicializar la base de datos: {e}")
            traceback.print_exc()
            raise RuntimeError(f"No se pudo inicializar la base de datos: {e}")
    else:
        print(f"[INFO-DB] La base de datos ya está inicializada: {db_path}")

def get_writable_db_path():
    """
    Devuelve la ruta a la base de datos SQLite hospital.db.

    - Usa hospital.db si existe en el directorio escribible del usuario (%LOCALAPPDATA%\\Epi).
    - Si no existe, copia hospital.db desde el directorio empaquetado.
    - Inicializa la base de datos solo si es necesario.
    - Asegura que sea escribible y usa modo WAL.
    """
    db_name = "hospital.db"
    db_bundled = resource_path(db_name)
    print(f"[DEBUG-DB] Verificando base de datos empaquetada: {db_bundled}")

    if not os.path.exists(db_bundled):
        print(f"[WARN-DB] No se encontró la base de datos empaquetada en {db_bundled}. Creando una nueva.")

    user_data_dir = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "Epi")
    os.makedirs(user_data_dir, exist_ok=True)
    print(f"[DEBUG-DB] Directorio escribible del usuario: {user_data_dir}")
    db_user_path = os.path.join(user_data_dir, db_name)
    print(f"[DEBUG-DB] Ruta de la base de datos del usuario: {db_user_path}")

    if not os.path.exists(db_user_path) and os.path.exists(db_bundled):
        try:
            shutil.copy(db_bundled, db_user_path)
            print(f"[OK-DB] Base de datos copiada a {db_user_path}")
        except Exception as e:
            print(f"[ERROR-DB] No se pudo copiar la BD a {db_user_path}: {e}")
            traceback.print_exc()
            raise RuntimeError(f"No se pudo copiar la BD a {db_user_path}: {e}")

    ensure_writable(db_user_path)

    try:
        with sqlite3.connect(db_user_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            print(f"[OK-DB] Conexión exitosa a la base de datos: {db_user_path}")
            initialize_database(db_user_path)
    except sqlite3.Error as e:
        print(f"[ERROR-DB] No se pudo conectar a la base de datos {db_user_path}: {e}")
        traceback.print_exc()
        raise RuntimeError(f"No se pudo conectar a la base de datos {db_user_path}: {e}")

    return db_user_path

# -----------------------
# MODO HIJO: ejecutar Streamlit
# -----------------------
def child_run_streamlit():
    # Buscar .env en la raíz de pag
    env_path = resource_path(".env")
    print(f"[DEBUG-ENV] Verificando archivo .env: {env_path}")
    if os.path.exists(env_path) and load_dotenv:
        load_dotenv(env_path)
        print(f"[OK-ENV] Variables de entorno cargadas desde {env_path}")
    else:
        print(f"[WARN-ENV] No se encontró .env o dotenv no está disponible: {env_path}")

    db_path = get_writable_db_path()
    if not os.path.exists(db_path):
        print(f"[ERROR-ENV] La base de datos {db_path} no existe o no es accesible")
        sys.exit(1)

    os.environ["hospital.db"] = db_path
    os.environ["AUTH_PEPPER"] = os.getenv("AUTH_PEPPER", "pepper_inseguro_cambiar")
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    print(f"[DEBUG-ENV] Variables de entorno configuradas: hospital.db={db_path}, STREAMLIT_SERVER_HEADLESS=true")

    main_app = resource_path("main.py")
    print(f"[DEBUG-MAIN] Verificando archivo main.py: {main_app}")
    if not os.path.exists(main_app):
        print(f"[ERROR-MAIN] No se encontró el archivo {main_app}")
        sys.exit(1)

    # Ajuste: static está en la raíz del bundle
    static_dir = resource_path("static")
    print(f"[DEBUG-STATIC] Verificando directorio static: {static_dir}")
    if not os.path.exists(static_dir):
        print(f"[ERROR-STATIC] No se encontró el directorio {static_dir}")
        sys.exit(1)
    elif not os.path.isdir(static_dir):
        print(f"[ERROR-STATIC] {static_dir} no es un directorio")
        sys.exit(1)

    streamlit_dir = resource_path(".streamlit")
    print(f"[DEBUG-STREAMLIT] Verificando directorio .streamlit: {streamlit_dir}")
    if not os.path.exists(streamlit_dir):
        print(f"[ERROR-STREAMLIT] No se encontró el directorio {streamlit_dir}")
        sys.exit(1)
    elif not os.path.isdir(streamlit_dir):
        print(f"[ERROR-STREAMLIT] {streamlit_dir} no es un directorio")
        sys.exit(1)

    utils_dir = resource_path("utils")
    print(f"[DEBUG-UTILS] Verificando directorio utils: {utils_dir}")
    if not os.path.exists(utils_dir):
        print(f"[ERROR-UTILS] No se encontró el directorio {utils_dir}")
        sys.exit(1)
    elif not os.path.isdir(utils_dir):
        print(f"[ERROR-UTILS] {utils_dir} no es un directorio")
        sys.exit(1)

    sys.argv = [
        "streamlit",
        "run",
        main_app,
        "--server.port", "8501",
        "--server.headless", "true",
        "--global.developmentMode", "false",
    ]
    print(f"[DEBUG-STREAMLIT] Argumentos de Streamlit: {sys.argv}")

    try:
        if stcli is not None:
            print("[DEBUG-STREAMLIT] Ejecutando Streamlit con stcli.main()")
            stcli.main()
        else:
            print("[DEBUG-STREAMLIT] Ejecutando Streamlit con runpy.run_module")
            import runpy
            runpy.run_module("streamlit", run_name="__main__")
    except Exception as e:
        print(f"[ERROR-STREAMLIT] Error al ejecutar Streamlit: {e}")
        traceback.print_exc()
        sys.exit(1)

# -----------------------
# MODO PADRE: lanzar hijo y abrir navegador local
# -----------------------
def parent_launch_local():
    # Buscar .env en la raíz de pag
    env_path = resource_path(".env")
    print(f"[DEBUG-ENV] Verificando archivo .env: {env_path}")
    if os.path.exists(env_path) and load_dotenv:
        load_dotenv(env_path)
        print(f"[OK-ENV] Variables de entorno cargadas desde {env_path}")
    else:
        print(f"[WARN-ENV] No se encontró .env o dotenv no está disponible: {env_path}")

    db_path = get_writable_db_path()
    if not os.path.exists(db_path):
        print(f"[ERROR-ENV] La base de datos {db_path} no existe o no es accesible")
        sys.exit(1)

    os.environ["hospital.db"] = db_path
    os.environ["AUTH_PEPPER"] = os.getenv("AUTH_PEPPER", "pepper_inseguro_cambiar")
    print(f"[DEBUG-ENV] Variables de entorno configuradas: hospital.db={db_path}")

    exe = sys.executable
    script = sys.argv[0]
    cmd = [exe, script, "--run-child"]
    print(f"[DEBUG-PROCESS] Comando para proceso hijo: {cmd}")

    try:
        proc = subprocess.Popen(cmd)
        print(f"[OK-PROCESS] Proceso hijo iniciado con PID {proc.pid}")
    except Exception as e:
        print(f"[ERROR-PROCESS] Error al iniciar el proceso hijo: {e}")
        traceback.print_exc()
        sys.exit(1)

    if not wait_for_port("localhost", 8501, timeout=60):
        try:
            proc.terminate()
            print("[INFO-PROCESS] Proceso hijo terminado debido a timeout")
        except Exception as e:
            print(f"[WARN-PROCESS] Error al terminar el proceso hijo: {e}")
        print("[ERROR-PROCESS] No se pudo conectar al servidor Streamlit en localhost:8501")
        sys.exit(1)

    url = "http://localhost:8501"
    print(f"[DEBUG-BROWSER] Abriendo navegador en {url}")
    webbrowser.open(url)

# -----------------------
# ENTRADA PRINCIPAL
# -----------------------
if __name__ == "__main__":
    print("[DEBUG-START] Iniciando launcher")
    try:
        if "--run-child" in sys.argv:
            print("[DEBUG-MODE] Ejecutando en modo hijo")
            child_run_streamlit()
        else:
            print("[DEBUG-MODE] Ejecutando en modo padre")
            parent_launch_local()
    except Exception as e:
        print(f"[ERROR-CRITICAL] Error crítico en el launcher: {e}")
        traceback.print_exc()
        sys.exit(1)