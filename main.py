from auth import iniciar_sesion, registrar_usuario
from admin import menu_admin
from data import log_in, registrar
from utils import iniciar_musica, menu_vertical
from menu_pp import menu 
import readchar
import os

def menu_inicio_sesion():
    opciones = ["Ingresar usuario y contraseña", "Volver al menú principal"]
    seleccion = 0
    
    while True:
        os.system("cls")
        print("\n" * 2)
        print(" " * 10 + "=" * 50)
        print(" " * 10 + "         INICIAR SESIÓN")
        print(" " * 10 + "=" * 50)
        print("\n")
        
        for i, opcion in enumerate(opciones):
            prefix = "➤ " if i == seleccion else "  "
            print(" " * 15 + f"{prefix}{opcion}")
        
        print("\n" * 2)
        print(" " * 10 + "Usa las flechas ↑↓ para navegar • ENTER para seleccionar")
        
        key = readchar.readkey()
        if key == readchar.key.UP:
            seleccion = (seleccion - 1) % len(opciones)
        elif key == readchar.key.DOWN:
            seleccion = (seleccion + 1) % len(opciones)
        elif key == readchar.key.ENTER:
            return seleccion

def menu_registro():
    opciones = ["Completar registro", "Volver al menú principal"]
    seleccion = 0
    
    while True:
        os.system("cls")
        print("\n" * 2)
        print(" " * 10 + "=" * 50)
        print(" " * 10 + "           REGISTRO")
        print(" " * 10 + "=" * 50)
        print("\n")
        
        for i, opcion in enumerate(opciones):
            prefix = "➤ " if i == seleccion else "  "
            print(" " * 15 + f"{prefix}{opcion}")
        
        print("\n" * 2)
        print(" " * 10 + "Usa las flechas ↑↓ para navegar • ENTER para seleccionar")
        
        key = readchar.readkey()
        if key == readchar.key.UP:
            seleccion = (seleccion - 1) % len(opciones)
        elif key == readchar.key.DOWN:
            seleccion = (seleccion + 1) % len(opciones)
        elif key == readchar.key.ENTER:
            return seleccion

def main():
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
                        opcion_login = menu_vertical(
                            "Iniciar Sesión", 
                            ["Ingresar usuario y contraseña", "Volver"]
                        )
                        if opcion_login == 1:
                            usuario, contraseña = log_in()
                            datos_usuario = iniciar_sesion(usuario, contraseña)

                            if datos_usuario:
                                usuario_actual = datos_usuario
                                os.system("cls")
                                
                                if datos_usuario["rol"] == "admin":
                                    menu_admin()
                                    usuario_actual = None
                                else:
                                    resultado = menu(usuario_actual)
                                    if resultado is False:
                                        usuario_actual = None
                            else:
                                print("\n❌ Usuario o contraseña incorrectos.\n")
                                readchar.readkey()

                case 2:
                    opcion_registro = menu_vertical(
                        "Registro",
                        ["Completar registro", "Volver"]
                    )
                    if opcion_registro == 1:
                        datos = registrar()
                        if not datos:
                            continue

                        usuario, contraseña = datos
                        if registrar_usuario(usuario, contraseña):
                            usuario_actual = {"usuario": usuario, "rol": "user"}
                            resultado = menu(usuario_actual)
                            if resultado is False:
                                usuario_actual = None
                        else:
                            print("\nEl usuario ya existe.\n")
                            readchar.readkey()

                case 3:
                    salir = True

        else:
            resultado = menu(usuario_actual)
            if resultado is False:
                usuario_actual = None

    print("Saliendo del sistema... Gracias por jugar :)")
if __name__ == "__main__":
    main()