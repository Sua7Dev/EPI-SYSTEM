import streamlit as st
import datetime
import time

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
        # aqui va la funcion receptora
        return funcion_receptora(variable)
    
def guadar_btn(funcion_receptora=None, variable_1=None, key_1=None):
    guardar = st.button("Guardar cambios", icon=":material/save:", width="stretch", key=key_1, type="primary")
    if guardar:   
        # aqui va la funcion receptora
        return funcion_receptora(variable_1)
    

def guadar_btn_2(funcion_receptora=None, variable_1=None, variable_2=None):
    guardar = st.button("Guardar cambios", icon=":material/save:", width="stretch")
    if guardar:   
        # aqui va la funcion receptora
        return funcion_receptora(variable_1, variable_2)