import streamlit as st
import pandas as pd
import sqlite3
from utils.informaciones import nosotros, hospital, mision, vision, manual_de_uso
from utils.verificaciones import verificar_superusuario, eliminar_usuario_completo, obtener_info_usuario
from utils.contra import borro_cassette
from utils.validaciones import validar_texto, validar_nombre_usuario, val_mail, validar_contraseña
import time
from utils.sql_edicion import obtener_usuarios, eliminar_usuarios_seleccionados, actualizar_usuario, eliminar_datos_seguridad, agregar_contra_nueva
import os

DB_PATH = os.getenv("hospital.db", "hospital.db")

# Initialize session state
if "autenticado_usuario" not in st.session_state:
    st.session_state["autenticado_usuario"] = None
if "edit_mode" not in st.session_state:
    st.session_state["edit_mode"] = False
################################## DIALOGS #############################################

@st.dialog(":material/preview_off: Ingrese la nueva contraseña", width="medium")
def contras_nuevas(nombre_usuario):
    with st.form(key='reestablecer_contra_admin'):
        col_contra, col_confirmar = st.columns(2)
        with col_contra:
            contrasena = st.text_input('Contraseña:', max_chars=16, 
                                       type='password', 
                                       key="contra_usuario", icon=":material/visibility_lock:")
        with col_confirmar:
            confirmar_contra = st.text_input('Confirmar Contraseña:', max_chars=16, 
                                             type='password', 
                                             key="confirmar_contra", icon=":material/preview_off:")
        st.info('La contraseña debe tener entre 8 y 16 caracteres, una letra minúscula, una mayúscula y al menos un número.', icon=":material/info:")
        st.warning("**Nota**: esta acción eliminará las preguntas y respuestas de seguridad del usuario.", icon=":material/warning:")
        col_verificar, col_cancelar = st.columns(2)
        with col_cancelar:    
            cancelar = st.form_submit_button("Cancelar", icon=":material/cancel:", width="stretch")
        with col_verificar:    
            verificar = st.form_submit_button("Verificar", icon=":material/logout:", width="stretch", type="primary")
    if cancelar:
        st.rerun()               
    if verificar:
         # validacion basica
        if contrasena != confirmar_contra:
            st.error("Las contraseñas no coinciden.", icon=":material/error:")
        elif not validar_contraseña(contrasena):
            return
        else:
            contrasena_hasheada = borro_cassette(contrasena)
        
            # eliminar preguntas/respuestas y actualizar contraseña para ese usuario
            ok_del = eliminar_datos_seguridad(nombre_usuario)
            ok_upd = agregar_contra_nueva(nombre_usuario, contrasena_hasheada)
            if ok_upd:
                st.success(f"Contraseña restablecida exitosamente para '{nombre_usuario}'.", icon=":material/check_circle:")
                time.sleep(2)
                st.rerun()
            else:
                st.error("No se pudo restablecer la contraseña.", icon=":material/error:")

@st.dialog(":material/person_remove: ¿Seguro que desea eliminar este usuario?")
def confirmar_eliminar_solitario(nombre_usuario):
    st.warning(f"**Nota**: esta acción eliminará permanentemente al usuario **{nombre_usuario}**", icon=":material/warning:")
    colsi, colno = st.columns(2)
    with colno:    
        no = st.button("Cancelar", icon=":material/cancel:", key="no_eliminar_usuario", width="stretch")
    with colsi:    
        si = st.button("Eliminar", icon=":material/delete_forever:", key="si_eliminar_usuario", width="stretch", type="primary")
    if no:
        st.rerun()               
    if si:
        eliminar_usuario_completo(nombre_usuario)
        #st.success(f"Usuario {row['Nombre y Apellido']} eliminado")
        time.sleep(2)
        st.rerun()


@st.dialog(":material/group_remove: ¿Seguro que desea eliminar estos usuarios?")
def confirmar_eliminar_multiples(usuarios_seleccionados): #nombre_usuario
    st.warning(f"**Nota**: esta acción eliminará permanentemente todo usuario(s) seleccionado(s)", icon=":material/warning:")
    colsi, colno = st.columns(2)
    with colno:    
        no = st.button("Cancelar", icon=":material/cancel:", key="no_eliminar_usuario", width="stretch")
    with colsi:    
        si = st.button("Eliminar ", icon=":material/delete_forever:", key="si_eliminar_usuario", width="stretch", type="primary")
    if no:
        st.rerun()               
    if si:
        if eliminar_usuarios_seleccionados(usuarios_seleccionados):
            #st.success(f"Usuario {row['Nombre y Apellido']} eliminado")
            time.sleep(1)
            st.rerun()
        
################################Aqui abajo lo que se ve#################################################

def extras():
    with st.expander("Extras", expanded=False, icon=":material/more:"):
        hospital()
        col_mision, col_vision, col_manual, col_nosotros = st.columns(4)
        with col_mision:
            mision()
        with col_vision:
            vision()
        with col_manual:
            manual_de_uso()        
        with col_nosotros:
            nosotros()
            

def mostrar_modo_normal():
    nombre_usuario = st.session_state.get("autenticado_usuario")
    if not nombre_usuario:
        st.error("Debes iniciar sesión para acceder a configuracion.", icon=":material/error:")
        return
    info_usuario = obtener_info_usuario(nombre_usuario)
    if not info_usuario:
        st.error("Usuario no encontrado. Por favor, inicia sesión nuevamente.", icon=":material/error:")
        return
    rol_usuario = info_usuario["rol"]
    if rol_usuario == "Administrador (a)":
        st.subheader(":material/demography: Tablas de usuarios", anchor=False)
        df = obtener_usuarios()
        if df.empty:
            st.warning("No hay usuarios registrados con roles de 'doctor' o 'secretaria'.", icon=":material/person_off:")
        else:
            st.dataframe(df.drop(columns=['id_usuario']), use_container_width=True, hide_index=True)
        # botones
        col_registrar, col_editar = st.columns(2)
        with col_registrar:
            registrar = st.button("Registrar usuarios", icon=":material/person_add:", width="stretch", type="primary")
        with col_editar:
            editar = st.button("Editar usuarios", icon=":material/person_edit:", width="stretch")
        # logica de los botones
        if registrar:
            st.switch_page("pages/registro.py")
            st.rerun()
        if editar:
                @st.dialog(":material/brightness_alert: Confirma que eres tú para continuar", width="medium")#, icon=":material/favorite:"
                def acceso_editar():
                    with st.form(key="verificar_administrador"):
                        col_nombre, col_contra = st.columns(2)
                        with col_nombre:    
                            nombre = st.text_input("Nombre de usuario", value="", 
                                                key="nombre_edicion", max_chars=16, icon=":material/supervised_user_circle:")
                        with col_contra:
                            contra = st.text_input("Contraseña", type="password", value="", 
                                                key="contra_edicion", max_chars=16, icon=":material/lock_person:")

                        col_verificar, col_cancelar = st.columns(2)
                        with col_cancelar:    
                            cancelar = st.form_submit_button("Cancelar", icon=":material/cancel:", width="stretch")
                        with col_verificar:    
                            verificar = st.form_submit_button("Verificar", icon=":material/logout:", width="stretch", type="primary")
                    if cancelar:
                        st.rerun()               
                    if verificar:
                        if verificar_superusuario(nombre, contra):
                        # agregar aqui otro if para verificar que el usuario y contraseña son correctos
                            st.session_state.edit_mode = True
                            st.rerun()
                acceso_editar()

    extras()


def mostrar_modo_edicion():
    df = obtener_usuarios()
    if df.empty:
        st.warning("No hay usuarios registrados con roles de 'Doctor' o 'Secretario'.")
    st.subheader(":material/person_edit: Editar usuarios", anchor=False)
    df[' '] = False
    column_config = {
        " ": st.column_config.CheckboxColumn(
            " ",
            help="Selecciona los usuarios a editar",
            default=False,
        ),
        "id_usuario": None, 
        "Nombre y Apellido": st.column_config.TextColumn(disabled=True),
        "Cédula": st.column_config.TextColumn(disabled=True),
        "Rol": st.column_config.TextColumn(disabled=True),
        "Correo": st.column_config.TextColumn(disabled=True),
    }
    edited_df = st.data_editor(
        df,
        column_config=column_config,
        use_container_width=True,
        hide_index=True,
    )
    usuarios_seleccionados = edited_df[edited_df[' ']]
    # botones
    col_volver, col_eliminar = st.columns(2) #editar columnas porque ya no hace cambios la pag xd 
    with col_volver:
        btn_volver = st.button("Volver", icon=":material/arrow_back:", width="stretch", type="primary",
                               help="Vuelves a la página anterior.")
    with col_eliminar:
        btn_eliminar = st.button("Eliminar usuario(s) seleccionado(s)", icon=":material/delete:", width="stretch")
    # logica botones
    if btn_volver:
        st.session_state.edit_mode = False
        st.rerun()      
    if btn_eliminar:
        confirmar_eliminar_multiples(usuarios_seleccionados)
            #time.sleep(1)
            #st.rerun
    # otra logica de edicion
    if not usuarios_seleccionados.empty:
        
        st.subheader(":material/person_edit: Editar información de usuarios seleccionados", anchor=False)
        for index, row in usuarios_seleccionados.iterrows():
            with st.expander(f"Editar {row['Nombre y Apellido']} ({row['Cédula']})", icon=":material/user_attributes:"):
                with st.form(key=f"form_{row['id_usuario']}"):
                    nuevo_rol = st.selectbox(
                        ":material/assignment_ind: Rol",
                        options=['Doctor (a)', 'Secretario (a)'],
                        index=0 if row['Rol'] == 'Doctor (a)' else 1,
                        key=f"rol_{row['id_usuario']}"
                    )
                    nuevo_correo = st.text_input(
                        "Correo",
                        value=row['Correo'] if pd.notna(row['Correo']) else "",
                        key=f"correo_{row['id_usuario']}",
                        icon=":material/mail:"
                    )
                    # botones
                    col_guardar, col_reestablecer, col_eliminar = st.columns(3)
                    with col_guardar:
                        guardar = st.form_submit_button("Guardar cambios para usuario", 
                                                        icon=":material/save:", width="stretch", type="primary")
                    with col_reestablecer:
                        reestablecer_contra = st.form_submit_button("Reestablecer contraseña", 
                                                                    icon=":material/reset_settings:", width="stretch")
                    with col_eliminar:
                        eliminar_usuario = st.form_submit_button("Eliminar este usuario", 
                                                                 icon=":material/delete:", width="stretch")
                    # logica de los botones
                    if guardar:
                        if not val_mail(nuevo_correo):
                            return
                        if actualizar_usuario(row['id_usuario'], nuevo_rol, nuevo_correo):
                            st.success(f"Cambios guardados para {row['Nombre y Apellido']}", icon=":material/save:")
                            time.sleep(2)
                            st.rerun()
                    if reestablecer_contra:
                        try:
                            conn_tmp = sqlite3.connect(DB_PATH)
                            cur_tmp = conn_tmp.cursor()
                            cur_tmp.execute("SELECT nombre_usuario FROM usuario WHERE id_usuario = ?", (row['id_usuario'],))
                            fila_usuario = cur_tmp.fetchone()
                        finally:
                            conn_tmp.close()
                        if not fila_usuario:
                            st.error("No se encontró el nombre de usuario asociado.", icon=":material/error:")
                        else:
                            nombre_usuario = fila_usuario[0]
                            contras_nuevas(nombre_usuario)  
                    if eliminar_usuario:
                        try:
                            conn_tmp = sqlite3.connect(DB_PATH)
                            cur_tmp = conn_tmp.cursor()
                            cur_tmp.execute("SELECT nombre_usuario FROM usuario WHERE id_usuario = ?", (row['id_usuario'],))
                            fila_usuario = cur_tmp.fetchone()
                        finally:
                            conn_tmp.close()
                        if not fila_usuario:
                            st.error("No se encontró el nombre de usuario asociado.", icon=":material/error:")
                        else:
                            nombre_usuario = fila_usuario[0]
                            confirmar_eliminar_solitario(nombre_usuario)
