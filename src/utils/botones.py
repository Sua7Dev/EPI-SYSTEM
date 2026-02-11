import streamlit as st
import datetime
import time

def bloquear_botones(segundos=3):
    """Establece el estado de bloqueo para evitar multiclicks.
    
    Args:
        segundos: Tiempo en segundos antes de permitir reactivación.
                  Por defecto 3 segundos.
    """
    st.session_state["btn_deshabilitado"] = True
    st.session_state["btn_timestamp"] = time.time()
    st.session_state["btn_timeout"] = segundos


def verificar_timeout_boton():
    """Verifica si ha pasado el tiempo suficiente para reactivar el botón."""
    if "btn_timestamp" in st.session_state and "btn_timeout" in st.session_state:
        tiempo_transcurrido = time.time() - st.session_state["btn_timestamp"]
        if tiempo_transcurrido >= st.session_state["btn_timeout"]:
            st.session_state["btn_deshabilitado"] = False
            return True
    return False

@st.dialog(":material/brightness_alert: ¿Desea eliminar el registro seleccionado?")
def confirmar_eliminar(funcion_receptora, variable):
    colno, colsi  = st.columns(2)
    with colno:    
        no = st.button("Cancelar", icon=":material/cancel:", key="cancelar_eliminar_confirmacion", 
                       width="stretch", type="primary")
    with colsi:    
        si = st.button("Confirmar", icon=":material/delete_forever:", key="confirmar_eliminar_confirmacion", 
                       width="stretch")
    if no:
        st.rerun()               
    if si:
        res = funcion_receptora(variable)
        return res
    
def guadar_btn(funcion_receptora=None, variable_1=None, key_1=None):
    guardar = st.button("Guardar cambios", icon=":material/save:", width="stretch", key=key_1, type="primary")
    if guardar:   
        res = funcion_receptora(variable_1)
        st.rerun()
        return res
    

def guadar_btn_2(funcion_receptora=None, variable_1=None, variable_2=None):
    guardar = st.button("Guardar cambios", icon=":material/save:", width="stretch")
    if guardar:   
        res = funcion_receptora(variable_1, variable_2)
        st.rerun()
        return res
    
def ver_btn(key_btn=None, data=None):
    ver = st.button("Ver reporte", icon=":material/visibility:",
                     width="stretch", type="primary",
                     key=key_btn)
    
    if ver:
        if data:
            st.session_state["pdf_buffer"] = data
        st.switch_page("pages/ver_reportes.py")
        st.rerun()