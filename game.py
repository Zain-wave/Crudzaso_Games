import threading
import queue
import random
import time
import readchar
from rich.align import Align
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.console import Group

import os

from admin import cargar_preguntas
from utils import (
    mezclar_opciones,
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
    os.system("cls")
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
    os.system("cls")
    preguntas = seleccionar_preguntas(dificultad=dificultad, cantidad=20)

    puntaje = 0

    for pregunta in preguntas:
        pregunta = mezclar_opciones(pregunta)
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
    console.print("\n[bold green]=== MODO: CONTRARRELOJ ===[/bold green]\n", justify="center")

    dificultad = seleccionar_dificultad()
    os.system("cls")
    preguntas = seleccionar_preguntas(dificultad=dificultad, cantidad=10)
    puntaje = 0

    tiempo_limite_total = 60
    inicio = time.time()

    key_queue = queue.Queue()

    def capturar_teclas():
        while True:
            key = readchar.readkey()
            key_queue.put(key)
            if key == readchar.key.ENTER:
                pass

    hilo = threading.Thread(target=capturar_teclas, daemon=True)
    hilo.start()

    for pregunta in preguntas:
        pregunta = mezclar_opciones(pregunta)
        seleccion = 0
        resp = None

        with Live(console=console, refresh_per_second=10) as live:
            while resp is None:
                tiempo_restante = tiempo_limite_total - (time.time() - inicio)
                if tiempo_restante <= 0:
                    live.update(Align.center("[bold red]⏳ Tiempo agotado![/bold red]"))
                    guardar_puntaje(usuario_actual, "contrarreloj", dificultad, puntaje)
                    return

                encabezado = Table.grid(expand=True)
                encabezado.add_column(justify="left")
                encabezado.add_column(justify="right")
                encabezado.add_row(
                    f"[bold cyan]{pregunta['pregunta']}[/bold cyan]",
                    f"[bold yellow]⏳ {tiempo_restante:.1f}s[/bold yellow]"
                )

                tabla = Table(show_header=False, box=None, padding=(0, 2))
                for _ in pregunta["opciones"]:
                    tabla.add_column(justify="center")

                botones = []
                for i, opt in enumerate(pregunta["opciones"]):
                    color = "bold yellow" if i == seleccion else "white"
                    border = "bright_magenta" if i == seleccion else "white"
                    panel = Panel(f"[{color}]{i+1}. {opt}[/{color}]", border_style=border, padding=(0, 2), expand=False)
                    botones.append(panel)
                tabla.add_row(*botones)

                layout = Align.center(Group(encabezado, tabla))
                live.update(layout)
                
                try:
                    key = key_queue.get_nowait()
                    if key == readchar.key.LEFT:
                        seleccion = (seleccion - 1) % len(pregunta["opciones"])
                    elif key == readchar.key.RIGHT:
                        seleccion = (seleccion + 1) % len(pregunta["opciones"])
                    elif key == readchar.key.ENTER:
                        resp = seleccion
                except queue.Empty:
                    pass

                time.sleep(0.05)

        if resp == pregunta["respuesta"]:
            console.print("[bold green]✔ Correcto![/bold green]")
            puntaje += 1
        else:
            console.print("[bold red]✘ Incorrecto![/bold red]")

        time.sleep(1.2)

    console.print(f"\n[bold magenta]Juego terminado. Puntaje final: {puntaje}[/bold magenta]\n")
    guardar_puntaje(usuario_actual, "contrarreloj", dificultad, puntaje)