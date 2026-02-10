import streamlit as st
import datetime
from pathlib import Path
from utils.sql_control import operaciones_sql_natalidad, eliminar_registros_natalidad
from dateutil.relativedelta import relativedelta
from utils.visuales import logo, configurar_pagina_espanol, recargar_una_vez, copyright_footer_dos
from utils.filtro import filtrar_por_fechas, descargar_pdf, descargar_registros_seleccionados
from utils.verificaciones import obtener_info_usuario
from pages.menu import menu
import time
from utils.base_64 import img_a_base64
from utils.limpieza import limpiar_campos_natalidad
from utils.botones import confirmar_eliminar, guadar_btn, ver_btn
from utils.guardar_cambios import procesar_guardado_cambios_natalidad
configurar_pagina_espanol()
from reportes.natalidad_general import formulario_reporte_general_natalidad
import sys


def get_project_root() -> Path:
    """Devuelve la raíz del proyecto, incluso empaquetado con PyInstaller."""
    if getattr(sys, "frozen", False):  # Si está empaquetado
        # Carpeta base del ejecutable
        return Path(sys._MEIPASS)
    else:
        # Carpeta base del código fuente
        return Path(__file__).resolve().parent.parent.parent

PROJECT_ROOT = get_project_root()
ASSETS_DIR = PROJECT_ROOT / "static" / "assets" / "imagenes"
menu()

def data_editor_natalidad(df, rol_usuario):

    if " " not in df.columns:
        df.insert(0, " ", False)

    # Mostrar todo excepto ids internos, pero dejar ID al final
    columns_to_display = [
        col for col in df.columns
        if col not in [" ", "id_doctor", "fecha_registro_formulario"]
    ]

    # Mover id al final
    if "id" in columns_to_display:
        columns_to_display.remove("id")
        columns_to_display.append("id")

    columns_to_show = [" "] + columns_to_display
    df = df[columns_to_show]

    column_config = {
        " ": st.column_config.CheckboxColumn(" ", default=False, disabled=False),
        "fecha_registro_formulario": st.column_config.DateColumn(
            "Fecha registro formulario", format="DD/MM/YYYY", disabled=True
        ),
        "fecha": st.column_config.DateColumn(
            "Fechas", format="DD/MM/YYYY",
            disabled=(rol_usuario == "Secretario (a)")
        ),
        "partos": st.column_config.NumberColumn(
            "Partos", min_value=0, step=1,
            disabled=(rol_usuario == "Secretario (a)")
        ),
        "cesareas": st.column_config.NumberColumn(
            "Cesáreas", min_value=0, step=1,
            disabled=(rol_usuario == "Secretario (a)")
        ),
        "varones": st.column_config.NumberColumn(
            "Varones", min_value=0, step=1,
            disabled=(rol_usuario == "Secretario (a)")
        ),
        "hembras": st.column_config.NumberColumn(
            "Hembras", min_value=0, step=1,
            disabled=(rol_usuario == "Secretario (a)")
        ),
        "gemelar": st.column_config.NumberColumn(
            "Gemelar", min_value=0, step=1, disabled=True
        ),
        "mto": st.column_config.NumberColumn(
            "Muertos (MTO)", min_value=0, step=1,
            disabled=(rol_usuario == "Secretario (a)")
        ),
        "partos_extrahospitalarios": st.column_config.NumberColumn(
            "Partos extrahospitalarios", min_value=0, step=1,
            disabled=(rol_usuario == "Secretario (a)")
        ),
        "sexo_gemelar": st.column_config.SelectboxColumn(
            "Sexo de los gemelos",
            options=["No aplica", "Varones", "Hembras", "Mixto"],
            disabled=(rol_usuario == "Secretario (a)")
        ),
        "id": st.column_config.TextColumn("ID", disabled=True),
        "id_doctor": st.column_config.TextColumn("ID_Doctor", disabled=True),
        "registrado_por": st.column_config.TextColumn("Registrado por", disabled=True),
    }

    for col in columns_to_show:
        if col not in column_config and col != " ":
            column_config[col] = st.column_config.TextColumn(col, disabled=True)

    edited_df = st.data_editor(
        df,
        hide_index=True,
        column_config=column_config,
        key="editor_natalidad"
    )

    return edited_df

@st.fragment
def formulario_natalidad():
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a esta area.", icon=":material/error:")
        return

    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)

    if not info_usuario:
        st.error("Usuario no encontrado. Por favor, inicia sesión nuevamente.", icon=":material/error:")
        return

    rol_usuario = info_usuario["rol"]
    id_doctor = info_usuario["id_doctor"]
    id_administrador = info_usuario["id_administrador"]

    st.header(":material/pediatrics: Datos De Natalidad", divider="gray", anchor=False)

    df = operaciones_sql_natalidad("cargar")
    if df is None:
        return

    if rol_usuario == "Secretario (a)":
        if df.empty:
            st.info("No hay registros disponibles.", icon=":material/info:")
            return

        df[' '] = False
        df_filtrado = filtrar_por_fechas(df, 'fecha')
        edited_df = data_editor_natalidad(df_filtrado, rol_usuario)

        if not df_filtrado.empty:
            has_selection = edited_df[' '].any()
            col1, col2 = st.columns(2)

            with col1:
                descargar_pdf(edited_df, "natalidad", label="Descargar PDF")

            with col2:
                df_sel = edited_df[edited_df[' '] == True]
                descargar_registros_seleccionados(edited_df, "natalidad")
                descargar_pdf(
                    df_sel,
                    "natalidad_seleccionado",
                    label="Descargar Selección",
                    disabled=not has_selection
                )

        return  

    if df.empty:
        st.info("No hay registros disponibles.", icon=":material/info:")
    else:
        mostrar_editor = st.toggle(
            "Mostrar datos de registros",
            value=False,
            key="toggle_editor_natalidad"
        )

        if mostrar_editor:
            df[' '] = False
            df_filtrado = filtrar_por_fechas(df, 'fecha')
            edited_df = data_editor_natalidad(df_filtrado, rol_usuario)

            if not df_filtrado.empty:
                has_selection = edited_df[' '].any()
                col_ver, col_guardar, col_descargar, col_sel, col_eliminar = st.columns(5)

                with col_ver:
                    ver_btn(key_btn="ver_btn_natalidad")

                with col_guardar:
                    guardar = st.button(
                        "Guardar cambios",
                        icon=":material/save:",
                        width="stretch",
                        type="primary"
                    )

                with col_descargar:
                    descargar_pdf(edited_df, "natalidad")

                with col_sel:
                    df_sel = edited_df[edited_df[' '] == True]
                    descargar_registros_seleccionados(edited_df, "natalidad")
                    descargar_pdf(
                        df_sel,
                        "natalidad_seleccionado",
                        label="Descarga selección",
                        disabled=not has_selection
                    )

                with col_eliminar:
                    btn_eliminar = st.button(
                        "Eliminar",
                        icon=":material/delete:",
                        disabled=not has_selection,
                        width="stretch"
                    )
                    if btn_eliminar:
                        confirmar_eliminar(eliminar_registros_natalidad, edited_df)

                if guardar:
                    procesar_guardado_cambios_natalidad(edited_df)

        st.components.v1.html("""
            <script>
            const setupLogic = () => {
                const doc = window.parent.document;
                const inputs = doc.querySelectorAll('input[type="number"]');
                
                inputs.forEach(input => {
                    if (!input.dataset.listenerActive) {
                        // Bloqueo por teclado (Keydown)
                        input.addEventListener('keydown', (e) => {
                            const prohibidas = ['e', 'E', '+', '-', '.', ','];
                            const esControl = ['Backspace', 'Delete', 'ArrowLeft', 'ArrowRight', 'Tab', "Enter"].includes(e.key);
                            
                            // 1. Bloquear caracteres especiales
                            if (prohibidas.includes(e.key)) {
                                e.preventDefault();
                            }
                            
                            // 2. Bloquear si supera 8 caracteres (y no es tecla de borrar/mover)
                            if (input.value.length >= 8 && !esControl) {
                                e.preventDefault();
                            }
                        });

                        // Bloqueo por pegado o arrastre (Input event)
                        input.addEventListener('input', (e) => {
                            if (input.value.length > 8) {
                                input.value = input.value.slice(0, 8);
                            }
                        });

                        input.dataset.listenerActive = "true";
                    }
                });
            };

            setupLogic();
            setInterval(setupLogic, 700);
            </script>
            """, height=0)

    if rol_usuario != "Secretario (a)":
        st.subheader(":material/new_label: Registrar Natalidad", anchor=False)
        with st.form("form_natalidad"):
            st.markdown("""
                <style>
                /* Ocultar los botones de + y - de todos los st.number_input */
                button[data-testid="stNumberInputStepDown"], 
                button[data-testid="stNumberInputStepUp"] {
                    display: none !important;
                }
                iframe {
                    display: none !important;
                    height: 0 !important;
                    margin: 0 !important;
                }
                }
                </style>
                    """, unsafe_allow_html=True)
            col_fecha, col_partos, col_hembras, col_varones = st.columns(4)

            with col_fecha:
                fecha_minima = datetime.datetime.now().date() - relativedelta(months=1)
                fecha_maxima = datetime.date.today() + relativedelta(months=1)
                fecha = st.date_input(
                    "Fecha",
                    format="DD/MM/YYYY",
                    min_value=fecha_minima,
                    max_value=fecha_maxima
                )

            with col_partos:
                partos = st.number_input("Partos", min_value=0, step=1)

            with col_hembras:
                hembras = st.number_input("Hembras", min_value=0, step=1)

            with col_varones:
                varones = st.number_input("Varones", min_value=0, step=1)

            col_sexo_gem, col_gemelar = st.columns(2)
            with col_sexo_gem:
                sexo_gemelar = st.selectbox(
                    "Sexo de los gemelos",
                    ["No aplica", "Varones", "Hembras", "Mixto"]
                )

            with col_gemelar:
                gemelar = st.number_input("Gemelar", min_value=0, step=1)

            col_cesareas, col_mto = st.columns(2)
            with col_cesareas:
                cesareas = st.number_input("Cesáreas", min_value=0, step=1)

            with col_mto:
                mto = st.number_input("Muertos (MTO)", min_value=0, step=1)

            partos_extrahospitalarios = st.number_input(
                "Partos extrahospitalarios", min_value=0, step=1
            )

            col_reg, col_limp = st.columns([30, 1])
            with col_reg:
                registrar = st.form_submit_button("Registrar", type="primary")
            with col_limp:
                st.form_submit_button(
                    "",
                    icon=":material/cleaning_services:",
                    on_click=limpiar_campos_natalidad,
                    type="tertiary"
                )

            if registrar:

                if sexo_gemelar == "No aplica" and gemelar > 0:
                    st.warning(
                        "Al seleccionar 'No aplica', la cantidad de gemelares se ajusta automáticamente y se registra a 0.",
                        icon=":material/info:"
                    )
                    gemelar = 0
                    return

                varones_aj = varones
                hembras_aj = hembras
                if sexo_gemelar == "Varones":
                    varones_aj += gemelar * 2
                elif sexo_gemelar == "Hembras":
                    hembras_aj += gemelar * 2
                elif sexo_gemelar == "Mixto":
                    varones_aj += gemelar
                    hembras_aj += gemelar
                    
                total_nacidos = varones_aj + hembras_aj + mto
                total_eventos = partos + cesareas

                if total_nacidos != total_eventos:
                    st.error(
                        "La suma de Hembras, Varones y MTO debe coincidir con el total de Partos y Cesáreas.",
                        icon=":material/error:"
                    )
                    st.stop()

                datos_registro = (
                    fecha, partos, cesareas,
                    varones_aj, hembras_aj,
                    gemelar, mto,
                    partos_extrahospitalarios,
                    id_doctor, id_administrador, rol_usuario
                )

                if operaciones_sql_natalidad("registrar", datos_registro=datos_registro):
                    st.success("Registro guardado correctamente.", icon=":material/check_circle:")
                    st.rerun()

import streamlit as st
import streamlit.components.v1 as components

def text_input_max_3_con_mensaje(label: str, key: str):
    valor = st.text_input(label, key=key)

    components.html(f"""
    <script>
    (function() {{
        const LABEL = "{label}";
        const MAX_LEN = 3;

        function setup() {{
            const doc = window.parent.document;
            const labels = [...doc.querySelectorAll("label")];
            const targetLabel = labels.find(l => l.innerText === LABEL);
            if (!targetLabel) return;

            const wrapper = targetLabel.parentElement;
            const input = wrapper.querySelector("input");
            if (!input || input.dataset.max3MsgActive) return;

            // Crear mensaje si no existe
            let msg = wrapper.querySelector(".max3-msg");
            if (!msg) {{
                msg = document.createElement("div");
                msg.className = "max3-msg";
                msg.style.fontSize = "12px";
                msg.style.marginTop = "4px";
                msg.style.color = "red";
                msg.style.display = "none";
                msg.innerText = "❌ Máximo 3 caracteres permitidos";
                wrapper.appendChild(msg);
            }}

            const validar = () => {{
                if (input.value.length <= MAX_LEN) {{
                    input.style.borderColor = "green";
                    msg.style.display = "none";
                }} else {{
                    input.style.borderColor = "red";
                    msg.style.display = "block";
                }}
            }};

            input.addEventListener("input", validar);
            input.addEventListener("blur", validar);

            validar();
            input.dataset.max3MsgActive = "true";
        }}

        setup();
        setInterval(setup, 600);
    }})();
    </script>
    """, height=0)

    return valor

import streamlit as st
import streamlit.components.v1 as components

def email_input_validado_inteligente(label: str, key: str):
    valor = st.text_input(label, key=key)

    components.html(f"""
    <script>
    (function() {{
        const LABEL = "{label}";

        // Dominios NO permitidos antes del @
        const TLD_BLOQUEADOS = ["com","org","net","edu","gob","mil","info"];

        // Regex estricto y realista
        const EMAIL_REGEX =
            /^[a-zA-Z0-9._%+-]+@([a-zA-Z0-9-]+\\.)+[a-zA-Z]{{2,}}$/;

        function autocorregir(value) {{
            let v = value.toLowerCase().trim();

            // Correcciones comunes
            v = v.replace(/\\s+/g, "");          // quitar espacios
            v = v.replace(/,+/g, ".");           // , -> .
            v = v.replace(/@+/g, "@");           // múltiples @

            return v;
        }}

        function dominioInvalido(localPart) {{
            return TLD_BLOQUEADOS.some(tld =>
                localPart.endsWith("." + tld)
            );
        }}

        function setup() {{
            const doc = window.parent.document;
            const labels = [...doc.querySelectorAll("label")];
            const targetLabel = labels.find(l => l.innerText === LABEL);
            if (!targetLabel) return;

            const wrapper = targetLabel.parentElement;
            const input = wrapper.querySelector("input");
            if (!input || input.dataset.emailSmartActive) return;

            // Mensaje
            let msg = wrapper.querySelector(".email-msg");
            if (!msg) {{
                msg = document.createElement("div");
                msg.className = "email-msg";
                msg.style.fontSize = "12px";
                msg.style.marginTop = "4px";
                msg.style.display = "none";
                msg.style.color = "red";
                wrapper.appendChild(msg);
            }}

            const validar = () => {{
                let value = input.value;

                // Autocorrección en vivo
                const corregido = autocorregir(value);
                if (corregido !== value) {{
                    input.value = corregido;
                }}

                if (corregido === "") {{
                    input.style.borderColor = "#ccc";
                    msg.style.display = "none";
                    return;
                }}

                const partes = corregido.split("@");
                if (partes.length !== 2) {{
                    error("Formato incorrecto del correo");
                    return;
                }}

                const [local, dominio] = partes;

                if (dominioInvalido(local)) {{
                    error("El correo no puede contener dominios antes del @");
                    return;
                }}

                if (!EMAIL_REGEX.test(corregido)) {{
                    error("Correo electrónico no válido");
                    return;
                }}

                // ✔ Válido
                input.style.borderColor = "green";
                msg.style.display = "none";
            }};

            function error(texto) {{
                input.style.borderColor = "red";
                msg.innerText = "❌ " + texto;
                msg.style.display = "block";
            }}

            input.addEventListener("input", validar);
            input.addEventListener("blur", validar);

            validar();
            input.dataset.emailSmartActive = "true";
        }}

        setup();
        setInterval(setup, 600);
    }})();
    </script>
    """, height=0)

    return valor



def mostrar_nata():
    logo_bandera = ASSETS_DIR / "imagebanderanueva2.png"
    logo_base64 = img_a_base64(logo_bandera)
    st.set_page_config(layout="wide", page_icon=logo_bandera)
    recargar_una_vez(__file__) # Llama a la función para recargar la página una vez.
    logo(tamano="100%")
    
    if "autenticado_usuario" not in st.session_state:
        st.error("Debes iniciar sesión para acceder a esta area.", icon=":material/error:")
        return

    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)

    if not info_usuario:
        st.error("Usuario no encontrado. Por favor, inicia sesión nuevamente.", icon=":material/error:")
        return
    
    tab1, tab2 = st.tabs(["| :material/pregnant_woman: Natalidad |", 
                                "| :material/article_shortcut: Reporte General |"])
    with tab1:
        formulario_natalidad()
        #codigo = text_input_max_3_con_mensaje("Código", key="codigo")
        #correo = email_input_validado_inteligente("Correo electrónico", key="email")

    with tab2:
        st.subheader(":material/arrow_circle_down: Descargas de reportes", anchor=False, divider="gray")
        col_izq, col_centro, col_der = st.columns([3.35, 4, 2.65])
        #with col_izq:
            #formulario_reporte_mensual_combinado()
        #st.markdown("---")
        with col_centro:
            formulario_reporte_general_natalidad()
        #st.markdown("---")
        #with col_der:
            #formulario_reporte_mensual_general()
        st.markdown("")
    copyright_footer_dos("Equipo Investigador")

mostrar_nata()