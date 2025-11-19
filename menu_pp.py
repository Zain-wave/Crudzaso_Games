from game import (
    jugar_trivia,
    jugar_suicida,
    jugar_contrarreloj
)
from auth import obtener_puntos
import os
import json
import readchar
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from utils import console

def mostrar_puntuaciones(usuario_actual):
    ruta = "users.json"

    if not os.path.exists(ruta):
        console.print("\n[bold yellow] No existe el archivo users.json[/bold yellow]\n")
        readchar.readkey()
        return

    with open(ruta, "r", encoding="utf-8") as f:
        usuarios = json.load(f)

    usuario = next((u for u in usuarios if u["usuario"] == usuario_actual["usuario"]), None)

    if not usuario:
        console.print("\n[bold red] Usuario no encontrado.[/bold red]\n")
        readchar.readkey()
        return

    puntuaciones = usuario.get("puntuaciones", [])

    if not puntuaciones:
        console.print(f"\n[bold yellow] {usuario_actual['usuario']} no tiene puntuaciones registradas.[/bold yellow]\n")
        readchar.readkey()
        return

    tabla = Table(title=f"Puntuaciones de {usuario_actual['usuario']}", header_style="bold magenta")
    tabla.add_column("Modo", justify="center")
    tabla.add_column("Dificultad", justify="center")
    tabla.add_column("Puntaje", justify="center")

    for p in puntuaciones:
        tabla.add_row(
            p["modo"].capitalize(),
            p["dificultad"].capitalize(),
            str(p["puntaje"])
        )

    console.print("\n")
    console.print(tabla)
    console.print("\n[bold cyan]Presiona cualquier tecla para volver al menú...[/bold cyan]")
    readchar.readkey()


def mostrar_top_global():
    ruta = "users.json"

    if not os.path.exists(ruta):
        console.print("\n[bold yellow] No existe el archivo users.json[/bold yellow]\n")
        readchar.readkey()
        return

    with open(ruta, "r", encoding="utf-8") as f:
        usuarios = json.load(f)

    tabla = Table(title="🏆 Top Global de Usuarios", header_style="bold cyan")
    tabla.add_column("Posición", justify="center")
    tabla.add_column("Usuario", justify="center")
    tabla.add_column("Mejor Puntaje", justify="center")
    tabla.add_column("Modo", justify="center")
    tabla.add_column("Dificultad", justify="center")

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
            "dificultad": mejor["dificultad"]
        })

    if not ranking:
        console.print("\n[bold yellow] No hay puntuaciones registradas aún.[/bold yellow]\n")
        readchar.readkey()
        return

    ranking.sort(key=lambda x: x["puntaje"], reverse=True)

    for i, r in enumerate(ranking, start=1):
        tabla.add_row(
            f"{i}",
            r["usuario"],
            str(r["puntaje"]),
            r["modo"].capitalize(),
            r["dificultad"].capitalize()
        )

    console.print("\n")
    console.print(tabla)
    console.print("\n[bold cyan]Presiona cualquier tecla para volver al menú...[/bold cyan]")
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
            "🎮 Iniciar juego (Trivia Normal)",
            "📊 Ver mis puntuaciones", 
            "💀 Jugar Punto Suicida",
            "🏆 Top Global",
            "🚪 Cerrar sesión"
        ]
        
        seleccion = menu_vertical_mejorado(titulo, opciones)
        
        puntos = obtener_puntos(usuario_actual) if usuario_actual else 0
        
        if seleccion == 1:
            jugar_trivia(usuario_actual)
        elif seleccion == 2:
            mostrar_puntuaciones(usuario_actual)
        elif seleccion == 3:
            jugar_suicida(usuario_actual)
        elif seleccion == 4:
            mostrar_top_global()
        elif seleccion == 5:
            console.print("\n[bold cyan]Cerrando sesión...[/bold cyan]\n")
            readchar.readkey()
            return False