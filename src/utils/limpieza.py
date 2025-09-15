import streamlit as st
import datetime
from dateutil.relativedelta import relativedelta
# funciones de limpiar casillas de todos los formularios

def limpiar_campos_registro_diario():
    fecha_minima = datetime.datetime.now().date() - relativedelta(months=1)
    min_value = 0.0
    st.session_state.fd_registro_diario = fecha_minima
    st.session_state.nombre_registro_diario = ""
    st.session_state.edad_sexo_registro_diario = ""
    st.session_state.mr_registro_diario = ""
    st.session_state.mo_registro_diario = ""
    st.session_state.so_registro_diario = ""
    st.session_state.cd_registro_diario = ""
    st.session_state.cb_registro_diario = ""
    st.session_state.gett_registro_diario = ""
    st.session_state.nc_registro_diario = ""
    st.session_state.talla_registro_diario = min_value
    st.session_state.peso_registro_diario = min_value
    st.session_state.autopsia_registro_diario = ""

def limpiar_campos_epi14():
    min_value = 0

    st.session_state.causa_epi14 = ""
    st.session_state.n_casos_epi14 = min_value
    st.session_state.pop("num_casos_epi14", None)
    st.session_state.pop("sexo_edad_list", None)


def limpiar_campos_registro_usuario():
    st.session_state.nombre = ""
    st.session_state.sexo = "Masculino"
    st.session_state.nacimiento = datetime.datetime.now()
    st.session_state.rol = "Doctor (a)"
    st.session_state.correo = ""
    st.session_state.nombre_usuario = ""
    st.session_state.ci = ""
    st.session_state.nacionalidad = "Venezolano (a)"
    st.session_state.contra_usuario = ""
    st.session_state.confirmar_contra = ""

def limpiar_campos_natalidad():
    fecha_minima = datetime.datetime.now().date() - relativedelta(months=1)
    min_value = 0
    st.session_state.fecha_natalidad = fecha_minima
    st.session_state.partos_natalidad = min_value
    st.session_state.hembras_natalidad = min_value
    st.session_state.varones_natalidad = min_value
    st.session_state.sexo_gemelar_natalidad = "No aplica"
    st.session_state.gemelar_natalidad = min_value
    st.session_state.cesareas_natalidad = min_value
    st.session_state.mto_natalidad = min_value
    st.session_state.partos_extra_natalidad = min_value

# ----------------------------------------------------------------------------------- #

# liempieza de los mensuales
def limpiar_campos_mensual_general():
    min_value=0
    st.session_state.causas_mensual_general = ""
    st.session_state.n_casos_mensual_general = min_value


def limpiar_campos_mensual_neonatal():
    min_value=0
    st.session_state.causas_mensual_neonatal = ""
    st.session_state.n_casos_mensual_neonatal = min_value

def limpiar_campos_mensual_infantil():
    min_value=0
    st.session_state.causas_mensual_infantil = ""
    st.session_state.n_casos_mensual_infantil = min_value

# limpieza de los normales
def limpiar_campos_materna():
    fecha_minima = datetime.datetime.now().date() - relativedelta(months=1)
    min_value=0
    value_min2=0.00
    value=datetime.datetime.now().time()
    def primera_parte():
        st.session_state.historia_clinica_materna = ""
        st.session_state.nombres_apellidos_materna = ""
        st.session_state.fecha_nacimiento_materna = fecha_minima
        st.session_state.fecha_ingreso_materna = fecha_minima
        st.session_state.fecha_defuncion_materna = fecha_minima
        st.session_state.hora_ingreso_materna = value
        st.session_state.hora_defuncion_materna = value
        st.session_state.idx_ingreso_materna = ""
    def segunda_parte():
        st.session_state.idx_defuncion_materna = ""
        st.session_state.edad_materna = min_value
        st.session_state.tiempo_materna = "Años"
        st.session_state.pais_hogar_materna = ""
        st.session_state.estado_hogar_materna = ""
        st.session_state.municipio_hogar_materna = ""
        st.session_state.parroquia_hogar_materna = ""
        st.session_state.ciudad_hogar_materna = ""
        st.session_state.direccion_exacta_hogar_materna = ""
        st.session_state.causa_materna = ""
    primera_parte()
    segunda_parte()

def limpiar_campos_infantil():
    fecha_minima = datetime.datetime.now().date() - relativedelta(months=1)
    min_value=0
    value_min2=0.00
    value=datetime.datetime.now().time()
    def primera_parte():
        st.session_state.historia_clinica_infantil = ""
        st.session_state.nombres_apellidos_infantil = ""
        st.session_state.nombre_madre_infantil = ""
        st.session_state.fecha_nacimiento_infantil = fecha_minima
        st.session_state.fecha_ingreso_infantil = fecha_minima
        st.session_state.fecha_defuncion_infantil = fecha_minima
        st.session_state.hora_defuncion_infantil = value
        st.session_state.edad_infantil = min_value
        st.session_state.tiempo_infantil = "Meses"
    def hora_ingreso_infantil():
        st.session_state.hora_ingreso_infantil = value    
    def segunda_parte():
        st.session_state.idx_ingreso_infantil = ""
        st.session_state.idx_defuncion_infantil = ""
        st.session_state.pais_hogar_infantil = ""
        st.session_state.estado_hogar_infantil = ""
        st.session_state.municipio_hogar_infantil = ""
        st.session_state.parroquia_hogar_infantil = ""
        st.session_state.ciudad_hogar_infantil = ""
        st.session_state.direccion_exacta_hogar_infantil = ""
    primera_parte()
    hora_ingreso_infantil()
    segunda_parte()

def limpiar_campos_neonatal():
    fecha_minima = datetime.datetime.now().date() - relativedelta(months=1)
    min_value=0
    value_min2=0.00
    value=datetime.datetime.now().time()
    def primera_parte():
        st.session_state.historia_clinica_neonatal  = ""
        st.session_state.nombres_apellidos_neonatal = ""
        st.session_state.nombre_madre_neonatal = ""
        st.session_state.fecha_nacimiento_neonatal = fecha_minima
        st.session_state.hora_nacimiento_neonatal = value
        st.session_state.fecha_ingreso_neonatal = fecha_minima
        st.session_state.hora_ingreso_neonatal = value # revisar
        st.session_state.fecha_defuncion_neonatal = fecha_minima
        st.session_state.hora_defuncion_neonatal = value
        st.session_state.edad_neonatal = min_value
        st.session_state.tiempo_neonatal = "Horas"
    def segunda_parte():
        st.session_state.idx_ingreso_neonatal = ""
        st.session_state.idx_defuncion_neonatal = ""
        st.session_state.pais_hogar_neonatal = ""
        st.session_state.estado_hogar_neonatal = ""
        st.session_state.municipio_hogar_neonatal = ""
        st.session_state.parroquia_hogar_neonatal = ""
        st.session_state.cuidad_hogar_neonatal = ""
        st.session_state.direccion_exacta_neonatal = ""
        st.session_state.causa_neonatal = ""
        st.session_state.semanas_gestacion_neonatal = min_value
        st.session_state.peso_neonatal = value_min2
        st.session_state.talla_neonatal = value_min2
    primera_parte()
    segunda_parte()


# ----------------------------------------------------------------------------------- #

def limpiar_campos_morb_extenso():
    fecha_minima = datetime.datetime.now().date() - relativedelta(months=1)
    min_value = 0
    st.session_state.hc_morb_extenso = ""
    st.session_state.nombres_apellidos_morb_extenso = ""
    st.session_state.cedula_morb_extenso = "" 
    st.session_state.telefono_morb_extenso = "" 
    st.session_state.diagnostico_morb_extenso = ""
    st.session_state.fecha_registro_morb_extenso = fecha_minima
    st.session_state.edad_morb_extenso = min_value
    st.session_state.sexo_morb_extenso = "Masculino"
    st.session_state.fecha_nacimiento_morb_extenso = fecha_minima
    st.session_state.estado_civil_morb_extenso = "Soltero/a" 
    st.session_state.pais_hogar_morb_extenso = ""
    st.session_state.estado_hogar_morb_extenso = ""
    st.session_state.municipio_hogar_morb_extenso = ""
    st.session_state.parroquia_hogar_morb_extenso = ""
    st.session_state.cuidad_hogar_morb_extenso = ""
    st.session_state.direccion_exacta_hogar_morb_extenso = ""
    st.session_state.pais_nacimiento_morb_extenso = ""
    st.session_state.estado_nacimiento_morb_extenso = ""
    st.session_state.municipio_nacimiento_morb_extenso = ""
    st.session_state.parroquia_nacimiento_morb_extenso = ""
    st.session_state.cuidad_nacimiento_morb_extenso = ""
    st.session_state.direccion_exacta_nacimiento_morb_extenso = ""

def limpiar_campos_morb_simplificado():
    fecha_minima = datetime.datetime.now().date() - relativedelta(months=1)
    min_value = 0
    st.session_state.diagnostico_morb_simplifica = ""
    st.session_state.fecha_registro_morb_simplifica = fecha_minima
    st.session_state.edad_morb_simplifica = min_value
    st.session_state.sexo_morb_simplifica = "Masculino"
