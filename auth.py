import json
import os
import bcrypt
from utils import esperar_tecla

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
        "rol": "user",
        "puntuaciones": []
    }

    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)
    print(f"Usuario '{nombre_usuario}' creado correctamente.")
    esperar_tecla()
    return True

def iniciar_sesion(nombre_usuario: str, contraseña: str):
    usuarios = cargar_usuarios()
    usuario = next((u for u in usuarios if u["usuario"] == nombre_usuario), None)

    if not usuario:
        print("Usuario no existe")
        esperar_tecla()
        return None

    if bcrypt.checkpw(contraseña.encode('utf-8'), usuario["contraseña"].encode('utf-8')):
        print(f"Iniciaste sesión exitosamente - '{nombre_usuario}'.")
        return usuario
    else:
        print("Contraseña incorrecta.")
        esperar_tecla()
        return None

def guardar_puntaje(usuario_actual, modo, dificultad, puntaje):
    usuarios = cargar_usuarios()

    for u in usuarios:
        if u["usuario"] == usuario_actual["usuario"]:
            if "puntuaciones" not in u:
                u["puntuaciones"] = []
            
            u["puntuaciones"].append({
                "modo": modo,
                "dificultad": dificultad,
                "puntaje": puntaje
            })
            break

    guardar_usuarios(usuarios)
