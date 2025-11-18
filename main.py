import asyncio
import multiprocessing

from auth import iniciar_sesion, registrar_usuario
from admin import menu_admin
from data import log_in, registrar
from utils import iniciar_musica, menu_vertical
from menu_pp import menu 


async def main():
    iniciar_musica()
    
    usuario_actual = None  
    salir = False

    while not salir:

        if not usuario_actual:

            opcion = menu_vertical(
                "Bienvenido a Cursdazo Trivia",
                ["Iniciar sesión", "Registrarse", "Salir"]
            )

            match opcion:
                case 1:
                    usuario, contraseña = log_in()
                    datos_usuario = iniciar_sesion(usuario, contraseña)

                    if datos_usuario:
                        usuario_actual = datos_usuario

                        if datos_usuario["rol"] == "admin":
                            menu_admin()
                            usuario_actual = None
                        else:
                            menu(usuario_actual)

                    else:
                        print("\nUsuario o contraseña incorrectos.\n")

                case 2:
                    datos = registrar()
                    if not datos:
                        continue

                    usuario, contraseña = datos
                    if registrar_usuario(usuario, contraseña):
                        usuario_actual = {"usuario": usuario, "rol": "user"}
                        menu(usuario_actual)
                    else:
                        print("\nEl usuario ya existe.\n")

                case 3:
                    salir = True

        else:
            menu(usuario_actual)
            usuario_actual = None

    print("Saliendo del sistema... Gracias por jugar :)")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    asyncio.run(main())
