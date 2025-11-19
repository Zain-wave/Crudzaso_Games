import threading
import queue
import random
import time
import readchar
import json
from rich.align import Align
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.console import Group
from auth import obtener_puntos
import os

from admin import cargar_preguntas
from utils import (
    mezclar_opciones,
    seleccionar_opcion,
    ofrecer_pista,
    seleccionar_dificultad,
    mostrar_pregunta_bonita,
    console,
    esperar_tecla
)
from auth import guardar_puntaje

from achievements import (
    verificar_logros_historia, 
    verificar_logros_trivia,
    verificar_logros_suicida,
    verificar_logros_contrarreloj,
    verificar_logros_generales,
    mostrar_logros_desbloqueados
)

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

def seleccionar_opcion_con_pistas(opciones, pregunta, usuario_actual):
    
    seleccion = 0
    pregunta_actual = pregunta.copy()
    
    while True:
        os.system("cls")
        
        puntos = obtener_puntos(usuario_actual)
        console.print(f"\n[bold cyan]Puntos disponibles: {puntos}[/bold cyan]")
        
        console.print("\n")
        console.print(Align.center(f"[bold cyan]{pregunta_actual['pregunta']}[/bold cyan]"))
        console.print("\n")
        
        tabla = Table(show_header=False, box=None, padding=(0, 2))
        for _ in pregunta_actual["opciones"]:
            tabla.add_column(justify="center")
        
        botones = []
        for i, opt in enumerate(pregunta_actual["opciones"]):
            color = "bold yellow" if i == seleccion else "white"
            border = "bright_magenta" if i == seleccion else "white"
            panel = Panel(f"[{color}]{i+1}. {opt}[/{color}]", border_style=border, padding=(0, 2), expand=False)
            botones.append(panel)
        
        tabla.add_row(*botones)
        console.print("\n")
        console.print(Align.center(tabla))
        
        console.print("\n[dim]← → para navegar • ENTER para responder • P para pistas[/dim]")
        
        key = readchar.readkey()
        
        if key == readchar.key.LEFT:
            seleccion = (seleccion - 1) % len(pregunta_actual["opciones"])
        elif key == readchar.key.RIGHT:
            seleccion = (seleccion + 1) % len(pregunta_actual["opciones"])
        elif key == readchar.key.ENTER:
            return seleccion, pregunta_actual
        elif key.lower() == 'p':
            nueva_pregunta = ofrecer_pista(usuario_actual, pregunta_actual)
            if nueva_pregunta and nueva_pregunta != pregunta_actual:
                pregunta_actual = nueva_pregunta
                seleccion = 0
                
# ----------------------------------------------------
#   MODO TRIVIA NORMAL
# ----------------------------------------------------
def jugar_trivia(usuario_actual):
    console.print("\n[bold green]=== MODO DE JUEGO: TRIVIA NORMAL ===[/bold green]\n")
    
    puntos = obtener_puntos(usuario_actual)
    console.print(f"[cyan]Puntos disponibles: {puntos}[/cyan]")
    console.print("[yellow]Durante el juego presiona 'P' para usar pistas[/yellow]\n")

    dificultad = seleccionar_dificultad("trivia")
    os.system("cls")
    preguntas = seleccionar_preguntas(dificultad=dificultad, cantidad=5)
    
    if not preguntas:
        console.print("[bold red] No hay preguntas para esa dificultad[/bold red]")
        esperar_tecla()
        return
    
    puntaje = 0
    
    for pregunta in preguntas:
        if 'pregunta' not in pregunta or 'opciones' not in pregunta or 'respuesta' not in pregunta:
            console.print("[bold red]Error: Pregunta con formato inválido, saltando...[/bold red]")
            continue
            
        pregunta = mezclar_opciones(pregunta)
        
        respuesta, pregunta_actual = seleccionar_opcion_con_pistas(pregunta["opciones"], pregunta, usuario_actual)
        
        if respuesta == pregunta_actual["respuesta"]:
            console.print("[bold green]✔ Correcto! +5 puntos[/bold green]")
            puntaje += 1
        else:
            console.print("[bold red]✘ Incorrecto![/bold red]")
            console.print(f"[green]La respuesta correcta era: {pregunta_actual['opciones'][pregunta_actual['respuesta']]}[/green]")

        time.sleep(2)
    
    puntos_ganados = puntaje * 5
    console.print(f"\n[bold magenta]Juego terminado. Puntaje final: {puntaje}[/bold magenta]")
    console.print(f"[bold green]Puntos ganados: +{puntos_ganados}[/bold green]")
    
    guardar_puntaje(usuario_actual, "trivia", dificultad, puntaje)
    logros_desbloqueados = []
    logros_desbloqueados.extend(verificar_logros_trivia(usuario_actual, dificultad, puntaje))
    logros_desbloqueados.extend(verificar_logros_generales(usuario_actual))
    
    if logros_desbloqueados:
        mostrar_logros_desbloqueados(usuario_actual, logros_desbloqueados)
        time.sleep(3)
    esperar_tecla()
    
# ----------------------------------------------------
#   MODO PUNTO SUICIDA
# ----------------------------------------------------

def jugar_suicida(usuario_actual):
    console.print("\n[bold green]=== MODO: PUNTO SUICIDA ===[/bold green]\n")

    puntos = obtener_puntos(usuario_actual)
    console.print(f"[cyan]Puntos disponibles: {puntos}[/cyan]")
    console.print("[yellow]Durante el juego presiona 'P' para usar pistas[/yellow]\n")
    
    dificultad = seleccionar_dificultad("suicida")
    os.system("cls")
    preguntas = seleccionar_preguntas(dificultad=dificultad, cantidad=50)

    if not preguntas:
        console.print("[bold red] No hay preguntas para esa dificultad[/bold red]")
        esperar_tecla()
        return

    puntaje = 0

    for pregunta in preguntas:
        if 'pregunta' not in pregunta or 'opciones' not in pregunta or 'respuesta' not in pregunta:
            console.print("[bold red]Error: Pregunta con formato inválido, saltando...[/bold red]")
            continue
            
        pregunta = mezclar_opciones(pregunta)
        
        respuesta, pregunta_actual = seleccionar_opcion_con_pistas(pregunta["opciones"], pregunta, usuario_actual)
        
        if respuesta == pregunta_actual["respuesta"]:
            console.print("[green]✔ Correcto! Continúas...[/green]")
            puntaje += 1
        else:
            console.print("[red]✘ Incorrecto! Fin del juego.[/red]")
            console.print(f"[green]La respuesta correcta era: {pregunta_actual['opciones'][pregunta_actual['respuesta']]}[/green]")
            break

    console.print(f"\n[bold magenta]Puntaje final: {puntaje}[/bold magenta]\n")
    guardar_puntaje(usuario_actual, "suicida", dificultad, puntaje)
    logros_desbloqueados = []
    logros_desbloqueados.extend(verificar_logros_suicida(usuario_actual, puntaje))
    logros_desbloqueados.extend(verificar_logros_generales(usuario_actual))
    
    if logros_desbloqueados:
        mostrar_logros_desbloqueados(usuario_actual, logros_desbloqueados)
        time.sleep(3)
    esperar_tecla()
    
# ----------------------------------------------------
#   MODO HISTORIA
# ----------------------------------------------------
def jugar_modo_historia(usuario_actual):
    console.print("\n[bold green]=== MODO: VIAJE EN EL TIEMPO ===[/bold green]\n")
    
    try:
        with open("categorias_historia.json", "r", encoding="utf-8") as f:
            epocas_data = json.load(f)
    except FileNotFoundError:
        console.print("[bold red]Error: No se encontró el archivo de épocas históricas[/bold red]")
        esperar_tecla()
        return

    if not epocas_data:
        console.print("[bold red]No hay épocas históricas disponibles[/bold red]")
        esperar_tecla()
        return

    epocas = []
    for key, value in epocas_data.items():
        value["key"] = key
        epocas.append(value)

    opciones_epocas = [epoca["nombre"] for epoca in epocas]
    seleccion = seleccionar_opcion(opciones_epocas, "Selecciona una época histórica")
    epoca_seleccionada = epocas[seleccion]
    
    console.print(f"\n[bold cyan]Viajando a: {epoca_seleccionada['nombre']}[/bold cyan]")
    console.print(f"[dim]Categorías: {', '.join(epoca_seleccionada['categorias'])}[/dim]")
    time.sleep(2)
    os.system("cls")

    todas_preguntas = cargar_preguntas()
    preguntas_epoca = []
    
    console.print("[yellow]Buscando preguntas de la época...[/yellow]")
    
    for pregunta_id in epoca_seleccionada["preguntas"]:
        pregunta = next((p for p in todas_preguntas if p.get("id") == pregunta_id), None)
        if pregunta:
            if all(key in pregunta for key in ['pregunta', 'opciones', 'respuesta']):
                if len(pregunta['opciones']) >= 2:  
                    preguntas_epoca.append(pregunta)
                else:
                    console.print(f"[yellow]⚠️ Pregunta ID {pregunta_id} ignorada: no tiene suficientes opciones[/yellow]")
            else:
                console.print(f"[yellow]⚠️ Pregunta ID {pregunta_id} ignorada: formato inválido[/yellow]")
        else:
            console.print(f"[yellow]⚠️ Pregunta ID {pregunta_id} no encontrada[/yellow]")
    
    console.print(f"[green]✅ Encontradas {len(preguntas_epoca)} preguntas válidas[/green]")
    time.sleep(1)
    
    if len(preguntas_epoca) < 5:
        console.print(f"[bold red]Error: Solo hay {len(preguntas_epoca)} preguntas disponibles para {epoca_seleccionada['nombre']}[/bold red]")
        console.print("[yellow]Se necesitan al menos 5 preguntas para jugar esta época[/yellow]")
        esperar_tecla()
        return

    random.shuffle(preguntas_epoca)
    preguntas_juego = preguntas_epoca[:5]
    
    console.print(f"[green]🎮 Iniciando juego con {len(preguntas_juego)} preguntas...[/green]")
    time.sleep(1)
    os.system("cls")
    
    puntaje = 0
    
    for i, pregunta in enumerate(preguntas_juego, 1):
        console.print(f"\n[bold yellow]Pregunta {i}/5 - {epoca_seleccionada['nombre']}[/bold yellow]")

        if not all(key in pregunta for key in ['pregunta', 'opciones', 'respuesta']):
            console.print("[bold red]Error: Pregunta con formato inválido, saltando...[/bold red]")
            continue
            
        if len(pregunta['opciones']) < 2:
            console.print("[bold red]Error: Pregunta sin suficientes opciones, saltando...[/bold red]")
            continue
            
        pregunta = mezclar_opciones(pregunta)
        
        respuesta, pregunta_actual = seleccionar_opcion_con_pistas(pregunta["opciones"], pregunta, usuario_actual)
        
        if respuesta == pregunta_actual["respuesta"]:
            console.print("[bold green]✔ Correcto! +5 puntos[/bold green]")
            puntaje += 1
        else:
            console.print("[bold red]✘ Incorrecto![/bold red]")
            console.print(f"[green]La respuesta correcta era: {pregunta_actual['opciones'][pregunta_actual['respuesta']]}[/green]")

        time.sleep(2)
        os.system("cls")

    console.print(f"\n[bold magenta]¡Viaje completado! Preguntas mostradas: {len(preguntas_juego)}/5[/bold magenta]")
    console.print(f"[bold magenta]Preguntas acertadas: {puntaje}/5[/bold magenta]")
    
    puntos_ganados = puntaje * 5
    console.print(f"[bold green]Puntos ganados: +{puntos_ganados}[/bold green]")
    console.print(f"[cyan]Gracias por visitar {epoca_seleccionada['nombre']}![/cyan]")
    
    epoca_id = epoca_seleccionada['nombre'].lower().replace(" ", "_").replace("ó", "o")
    
    guardar_puntaje(usuario_actual, "historia", epoca_seleccionada['nombre'], puntaje)
    

    
    logros_desbloqueados = []
    logros_desbloqueados.extend(verificar_logros_historia(usuario_actual, epoca_id, puntaje))
    logros_desbloqueados.extend(verificar_logros_generales(usuario_actual))
    
    if logros_desbloqueados:
        mostrar_logros_desbloqueados(usuario_actual, logros_desbloqueados)
        time.sleep(3)
    
    esperar_tecla()
    
# ----------------------------------------------------
#   MODO CONTRARRELOJ
# ----------------------------------------------------
def jugar_contrarreloj(usuario_actual):
    console.print("\n[bold green]=== MODO: CONTRARRELOJ ===[/bold green]\n", justify="center")
    
    dificultad = seleccionar_dificultad("contrarreloj")
    os.system("cls")
    preguntas = seleccionar_preguntas(dificultad=dificultad, cantidad=50)
    puntaje = 0

    tiempo_limite_total = 30
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
                    esperar_tecla()
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
    logros_desbloqueados = []
    logros_desbloqueados.extend(verificar_logros_contrarreloj(usuario_actual, puntaje))
    logros_desbloqueados.extend(verificar_logros_generales(usuario_actual))
    
    if logros_desbloqueados:
        mostrar_logros_desbloqueados(usuario_actual, logros_desbloqueados)
        time.sleep(3)
    esperar_tecla()
