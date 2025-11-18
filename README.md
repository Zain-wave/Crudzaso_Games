# 🎮 Cursdazo Trivia

Cursdazo Trivia es un juego de trivia interactivo por consola, desarrollado completamente en Python. Incluye interfaz visual usando **Rich**, música de fondo mediante **pygame**, sistema de usuarios, puntuaciones guardadas, modos de juego avanzados y un panel de administración para gestionar preguntas.

---

## 📘 Descripción Breve

Cursdazo Trivia es un juego tipo quiz donde los usuarios responden preguntas en diferentes categorías y niveles de dificultad.  
Incluye:

- ✨ Sistema de login y registro  
- 🛠️ Modo Administrador (gestionar preguntas)  
- 🎵 Música de fondo  
- 🎨 Interfaz visual con Rich  
- 🏆 Puntuaciones y estadísticas  
- 🎲 Tres modos de juego:
  - **Trivia Normal**
  - **Punto Suicida**
  - **Contrarreloj**

---

## 🚀 Instrucciones para Ejecutarlo

1. Instala **Python 3.10+**
2. Instala las dependencias:
   ```bash
   pip install rich pygame
3. Ejecuta el juego
   ```bash
   python main.py

---

## 📚 Librerías Externas Utilizadas

| Librería             | Uso                                                                |
| -------------------- | ------------------------------------------------------------------ |
| **Rich**             | Interfaz visual en consola (colores, paneles, tablas, animaciones) |
| **pygame**           | Reproducción de música de fondo                                    |
| **msvcrt**           | Lectura inmediata de teclas en Windows                             |
| **os / json / time** | Gestión interna de archivos, sesiones, puntuaciones y datos        |

---

## 🗂️ Gestión de Información Implementada

El sistema usa una arquitectura modular que incluye:

# 🔐 Autenticación

Archivos: auth.py, data.py

Registro e inicio de sesión

Validación de credenciales

Almacenamiento en JSON

# 🛠️ Administración

Archivos: admin.py

Crear, editar y eliminar preguntas

Gestión de categorías y niveles

Panel exclusivo para usuarios administradores

# 🎮 Lógica del Juego

Archivos: game.py
Modos implementados:

Trivia Normal → Preguntas continuas, puntuación acumulativa

Punto Suicida → Un error y pierdes

Contrarreloj → Tiempo limitado por pregunta

# 🧭 Menús e Interfaz

Archivos: menu.py, utils.py

Menú principal y menú de modos

Mostrar el nickname del usuario activo

Controles de entrada con msvcrt

Música de fondo con pygame

# 💾 Persistencia de Datos

Preguntas guardadas en JSON

Puntuaciones almacenadas por usuario

---

##🧪 Escenarios de Prueba


# Escenario 1 — Inicio de Sesión Exitoso

Entrada:
Usuario: juan
Contraseña: 1234

Resultado Esperado:
El sistema valida las credenciales, inicia la música, muestra el menú con el nickname del usuario y habilita los modos de juego.

# Escenario 2 — Trivia Normal (respuesta correcta)

Entrada:

Usuario elige Trivia Normal.

Pregunta: “Capital de Francia?”

Respuesta: París

Resultado Esperado:

Se suma 1 punto al usuario.

Se muestra retroalimentación correcta.

Se pasa a la siguiente pregunta.

# Escenario 3 — Modo Punto Suicida (respuesta incorrecta)

Entrada:

Usuario inicia Punto Suicida.

Responde incorrectamente a la primera pregunta.

Resultado Esperado:

El juego termina de inmediato.

Puntuación final mostrada.

Se registra la partida en datos del usuario (si corresponde).


---

# 🧑‍💻 Crudzaso_Games   ------   Guía de Trabajo en Equipo con GitHub

Este documento explica el flujo de trabajo que seguiremos para colaborar en github
---

## 📦 1. Primeros pasos

### 🧭 Clonar el repositorio
Cada uno debe clonar el proyecto en su equipo:

```bash
git clone https://github.com/Zain-wave/Crudzaso_Games
```

### ⚙️ Configuren su identidad en Git de ser necesario(solo una vez)
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu_correo@ejemplo.com"
```

---

## 🌿 2. Trabajaremos todos en la misma rama

Todos trabajaremos sobre la **rama principal (`main`)**.  
Esto sirve **solo si cada uno edita archivos diferentes o módulos independientes** del proyecto.

Verifiquen que estan en la rama correcta usando:
```bash
git branch
```

Si no estan en `main` usen:
```bash
git checkout main
```

---

## 💾 3. Guardar y subir cambios

Cuando terminen una parte o hagan un avancen importantes:

```bash
git add .
git commit -m "Descripción clara del cambio realizado"
git push origin main
```

🧠 **Ejemplo de mensajes de commit:**
- `Agregada funcion de xxxxxxx`
- `Mejorada función de xxxxxxx`
- `Corregido el problema en xxxxxxx`

---

## 🔄 4. Mantengan su repositorio local actualizado

Antes de empezar a trabajar cada día:

```bash
git pull origin main
```

Esto descarga los cambios que subieron los demas.  
Si no hacen este paso, podrías tener algun problema al subir sus cambios.

---

## ⚔️ 5. Resolver conflictos (si ocurren)/(INTENTAR NO HACER ESTO)

Si dos personas modifican el mismo archivo, Git mostrará un conflicto.  
Para solucionarlo:

1. Ejecutamos:
   ```bash
   git status
   ```
2. Abrimos los archivos marcados en conflicto.  
   Vamos a ver secciones como:
   ```
   <<<<<<< HEAD
   # Tu versión
   =======
   # Versión del otro
   >>>>>>>
   ```
3. Eliminamos los marcadores (`<<<<<<<`, `=======`, `>>>>>>>`) y dejamos la versión correcta.
4. Guardamos el archivo y ejecutamos:
   ```bash
   git add <archivo-resuelto>
   git commit
   ```

---

## 🧹 6. Buenas prácticas

- **Antes de subir**, usen `git pull origin main` para traer los últimos cambios.  
- **Eviten modificar archivos que estén siendo trabajados por los otros.**
- **Usen mensajes de commit descriptivos.**

---

## 🧠 7. Flujo recomendado diario

1️⃣ Actualizen su código local  
```bash
git pull origin main
```

2️⃣ Realizen cambios en los archivos asignados  
3️⃣ Guarden y suban su trabajo
```bash
git add .
git commit -m "Mensaje descriptivo"
git push origin main
```

4️⃣ Avisen a los otros que sus cambios ya están en GitHub ✅

---
