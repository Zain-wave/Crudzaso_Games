import random
import time
import os
import msvcrt
from rich.align import Align
from rich.table import Table
from rich.panel import Panel

from admin import cargar_preguntas
from utils import (mezclar_opciones,
                   seleccionar_opcion,
                   seleccionar_dificultad,
                   mostrar_pregunta_bonita,
                   console
                   )
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
        pregunta = mezclar_opciones(pregunta)

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

    dificultad = seleccionar_dificultad()

    preguntas = seleccionar_preguntas(dificultad=dificultad, cantidad=20)

    puntaje = 0

    for pregunta in preguntas:
        pregunta = mezclar_opciones(pregunta)   # <<<<<<<<<< NUEVO

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

    dificultad = seleccionar_dificultad()

    preguntas = seleccionar_preguntas(dificultad=dificultad, cantidad=10)

    tiempo_limite = 30
    inicio = time.time()
    puntaje = 0

    for pregunta in preguntas:
        while True:
            tiempo_restante = tiempo_limite - (time.time() - inicio)

            if tiempo_restante <= 0:
                console.print("\n[bold red]⏳ Tiempo agotado![/bold red]")
                guardar_puntaje(usuario_actual, "contrarreloj", dificultad, puntaje)
                return

            os.system("cls")

            console.print(
                f"[bold cyan]{pregunta['pregunta']}[/bold cyan]"
                f"{' ' * 10}[bold yellow]⏳ {tiempo_restante:.1f}s[/bold yellow]",
                justify="left"
            )
            console.print("\n")

            tabla = Table(show_header=False, box=None, padding=(0, 2))
            for _ in pregunta["opciones"]:
                tabla.add_column(justify="center")

            botones = []
            for i, opt in enumerate(pregunta["opciones"]):
                panel = Panel(
                    f"[white]{i+1}. {opt}[/white]",
                    border_style="white",
                    padding=(0, 1),
                    expand=False
                )
                botones.append(panel)

            tabla.add_row(*botones)
            console.print(Align.center(tabla))


            if msvcrt.kbhit():
                key = msvcrt.getch()

                if key in [b"1", b"2", b"3", b"4"]:
                    resp = int(key.decode()) - 1
                    break

        if resp == pregunta["respuesta"]:
            console.print("[green]✔ Correcto![/green]")
            puntaje += 1
        else:
            console.print("[red]✘ Incorrecto![/red]")

        time.sleep(1.2)

    console.print(f"\n[bold magenta]Puntaje final: {puntaje}[/bold magenta]\n")
    guardar_puntaje(usuario_actual, "contrarreloj", dificultad, puntaje)
