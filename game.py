import json
import random
from admin import cargar_preguntas


def seleccionar_preguntas(categoria=None, dificultad=None, cantidad=5):
    preguntas = cargar_preguntas()

    if categoria:
        preguntas = [p for p in preguntas if p["categoria"].lower() == categoria.lower()]
    
    if dificultad:
        preguntas = [p for p in preguntas if p["dificultad"].lower() == dificultad.lower()]

    random.shuffle(preguntas)
    return preguntas[:cantidad]


def jugar_trivia():
    print("\n=== MODO DE JUEGO: TRIVIA NORMAL ===\n")

    preguntas = seleccionar_preguntas(cantidad=5)

    if not preguntas:
        print("No hay preguntas disponibles")
        return

    puntaje = 0

    for pregunta in preguntas:
        print(f"\nPregunta: {pregunta['pregunta']}")

        for idx, op in enumerate(pregunta["opciones"], start=1):
            print(f" {idx}. {op}")

        try:
            respuesta = int(input("Tu respuesta: ")) - 1
        except ValueError:
            print("Respuesta inválida. Se contará como incorrecta.")
            respuesta = -1

        if respuesta == pregunta["respuesta"]:
            print("Correcto!")
            puntaje += 1
        else:
            print(f"Incorrecto! La respuesta correcta era: {pregunta['opciones'][pregunta['respuesta']]}")

    print(f"\nJuego terminado. Tu puntaje final es: {puntaje}")
    print("=======================================\n")


def jugar_suicida():
    print("\n=== MODO: PUNTO SUICIDA ===\n")

    preguntas = seleccionar_preguntas(cantidad=20)
    puntaje = 0

    for pregunta in preguntas:
        print(f"\nPregunta: {pregunta['pregunta']}")
        for idx, op in enumerate(pregunta["opciones"], start=1):
            print(f" {idx}. {op}")

        try:
            resp = int(input("Tu respuesta: ")) - 1
        except ValueError:
            resp = -1

        if resp == pregunta["respuesta"]:
            puntaje += 1
            print("Correcto! Continuas...")
        else:
            print("Incorrecto! Fin del juego.")
            break

    print(f"\nPuntaje final: {puntaje}")


def jugar_contrarreloj():
    import time

    print("\n=== MODO: CONTRARRELOJ ===\n")
    preguntas = seleccionar_preguntas(cantidad=10)

    tiempo_limite = 30
    inicio = time.time()
    puntaje = 0

    for pregunta in preguntas:
        if time.time() - inicio >= tiempo_limite:
            print("\nTiempo agotado!")
            break

        print(f"\nPregunta: {pregunta['pregunta']}")
        for idx, op in enumerate(pregunta["opciones"], start=1):
            print(f" {idx}. {op}")

        restante = tiempo_limite - (time.time() - inicio)
        print(f"Tiempo restante: {restante:.1f}s")

        try:
            resp = int(input("Tu respuesta: ")) - 1
        except ValueError:
            resp = -1

        if resp == pregunta["respuesta"]:
            print("Correcto!")
            puntaje += 1
        else:
            print("Incorrecto!")

    print(f"\nPuntaje final: {puntaje}")