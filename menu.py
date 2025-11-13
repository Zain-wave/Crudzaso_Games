def mostrar_menu():

    print ("==================================")
    print ("= Bienvenido a Cursdazo Trivia =")
    print ("==================================")
    
    print ("Selecciona una opción:")

mostrar_menu()

opcion = (input("1. log in\n2. registrarse\n3. selección de dificultad\n4 Logros \n5 Salir\n"))
cont = 1

while cont == 1:
    if opcion == "1":
        cont = 2
        print("Redirigiendo a la página de inicio de sesión...")
    elif opcion == "2":
        cont = 2
        print("Redirigiendo a la página de registro...")
    elif opcion == "3":
        print("Redirigiendo a la selección de dificultad...")
        cont = 2
    elif opcion == "4":
        print("Redirigiendo a la sala de logros...")
        cont = 2
    elif opcion == "5":
        print("Saliendo del juego. ¡Hasta luego!")
        exit()
    else:
        opcion = input("Opción inválida. Por favor ingresa 1, 2 o 3: ") 
        cont = 1

if opcion == "1":
    usuario = input("Ingresa tu nombre de usuario: ")
    contraseña = input("Ingresa tu contraseña: ")
    print(f"¡Bienvenido de nuevo, {usuario}!")

elif opcion == "2":
    nuevo_usuario = input("Elige un nombre de usuario: ")
    nueva_contraseña = input("Elige una contraseña: ")
    print(f"¡Registro exitoso! Bienvenido, {nuevo_usuario}!")
else:
    pass

if opcion == "3":
    exit()

def menu_():
    print ("==================================")
print ("=         Menú de Juego   =")
print ("==================================")

menu_()
print ("Selecciona una opción:")

opcion_juego = (input("1. Iniciar juego\n2 Puntuciaciones\n3. Jugar punto suicida\n4 Jugar Contrareloj\n5 Randomize \n6 Menu_p\n"))

cont_juego = 1

while cont_juego == 1:
    if opcion_juego == "1":
        cont_juego = 2
        print("Iniciando el juego...")
    elif opcion_juego == "2":
        cont_juego = 2
        print("Mostrando las puntuaciones...")
    elif opcion_juego == "3":
        print("Iniciando modo Punto Suicida. !Buena suerte!")
        cont_juego = 2
    elif opcion_juego == "4":
        print("Iniciando Contrarreloj. ¡Date prisa!")
        cont_juego = 2
    elif opcion_juego == "5":
        print("Iniciando modo Randomize. ¡Prepárate para cualquier cosa!")
    elif opcion_juego == "6":
        print("Redirigiendo al menú principal...")
        cont_juego = 2
        mostrar_menu()
    else:
        opcion_juego = input("Opción inválida. Por favor ingresa 1, 2 o 3: ") 
        cont_juego = 1
    if opcion_juego == "1":
        print("Selecciona el modo de juego:")
