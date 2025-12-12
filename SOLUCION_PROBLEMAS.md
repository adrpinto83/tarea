# 🔧 Guía de Solución de Problemas

## ⚠️ Problema: "No se ve el tanque 3D, no permite cambiar valores"

### 🎯 Solución Rápida (Recomendada)

Ejecuta el script de reinicio limpio:

```bash
./reiniciar_dashboard.sh
```

Luego en tu navegador:
1. **Presiona `Ctrl+Shift+R`** (Windows/Linux) o **`Cmd+Shift+R`** (Mac) para hacer un hard refresh
2. O abre una **ventana de incógnito/privada** y accede a `http://localhost:8501`

---

## 🔍 Pasos Detallados de Diagnóstico

### Paso 1: Detener procesos anteriores

```bash
# Detener todos los procesos de Streamlit
pkill -f streamlit

# Verificar que no hay procesos corriendo
ps aux | grep streamlit
```

### Paso 2: Limpiar caché

```bash
# Limpiar caché de Streamlit
rm -rf ~/.streamlit/cache
rm -rf .streamlit/cache

# Limpiar caché del navegador (o usar incógnito)
```

### Paso 3: Verificar entorno virtual

```bash
# Activar entorno virtual
source venv/bin/activate

# Verificar que estás en el entorno correcto
which python
# Debería mostrar: /home/adrpinto/evaluacion3_sce/venv/bin/python

# Verificar dependencias
python -c "import streamlit; import plotly; print('✓ OK')"
```

### Paso 4: Ejecutar dashboard

```bash
# Desde el directorio del proyecto
streamlit run dashboard/dashboard_3d_interactivo.py
```

### Paso 5: Acceder y refrescar navegador

1. Abre `http://localhost:8501` en tu navegador
2. **IMPORTANTE:** Haz un hard refresh:
   - **Chrome/Firefox (Windows/Linux):** `Ctrl+Shift+R` o `Ctrl+F5`
   - **Chrome/Firefox (Mac):** `Cmd+Shift+R`
   - **Safari:** `Cmd+Option+R`
3. O abre una ventana de **incógnito/privada**

---

## 🐛 Problemas Comunes y Soluciones

### Problema 1: "Puerto 8501 ya está en uso"

**Solución:**
```bash
# Opción A: Matar el proceso
pkill -f streamlit

# Opción B: Usar otro puerto
streamlit run dashboard/dashboard_3d_interactivo.py --server.port 8502
```

### Problema 2: "No se ven los controles en el sidebar"

**Causa:** Caché del navegador
**Solución:**
1. Hard refresh: `Ctrl+Shift+R`
2. Limpiar caché del navegador manualmente
3. Usar ventana de incógnito

### Problema 3: "El tanque 3D aparece en blanco"

**Causa:** WebGL no está habilitado o el navegador no soporta Plotly
**Solución:**
1. Verifica que WebGL está habilitado: Visita `chrome://gpu` (Chrome) o `about:support` (Firefox)
2. Usa Google Chrome (recomendado para Plotly)
3. Actualiza tu navegador a la última versión

### Problema 4: "Los sliders no responden"

**Causa:** JavaScript no cargó correctamente
**Solución:**
1. Hard refresh: `Ctrl+Shift+R`
2. Verifica la consola del navegador (F12) por errores
3. Deshabilita extensiones del navegador temporalmente

### Problema 5: "Error: ModuleNotFoundError"

**Causa:** Entorno virtual no activado o dependencias no instaladas
**Solución:**
```bash
# Activar entorno virtual
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt

# Verificar instalación
python -c "import streamlit; import plotly; import numpy; print('✓ OK')"
```

---

## ✅ Checklist de Verificación

Antes de reportar un problema, verifica:

- [ ] Entorno virtual activado (`source venv/bin/activate`)
- [ ] Procesos anteriores de Streamlit detenidos (`pkill -f streamlit`)
- [ ] Caché de Streamlit limpiado (`rm -rf ~/.streamlit/cache`)
- [ ] Hard refresh en el navegador (`Ctrl+Shift+R`)
- [ ] Puerto 8501 disponible (`lsof -i :8501`)
- [ ] Dependencias instaladas (`pip list | grep streamlit`)
- [ ] Navegador actualizado (Chrome recomendado)
- [ ] WebGL habilitado en el navegador

---

## 🧪 Test de Funcionalidad

Ejecuta este comando para verificar que todo funciona:

```bash
source venv/bin/activate && python -c "
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
print('✓ Streamlit:', st.__version__)
print('✓ Plotly:', go.__version__)
print('✓ NumPy:', np.__version__)
print('✓ Pandas:', pd.__version__)
print('\\n✅ Todas las dependencias funcionan correctamente')
"
```

Salida esperada:
```
✓ Streamlit: 1.x.x
✓ Plotly: 5.x.x
✓ NumPy: 1.x.x
✓ Pandas: 1.x.x

✅ Todas las dependencias funcionan correctamente
```

---

## 🔄 Reinicio Completo (Última Opción)

Si nada funciona, haz un reinicio completo:

```bash
# 1. Detener todo
pkill -f streamlit

# 2. Limpiar cachés
rm -rf ~/.streamlit/cache
rm -rf .streamlit/cache
rm -rf __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# 3. Reiniciar entorno virtual
deactivate 2>/dev/null
source venv/bin/activate

# 4. Reinstalar dependencias críticas
pip install --upgrade streamlit plotly

# 5. Ejecutar
streamlit run dashboard/dashboard_3d_interactivo.py

# 6. En el navegador: Ventana de incógnito + Hard refresh
```

---

## 📊 Verificar que las Optimizaciones Funcionan

Una vez que el dashboard cargue, verifica:

1. **No hay mensajes "DEBUG:"** en la interfaz ✅
2. **Los sliders responden inmediatamente** (sin delay de 500ms+) ✅
3. **El tanque 3D se actualiza fluidamente** ✅
4. **Los botones de escenarios funcionan instantáneamente** ✅
5. **Hay máximo 4 gotas animadas** (no 20) ✅

---

## 🆘 Si Aún Hay Problemas

Si después de seguir todos estos pasos el problema persiste:

1. **Verifica la consola del navegador (F12):**
   - Ve a la pestaña "Console"
   - Copia cualquier error en rojo
   - Busca errores de WebGL, JavaScript, o CORS

2. **Verifica logs de Streamlit:**
   - Los errores aparecen en la terminal donde ejecutaste streamlit
   - Busca líneas que empiecen con "Error" o "Traceback"

3. **Prueba con el dashboard original:**
   ```bash
   # Si tienes un backup del original
   streamlit run dashboard/dashboard_streamlit.py
   ```

4. **Revisa requisitos del sistema:**
   - Python >= 3.8
   - Navegador moderno con WebGL
   - Al menos 2GB de RAM disponible

---

## 📝 Información para Reportar Problemas

Si necesitas reportar un problema, incluye:

```bash
# Ejecuta este comando y copia la salida:
echo "=== INFORMACIÓN DEL SISTEMA ==="
python --version
pip list | grep -E "streamlit|plotly|numpy|pandas"
echo ""
echo "=== PROCESOS STREAMLIT ==="
ps aux | grep streamlit
echo ""
echo "=== PUERTO 8501 ==="
lsof -i :8501 2>/dev/null || echo "Puerto disponible"
```

---

**Última actualización:** 2025-12-11
**Archivo:** SOLUCION_PROBLEMAS.md
