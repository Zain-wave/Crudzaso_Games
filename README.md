# 🧑‍💻 Crudzaso_Games   ------   Guía de Trabajo en Equipo con GitHub

Este documento explica el flujo de trabajo que seguiremos para colaborar en github
---

## 📦 1. Primeros pasos

### 🧭 Clonar el repositorio
Cada uno debe clonar el proyecto en su equipo:

```bash
git clone [<URL-del-repo>](https://github.com/Zain-wave/Crudzaso_Games)
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
