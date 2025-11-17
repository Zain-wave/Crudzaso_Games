import pygame
import os
import msvcrt
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


def mostrar_pregunta_bonita(pregunta, seleccion = None):
    console.print("\n")
    console.print(Align.center(f"[bold cyan]{pregunta['pregunta']}[/bold cyan]"))
    console.print("\n")


def seleccionar_opcion(opciones, pregunta = None):
    seleccion = 0
    while True:
# Solo limpiar pantalla si es una pregunta de juego
        if pregunta:
            os.system("cls")
            console.print("\n")
            console.print(Align.center(f"[bold cyan]{pregunta['pregunta']}[/bold cyan]"))
            console.print("\n")
        else:
            # Si NO es pregunta, NO limpiar pantalla.
            pass


        
        tabla = Table(show_header=False, box=None, padding=(0, 2))
        for _ in opciones:
            tabla.add_column(justify="center")

        botones = []
        for i, opt in enumerate(opciones):
            if i == seleccion:
                panel = Panel(
                    f"[bold yellow]{i+1}. {opt}[/bold yellow]",
                    border_style="bright_magenta",
                    padding=(0, 2),
                    expand=False
                )
            else:
                panel = Panel(
                    f"[white]{i+1}. {opt}[/white]",
                    border_style="white",
                    padding=(0, 2),
                    expand=False
                )
            botones.append(panel)

        tabla.add_row(*botones)
        console.print("\n")
        console.print(Align.center(tabla))

        key = msvcrt.getch()

        # Flechas
        if key == b'\xe0':
            flecha = msvcrt.getch()

            if flecha == b'K':   # Izquierda
                seleccion = (seleccion - 1) % len(opciones)

            elif flecha == b'M':  # Derecha
                seleccion = (seleccion + 1) % len(opciones)

        # ENTER
        elif key == b'\r':
            return seleccion
        
        
def seleccionar_dificultad():
    opciones = ["Fácil", "Media", "Difícil"]
    
    console.print("\n")
    console.print(Align.center("[bold cyan]Selecciona la dificultad[/bold cyan]"))
    console.print("\n")
    
    seleccion = seleccionar_opcion(opciones)

    if seleccion == 0:
        return "Fácil"
    elif seleccion == 1:
        return "Media"
    else:
        return "Difícil"
