# {
#     "usuario": "nombre_de_usuario",
#     "contraseña": "hash_bcrypt",
#     "puntuaciones": []
# }

import json
import os
import bcrypt

ARCHIVO_USUARIOS = "users.json"

def cargar_usuarios():
    if not os.path.exists(ARCHIVO_USUARIOS):
        return []
    with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as archivo_json:
        return json.load(archivo_json)


def guardar_usuarios(usuarios):
    with open(ARCHIVO_USUARIOS, "w", encoding="utf-8") as archivo_json:
        json.dump(usuarios, archivo_json, indent=4, ensure_ascii=False)

def registrar_usuario(nombre_usuario: str, contraseña: str):
    usuarios = cargar_usuarios()

    if any(u["usuario"] == nombre_usuario for u in usuarios):
        print("El usuario ya existe.")
        return False

    hash_contraseña = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

    nuevo_usuario = {
        "usuario": nombre_usuario,
        "contraseña": hash_contraseña.decode('utf-8'),
        "puntuaciones": []
    }

    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)
    print(f"Usuario '{nombre_usuario}' creadp correctamente.")
    return True

def iniciar_sesion(nombre_usuario: str, contraseña: str):
    pass

registrar_usuario("Sebastian", "123")
