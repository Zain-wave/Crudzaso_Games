import asyncio
import multiprocessing

from auth import iniciar_sesion, registrar_usuario
from admin import menu_admin
from data import log_in, registrar
from utils import iniciar_musica
from menu import mostrar_menu_pp, menu

async def main():
    iniciar_musica()

    salir = False
    
    while not salir:
        print("")
        opcion = mostrar_menu_pp()

        match opcion:
            case "1":
                usuario, contraseña = log_in()
                print("")

                datos_usuario = iniciar_sesion(usuario, contraseña)

                if datos_usuario:
                    rol = datos_usuario["rol"]

                    if rol == "admin":
                        print("\nBienvenido administrador.\n")
                        menu_admin()
                    else:
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
    #para que windows permita el loop
    multiprocessing.freeze_support()
    asyncio.run(main())
