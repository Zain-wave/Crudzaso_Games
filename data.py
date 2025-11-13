edad = int(input("¿Cual es tu edad? "))
def tiene_numero(cadena):
    for caracter in cadena:
        if caracter.isdigit():
            return True
    return False

if edad >= 5:  
    nombre = input("Queremos conocerte, ¿Cual es tu nombre? ")
    tiene_numero(nombre)

    nombre_usuario = input("Ahora, como te llamamos en el juego? ")
    print("¡Registro exitoso!")
    print(edad)
    print(nombre)
    print(nombre_usuario)
else:
    print("Perdon no puedes jugar, cerrando sistema...")
