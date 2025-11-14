import pygame
import os

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
    """Ajusta el volumen de la música (0.0 a 1.0)"""
    if musica_iniciada:
        pygame.mixer.music.set_volume(volumen)


def dar_formato_pregunta(pregunta):
    """Formatea una pregunta para mostrarla con colores"""
    
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