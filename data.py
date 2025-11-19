from utils import esperar_tecla

def registrar():
    nombre_usuario = input("Nombre de usuario para el juego: ").strip()

    while True:
        contraseña = input("Crea una contraseña: ").strip()
        repetir = input("Repite la contraseña: ").strip()

        if contraseña == repetir:
            break
        print("\nLas contraseñas no coinciden. Inténtalo nuevamente.\n")

    print("\n¡Registro exitoso!")
    print(f"Usuario: {nombre_usuario}")
    print("==================================")
    esperar_tecla()

    return nombre_usuario, contraseña


def log_in():
    usuario = input("Ingresa tu nombre de usuario: ").strip()
    contraseña = input("Ingresa tu contraseña: ").strip()
    return usuario, contraseña