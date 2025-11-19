from game import (
    jugar_trivia,
    jugar_suicida,
    jugar_modo_historia
)
from auth import obtener_puntos
import os
import json
import readchar
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from utils import console

from achievements import obtener_logros_usuario, cargar_logros



def calcular_estadisticas_simples(usuario_actual):
    ruta = "users.json"
    
    if not os.path.exists(ruta):
        return None
        
    with open(ruta, "r", encoding="utf-8") as f:
        usuarios = json.load(f)

    usuario = next((u for u in usuarios if u["usuario"] == usuario_actual["usuario"]), None)
    
    if not usuario:
        return None
        
    puntuaciones = usuario.get("puntuaciones", [])
    puntos_totales = usuario.get("puntos", 0)
    
    if not puntuaciones:
        return {
            "total_preguntas": 0,
            "porcentaje_acierto": 0,
            "mejor_racha": 0,
            "categoria_favorita": "Ninguna",
            "mejor_puntuacion_suicida": 0,
            "puntos_totales": puntos_totales
        }
    
    total_preguntas = 0
    aciertos_totales = 0
    
    for p in puntuaciones:
            if p["modo"] == "trivia":
                total_preguntas += 5
                aciertos_totales += p["puntaje"]
            elif p["modo"] == "suicida":
                total_preguntas += p["puntaje"] + 1
                aciertos_totales += p["puntaje"]
            elif p["modo"] == "historia":
                total_preguntas += 5
                aciertos_totales += p["puntaje"]
    
    porcentaje_acierto = (aciertos_totales / total_preguntas * 100) if total_preguntas > 0 else 0
    
    mejor_racha = max([p["puntaje"] for p in puntuaciones if p["modo"] == "suicida"], default=0)
    
    mejor_puntuacion_suicida = max([p["puntaje"] for p in puntuaciones if p["modo"] == "suicida"], default=0)
    
    categoria_favorita = "Historia"
    
    return {
        "total_preguntas": total_preguntas,
        "porcentaje_acierto": round(porcentaje_acierto, 1),
        "mejor_racha": mejor_racha,
        "categoria_favorita": categoria_favorita,
        "mejor_puntuacion_suicida": mejor_puntuacion_suicida,
        "puntos_totales": puntos_totales
    }
    
    
def mostrar_estadisticas_personales(usuario_actual):

    stats = calcular_estadisticas_simples(usuario_actual)
    logros_usuario = obtener_logros_usuario(usuario_actual)
    todos_logros = cargar_logros()
    
    if not stats:
        console.print("\n[bold red]❌ Error al cargar las estadísticas[/bold red]\n")
        readchar.readkey()
        return
    
    # Contar logros por categoría
    logros_totales = 0
    logros_desbloqueados = len(logros_usuario)
    
    for categoria in todos_logros.values():
        logros_totales += len(categoria)
    
    porcentaje_logros = (logros_desbloqueados / logros_totales * 100) if logros_totales > 0 else 0
    
    contenido = f"""
[bold white]Total de preguntas:[/bold white] [bold yellow]{stats['total_preguntas']}[/bold yellow]
[bold white]Porcentaje de acierto:[/bold white] [bold yellow]{stats['porcentaje_acierto']}%[/bold yellow]
[bold white]Mejor racha:[/bold white] [bold yellow]{stats['mejor_racha']} preguntas[/bold yellow]
[bold white]Categoría favorita:[/bold white] [bold yellow]{stats['categoria_favorita']}[/bold yellow]
[bold white]Mejor puntuación (Suicida):[/bold white] [bold yellow]{stats['mejor_puntuacion_suicida']}[/bold yellow]
[bold white]Puntos totales ganados:[/bold white] [bold yellow]{stats['puntos_totales']}[/bold yellow]

[bold cyan]--- LOGROS ---[/bold cyan]
[bold white]Logros desbloqueados:[/bold white] [bold yellow]{logros_desbloqueados}/{logros_totales}[/bold yellow]
[bold white]Progreso:[/bold white] [bold yellow]{porcentaje_logros:.1f}%[/bold yellow]
"""
    
    panel = Panel(
        Align.left(contenido),
        title="[bold cyan]📈 MIS ESTADÍSTICAS[/bold cyan]",
        border_style="bright_magenta",
        padding=(1, 4),
        width=50
    )
    
    os.system("cls")
    console.print("\n" * 3)
    console.print(Align.center(panel))
    
    console.print("\n" * 2)
    console.print(Align.center("[bold cyan]Presiona 'L' para ver logros o cualquier tecla para volver...[/bold cyan]"))
    
    key = readchar.readkey()
    if key.lower() == 'l':
        mostrar_logros_detallados(usuario_actual)

def mostrar_logros_detallados(usuario_actual):

    
    logros_usuario = obtener_logros_usuario(usuario_actual)
    todos_logros = cargar_logros()
    
    os.system("cls")
    console.print("\n" * 2)
    console.print(Align.center("[bold cyan]🏆 MIS LOGROS[/bold cyan]"))
    console.print("\n")
    
    for categoria_nombre, logros_categoria in todos_logros.items():
        nombre_bonito = categoria_nombre.replace("logros_", "").replace("_", " ").title()
        console.print(f"[bold magenta]=== {nombre_bonito} ===[/bold magenta]")
        
        for logro_id, logro_info in logros_categoria.items():
            desbloqueado = logro_id in logros_usuario
            
            color_estado = "green" if desbloqueado else "dim"
            icono = "✅" if desbloqueado else "🔒"
            color_dificultad = {
                "bronce": "yellow",
                "plata": "white",
                "oro": "yellow", 
                "platino": "bright_cyan"
            }.get(logro_info["dificultad"], "white")
            
            console.print(f"  {icono} [{color_dificultad}]{logro_info['nombre']}[/{color_dificultad}] - {logro_info['descripcion']}")
            if desbloqueado:
                console.print(f"     [green]✓ Desbloqueado • +{logro_info['recompensa']} puntos[/green]")
            else:
                console.print(f"     [dim](No desbloqueado)[/dim]")
        
        console.print()
    
    console.print("\n" * 2)
    console.print(Align.center("[bold cyan]Presiona cualquier tecla para volver...[/bold cyan]"))
    readchar.readkey()
    
def mostrar_top_global():
    ruta = "users.json"

    if not os.path.exists(ruta):
        console.print("\n[bold yellow] No existe el archivo users.json[/bold yellow]\n")
        readchar.readkey()
        return

    with open(ruta, "r", encoding="utf-8") as f:
        usuarios = json.load(f)

    ranking = []

    for u in usuarios:
        puntuaciones = u.get("puntuaciones", [])
        if not puntuaciones:
            continue
        mejor = max(puntuaciones, key=lambda p: p["puntaje"])
        ranking.append({
            "usuario": u["usuario"],
            "puntaje": mejor["puntaje"],
            "modo": mejor["modo"],
            "dificultad": mejor["dificultad"],
            "puntos_totales": u.get("puntos", 0)
        })

    if not ranking:
        panel = Panel(
            Align.center("[bold yellow]No hay puntuaciones registradas aún.[/bold yellow]\n\n[cyan]¡Sé el primero en jugar![/cyan]"),
            title="[bold cyan]🏆 TOP GLOBAL[/bold cyan]",
            border_style="bright_magenta",
            width=60
        )
        os.system("cls")
        console.print("\n" * 3)
        console.print(Align.center(panel))
        console.print("\n" * 2)
        console.print(Align.center("[bold cyan]Presiona cualquier tecla para volver al menú...[/bold cyan]"))
        readchar.readkey()
        return

    ranking.sort(key=lambda x: x["puntaje"], reverse=True)

    tabla = Table(
        title="[bold cyan]🏆 TOP GLOBAL DE JUGADORES[/bold cyan]",
        title_justify="center",
        header_style="bold magenta",
        box=None,
        show_header=True,
        width=70
    )
    
    tabla.add_column("Posición", justify="center", style="cyan", width=10)
    tabla.add_column("Jugador", justify="center", style="white", width=20)
    tabla.add_column("Mejor Puntaje", justify="center", style="yellow", width=15)
    tabla.add_column("Modo", justify="center", style="green", width=15)
    tabla.add_column("Puntos Totales", justify="center", style="blue", width=15)

    for i, r in enumerate(ranking, start=1):
        if i == 1:
            posicion = "🥇 1°"
        elif i == 2:
            posicion = "🥈 2°"
        elif i == 3:
            posicion = "🥉 3°"
        else:
            posicion = f"{i}°"
        
        modo_formateado = {
            "trivia": "Trivia",
            "suicida": "Suicida",
            "contrarreloj": "Contrarreloj"
        }.get(r["modo"], r["modo"].capitalize())
        
        tabla.add_row(
            posicion,
            r["usuario"],
            str(r["puntaje"]),
            modo_formateado,
            str(r["puntos_totales"])
        )


    os.system("cls")
    console.print("\n" * 2)
    console.print(Align.center(tabla))
    
    console.print(Align.center("[dim]Basado en la mejor puntuación individual de cada jugador[/dim]"))
    console.print("\n" * 2)
    console.print(Align.center("[bold cyan]Presiona cualquier tecla para volver al menú...[/bold cyan]"))
    readchar.readkey()

def menu_vertical_mejorado(titulo, opciones):
    seleccion = 0
    width = 45

    while True:
        os.system("cls")

        console.print("\n")
        console.print(Align.center(f"[bold cyan]{titulo}[/bold cyan]"))
        console.print("\n")

        for i, opt in enumerate(opciones):
            color_texto = "bold yellow" if i == seleccion else "white"
            panel = Panel(
                Align.center(f"[{color_texto}]{opt}[/{color_texto}]"),
                border_style="bright_magenta" if i == seleccion else "white",
                padding=(1, 2),
                width=width
            )
            console.print("     ", panel, justify="center")

        console.print("\n[dim]Usa las flechas ↑↓ para navegar • ENTER para seleccionar[/dim]")

        key = readchar.readkey()
        if key == readchar.key.UP:
            seleccion = (seleccion - 1) % len(opciones)
        elif key == readchar.key.DOWN:
            seleccion = (seleccion + 1) % len(opciones)
        elif key == readchar.key.ENTER:
            return seleccion + 1
        
def menu(usuario_actual=None):
    nick = usuario_actual.get("usuario") if usuario_actual else "Invitado"
    puntos = obtener_puntos(usuario_actual) if usuario_actual else 0
    
    while True:
        titulo = f"👤 {nick} | ⭐ {puntos} puntos"
        opciones = [
            "🎮 Iniciar Juego (Trivia)",
            "💀 Jugar Modo Suicida",
            "📜 Jugar Modo Historia",
            "📈 Mis Estadísticas",
            "🏆 Top Global",
            "🚪 Cerrar Sesión"
        ]
        
        seleccion = menu_vertical_mejorado(titulo, opciones)
        
        puntos = obtener_puntos(usuario_actual) if usuario_actual else 0
        
        if seleccion == 1:
            jugar_trivia(usuario_actual)
        elif seleccion == 2:
            jugar_suicida(usuario_actual)
        elif seleccion == 3:
            jugar_modo_historia(usuario_actual)
        elif seleccion == 4:
            mostrar_estadisticas_personales(usuario_actual)
        elif seleccion == 5:
            mostrar_top_global()
        elif seleccion == 6:
            console.print("\n[bold cyan]Cerrando sesión...[/bold cyan]\n")
            readchar.readkey()
            return False