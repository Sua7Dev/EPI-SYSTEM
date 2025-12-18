import re
import streamlit as st
from datetime import datetime

# Función para validar que el contenido sea texto válido
# campo se reemplaza por el mensaje que se quiera dar
def validar_texto(texto, el_la, campo):
    if texto.strip() == "":
        st.error(f"{el_la} {campo} no puede estar vacío.", icon=":material/error:")
        return False
    if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ' ]+", texto):
        st.error(f"{el_la} {campo} solo debe contener letras, espacios o el carácter especial '", icon=":material/error:")
        return False
    return True

def validar_pais(texto, el_la, campo):
    # Permitir que el campo esté vacío
    if not texto or texto.strip() == "":
        return True
    # Si no está vacío, aplicar la validación de texto
    if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ' ]+", texto):
        st.error(f"{el_la} {campo} solo debe contener letras, espacios o el carácter especial '", icon=":material/error:")
        return False
    return True

# Funcion para validar que no hayan mas de 5 espacios
def validar_cinco_espacios(texto, el_la, campo):
    cantidad_espacios = texto.count(" ") # cuenta los espacios, obvio no?
    if cantidad_espacios > 5:
        st.error(f"{el_la} {campo} no puede tener más de 5 espacios. Justo ahora tiene {cantidad_espacios}", icon=":material/error:")
        return False
    return True

# Función para validar el nombre de usuario
def validar_nombre_usuario(nombredeusuario):
    # Expresión regular: no puede contener espacios
    if " " in nombredeusuario:
        st.error("El nombre de usuario no puede contener espacios.", icon=":material/error:")
        return False
    # Expresión regular: mínimo 3 letras, puede contener números, pero no solo números, y sin caracteres especiales
    if not re.fullmatch(r"(?=.*[a-zA-ZñÑ])[a-zA-ZñÑ0-9]{3,}", nombredeusuario):
        st.error("El nombre de usuario debe tener al menos 3 caracteres, pero no caracteres especiales ni ser solo números.", icon=":material/error:")
        return False
    return True

# valida que un Texto no tenga solo espacio y q pueda tener numeros y letras
# el_la se reempalza segun convenga
def val_texynum(texynum, el_la, campo):
    if texynum.strip() == "":
        st.error(f"{el_la} {campo} no puede estar vacía.", icon=":material/error:")
        return False
    # Expresión regular: permite letras, números, espacios y los caracteres especiales - y /
    if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\-/]+", texynum):
        st.error(f"{el_la} {campo} solo debe contener letras, números, espacios y los caracteres especiales - y /", icon=":material/error:")
        return False
    return True

# Función para validar correo electrónico
def val_mail(mail):
    # Diccionario de correos permitidos
    dominios_permitidos = {
        "@gmail.com": "Correo de Gmail",
        "@outlook.com": "Correo de Outlook",
        "@yahoo.com": "Correo de Yahoo",
        "@hotmail.com": "Correo de Hotmail",
        "@ymail.com": "Correo de Ymail",
        "@protonmail.com": "Correo de ProtonMail"
    }

    # Verifica si el correo está vacío o tiene espacios
    if " " in mail:
        st.error("El correo no puede contener espacios", icon=":material/error:")
        return False

    # Verifica que solo haya un @ en el correo
    if mail.count("@") != 1:
        st.error("El correo debe contener exactamente un '@'", icon=":material/error:")
        return False

    # Verifica que el correo comience con una letra del alfabeto
    if not re.match(r"^[a-zA-ZñÑ]", mail):
        st.error("El correo debe comenzar con una letra del alfabeto", icon=":material/error:")
        return False

    # Verifica que el correo tenga un formato válido antes del dominio
    if not re.match(r"^[a-zA-ZñÑ0-9._%+-]+@[a-zA-ZñÑ0-9.-]+\.[a-zA-ZñÑ]{2,}$", mail):
        st.error("El correo no tiene un formato válido", icon=":material/error:")
        return False

    # Palabras restringidas antes del dominio
    palabras_restringidas = ["gmail", "outlook", "yahoo", "ymail", "protonmail"]
    local_part = mail.split("@")[0]  # Parte antes del @

    # Verifica que la parte antes del dominio no sea completamente numérica
    if local_part.isdigit():
        st.error("La parte antes del dominio no puede ser completamente numérica", icon=":material/error:")
        return False

    # Verifica que la parte antes del dominio no contenga palabras restringidas
    if any(palabra in local_part.lower() for palabra in palabras_restringidas):
        st.error("El correo no puede contener palabras restringidas como 'gmail', 'outlook', 'yahoo', etc., antes del dominio", icon=":material/error:")
        return False

    # Verifica que "com" no aparezca sola antes del dominio #
    if "com" in local_part.lower().split("."):
        st.error("La palabra 'com' no puede aparecer sola antes del dominio", icon=":material/error:")
        return False

    # Verifica si el correo termina con alguno de los dominios permitidos
    if not any(mail.endswith(dominio) for dominio in dominios_permitidos):
        st.error("Dominio del correo incorrecto", icon=":material/error:")
        return False

    return True

# Función para validar la contraseña
def validar_contraseña(contraseña):
    requisitos = [
        (8 <= len(contraseña) <= 16, 'La contraseña debe tener entre 8 y 16 caracteres.'),
        (re.search(r"[a-zñ]", contraseña), 'La contraseña debe contener al menos una letra minúscula.'),
        (re.search(r"[A-ZÑ]", contraseña), 'La contraseña debe contener al menos una letra mayúscula.'),
        (re.search(r"[0-9]", contraseña), 'La contraseña debe contener al menos un número.'),
        (' ' not in contraseña, 'La contraseña no puede contener espacios.')
    ]
    for valido, mensaje in requisitos:
        if not valido:
            st.error(mensaje, icon=":material/error:")
            return False
    return True

# Funcion para validar notas, ahora sirve para campos iguales a notas
def val_notas(notas, el_la, campo):
    # Permitir que el campo esté vacío
    if notas.strip() == "":
        return True
    # Verificar que no sea solo números
    if notas.isdigit():
        st.error(f"{el_la} {campo} no puede contener solo números.", icon=":material/error:")
        return False

    # Expresión regular para validar el contenido d
    if not re.fullmatch(r"(?=.*[a-zA-ZáéíóúÁÉÍÓÚñÑ])[\w\s\-/',.#]+", notas):
        st.error(f"{el_la} {campo} solo puede contener letras, números y los caracteres especiales ' / -.,#", icon=":material/error:")
        return False



    # Expresión regular para validar el contenido.
    # Se asegura de que haya al menos una letra y que los caracteres sean válidos.
    if not re.fullmatch(r"(?=.*[a-zA-ZáéíóúÁÉÍÓÚñÑ])[\w\s\-/',.#]+", notas):
        st.error(f"{el_la} {campo} solo puede contener letras, números y los caracteres especiales ' / - . , #", icon=":material/error:")
        return False

    return True

# Funcion para validar que las fechas no se alteren en las tablas editables
def fecha_no_editable(df_original, df_editado):
    for index, row in df_editado.iterrows():
        # Comparar la fecha original con la fecha editada
        if row['fecha'] != df_original.loc[index, 'fecha']:
            st.error(f"La fecha del registro con ID {row['id']} no puede ser modificada. Corrige este cambio antes de guardar.", icon=":material/error:")
            return False
    return True

# Funcion para dejar campos con solo numeros y espacios
def val_num_espacios(campo, el_la, nombre_campo):
    if campo.strip() == "":
        st.error(f"{el_la} {nombre_campo} no puede estar vacío.", icon=":material/error:")
        return False
    
    cantidad_espacios = campo.count(" ") # cuenta los espacios, obvio no?
    if cantidad_espacios > 3:
        st.error(f"{el_la} {nombre_campo} no puede tener más de 3 espacios. Justo ahora tiene {cantidad_espacios}", icon=":material/error:")
        return False
    
    # Expresión regular: permite solo números y espacios
    if not re.fullmatch(r"[0-9\s\-/]+", campo):
        st.error(f"{el_la} {nombre_campo} solo debe contener números y espacios.", icon=":material/error:")
        return False
    return True

# Funcion para validar que algo es solo numeros sin espaacio ( usada en la cedula)
def val_solo_numeros(campo, el_la, nombre_campo):
    if campo.strip() == "":
        st.error(f"{el_la} {nombre_campo} no puede estar vacío.", icon=":material/error:")
        return False

    # Expresión regular: permite solo números
    if not re.fullmatch(r"[0-9]+", campo):
        st.error(f"{el_la} {nombre_campo} solo debe contener números.", icon=":material/error:")
        return False

    return True

# Funcion para validar que la nueva contraseña sea diferente a la anterior
def contra_igual(nueva_contra, contra_anterior):
    if nueva_contra == contra_anterior:
        st.error("La contraseña nueva no puede ser igual a la anterior.", icon=":material/error:")
        return False
    return True

# Funcion para validar que la fecha de nacimiento sea mayor a 18 años
def mayor_de_edad(fecha_nacimiento):
    hoy = datetime.now().date()
    diferencia_anos = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

    if diferencia_anos < 18:
        st.error("No puedes registrarte si no eres mayor de edad.", icon=":material/error:")
        return False
    return True

def val_diagnostico(diagnostico, el_la, campo):
    """
    Valida un diagnóstico:
    - No puede estar vacío.
    - Permite letras, números, espacios, paréntesis '()' y los caracteres '- / ' . ,'
    """
    if diagnostico.strip() == "":
        st.error(f"{el_la} {campo} no puede estar vacío.", icon=":material/error:")
        return False

    if "#" in diagnostico:
        st.error(f"{el_la} {campo} no puede contener el carácter '#'.", icon=":material/error:")
        return False

    # Permitir letras, números, acentos, espacios, paréntesis y los símbolos - / ' . ,
    if not re.fullmatch(r"[a-zA-ZáéíóúÁÉÍÓÚñÑ0-9\s\-\(\)\/'.,]+", diagnostico):
        st.error(f"{el_la} {campo} solo puede contener letras, números, espacios, paréntesis y los caracteres - / ' . ,", icon=":material/error:")
        return False

    return True