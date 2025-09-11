import base64

# meter aqui todas las conversiones de base 64 para no hacer 1 x archivo

# Función para convertir una imagen a base64
def img_a_base64(img_path):
    with open(img_path, "rb") as img_file:
        b64_str = base64.b64encode(img_file.read()).decode()
    return b64_str