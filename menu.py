def mostrar_menu_pp():

    print ("==================================")
    print ("= Bienvenido a Cursdazo Trivia =")
    print ("==================================")
    
    print("1.Iniciar sesion\n2.Registrarse\n3.Salir: \n")  
    opcion = (input("Selecciona una opción: "))

    cont = 1

    while cont == 1:
        if opcion == "1":
            cont = 2
            print("Redirigiendo a la página de inicio de sesión...")
            return opcion
        elif opcion == "2":
            cont = 2
            print("Redirigiendo a la página de registro...")
            return opcion
        elif opcion == "3":
            print("Redirigiendo a la selección de dificultad...")
            opcion = True
            cont = 2
            return opcion
        else:
            opcion = input("Opción inválida. Por favor ingresa 1, 2 o 3: ") 
            cont = 1



def menu():
    print ("==================================")
    print ("=         Menú de Juego   =")
    print ("==================================")

    print("1.Iniciar juego\n2.Puntuciación\n3.Jugar punto suicida\n4 Jugar Contrareloj\n5.Randomize \n6.Menu principal\n")
    opcion_juego =(input("Selecciona una opción: "))

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
        else:
            opcion_juego = input("Opción inválida. Por favor ingresa 1, 2 o 3: ") 
            cont_juego = 1
        if opcion_juego == "1":
            print("Selecciona el modo de juego:")
