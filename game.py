import random
import time

from admin import cargar_preguntas
from utils import mostrar_pregunta_bonita, console
from utils import seleccionar_opcion, seleccionar_dificultad
from auth import guardar_puntaje


# ----------------------------------------------------
#   SELECCIONAR PREGUNTAS
# ----------------------------------------------------
def seleccionar_preguntas(categoria=None, dificultad=None, cantidad=5):
    preguntas = cargar_preguntas()

    if categoria:
        preguntas = [p for p in preguntas if p["categoria"].lower() == categoria.lower()]
    
    if dificultad:
        preguntas = [p for p in preguntas if p["dificultad"].lower() == dificultad.lower()]

    random.shuffle(preguntas)
    return preguntas[:cantidad]


# ----------------------------------------------------
#   MODO TRIVIA NORMAL
# ----------------------------------------------------
def jugar_trivia(usuario_actual):
    console.print("\n[bold green]=== MODO DE JUEGO: TRIVIA NORMAL ===[/bold green]\n")

    dificultad = seleccionar_dificultad()

    preguntas = seleccionar_preguntas(dificultad=dificultad, cantidad=5)

    if not preguntas:
        console.print("[bold red] No hay preguntas para esa dificultad[/bold red]")
        return

    puntaje = 0

    for pregunta in preguntas:
        mostrar_pregunta_bonita(pregunta)

        respuesta = seleccionar_opcion(pregunta["opciones"], pregunta)

        if respuesta == pregunta["respuesta"]:
            console.print("[bold green]✔ Correcto![/bold green]")
            puntaje += 1
        else:
            console.print("[bold red]✘ Incorrecto![/bold red]")
        
        time.sleep(1.5)

    console.print(f"\n[bold magenta]Juego terminado. Puntaje final: {puntaje}[/bold magenta]\n")

    guardar_puntaje(usuario_actual, "trivia", dificultad, puntaje)



# ----------------------------------------------------
#   MODO PUNTO SUICIDA
# ----------------------------------------------------
def jugar_suicida(usuario_actual):
    console.print("\n[bold green]=== MODO: PUNTO SUICIDA ===[/bold green]\n")

    console.print("[cyan]Selecciona la dificultad:[/cyan]")
    dificultad = seleccionar_dificultad()

    preguntas = seleccionar_preguntas(dificultad=dificultad, cantidad=20)

    puntaje = 0

    for pregunta in preguntas:
        mostrar_pregunta_bonita(pregunta)

        resp = seleccionar_opcion(pregunta["opciones"], pregunta)

        if resp == pregunta["respuesta"]:
            console.print("[green]✔ Correcto! Continúas...[/green]")
            puntaje += 1
        else:
            console.print("[red]✘ Incorrecto! Fin del juego.[/red]")
            break

    console.print(f"\n[bold magenta]Puntaje final: {puntaje}[/bold magenta]\n")

    guardar_puntaje(usuario_actual, "suicida", dificultad, puntaje)



# ----------------------------------------------------
#   MODO CONTRARRELOJ
# ----------------------------------------------------
def jugar_contrarreloj(usuario_actual):
    console.print("\n[bold green]=== MODO: CONTRARRELOJ ===[/bold green]\n")

    console.print("[cyan]Selecciona la dificultad:[/cyan]")
    dificultad = seleccionar_dificultad()

    preguntas = seleccionar_preguntas(dificultad=dificultad, cantidad=10)

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

        resp = seleccionar_opcion(pregunta["opciones"], pregunta)

        if resp == pregunta["respuesta"]:
            console.print("[green]✔ Correcto![/green]")
            puntaje += 1
        else:
            console.print("[red]✘ Incorrecto![/red]")

    console.print(f"\n[bold magenta]Puntaje final: {puntaje}[/bold magenta]\n")

    guardar_puntaje(usuario_actual, "contrarreloj", dificultad, puntaje)
