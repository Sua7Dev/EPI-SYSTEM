import streamlit as st  
import pandas as pd
import sqlite3
import os
from datetime import date, datetime
from pathlib import Path
from utils.verificaciones import obtener_info_usuario


DB_PATH = os.getenv("hospital.db", "hospital.db")
PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_ACTIVIDADES = PROJECT_ROOT / "actividades.log"


def registrar_actividad_duradera(
    accion: str,
    modulo: str,
    id_registro: str | int = "-",
    usuario: str = None
):
    # Si no se pasa usuario explícitamente y no hay usuario autenticado, NO registrar nada
    if usuario is None:
        autenticado = st.session_state.get("autenticado_usuario")
        if autenticado is None:
            return  # No se escribe en el log → "Desconocido" nunca aparecerá
        usuario = autenticado

    try:
        id_str = f"ID:{id_registro}" if id_registro != "-" else "-"
        now = datetime.now()

        fecha_hora = now.strftime("%d/%m/%Y %I:%M:%S %p")
        linea = f"{fecha_hora} | {usuario} | {modulo} | {accion} | {id_str}\n"

        with open(LOG_ACTIVIDADES, "a", encoding="utf-8") as f:
            f.write(linea)
    except Exception:
        pass

def obtener_datos_historial(nombre_usuario: str):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT p.nombre_apellido, u.rol, p.CI
                FROM usuario u
                JOIN persona p ON u.CI = p.CI
                WHERE u.nombre_usuario = ?
            """, (nombre_usuario,))
            result = cursor.fetchone()

            if result:
                nombre_apellido, rol, ci = result
                nombre, apellido = (
                    nombre_apellido.split(" ", 1)
                    if " " in nombre_apellido
                    else (nombre_apellido, "")
                )
                return {
                    "nombre": nombre.strip(),
                    "apellido": apellido.strip(),
                    "rol": rol,
                    "cedula": f"V-{ci}" if ci else "N/A"
                }
    except Exception:
        pass

    return None


def mostrar_historial_actividades():
    if "autenticado_usuario" not in st.session_state:
        return

    nombre_usuario = st.session_state["autenticado_usuario"]
    info_usuario = obtener_info_usuario(nombre_usuario)

    if not info_usuario:
        return

    with st.expander("Historial de actividades", expanded=False, icon=":material/history:"):
        st.subheader(":material/chronic: Registro de acciones", anchor=False)

        if not os.path.exists(LOG_ACTIVIDADES):
            st.info("No hay actividades registradas aún.")
            return

        try:
            with open(LOG_ACTIVIDADES, "r", encoding="utf-8") as f:
                lineas = f.readlines()[::-1]
        except Exception as e:
            st.error(f"Error leyendo historial: {e}")
            return

        datos = []

        for linea in lineas:
            partes = linea.strip().split(" | ")
            if len(partes) != 5:
                continue

            fecha_hora_raw, usuario_log, modulo, accion_raw, id_raw = partes
            id_reg = id_raw.replace("ID:", "") if id_raw.startswith("ID:") else id_raw

            try:
                fecha_dt = datetime.strptime(
                    fecha_hora_raw,
                    "%d/%m/%Y %I:%M:%S %p"
                )
            except ValueError:
                continue

            fecha_str = fecha_dt.strftime("%d/%m/%Y")
            hora_str = fecha_dt.strftime("%I:%M:%S %p") 

            info = obtener_datos_historial(usuario_log)
            if info:
                nombre_completo = f"{info['nombre']} {info['apellido']}".strip()
                rol = info["rol"]
                cedula = info["cedula"]
                if rol == "Administrador (a)":
                    usuario_mostrar = f"{nombre_completo} ({rol})"
                else:
                    usuario_mostrar = f"{nombre_completo} ({rol} - C.I: {cedula})"
            else:
                usuario_mostrar = usuario_log

            accion_texto = {
                "CREADO": "Registro creado",
                "EDITADO": "Registro editado",
                "ELIMINADO": "Registro eliminado",
                "DESCARGA PDF": "Descarga de PDF",
                "LOGIN": "Inicio de sesión",
                "LOGOUT": "Cierre de sesión"
            }.get(accion_raw, accion_raw)

            datos.append({
                "Fecha": fecha_str,
                "Hora": hora_str,  
                "Usuario": usuario_mostrar,
                "Módulo": modulo,
                "Acción realizada": accion_texto,
                "ID del registro": id_reg if id_reg != "-" else "-",
                "fecha_dt": fecha_dt
            })

        if not datos:
            st.info("No hay actividades registradas aún.")
            return

        df = pd.DataFrame(datos)

        # Asegurar que fecha_dt es datetime64 (necesario para .dt)
        df["fecha_dt"] = pd.to_datetime(df["fecha_dt"], errors="coerce")

        fecha_min = df["fecha_dt"].min().date()
        fecha_max = df["fecha_dt"].max().date()

        col1, col2, col3, col4, col5 = st.columns(5)

        for name in ("modulos", "usuarios", "acciones"):
            key_prev = f"prev_{name}"
            if key_prev not in st.session_state:
                st.session_state[key_prev] = ["Todos"]

        def _multiselect_on_change(key):
            current = st.session_state.get(key, [])
            prev_key = f"prev_{key.split('_', 1)[1]}"
            prev = st.session_state.get(prev_key, ["Todos"])

            if "Todos" in current and "Todos" not in prev:
                st.session_state[key] = ["Todos"]
                st.session_state[prev_key] = ["Todos"]
                return

            if "Todos" in prev and "Todos" in current and len(current) > 1:
                new = [c for c in current if c != "Todos"]
                st.session_state[key] = new
                st.session_state[prev_key] = new
                return

            if len(current) == 0:
                st.session_state[key] = ["Todos"]
                st.session_state[prev_key] = ["Todos"]
                return

            st.session_state[prev_key] = st.session_state.get(key, current)

        key_mod = "ms_modulos"
        key_usr = "ms_usuarios"
        key_acc = "ms_acciones"

        opciones_mod = sorted(df["Módulo"].unique())
        opciones_usr = sorted(df["Usuario"].unique())
        opciones_acc = sorted(df["Acción realizada"].unique())

        with col1:
            if key_mod not in st.session_state:
                st.session_state[key_mod] = ["Todos"]
            modulos_f = st.multiselect(
                ":material/view_module: Módulos",
                options=["Todos"] + opciones_mod,
                default=st.session_state[key_mod],
                key=key_mod,
                on_change=_multiselect_on_change,
                args=(key_mod,)
            )

        with col2:
            if key_usr not in st.session_state:
                st.session_state[key_usr] = ["Todos"]
            usuarios_f = st.multiselect(
                ":material/patient_list: Usuarios",
                options=["Todos"] + opciones_usr,
                default=st.session_state[key_usr],
                key=key_usr,
                on_change=_multiselect_on_change,
                args=(key_usr,)
            )

        with col3:
            if key_acc not in st.session_state:
                st.session_state[key_acc] = ["Todos"]
            acciones_f = st.multiselect(
                ":material/action_key: Acciones",
                options=["Todos"] + opciones_acc,
                default=st.session_state[key_acc],
                key=key_acc,
                on_change=_multiselect_on_change,
                args=(key_acc,)
            )

        with col4:
            fecha_desde = st.date_input(
                ":material/calendar_clock: Desde",
                fecha_min,
                format="DD/MM/YYYY"
            )

        with col5:
            fecha_hasta = st.date_input(
                ":material/event_upcoming: Hasta",
                fecha_max,
                format="DD/MM/YYYY"
            )

        modulos_f = st.session_state.get(key_mod, ["Todos"])
        usuarios_f = st.session_state.get(key_usr, ["Todos"])
        acciones_f = st.session_state.get(key_acc, ["Todos"])

        f = df.copy()

        if "Todos" not in modulos_f:
            f = f[f["Módulo"].isin(modulos_f)]
        if "Todos" not in usuarios_f:
            f = f[f["Usuario"].isin(usuarios_f)]
        if "Todos" not in acciones_f:
            f = f[f["Acción realizada"].isin(acciones_f)]

        f = f[
            (f["fecha_dt"].dt.date >= fecha_desde) &
            (f["fecha_dt"].dt.date <= fecha_hasta)
        ]

        f = f.sort_values(by="fecha_dt", ascending=False)

        st.markdown("**:material/filter_alt: Filtros aplicados:**")
        filtros_texto = []
        if "Todos" not in modulos_f:
            filtros_texto.append("Módulos: " + ", ".join(modulos_f))
        if "Todos" not in usuarios_f:
            filtros_texto.append("Usuarios: " + ", ".join(usuarios_f))
        if "Todos" not in acciones_f:
            filtros_texto.append("Acciones: " + ", ".join(acciones_f))
        if filtros_texto:
            st.markdown(" | ".join(filtros_texto))
        else:
            st.markdown("Todos los registros")


        display_df = f.copy()


        display_df["Hora"] = display_df["fecha_dt"].apply(
            lambda x: x.strftime("%I:%M:%S") + (" AM" if x.hour < 12 else " PM")
)


        display_df = display_df[
            ["Fecha", "Hora", "Usuario", "Módulo", "Acción realizada", "ID del registro"]
        ].copy()


        column_config = {
            "Fecha": st.column_config.TextColumn("Fecha"),
            "Hora": st.column_config.TextColumn(
                "Hora", 
                help="Hora de la actividad",
                disabled=True
            ),
            "ID del registro": st.column_config.TextColumn("ID del registro")
        }

        if display_df.empty:
            st.warning("No se encontraron actividades que coincidan con los filtros seleccionados.", icon=":material/search_off:")
        else:
            st.data_editor(
                display_df,
                use_container_width=True,
                hide_index=True,
                disabled=True, 
                column_config=column_config
            )