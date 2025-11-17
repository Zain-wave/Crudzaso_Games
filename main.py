import asyncio
import multiprocessing

from auth import iniciar_sesion, registrar_usuario
from admin import menu_admin
from data import log_in, registrar
from utils import iniciar_musica
from menu_pp import menu  # menú de usuario

async def main():
    iniciar_musica()
    
    usuario_actual = None  # Estado de sesión
    salir = False

    while not salir:
        if not usuario_actual:
            print("==================================")
            print("=     Bienvenido a Cursdazo Trivia     =")
            print("==================================\n")

            print("1. Iniciar sesión")
            print("2. Registrarse")
            print("3. Salir\n")

            opcion = input("Selecciona una opción (1-3): ").strip()

            match opcion:
                case "1":
                    usuario, contraseña = log_in()
                    print("")

                    datos_usuario = iniciar_sesion(usuario, contraseña)
                    if datos_usuario:
                        usuario_actual = datos_usuario
                        rol = datos_usuario["rol"]

                        if rol == "admin":
                            print("\n¡Bienvenido administrador!\n")
                            menu_admin()
                            usuario_actual = None
                        else:
                            print(f"\n¡Bienvenido de nuevo, {usuario}!\n")
                            menu(usuario_actual)
                    else:
                        print("\nUsuario o contraseña incorrectos.\n")

                case "2":
                    datos = registrar()
                    if datos is None:
                        continue

                    usuario, contraseña = datos
                    if registrar_usuario(usuario, contraseña):
                        print("\n¡Usuario registrado correctamente!\n")
                        usuario_actual = {"usuario": usuario, "rol": "user"}
                        menu(usuario_actual)
                    else:
                        print("\nEl usuario ya existe.\n")

                case "3":
                    salir = True

                case _:
                    print("\nOpción no válida.\n")

        else:
            menu(usuario_actual)
            usuario_actual = None  

    print("Saliendo del sistema... Gracias por jugar :)")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    asyncio.run(main())
