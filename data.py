from utils import input_con_asteriscos

def validar_contraseña(contraseña):
    if len(contraseña) < 4:
        return "La contraseña debe tener al menos 4 caracteres"
    if len(contraseña) > 20:
        return "La contraseña no puede tener más de 20 caracteres"
    return None

def registrar():
    nombre_usuario = input("Nombre de usuario para el juego: ").strip()

    while True:
        print("\n🔒 Crear contraseña:")
        contraseña = input_con_asteriscos("   • Contraseña: ")
        
        if contraseña is None:
            return None
            
        if not contraseña:
            print("   ❌ La contraseña no puede estar vacía")
            continue
            
        print("   🔒 Confirmar contraseña:")
        repetir = input_con_asteriscos("   • Repite la contraseña: ")
        
        if repetir is None:
            return None

        if contraseña == repetir:
            break
            
        print("\n   ❌ Las contraseñas no coinciden. Inténtalo nuevamente.\n")

    print("\n✅ ¡Registro exitoso!")
    print(f"👤 Usuario: {nombre_usuario}")
    print("=" * 40)
    
    return nombre_usuario, contraseña

def log_in():
    usuario = input("Ingresa tu nombre de usuario: ").strip()
    
    if not usuario:
        print("❌ El nombre de usuario no puede estar vacío")
        return None, None
        
    contraseña = input_con_asteriscos("Ingresa tu contraseña: ")
    
    if contraseña is None:
        return None, None
        
    return usuario, contraseña