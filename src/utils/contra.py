# Funciones relacionadas con las contraseñas

import os
import hashlib
import hmac

# Funcion para hashear contraseñas
# Primero la configuracion del hash
ITERATION = 1000 # Iteraciones para el hash, mientras mas, mas seguro y mas lento
SALT_SIZE = 16 # sal en bytes
HASH_ALGORITHM = 'sha256' # Algoritmo de hash a usar, sha256 es el mas comun y seguro

# y ahora la funcion
def borro_cassette(contrasena1):
    salt = os.urandom(SALT_SIZE) # Genera una sal aleatoria

    hashed_bytes = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        contrasena1.encode('utf-8'), # Convierte la contrasena a bytes
        salt,
        ITERATION
    )

    salt_hex = salt.hex() # Convierte la sal a hexadecimal
    hash_hex = hashed_bytes.hex() # Convierte el hash a hexadecimal

    stored_hash = f"{HASH_ALGORITHM}${ITERATION}${salt_hex}${hash_hex}" 
    # Guarda el hash en el formato: iteraciones$sal$hash
    return stored_hash # Devuelve el hash completo

# Funcion para verificar contraseñas
def verifi_contra_hasheada(contrasena1, hash_contrasena):
    try:
        # Si no hay hash disponible, no se puede verificar
        if not hash_contrasena or not isinstance(hash_contrasena, str):
            return False
        algorithm, iterations_str, salt_hex, hash_hex = hash_contrasena.split('$') # Separa el hash en sus partes
        iterations = int(iterations_str) # Convierte las iteraciones a entero
        salt = bytes.fromhex(salt_hex) # Convierte la sal de hexadecimal a bytes
        hash_bytes = bytes.fromhex(hash_hex) # Convierte el hash de hexadecimal a bytes
        # Hashea la contrasena introducida con la sal y el algoritmo
        hashed_bytes = hashlib.pbkdf2_hmac(
            algorithm,
            contrasena1.encode('utf-8'),
            salt,
            iterations
        )
        return hmac.compare_digest(hash_bytes, hashed_bytes) # Compara el hash guardado con el nuevo hash
    
    except (ValueError, IndexError):
        # Si el hash no es valido, devuelve False
        return False