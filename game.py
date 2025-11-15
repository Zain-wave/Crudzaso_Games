import random
from admin import cargar_preguntas
from utils import mostrar_pregunta_bonita, console
from utils import seleccionar_opcion
import time


def seleccionar_preguntas(categoria=None, dificultad=None, cantidad=5):
    preguntas = cargar_preguntas()

    if categoria:
        preguntas = [p for p in preguntas if p["categoria"].lower() == categoria.lower()]
    
    if dificultad:
        preguntas = [p for p in preguntas if p["dificultad"].lower() == dificultad.lower()]

    random.shuffle(preguntas)
    return preguntas[:cantidad]


def jugar_trivia():
    console.print("\n[bold green]=== MODO DE JUEGO: TRIVIA NORMAL ===[/bold green]\n")

    preguntas = seleccionar_preguntas(cantidad=5)

    if not preguntas:
        print("No hay preguntas disponibles")
        return

    puntaje = 0

    for pregunta in preguntas:
        # Título
        mostrar_pregunta_bonita(pregunta)

        # Selección bonita
        respuesta = seleccionar_opcion(pregunta["opciones"], pregunta)

        if respuesta == pregunta["respuesta"]:
            console.print("[bold green]✔ Correcto![/bold green]")
            puntaje += 1
        else:
            console.print("[bold red]✘ Incorrecto![/bold red] ")
        
        time.sleep(2)
        

    console.print(f"\n[bold magenta]Juego terminado. Puntaje final: {puntaje}[/bold magenta]\n")

def jugar_suicida():
    console.print("\n[bold green]=== MODO: PUNTO SUICIDA ===[/bold green]\n")

    preguntas = seleccionar_preguntas(cantidad=20)
    puntaje = 0

    for pregunta in preguntas:
        mostrar_pregunta_bonita(pregunta)

        try:
            resp = int(input("Selecciona una opción (1-4): ")) - 1
        except ValueError:
            resp = -1

        if resp == pregunta["respuesta"]:
            console.print("[green]✔ Correcto! Continúas...[/green]")
            puntaje += 1
        else:
            console.print("[red]✘ Incorrecto! Fin del juego.[/red]")
            break

    console.print(f"\n[bold magenta]Puntaje final: {puntaje}[/bold magenta]\n")


def jugar_contrarreloj():
    import time

    console.print("\n[bold green]=== MODO: CONTRARRELOJ ===[/bold green]\n")
    preguntas = seleccionar_preguntas(cantidad=10)

    tiempo_limite = 30
    inicio = time.time()
    puntaje = 0

    for pregunta in preguntas:
        tiempo_transcurrido = time.time() - inicio
        if tiempo_transcurrido >= tiempo_limite:
            console.print("\n[bold red]⏳ Tiempo agotado![/bold red]")
            break

        mostrar_pregunta_bonita(pregunta)

        restante = tiempo_limite - tiempo_transcurrido
        console.print(f"[yellow]Tiempo restante: {restante:.1f}s[/yellow]")

        try:
            resp = int(input("Selecciona una opción (1-4): ")) - 1
        except ValueError:
            resp = -1

        if resp == pregunta["respuesta"]:
            console.print("[green]✔ Correcto![/green]")
            puntaje += 1
        else:
            console.print("[red]✘ Incorrecto![/red]")

    console.print(f"\n[bold magenta]Puntaje final: {puntaje}[/bold magenta]\n")
