def tiene_numero(cadena):
    for caracter in cadena:
        if caracter.isdigit():
            return True
    return False

def registrar():
    edad = int(input("¿Cual es tu edad?: "))
    if edad >= 5:  
        nombre = input("Queremos conocerte, ¿Cual es tu nombre?: ")
        val = tiene_numero(nombre)

        if val != True:
            nombre_usuario = input("Ahora, como te llamamos en el juego? ")
            contraseña = input("Para proteger tu cuenta, crea una contraseña: ")
            print("¡Registro exitoso!")
            print(edad)
            print(nombre)
            print(nombre_usuario)
            return nombre_usuario, contraseña
        
        elif val == True:
            print("")
            print("Ups, tu nombre contiene numero(s), Registrate nuevamente")
            return val




    else:
        print("Perdon no puedes jugar, cerrando sistema...")
    

def log_in():

    usuario = input("Ingresa tu nombre de usuario: ")
    contraseña = input("Ingresa tu contraseña: ")
    

    return usuario, contraseña