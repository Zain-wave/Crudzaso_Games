from game import (
    jugar_trivia,
    jugar_suicida,
    jugar_contrarreloj
)

def menu(usuario_actual=None):
    nick = usuario_actual.get("usuario") if usuario_actual else "Invitado"

    while True:
        print("\n==================================")
        print(f"=      Menú de Juego - {nick}       =")
        print("==================================\n")

        print("1. Iniciar juego (Trivia Normal)")
        print("2. Puntuación")
        print("3. Jugar Punto Suicida")
        print("4. Jugar Contrarreloj")
        print("5. Randomize")
        print("6. Cerrar sesión / Volver al menú principal\n")

        opcion_juego = input("Selecciona una opción (1-6): ").strip()

        if opcion_juego == "1":
            jugar_trivia()
        elif opcion_juego == "2":
            print("Sistema de puntuación en desarrollo.")
        elif opcion_juego == "3":
            jugar_suicida()
        elif opcion_juego == "4":
            jugar_contrarreloj()
        elif opcion_juego == "5":
            print("Randomize aún no está implementado.")
        elif opcion_juego == "6":
            print("\nCerrando sesión...\n")
            break
        else:
            print("Opción no válida.")
