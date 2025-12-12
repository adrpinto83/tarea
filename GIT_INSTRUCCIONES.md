# 📚 Instrucciones para Conectar a GitHub

## ✅ Estado Actual

El repositorio Git local ha sido creado exitosamente:

- ✅ Repositorio Git inicializado
- ✅ Rama principal: `main`
- ✅ `.gitignore` configurado
- ✅ Commit inicial realizado
- ✅ 39 archivos versionados

**Commit inicial:**
```
08a29ca 🎉 Initial commit: SCE Gemelo Digital 3D v3.0
```

---

## 🚀 Conectar a GitHub

### Opción 1: Crear Repositorio en GitHub (Recomendado)

#### Paso 1: Crear Repositorio en GitHub

1. Ve a [GitHub](https://github.com)
2. Inicia sesión
3. Click en el botón **"+"** → **"New repository"**
4. Configurar:
   - **Repository name:** `sce-gemelo-digital-3d`
   - **Description:** Sistema Computacional Empotrado con Gemelo Digital 3D Interactivo
   - **Visibility:** Public o Private (según preferencia)
   - ❌ **NO** marcar "Initialize this repository with a README"
   - ❌ **NO** agregar .gitignore (ya lo tenemos)
   - ❌ **NO** agregar license (opcional, se puede agregar después)
5. Click en **"Create repository"**

#### Paso 2: Conectar Repositorio Local

GitHub te mostrará instrucciones. Usa estas:

```bash
# Agregar remote origin
git remote add origin https://github.com/TU_USUARIO/sce-gemelo-digital-3d.git

# O si usas SSH (recomendado):
# git remote add origin git@github.com:TU_USUARIO/sce-gemelo-digital-3d.git

# Push del commit inicial
git push -u origin main
```

**Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub.**

---

### Opción 2: Usar GitHub CLI (gh)

Si tienes GitHub CLI instalado:

```bash
# Crear repositorio directamente desde terminal
gh repo create sce-gemelo-digital-3d --public --source=. --remote=origin

# Push
git push -u origin main
```

---

## 📝 Comandos Git Útiles

### Ver Estado del Repositorio

```bash
# Ver archivos modificados
git status

# Ver commits
git log --oneline

# Ver archivos ignorados
git status --ignored
```

### Agregar Cambios

```bash
# Agregar archivos específicos
git add archivo.py

# Agregar todos los cambios
git add .

# Ver qué se agregó
git status
```

### Hacer Commits

```bash
# Commit con mensaje
git commit -m "Descripción del cambio"

# Commit con mensaje largo
git commit -m "Título" -m "Descripción detallada"
```

### Sincronizar con GitHub

```bash
# Subir cambios
git push

# Descargar cambios
git pull

# Ver repositorios remotos
git remote -v
```

---

## 🌿 Gestión de Ramas

### Crear Nueva Rama

```bash
# Crear y cambiar a nueva rama
git checkout -b feature/nueva-funcionalidad

# Ver todas las ramas
git branch -a

# Cambiar de rama
git checkout main
```

### Fusionar Ramas

```bash
# Estar en la rama destino (main)
git checkout main

# Fusionar rama
git merge feature/nueva-funcionalidad

# Push de los cambios
git push
```

---

## 🔐 Autenticación con GitHub

### Opción 1: HTTPS con Token Personal

1. Ve a GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Selecciona scopes: `repo`, `workflow`
4. Copia el token
5. Al hacer push, usa el token como contraseña

### Opción 2: SSH (Recomendado)

```bash
# Generar clave SSH (si no tienes)
ssh-keygen -t ed25519 -C "tu_email@ejemplo.com"

# Copiar clave pública
cat ~/.ssh/id_ed25519.pub

# Agregar clave a GitHub:
# Settings → SSH and GPG keys → New SSH key
```

Luego usa URL SSH:
```bash
git remote set-url origin git@github.com:TU_USUARIO/sce-gemelo-digital-3d.git
```

---

## 📊 Información del Repositorio

### Archivos Versionados

**Total:** 39 archivos
**Líneas de código:** ~8,131

### Estructura Incluida

```
✅ dashboard/          - Dashboards web
✅ simuladores/        - Física y sensores
✅ sce/               - Sistema embebido
✅ ml/                - Machine Learning
✅ datos/             - Base de datos
✅ Scripts (*.sh)     - Automatización
✅ Documentación      - Guías y manuales
✅ requirements.txt   - Dependencias
```

### Archivos Excluidos (por .gitignore)

```
❌ venv/              - Entorno virtual
❌ __pycache__/       - Caché Python
❌ *.pyc              - Bytecode
❌ .streamlit/cache/  - Caché Streamlit
❌ *.zip              - Archivos ZIP
❌ *.log              - Logs
```

---

## 🏷️ Tags y Releases

### Crear Tag para Versión

```bash
# Crear tag anotado
git tag -a v3.0.0 -m "Release v3.0.0 - Dashboard 3D Optimizado"

# Push del tag
git push origin v3.0.0

# Ver tags
git tag -l
```

### Crear Release en GitHub

1. Ve al repositorio en GitHub
2. Click en "Releases" → "Create a new release"
3. Selecciona el tag `v3.0.0`
4. Título: "v3.0.0 - Dashboard 3D Optimizado"
5. Descripción: Agregar changelog
6. Adjuntar el archivo `evaluacion3_sce_v3.0.zip`
7. Publicar

---

## 📋 Buenas Prácticas

### Mensajes de Commit

```bash
# Formato recomendado
<tipo>: <descripción corta>

<descripción larga opcional>

# Tipos comunes:
feat:     Nueva funcionalidad
fix:      Corrección de bug
docs:     Cambios en documentación
style:    Formato, punto y coma, etc
refactor: Refactorización de código
perf:     Mejora de rendimiento
test:     Agregar tests
chore:    Tareas de mantenimiento
```

### Ejemplo

```bash
git commit -m "feat: agregar modo de control manual

- Implementado control directo de todos los parámetros
- Agregados escenarios predefinidos
- Actualizada documentación"
```

---

## 🔄 Workflow Recomendado

### Para Desarrollo Individual

```bash
# 1. Hacer cambios
# editar archivos...

# 2. Ver qué cambió
git status
git diff

# 3. Agregar cambios
git add .

# 4. Commit
git commit -m "descripción del cambio"

# 5. Push
git push
```

### Para Trabajo en Equipo

```bash
# 1. Actualizar repositorio
git pull

# 2. Crear rama para nueva funcionalidad
git checkout -b feature/mi-funcionalidad

# 3. Hacer cambios y commits
git add .
git commit -m "feat: nueva funcionalidad"

# 4. Push de la rama
git push -u origin feature/mi-funcionalidad

# 5. Crear Pull Request en GitHub
# (desde la interfaz web)

# 6. Después de merge, actualizar main
git checkout main
git pull
```

---

## 🆘 Solución de Problemas

### Error: "fatal: remote origin already exists"

```bash
# Ver remotes actuales
git remote -v

# Eliminar remote existente
git remote remove origin

# Agregar nuevo remote
git remote add origin https://github.com/TU_USUARIO/sce-gemelo-digital-3d.git
```

### Error: "Updates were rejected"

```bash
# Pull primero
git pull origin main --rebase

# O si quieres forzar (¡cuidado!)
# git push -f origin main
```

### Deshacer Último Commit (sin perder cambios)

```bash
git reset --soft HEAD~1
```

### Deshacer Cambios No Commiteados

```bash
# Descartar todos los cambios
git checkout -- .

# O resetear
git reset --hard HEAD
```

---

## 📚 Recursos Adicionales

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [GitHub CLI](https://cli.github.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## ✅ Checklist de Configuración

- [x] Repositorio Git inicializado
- [x] Rama principal configurada como `main`
- [x] `.gitignore` creado
- [x] Commit inicial realizado
- [ ] Repositorio creado en GitHub
- [ ] Remote `origin` configurado
- [ ] Push inicial realizado
- [ ] README visible en GitHub
- [ ] Configuración de colaboradores (opcional)
- [ ] GitHub Actions/CI configurado (opcional)

---

## 🎯 Próximos Pasos

1. **Crear repositorio en GitHub**
2. **Conectar con `git remote add origin`**
3. **Push inicial:** `git push -u origin main`
4. **Verificar en GitHub** que todo se subió correctamente
5. **Agregar descripción** y topics en GitHub
6. **Crear Release v3.0.0** (opcional)

---

**Fecha de creación:** 2025-12-11
**Rama principal:** main
**Commit inicial:** 08a29ca
**Estado:** ✅ Listo para conectar a GitHub
