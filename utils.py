import pygame
import os
import random
import readchar
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.table import Table

console = Console()

musica_iniciada = False

def iniciar_musica():
    global musica_iniciada

    if musica_iniciada:
        return

    ruta = os.path.join(os.getcwd(), "sounds", "fondo.wav")

    if not os.path.exists(ruta):
        print(f"No se encontró el archivo de música en {ruta}")
        return

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(ruta)
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)
        musica_iniciada = True
    except Exception as e:
        print(f"Error al reproducir música: {e}")

def ajustar_volumen(volumen):
    if musica_iniciada:
        pygame.mixer.music.set_volume(volumen)

def dar_formato_pregunta(pregunta): 
    dificultad_color = { 
        "facil": "green", 
        "media": "yellow", 
        "dificil": "red" 
    } 
    color = dificultad_color.get(pregunta['dificultad'].lower(), "white") 
    titulo = f"[b blue]ID {pregunta['id']} | {pregunta['categoria']}[/b blue]\n" 
    dificultad = f"[{color}]Dificultad: {pregunta['dificultad']}[/{color}]\n" 
    cuerpo = f"[bold white]{pregunta['pregunta']}[/bold white]\n" 
    opciones_str = "" 
    for idx, opt in enumerate(pregunta['opciones']): 
        if idx == pregunta['respuesta']: 
            opciones_str += f"[green_on_black] {idx+1}. {opt} (CORRECTA)[/green_on_black]\n" 
        else: 
            opciones_str += f" {idx+1}. {opt}\n"
    return titulo + dificultad + "\n" + cuerpo + opciones_str.strip()


def mostrar_pregunta_bonita(pregunta, seleccion=None):
    console.print("\n")
    console.print(Align.center(f"[bold cyan]{pregunta['pregunta']}[/bold cyan]"))
    console.print("\n")

def seleccionar_opcion(opciones, pregunta=None):
    seleccion = 0
    while True:

        os.system("cls")
        if pregunta == "dificultad":
            console.print("\n")
            console.print(Align.center("[bold cyan]Selecciona la dificultad[/bold cyan]"))
            console.print("\n")
        elif pregunta:
            console.print("\n")
            console.print(Align.center(f"[bold cyan]{pregunta['pregunta']}[/bold cyan]"))
            console.print("\n")

        tabla = Table(show_header=False, box=None, padding=(0, 2))
        for _ in opciones:
            tabla.add_column(justify="center")

        botones = []
        for i, opt in enumerate(opciones):
            color = "bold yellow" if i == seleccion else "white"
            border = "bright_magenta" if i == seleccion else "white"
            panel = Panel(f"[{color}]{i+1}. {opt}[/{color}]", border_style=border, padding=(0, 2), expand=False)
            botones.append(panel)

        tabla.add_row(*botones)
        console.print("\n")
        console.print(Align.center(tabla))

        key = readchar.readkey()
        if key == readchar.key.LEFT:
            seleccion = (seleccion - 1) % len(opciones)
        elif key == readchar.key.RIGHT:
            seleccion = (seleccion + 1) % len(opciones)
        elif key == readchar.key.ENTER:
            return seleccion

def seleccionar_dificultad():
    opciones = ["Fácil", "Media", "Difícil"]
    seleccion = seleccionar_opcion(opciones, "dificultad")
    return opciones[seleccion]

def menu_vertical(titulo, opciones):
    seleccion = 0
    width = 40

    while True:
        os.system("cls")

        console.print("\n")
        console.print(Align.center(f"[bold cyan]{titulo}[/bold cyan]"))
        console.print("\n")

        for i, opt in enumerate(opciones):
            panel = Panel(
                Align.center(f"[white]{opt}[/white]"),
                border_style="bright_magenta" if i == seleccion else "white",
                padding=(1, 2),
                width=width
            )
            console.print("     ", panel, justify="center")

        key = readchar.readkey()
        if key == readchar.key.UP:
            seleccion = (seleccion - 1) % len(opciones)
        elif key == readchar.key.DOWN:
            seleccion = (seleccion + 1) % len(opciones)
        elif key == readchar.key.ENTER:
            return seleccion + 1

def mezclar_opciones(pregunta):
    opciones = pregunta["opciones"]
    correcta = pregunta["respuesta"]

    pares = list(enumerate(opciones))
    random.shuffle(pares)

    nueva_respuesta = next(
        i for i, (idx_original, _) in enumerate(pares) if idx_original == correcta
    )

    nuevas_opciones = [texto for _, texto in pares]

    pregunta["opciones"] = nuevas_opciones
    pregunta["respuesta"] = nueva_respuesta

    return pregunta
