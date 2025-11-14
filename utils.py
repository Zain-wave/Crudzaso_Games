import simpleaudio as sa
import threading

def reproducir_en_fondo():
    def _loop():
        wave = sa.WaveObject.from_wave_file("sounds/fondo.wav")
        while True:
            play_obj = wave.play()
            play_obj.wait_done()
    threading.Thread(target=_loop, daemon=True).start()

    
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
