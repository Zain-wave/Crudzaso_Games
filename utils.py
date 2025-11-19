import readchar
import pygame
import os
import random
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.table import Table
from auth import obtener_puntos, usar_pista
import pyttsx3

import copy
    
    
console = Console()

musica_iniciada = False
volumen_original = 0.5

PUNTOS_POR_ACIERTO = 5
COSTO_PISTA_ELIMINAR = 15
COSTO_PISTA_IA = 35

def iniciar_musica():
    global musica_iniciada, volumen_original

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
        volumen_original = 0.5
        pygame.mixer.music.set_volume(volumen_original)
        musica_iniciada = True
    except Exception as e:
        print(f"Error al reproducir música: {e}")

def ajustar_volumen(volumen):
    global volumen_original
    if musica_iniciada:
        pygame.mixer.music.set_volume(volumen)

def bajar_volumen_musica():
    global musica_iniciada
    if musica_iniciada:
        pygame.mixer.music.set_volume(0.1)

def restaurar_volumen_musica():
    global musica_iniciada, volumen_original
    if musica_iniciada:
        pygame.mixer.music.set_volume(volumen_original)

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

def esperar_tecla():
    console.print("\n[bold cyan]Presiona cualquier tecla para continuar...[/bold cyan]")
    readchar.readkey()

def mostrar_menu_pistas(puntos_disponibles):
    console.print("\n[bold yellow]🎯 SISTEMA DE PISTAS[/bold yellow]")
    console.print(f"[cyan]Puntos disponibles: {puntos_disponibles}[/cyan]")
    
    tabla = Table(show_header=False, box=None, padding=(0, 2))
    tabla.add_column("Tecla", justify="center", width=8)
    tabla.add_column("Pista", justify="left")
    tabla.add_column("Costo", justify="center")
    
    tabla.add_row(
        "[bold yellow]1[/bold yellow]",
        "❌ Eliminar 2 opciones incorrectas",
        f"[red]{COSTO_PISTA_ELIMINAR} puntos[/red]"
    )
    tabla.add_row(
        "[bold yellow]2[/bold yellow]", 
        "🤖 Consultar a IA (respuesta por audio)",
        f"[red]{COSTO_PISTA_IA} puntos[/red]"
    )
    tabla.add_row(
        "[bold yellow]3[/bold yellow]",
        "🔙 Volver al juego",
        "[green]Gratis[/green]"
    )
    
    console.print(tabla)
    console.print("[dim]Presiona la tecla correspondiente...[/dim]")

def aplicar_pista_eliminar(pregunta):
    pregunta_modificada = copy.deepcopy(pregunta)
    
    opciones = pregunta_modificada["opciones"]
    respuesta_correcta_original = pregunta_modificada["respuesta"]
    respuesta_correcta_texto = opciones[respuesta_correcta_original]

    opciones_incorrectas = [i for i in range(len(opciones)) if i != respuesta_correcta_original]
    
    if len(opciones_incorrectas) >= 2:
        opciones_a_eliminar = random.sample(opciones_incorrectas, 2)
        
        nuevas_opciones = []
        for i, opcion in enumerate(opciones):
            if i not in opciones_a_eliminar:
                nuevas_opciones.append(opcion)
        
        nuevo_indice_correcto = nuevas_opciones.index(respuesta_correcta_texto)
        
        pregunta_modificada["opciones"] = nuevas_opciones
        pregunta_modificada["respuesta"] = nuevo_indice_correcto
        pregunta_modificada["pista_usada"] = True
        
        return pregunta_modificada
    
    return pregunta_modificada

def obtener_respuesta_ia(pregunta):
    try:
        respuesta_correcta = pregunta["opciones"][pregunta["respuesta"]]
        
        return f"Basándome en mis conocimientos, creo que la respuesta correcta es: {respuesta_correcta}"
    except Exception as e:
        return f"No pude obtener una respuesta de la IA. Error: {str(e)}"

def hablar_texto(texto):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.8)
        engine.say(texto)
        engine.runAndWait()
    except Exception as e:
        console.print(f"[bold red]Error al reproducir audio: {e}[/bold red]")

def aplicar_pista_ia_audio(usuario_actual, pregunta_actual):
    if usar_pista(usuario_actual, COSTO_PISTA_IA):
        console.print("\n[bold green]🤖 Consultando a la IA...[/bold green]")
        
        respuesta_ia = obtener_respuesta_ia(pregunta_actual)
        
        console.print(f"[cyan]{respuesta_ia}[/cyan]")
        console.print("[yellow]🔊 Reproduciendo respuesta por audio...[/yellow]")
        
        bajar_volumen_musica()
        
        try:
            hablar_texto(respuesta_ia)
        finally:
            restaurar_volumen_musica()
        
        console.print("[green]✅ Pista de IA completada[/green]")
        esperar_tecla()
        return pregunta_actual
    else:
        console.print("\n[bold red]❌ No tienes puntos suficientes para esta pista[/bold red]")
        esperar_tecla()
        return pregunta_actual

def ofrecer_pista(usuario_actual, pregunta_actual):
    
    puntos = obtener_puntos(usuario_actual)
    
    if puntos < min(COSTO_PISTA_ELIMINAR, COSTO_PISTA_IA):
        console.print("\n[bold red]❌ No tienes puntos suficientes para usar pistas[/bold red]")
        console.print(f"[yellow]Puntos necesarios: {min(COSTO_PISTA_ELIMINAR, COSTO_PISTA_IA)}[/yellow]")
        esperar_tecla()
        return pregunta_actual
    
    while True:
        os.system("cls")
        console.print("\n")
        mostrar_menu_pistas(puntos)
        
        key = readchar.readkey()
        
        if key == '1':
            if usar_pista(usuario_actual, COSTO_PISTA_ELIMINAR):
                console.print("\n[bold green]✅ Pista aplicada: 2 opciones eliminadas[/bold green]")
                nueva_pregunta = aplicar_pista_eliminar(pregunta_actual)
                esperar_tecla()
                return nueva_pregunta
            else:
                console.print("\n[bold red]❌ No tienes puntos suficientes para esta pista[/bold red]")
                esperar_tecla()
                
        elif key == '2': 
            return aplicar_pista_ia_audio(usuario_actual, pregunta_actual)
                
        elif key == '3':
            return pregunta_actual