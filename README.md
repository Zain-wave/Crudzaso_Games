# 🧑‍💻 Crudzaso_Games   ------   Guía de Trabajo en Equipo con GitHub

Este documento explica el flujo de trabajo que seguiremos para colaborar en github
---

## 📦 1. Primeros pasos

### 🧭 Clonar el repositorio
Cada uno debe clonar el proyecto en su equipo:

```bash
git clone [<URL-del-repo>](https://github.com/Zain-wave/Crudzaso_Games)
```

### ⚙️ Configurar tu identidad en Git (solo una vez/ si es necesario)
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu_correo@ejemplo.com"
```

---

## 🌿 2. Trabajaremos todos en la misma rama

Todos los integrantes trabajaremos sobre la **rama principal (`main`)**.  
Esto es válido **solo si cada uno edita archivos diferentes o módulos independientes** del proyecto.

Verifica que estás en la rama correcta:
```bash
git branch
```

Si no estás en `main` usa:
```bash
git checkout main
```

---

## 💾 3. Guardar y subir cambios

Cuando termines una parte o hagas avances importantes:

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

## 🔄 4. Mantener tu repositorio actualizado

Antes de empezar a trabajar cada día:

```bash
git pull origin main
```

Esto descarga los cambios que subieron los otros.  
Si no haces este paso, podrías tener problemas al subir tus propios cambios.

---

## ⚔️ 5. Resolver conflictos (si ocurren)/(INTENTAR NO HACER ESTO)

Si dos personas modifican el mismo archivo, Git mostrará un conflicto.  
Para solucionarlo:

1. Ejecuta:
   ```bash
   git status
   ```
2. Abre los archivos marcados en conflicto.  
   Verás secciones como:
   ```
   <<<<<<< HEAD
   # Tu versión
   =======
   # Versión del otro miembro
   >>>>>>>
   ```
3. Elimina los marcadores (`<<<<<<<`, `=======`, `>>>>>>>`) y deja la versión correcta.
4. Guarda el archivo y ejecuta:
   ```bash
   git add <archivo-resuelto>
   git commit
   ```

---

## 🧹 6. Buenas prácticas

- **Antes de subir**, haz `git pull origin main` para traer los últimos cambios.  
- **Evita modificar archivos que estén siendo trabajados por otros.**
- **Usa mensajes de commit descriptivos.**
- **No subas** carpetas o archivos temporales.

---

## 🧠 7. Flujo recomendado diario

1️⃣ Actualiza tu código local  
```bash
git pull origin main
```

2️⃣ Realiza tus cambios en los archivos asignados  
3️⃣ Guarda y sube tu trabajo  
```bash
git add .
git commit -m "Mensaje descriptivo"
git push origin main
```

4️⃣ Avisa al grupo que tus cambios ya están en GitHub ✅

---
