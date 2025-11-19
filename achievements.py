from utils import console
from rich.panel import Panel
from rich.align import Align
import json
import os
from auth import cargar_usuarios, guardar_usuarios

ARCHIVO_LOGROS = "logros.json"  

def cargar_logros():
    if not os.path.exists(ARCHIVO_LOGROS):
        console.print(f"[red]❌ Error: No se encontró el archivo {ARCHIVO_LOGROS}[/red]")
        return {}
    
    try:
        with open(ARCHIVO_LOGROS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[red]❌ Error al cargar logros: {e}[/red]")
        return {}

def obtener_logros_usuario(usuario_actual):
    usuarios = cargar_usuarios()
    usuario = next((u for u in usuarios if u["usuario"] == usuario_actual["usuario"]), None)
    
    if usuario and "logros" in usuario:
        return usuario["logros"]
    return []

def guardar_logro_usuario(usuario_actual, logro_id):
    usuarios = cargar_usuarios()
    
    for usuario in usuarios:
        if usuario["usuario"] == usuario_actual["usuario"]:
            if "logros" not in usuario:
                usuario["logros"] = []
            
            if logro_id not in usuario["logros"]:
                usuario["logros"].append(logro_id)
                
                todos_logros = cargar_logros()
                for categoria in todos_logros.values():
                    if logro_id in categoria:
                        recompensa = categoria[logro_id]["recompensa"]
                        usuario["puntos"] = usuario.get("puntos", 0) + recompensa
                        usuario_actual["puntos"] = usuario["puntos"]
                        break
                
                guardar_usuarios(usuarios)
                return True
    
    return False

def verificar_logros_historia(usuario_actual, epoca, puntaje):
    logros_desbloqueados = []
    todos_logros = cargar_logros()
    
    if puntaje == 5:
        logro_id = f"{epoca}_perfecto"
        if logro_id in todos_logros.get("logros_historia", {}):
            if guardar_logro_usuario(usuario_actual, logro_id):
                logros_desbloqueados.append(logro_id)
    
    if verificar_todas_epocas_perfectas(usuario_actual):
        if guardar_logro_usuario(usuario_actual, "historiador_maestro"):
            logros_desbloqueados.append("historiador_maestro")
    
    if verificar_todas_epocas_jugadas(usuario_actual):
        if guardar_logro_usuario(usuario_actual, "viajero_temporal"):
            logros_desbloqueados.append("viajero_temporal")
    
    return logros_desbloqueados

def verificar_todas_epocas_perfectas(usuario_actual):
    usuarios = cargar_usuarios()
    usuario = next((u for u in usuarios if u["usuario"] == usuario_actual["usuario"]), None)
    
    if not usuario or "puntuaciones" not in usuario:
        return False
    
    epocas_requeridas = ["grecia_antigua", "egipto_ptolemaico", "renacimiento", "revolucion_industrial", "era_digital"]
    epocas_perfectas = set()
    
    for puntuacion in usuario["puntuaciones"]:
        if puntuacion["modo"] == "historia" and puntuacion["puntaje"] == 5:
            epoca_id = puntuacion["dificultad"].lower().replace(" ", "_").replace("ó", "o")
            epocas_perfectas.add(epoca_id)
    
    return all(epoca in epocas_perfectas for epoca in epocas_requeridas)

def verificar_todas_epocas_jugadas(usuario_actual):
    usuarios = cargar_usuarios()
    usuario = next((u for u in usuarios if u["usuario"] == usuario_actual["usuario"]), None)
    
    if not usuario or "puntuaciones" not in usuario:
        return False
    
    epocas_requeridas = ["Grecia Antigua", "Egipto Ptolemaico", "Renacimiento", "Revolución Industrial", "Era Digital"]
    epocas_jugadas = set()
    
    for puntuacion in usuario["puntuaciones"]:
        if puntuacion["modo"] == "historia":
            epocas_jugadas.add(puntuacion["dificultad"])
    
    return all(epoca in epocas_jugadas for epoca in epocas_requeridas)

def verificar_logros_trivia(usuario_actual, dificultad, puntaje):
    logros_desbloqueados = []
    
    if puntaje == 5:
        if guardar_logro_usuario(usuario_actual, "trivia_perfecta"):
            logros_desbloqueados.append("trivia_perfecta")
    
    verificar_logros_cantidad_partidas(usuario_actual, "trivia")
    
    return logros_desbloqueados

def verificar_logros_suicida(usuario_actual, puntaje):
    logros_desbloqueados = []
    
    if puntaje >= 10:
        if guardar_logro_usuario(usuario_actual, "suicida_10"):
            logros_desbloqueados.append("suicida_10")
    
    if puntaje >= 25:
        if guardar_logro_usuario(usuario_actual, "suicida_25"):
            logros_desbloqueados.append("suicida_25")
    
    if puntaje >= 50:
        if guardar_logro_usuario(usuario_actual, "suicida_50"):
            logros_desbloqueados.append("suicida_50")
    
    return logros_desbloqueados

def verificar_logros_contrarreloj(usuario_actual, puntaje):
    logros_desbloqueados = []
    
    if puntaje >= 5:
        if guardar_logro_usuario(usuario_actual, "contrarreloj_5"):
            logros_desbloqueados.append("contrarreloj_5")
    
    if puntaje >= 10:
        if guardar_logro_usuario(usuario_actual, "contrarreloj_10"):
            logros_desbloqueados.append("contrarreloj_10")
    
    if puntaje >= 20:
        if guardar_logro_usuario(usuario_actual, "contrarreloj_20"):
            logros_desbloqueados.append("contrarreloj_20")
    
    return logros_desbloqueados

def verificar_logros_generales(usuario_actual):
    logros_desbloqueados = []
    
    usuarios = cargar_usuarios()
    usuario = next((u for u in usuarios if u["usuario"] == usuario_actual["usuario"]), None)
    
    if usuario and "puntuaciones" in usuario and len(usuario["puntuaciones"]) >= 1:
        if guardar_logro_usuario(usuario_actual, "primer_juego"):
            logros_desbloqueados.append("primer_juego")
    
    puntos = usuario.get("puntos", 0) if usuario else 0
    
    if puntos >= 1000:
        if guardar_logro_usuario(usuario_actual, "puntos_1000"):
            logros_desbloqueados.append("puntos_1000")
    
    if puntos >= 5000:
        if guardar_logro_usuario(usuario_actual, "puntos_5000"):
            logros_desbloqueados.append("puntos_5000")
    
    if puntos >= 10000:
        if guardar_logro_usuario(usuario_actual, "puntos_10000"):
            logros_desbloqueados.append("puntos_10000")
    
    return logros_desbloqueados

def verificar_logros_cantidad_partidas(usuario_actual, modo):
    usuarios = cargar_usuarios()
    usuario = next((u for u in usuarios if u["usuario"] == usuario_actual["usuario"]), None)
    
    if not usuario or "puntuaciones" not in usuario:
        return
    
    count = sum(1 for p in usuario["puntuaciones"] if p["modo"] == modo)
    
    if modo == "trivia":
        if count >= 10:
            guardar_logro_usuario(usuario_actual, "trivia_facil_maestro")
            
def mostrar_logros_desbloqueados(usuario_actual, logros_ids):
    
    if not logros_ids:
        return
    
    todos_logros = cargar_logros()
    
    for logro_id in logros_ids:
        logro_info = None
        for categoria in todos_logros.values():
            if logro_id in categoria:
                logro_info = categoria[logro_id]
                break
        
        if logro_info:
            color_dificultad = {
                "bronce": "yellow",
                "plata": "white", 
                "oro": "yellow",
                "platino": "bright_cyan"
            }.get(logro_info["dificultad"], "white")
            
            mensaje = f"""
[bold {color_dificultad}]🎉 ¡LOGRO DESBLOQUEADO! 🎉[/bold {color_dificultad}]

[bold white]{logro_info['nombre']}[/bold white]
[italic]{logro_info['descripcion']}[/italic]

[green]+{logro_info['recompensa']} puntos[/green]
            """
            
            panel = Panel(
                Align.center(mensaje),
                title=f"[bold {color_dificultad}]🏆 {logro_info['dificultad'].upper()}[/bold {color_dificultad}]",
                border_style=color_dificultad,
                width=50
            )
            
            console.print("\n")
            console.print(Align.center(panel))
            console.print("\n")