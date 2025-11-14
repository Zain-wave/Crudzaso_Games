from auth import iniciar_sesion, registrar_usuario
from menu import mostrar_menu_pp, menu
from data import log_in, registrar

def main():
    salir = False
    
    while not salir:
        print("")
        opcion = mostrar_menu_pp()

        match opcion:
            case "1":
                usuario, contraseña = log_in()
                print("")

                if iniciar_sesion(usuario, contraseña):
                    print(f"\n¡Bienvenido de nuevo, {usuario}!\n")
                    menu()
                else:
                    print("\nUsuario o contraseña incorrectos.\n")

            case "2":
                datos = registrar()

                if datos is None:
                    continue
                
                usuario, contraseña = datos
                if registrar_usuario(usuario, contraseña):
                    print("\n¡Usuario registrado correctamente!\n")
                    menu()
                else:
                    print("\nEl usuario ya existe.\n")

            case "3":
                salir = True

            case _:
                print("\nOpción no válida.\n")

    print("Saliendo del sistema... Gracias por jugar :)")

if __name__ == "__main__":
    main()
