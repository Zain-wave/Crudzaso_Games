import json
import os

from rich.console import Console 
from rich.columns import Columns
from rich.panel import Panel


from utils import reproducir_en_fondo
from utils import dar_formato_pregunta
ARCHIVO_PREGUNTAS = "preguntas.json"



def cargar_preguntas():
    if not os.path.exists(ARCHIVO_PREGUNTAS):
        return []
    with open(ARCHIVO_PREGUNTAS, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_preguntas(preguntas):
    with open(ARCHIVO_PREGUNTAS, "w", encoding="utf-8") as f:
        json.dump(preguntas, f, indent=4, ensure_ascii=False)


def crear_pregunta():
    preguntas = cargar_preguntas()
    id_nuevo = max((p["id"] for p in preguntas), default=0) + 1

    pregunta = input("Ingresa la pregunta: ").strip()
    opciones = []
    for i in range(4):
        opcion = input(f"Ingresa la opción {i+1}: ").strip()
        opciones.append(opcion)
        
    categoria = input("Ingresa la categoría (ej: Geografía, Historia, etc.): ").strip()
    
    dificultad_valida = False
    dificultad = ""
    while not dificultad_valida:
        dificultad = input("Ingresa la dificultad (Fácil, Media, Difícil): ").strip().lower()
        if dificultad in ["facil", "media", "dificil"]:
            dificultad_valida = True
        else:
            print("Dificultad inválida. Solo 'Fácil', 'Media' o 'Difícil'.")

    entrada_valida = False
    respuesta = 0
    while not entrada_valida:
        try:
            if 1 <= (respuesta := int(input("Cual seria la opción correcta (1-4): "))) <= 4:
                entrada_valida = True
            else:
                print("Tiene que ser un número entre 1 y 4")
        except ValueError:
            print("Eso no es un número. Intenta de nuevo")

    nueva = {
        "id": id_nuevo,
        "pregunta": pregunta,
        "opciones": opciones,
        "respuesta": respuesta - 1,
        "categoria": categoria,
        "dificultad": dificultad.capitalize(),
    }

    preguntas.append(nueva)
    guardar_preguntas(preguntas)
    print(f"¡Pregunta ID {id_nuevo} guardada con exito!")


def ver_preguntas():
    preguntas = cargar_preguntas()
    if not preguntas:
        print("No hay preguntas registradas. ¡Añade algunas!")
        return
    console = Console()
    
    renderables_preguntas = []
    for p in preguntas:
        try:
            contenido = dar_formato_pregunta(p)
            renderables_preguntas.append(
                Panel(contenido, expand=True, border_style="cyan")
            )
        except (TypeError, KeyError):
            pass 
            
    if not renderables_preguntas:
        console.print("[bold red]Error:[/bold red] No se encontraron preguntas válidas.")
        return

    console.print("\n=== INVENTARIO DE PREGUNTAS ===")
    console.print(Columns(renderables_preguntas, equal=True, padding=(1, 2)))
    print("-" * console.width)

def editar_pregunta():
    preguntas = cargar_preguntas()
    if not preguntas:
        print("No hay preguntas para editar")
        return

    try:
        print("Si no deseas cambiar algun dato dejalo vacío")
        id_edit = int(input("ID de la pregunta que quieres arreglar: "))
    except ValueError:
        print("ID inválido.")
        return

    if not (pregunta := next((p for p in preguntas if p["id"] == id_edit), None)):
        print("Esa pregunta no existe. ¡Error de ID!")
        return

    nueva_categoria = input(f"Editar categoría (Actual: {pregunta['categoria']}): ").strip()
    if nueva_categoria:
        pregunta["categoria"] = nueva_categoria
        
    entrada_valida = False
    while not entrada_valida:
        nueva_dificultad = input(f"Editar dificultad (Actual: {pregunta['dificultad']})").strip().lower()
        if nueva_dificultad == "":
            entrada_valida = True
        elif nueva_dificultad in ["facil", "media", "dificil"]:
            pregunta["dificultad"] = nueva_dificultad.capitalize()
            entrada_valida = True
        else:
            print("Dificultad inválida. Solo 'Fácil', 'Media' o 'Difícil'.")

    nueva_pregunta = input(f"Editar pregunta (Actual: {pregunta['pregunta']}): ").strip()
    if nueva_pregunta:
        pregunta["pregunta"] = nueva_pregunta

    for i in range(4):
        nueva_op = input(f"Editar opción {i+1} (Actual: {pregunta['opciones'][i]}): ").strip()
        if nueva_op:
            pregunta["opciones"][i] = nueva_op

    entrada_valida = False
    while not entrada_valida:
        try:
            if (nueva_resp_str := input(f"Editar respuesta correcta (Actual: {pregunta['respuesta'] + 1}). Deja vacío para no cambiar: ").strip()) == "":
                entrada_valida = True
            else:
                if 1 <= (nueva_resp := int(nueva_resp_str)) <= 4:
                    pregunta["respuesta"] = nueva_resp - 1
                    entrada_valida = True
                else:
                    print("¡Recuerda, solo del 1 al 4!")
        except ValueError:
            print("Debes ingresar un numero")

    guardar_preguntas(preguntas)
    print(f"¡La pregunta ID {id_edit} ha sido parcheada y guardada!")


def eliminar_pregunta():
    preguntas = cargar_preguntas()
    if not preguntas:
        print("No hay preguntas para borrar")
        return
    try:
        id_del = int(input("ID de la pregunta que quieres eliminar: "))
    except ValueError:
        print("Eso no es un ID")
        return

    preguntas_nuevas = [p for p in preguntas if p["id"] != id_del]

    if ( len(preguntas)) == len(preguntas_nuevas):
        print("Ese ID no está en la lista")
        return

    guardar_preguntas(preguntas_nuevas)
    print(f"Pregunta ID {id_del} eliminada")

def menu_admin():
    opcion = 0
    corriendo = True
    while corriendo:
        print("\n=== ADMINISTRACIÓN DE PREGUNTAS ===")
        print("1. Crear pregunta")
        print("2. Ver preguntas")
        print("3. Editar pregunta")
        print("4. Eliminar pregunta")
        print("5. Volver al menú principal")
        try:
            if not (opcion := int(input("Selecciona una opcion "))):
                continue

            if opcion == 1:
                crear_pregunta()
            elif opcion == 2:
                ver_preguntas()
            elif opcion == 3:
                editar_pregunta()
            elif opcion == 4:
                eliminar_pregunta()
            elif opcion == 5:
                print("Regresando...")
                corriendo = False
            else:
                print("Opción inválida. Solo del 1 al 5.")
        except ValueError:
            print("¡Eso no es una opción numérica!")
            continue
        
reproducir_en_fondo("/sounds/fondo.wav")
menu_admin()