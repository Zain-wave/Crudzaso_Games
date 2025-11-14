def mostrar_menu_pp():
    print("==================================")
    print("=     Bienvenido a Cursdazo Trivia     =")
    print("==================================")

    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir")
    print("")

    opcion = input("Selecciona una opción (1-3): ").strip()

    if opcion in ("1", "2", "3"):
        return opcion
    return None
    


def menu():
    print("==================================")
    print("=          Menú de Juego          =")
    print("==================================")

    print("1. Iniciar juego")
    print("2. Puntuación")
    print("3. Jugar Punto Suicida")
    print("4. Jugar Contrarreloj")
    print("5. Randomize")
    print("6. Menú principal")
    print("")

    opcion_juego = input("Selecciona una opción (1-6): ").strip()

    if opcion_juego in ("1", "2", "3", "4", "5", "6"):
        return opcion_juego
    return None
