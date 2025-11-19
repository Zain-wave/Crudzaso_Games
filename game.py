import random
import time
import readchar
import json
from rich.align import Align
from rich.table import Table
from rich.panel import Panel
from auth import obtener_puntos
import os

from admin import cargar_preguntas
from utils import (
    mezclar_opciones,
    seleccionar_opcion,
    ofrecer_pista,
    seleccionar_dificultad,
    console,
    esperar_tecla,
    mostrar_progreso,
    animacion_carga
)
from auth import guardar_puntaje

from achievements import (
    verificar_logros_historia, 
    verificar_logros_trivia,
    verificar_logros_suicida,
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
    
    animacion_carga("Cargando preguntas...", 1)
    
    puntos = obtener_puntos(usuario_actual)
    console.print(f"[cyan]Puntos disponibles: {puntos}[/cyan]")
    console.print("[yellow]Durante el juego presiona 'P' para usar pistas[/yellow]\n")

    dificultad = seleccionar_dificultad("trivia")
    os.system("cls")
    
    vidas_por_dificultad = {
        "Fácil": 3,
        "Media": 2, 
        "Difícil": 1
    }
    vidas = vidas_por_dificultad.get(dificultad, 2)
    
    preguntas = seleccionar_preguntas(dificultad=dificultad, cantidad=10)
    
    if not preguntas:
        console.print("[bold red] No hay preguntas para esa dificultad[/bold red]")
        esperar_tecla()
        return
    
    puntaje = 0
    pregunta_actual_num = 0
    
    for pregunta in preguntas:
        pregunta_actual_num += 1
        
        progreso = (pregunta_actual_num / len(preguntas)) * 100
        mostrar_progreso("Progreso del juego", progreso)
        console.print(f"[red]❤️  Vidas: {vidas}[/red]")
        console.print(f"[yellow]📊 Puntuación actual: {puntaje}[/yellow]\n")
        
        if 'pregunta' not in pregunta or 'opciones' not in pregunta or 'respuesta' not in pregunta:
            console.print("[bold red]Error: Pregunta con formato inválido, saltando...[/bold red]")
            continue
            
        pregunta = mezclar_opciones(pregunta)
        
        respuesta, pregunta_actual = seleccionar_opcion_con_pistas(pregunta["opciones"], pregunta, usuario_actual)
        
        if respuesta == pregunta_actual["respuesta"]:
            console.print("[bold green]✔ Correcto! +5 puntos[/bold green]")
            puntaje += 1
            
            if puntaje % 3 == 0:
                console.print("[bold yellow]🎯 ¡Racha! +2 puntos extra[/bold yellow]")
                puntaje += 2
        else:
            console.print("[bold red]✘ Incorrecto![/bold red]")
            console.print(f"[green]La respuesta correcta era: {pregunta_actual['opciones'][pregunta_actual['respuesta']]}[/green]")
            vidas -= 1
            
            if vidas <= 0:
                console.print("\n[bold red]💀 ¡Te has quedado sin vidas! Juego terminado.[/bold red]")
                break

        time.sleep(1.5)
        os.system("cls")
        
        if pregunta_actual_num >= len(preguntas):
            console.print("[bold green]🎉 ¡Has completado todas las preguntas![/bold green]")
            break

    animacion_carga("Calculando resultados...", 1)
    
    puntos_ganados = puntaje * 5
    console.print(f"\n[bold magenta]Juego terminado. Preguntas acertadas: {puntaje}/{pregunta_actual_num}[/bold magenta]")
    console.print(f"[bold green]Puntos ganados: +{puntos_ganados}[/bold green]")
    console.print(f"[cyan]Vidas restantes: {vidas}[/cyan]")
    
    if vidas > 0:
        bonus_vidas = vidas * 10
        console.print(f"[bold yellow]⭐ Bonus por vidas restantes: +{bonus_vidas} puntos[/bold yellow]")
        puntos_ganados += bonus_vidas
    
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
    
    animacion_carga("Preparando modo suicida...", 1)

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
    racha_actual = 0
    mejor_racha = 0

    for i, pregunta in enumerate(preguntas, 1):
        console.print(f"[bold cyan]Pregunta #{i}[/bold cyan]")
        console.print(f"[green]🔥 Racha actual: {racha_actual}[/green]")
        console.print(f"[yellow]🏆 Mejor racha: {mejor_racha}[/yellow]")
        console.print(f"[red]💀 Modo: Un error y pierdes[/red]\n")
        
        if 'pregunta' not in pregunta or 'opciones' not in pregunta or 'respuesta' not in pregunta:
            console.print("[bold red]Error: Pregunta con formato inválido, saltando...[/bold red]")
            continue
            
        pregunta = mezclar_opciones(pregunta)
        
        respuesta, pregunta_actual = seleccionar_opcion_con_pistas(pregunta["opciones"], pregunta, usuario_actual)
        
        if respuesta == pregunta_actual["respuesta"]:
            console.print("[green]✔ Correcto! Continúas...[/green]")
            puntaje += 1
            racha_actual += 1
            mejor_racha = max(mejor_racha, racha_actual)
            
            if racha_actual % 5 == 0:
                console.print(f"[bold yellow]🎯 ¡Increíble! Racha de {racha_actual} preguntas[/bold yellow]")
        else:
            console.print("[red]✘ Incorrecto! Fin del juego.[/red]")
            console.print(f"[green]La respuesta correcta era: {pregunta_actual['opciones'][pregunta_actual['respuesta']]}[/green]")
            break

        time.sleep(1)
        os.system("cls")

    animacion_carga("Calculando tu desempeño...", 1)
    
    console.print(f"\n[bold magenta]Puntaje final: {puntaje}[/bold magenta]")
    console.print(f"[bold yellow]Mejor racha: {mejor_racha}[/bold yellow]")
    
    if mejor_racha >= 10:
        bonus_racha = mejor_racha * 2
        console.print(f"[bold green]🌟 Bonus por racha larga: +{bonus_racha} puntos[/bold green]")
    
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
    
    animacion_carga("Preparando máquina del tiempo...", 2)
    
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
    
    console.print(f"\n[bold cyan]🕰️  Viajando a: {epoca_seleccionada['nombre']}[/bold cyan]")
    animacion_carga(f"Transportándote a {epoca_seleccionada['nombre']}...", 2)
    
    console.print(f"[dim]Categorías: {', '.join(epoca_seleccionada['categorias'])}[/dim]")
    time.sleep(1)
    os.system("cls")

    todas_preguntas = cargar_preguntas()
    preguntas_epoca = []
    
    console.print("[yellow]Buscando artefactos históricos...[/yellow]")
    animacion_carga("Recopilando conocimiento histórico...", 1)
    
    for pregunta_id in epoca_seleccionada["preguntas"]:
        pregunta = next((p for p in todas_preguntas if p.get("id") == pregunta_id), None)
        if pregunta:
            if all(key in pregunta for key in ['pregunta', 'opciones', 'respuesta']):
                if len(pregunta['opciones']) >= 2:  
                    preguntas_epoca.append(pregunta)
    
    console.print(f"[green]✅ Encontradas {len(preguntas_epoca)} artefactos históricos[/green]")
    time.sleep(1)
    
    if len(preguntas_epoca) < 5:
        console.print(f"[bold red]Error: Solo hay {len(preguntas_epoca)} artefactos disponibles para {epoca_seleccionada['nombre']}[/bold red]")
        console.print("[yellow]Se necesitan al menos 5 artefactos para viajar a esta época[/yellow]")
        esperar_tecla()
        return

    random.shuffle(preguntas_epoca)
    preguntas_juego = preguntas_epoca[:5]
    
    console.print(f"[green]🎮 Iniciando exploración histórica con {len(preguntas_juego)} artefactos...[/green]")
    time.sleep(1)
    os.system("cls")
    
    puntaje = 0
    
    for i, pregunta in enumerate(preguntas_juego, 1):
        progreso = (i / len(preguntas_juego)) * 100
        mostrar_progreso("Progreso del viaje temporal", progreso)
        console.print(f"[bold yellow]Artefacto {i}/5 - {epoca_seleccionada['nombre']}[/bold yellow]")
        console.print(f"[cyan]Conocimiento acumulado: {puntaje}/5[/cyan]\n")

        if not all(key in pregunta for key in ['pregunta', 'opciones', 'respuesta']):
            console.print("[bold red]Error: Artefacto histórico corrupto, saltando...[/bold red]")
            continue
            
        if len(pregunta['opciones']) < 2:
            console.print("[bold red]Error: Artefacto histórico incompleto, saltando...[/bold red]")
            continue
            
        pregunta = mezclar_opciones(pregunta)
        
        respuesta, pregunta_actual = seleccionar_opcion_con_pistas(pregunta["opciones"], pregunta, usuario_actual)
        
        if respuesta == pregunta_actual["respuesta"]:
            console.print("[bold green]✔ ¡Conocimiento adquirido! +5 puntos[/bold green]")
            puntaje += 1
        else:
            console.print("[bold red]✘ Error histórico[/bold red]")
            console.print(f"[green]El conocimiento correcto era: {pregunta_actual['opciones'][pregunta_actual['respuesta']]}[/green]")

        time.sleep(2)
        os.system("cls")

    animacion_carga("Regresando al presente...", 2)
    
    console.print(f"\n[bold magenta]¡Viaje temporal completado![/bold magenta]")
    console.print(f"[bold magenta]Artefactos estudiados: {len(preguntas_juego)}/5[/bold magenta]")
    console.print(f"[bold magenta]Conocimiento adquirido: {puntaje}/5[/bold magenta]")
    
    puntos_ganados = puntaje * 5
    console.print(f"[bold green]Puntos de sabiduría: +{puntos_ganados}[/bold green]")
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