from auth import iniciar_sesion
from auth import registrar_usuario
from menu import mostrar_menu_pp
from data import log_in
from data import registrar
from menu import menu


salir = False


while salir != True:
    print("")
    opcion = mostrar_menu_pp()
    match opcion:
        case "1":
            datos_u = log_in()
            exist_user = iniciar_sesion(datos_u[0], datos_u[1])
            print("")

            if exist_user == True:
                print("")
                print(f"¡Bienvenido de nuevo, {datos_u[0]}!")
                print("")
                opcion = menu()
        case "2":
            datos_u = registrar()

            if datos_u != True:
                print("")
                val = registrar_usuario(datos_u[0],datos_u[1])
                if val == True:
                    opcion = menu()    
        case "3":
            salir = opcion

       
print("Saliendo del sistema, Gracias por utilizar nuestro juego...")
