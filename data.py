def tiene_numero(cadena: str) -> bool:
    return any(char.isdigit() for char in cadena)


def registrar():
    try:
        edad = int(input("¿Cuál es tu edad?: "))
    except ValueError:
        print("Edad inválida. Inténtalo de nuevo.\n")
        return None

    if edad < 5:
        print("Perdón, no puedes jugar. Cerrando sistema...")
        return None

    nombre = input("Queremos conocerte, ¿Cuál es tu nombre?: ").strip()

    if tiene_numero(nombre):
        print("\nUps, tu nombre contiene número(s). Regístrate nuevamente.\n")
        return None

    nombre_usuario = input("Nombre de usuario para el juego: ").strip()

    while True:
        contraseña = input("Crea una contraseña: ").strip()
        repetir = input("Repite la contraseña: ").strip()

        if contraseña == repetir:
            break
        print("\nLas contraseñas no coinciden. Inténtalo nuevamente.\n")

    print("\n¡Registro exitoso!")
    print(f"Edad: {edad}")
    print(f"Nombre real: {nombre}")
    print(f"Usuario: {nombre_usuario}")
    print ("==================================")


    return nombre_usuario, contraseña


def log_in():
    usuario = input("Ingresa tu nombre de usuario: ").strip()
    contraseña = input("Ingresa tu contraseña: ").strip()
    return usuario, contraseña