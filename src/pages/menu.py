import streamlit as st
from utils.informaciones import usuario_activo_fixed


def menu():
    usuario_activo_fixed()
    try:
        st.markdown("""
            <style>
                /* Elimina el fondo y borde de la cabecera principal */
                header[data-testid="stHeader"] {
                    background: none;
                    border-bottom: none;
                }
            </style>
        """, unsafe_allow_html=True)
        # Ocultar la cabecera del sidebar que contiene el botón de retraer original
        st.markdown("""
            <style>
                div[data-testid="stSidebarHeader"] {
                    display: none;
                }
            </style>
        """, unsafe_allow_html=True)

        st.sidebar.markdown(
        "<div class='menu-title' style='margin-top: 18px; text-align: center;'>Menú</div>"
        "<hr style='border: 1px solid #000000; margin: 0px 0;'>"
        "<div style='margin-top: 1px;'>"
        "<div style='margin-bottom: 12px;'>"
        """
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
        <style>
            .menu-title {
                font-family: 'Roboto', sans-serif;
                font-size: 26px;
                font-weight: 700;
                margin-bottom: 0px;
                color: #000000;
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True)
        # Botones de inicio
        inicioicon, iniciobtn = st.sidebar.columns((0.1, 1))
        inicio_logo = inicioicon.button("", type="tertiary", width="stretch", icon=":material/home:", key="inicio_logo")
        inicio_Boton = iniciobtn.button("Inicio", type="primary", width="stretch")
        # Botones de mortalidad
        mortalidadicon, mortalidadbtn = st.sidebar.columns((0.1, 1))
        mortalidad_logo = mortalidadicon.button("", type="tertiary", width="stretch", icon=":material/skull:", key="mortalidad_logo")
        mortalidad_boton = mortalidadbtn.button("Mortalidad", type="primary", width="stretch")
        # Botones de natalidad
        natalidadicon, natalidadbtn = st.sidebar.columns((0.1, 1))
        natalidad_Logo = natalidadicon.button("", type="tertiary", width="stretch", icon=":material/pregnant_woman:", key="natalidad_logo")
        natalidad_boton = natalidadbtn.button("Natalidad", type="primary", width="stretch")
        # Botones de morbilidad
        morbilidadicon, morbilidadbtn = st.sidebar.columns((0.1, 1))
        morbilidad_Logo = morbilidadicon.button("", type="tertiary", width="stretch", icon=":material/personal_injury:", key="morbilidad_logo")
        morbilidad_boton = morbilidadbtn.button("Morbilidad", type="primary", width="stretch")
        # Botones de estadísticas
        estadisticaicon, estadisticabtn = st.sidebar.columns((0.1, 1))
        estadistica_Logo = estadisticaicon.button("", type="tertiary", width="stretch", icon=":material/bar_chart_4_bars:", key="estadistica_Logo")
        estadistica_boton = estadisticabtn.button("Estadísticas", type="primary", width="stretch")
        # Margen divisor
        st.sidebar.markdown(
        "<hr style='border: 1px solid #000000; margin-top: 0px; margin-bottom: 1px;'>"
        , unsafe_allow_html=True)

        configicon, configbtn = st.sidebar.columns((0.1, 1))
        configuracion_Logo = configicon.button("", type="tertiary", width="stretch", icon=":material/settings:", key="config_logo")
        configuracion_boton = configbtn.button("Configuración", type="primary", width="stretch")

        # Botones de cerrar sesión
        logouticon, logoutbtn = st.sidebar.columns((0.1, 1))
        cerrar_Logo = logouticon.button("", type="tertiary", width="stretch", icon=":material/exit_to_app:", key="cerrar_logo")
        cerrar_boton = logoutbtn.button("Cerrar sesión", type="primary", width="stretch")
        # Lógica de los botones
        if inicio_logo or inicio_Boton:
            st.switch_page("pages/inicio.py")
            st.rerun()
        if mortalidad_logo or mortalidad_boton:
            st.switch_page("pages/mortalidad.py")
            st.rerun()
        if natalidad_Logo or natalidad_boton:
            st.switch_page("pages/natalidad.py")
            st.rerun()
        if morbilidad_Logo or morbilidad_boton:
            st.switch_page("pages/morbilidad.py")
            st.rerun()
        if estadistica_Logo or estadistica_boton:
            st.switch_page("pages/estadisticas.py")
            st.rerun()
        if configuracion_Logo or configuracion_boton:
            st.switch_page("pages/configuracion.py")
            st.rerun()
        if cerrar_Logo or cerrar_boton:
            @st.dialog(":material/brightness_alert: ¿Estás seguro de que quieres cerrar sesión?")
            def cerrar_sesion():
                colsi, colno = st.columns(2)
                with colno:    
                    no = st.button("No", icon=":material/cancel:", key="no", width="stretch")
                with colsi:    
                    si = st.button("Sí", icon=":material/logout:", key="si", width="stretch", type="primary")
                if no:
                    st.rerun()               
                if si:
                    st.session_state['edit_mode'] = False
                    #    del st.session_state['edit_mode'] # da error
                    st.success("Cerrando sesión", icon=":material/favorite:")
                    st.switch_page("pages/inicio_sesion.py")
                    st.rerun()
                    st.rerun() 
            cerrar_sesion() 
    except Exception as e:
        st.error(e)