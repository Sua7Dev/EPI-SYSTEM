import streamlit as st
from db import create_all_tables
from utils.sql_control import insertar_hospital_info, crear_superusuario

create_all_tables()
insertar_hospital_info()
crear_superusuario()

# configuracion de paginas accesibles ( sino se ponen aqui no se pueden acceder )
def paginas():
    #try:
    paginas = {
        "Cuenta": [
            st.Page("pages/inicio_sesion.py", title="Inicio de sesión", icon=":material/home:"),
            st.Page("pages/registro.py", title="Registro", icon=":material/person_add:"),
            st.Page("pages/olvido_contraseña.py", title="Olvido de contraseña", icon=":material/lock_reset:"),
            st.Page("pages/configuracion.py", title="Configuracion", icon=":material/settings:"),
            st.Page("pages/manual_usuario.py", title="Manual de Usuario", icon=":material/developer_guide:"),
        ],
        "Menu": [
            st.Page("pages/inicio.py", title="Dashboard", icon=":material/home:"),
            st.Page("pages/mortalidad.py", title="Mortalidad", icon=":material/skull:"),
            st.Page("pages/natalidad.py", title="Natalidad", icon=":material/pregnant_woman:"),
            st.Page("pages/morbilidad.py", title="Morbilidad", icon=":material/personal_injury:"),
            st.Page("pages/epi14.py", title="Epi14", icon=":material/coronavirus:"),
            st.Page("pages/registro_diario.py", title="Registro Diario", icon=":material/calendar_add_on:"),
            st.Page("pages/estadisticas.py", title="Estadisticas", icon=":material/bar_chart_4_bars:"),
        ],
    }
    pg = st.navigation(paginas, position="sidebar", expanded=False)#
    pg.run()
    #except Exception as e:
     #   st.error(f"Ocurrió un error: {e}")

# ejecucion de paginas(muestra siempre la primera, en este caso la de inicio de sesion)
def main():
    paginas()


main()