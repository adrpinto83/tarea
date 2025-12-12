# 🌊 Dashboard 3D Interactivo - Guía de Usuario

## 🎯 Descripción

Dashboard avanzado con **visualización 3D del tanque** y **simulación interactiva en tiempo real**. Permite controlar y modificar todos los parámetros del sistema de forma visual e intuitiva.

---

## 🚀 Inicio Rápido

### Lanzar el Dashboard

```bash
./dashboard_3d.sh
```

O manualmente:

```bash
source venv/bin/activate
streamlit run dashboard/dashboard_3d_interactivo.py
```

El dashboard se abrirá automáticamente en: **http://localhost:8501**

---

## 🎮 Modos de Operación

### 1. 📊 Modo Visualización

**¿Qué hace?**
- Muestra datos históricos guardados en la base de datos
- Visualiza gráficas y estadísticas de ejecuciones previas
- Tanque 3D muestra el último nivel registrado

**Cuándo usarlo:**
- Para analizar resultados de simulaciones previas
- Para generar reportes
- Para revisar tendencias históricas

**Características:**
- ✅ Tanque 3D con último nivel conocido
- ✅ Gráficas de series temporales
- ✅ Estadísticas descriptivas
- ✅ Distribución de estados (NORMAL, ALERTA_BAJA, ALERTA_ALTA)
- ✅ Tabla de últimas mediciones
- ✅ Auto-refresh opcional

---

### 2. 🎮 Modo Simulación Interactiva

**¿Qué hace?**
- Ejecuta una simulación física del tanque **dentro del dashboard**
- Permite modificar parámetros en tiempo real
- Visualiza el comportamiento del sistema instantáneamente

**Cuándo usarlo:**
- Para experimentar con diferentes configuraciones
- Para entender el comportamiento del sistema
- Para demostraciones interactivas
- Para ajustar y probar controladores

**Características:**
- ✅ Simulación física en tiempo real
- ✅ Controles interactivos (sliders)
- ✅ Tanque 3D animado
- ✅ Modificación de parámetros sin reiniciar
- ✅ Control manual de válvulas
- ✅ Pausa/reanudación de simulación

---

## 🎛️ Controles Interactivos (Modo Simulación)

### ⚙️ Parámetros del Tanque

| Control | Rango | Default | Descripción |
|---------|-------|---------|-------------|
| **Altura Máxima** | 100-300 cm | 200 cm | Altura total del tanque |
| **Diámetro** | 50-200 cm | 100 cm | Diámetro del tanque cilíndrico |

### 💧 Caudales

| Control | Rango | Default | Descripción |
|---------|-------|---------|-------------|
| **Caudal Entrada** | 0-10 L/min | 5 L/min | Flujo de entrada de agua |
| **Caudal Salida** | 0-10 L/min | 3 L/min | Flujo de salida de agua |

### ⚠️ Umbrales de Control

| Control | Rango | Default | Descripción |
|---------|-------|---------|-------------|
| **Umbral Bajo** | 10-100 cm | 30 cm | Nivel mínimo - genera ALERTA_BAJA |
| **Umbral Alto** | 100-250 cm | 170 cm | Nivel máximo - genera ALERTA_ALTA |

### 🎯 Control Manual

| Control | Estado | Descripción |
|---------|--------|-------------|
| **Válvula Entrada** | ON/OFF | Abre/cierra entrada de agua manualmente |
| **Bomba Salida** | ON/OFF | Enciende/apaga bomba de salida manualmente |

### ▶️ Botones de Simulación

| Botón | Acción |
|-------|--------|
| **▶️ Iniciar / ⏸️ Pausar** | Inicia o pausa la simulación |
| **🔄 Reiniciar** | Resetea el tanque a nivel inicial (50 cm) |

### ⏱️ Velocidad de Simulación

- **Rango:** 0.1 - 2.0 segundos
- **Default:** 0.5 segundos
- **Descripción:** Tiempo entre actualizaciones de la simulación

---

## 📊 Visualizaciones Disponibles

### Tab 1: 🌊 Tanque 3D

#### Vista Principal - Tanque 3D Interactivo

**Características:**
- 🎨 Representación 3D del tanque cilíndrico
- 💧 Agua animada en tiempo real
- 🔴 Línea roja: Umbral Alto
- 🟠 Línea naranja: Umbral Bajo
- 🔄 Rotación interactiva (arrastra con el mouse)
- 🔍 Zoom (scroll del mouse)
- 📏 Escalas en cm para X, Y, Z

**Medidor de Nivel (Gauge)**
- 🎯 Indicador tipo velocímetro
- ✅ Zona verde: Normal (30-170 cm)
- 🟡 Zona naranja: Nivel bajo (0-30 cm)
- 🔴 Zona roja: Nivel alto (170-200 cm)
- 📊 Porcentaje de capacidad

**Panel de Información**
- 💧 Volumen actual (Litros)
- 📦 Volumen máximo (Litros)
- 📈 Capacidad utilizada (%)
- 📏 Dimensiones del tanque

---

### Tab 2: 📊 Gráficas

#### Gráfica Principal - Nivel del Tanque
- 📈 Serie temporal del nivel
- ⏱️ Eje X: Tiempo
- 📊 Eje Y: Nivel (cm)
- 🔴 Línea de umbral alto
- 🟠 Línea de umbral bajo
- 🔵 Datos históricos (modo visualización)
- 🟢 Simulación actual (modo interactivo)

#### Sensores Ambientales

**Temperatura**
- 🌡️ Serie temporal
- Rango típico: 24-26°C
- Simula deriva térmica lenta

**Presión Barométrica**
- 🔽 Serie temporal
- Rango típico: 1010-1015 hPa
- Simula variaciones atmosféricas

---

### Tab 3: 📈 Análisis

#### Modo Visualización

**Estadísticas Descriptivas:**
- Media, desviación estándar
- Mínimo, máximo
- Cuartiles (25%, 50%, 75%)
- Cantidad de muestras

**Distribución de Estados:**
- Gráfica de barras coloreada
- ✅ NORMAL: Verde
- 🟡 ALERTA_BAJA: Naranja
- 🔴 ALERTA_ALTA: Rojo

**Tabla de Últimas Mediciones:**
- 20 registros más recientes
- Ordenados por fecha descendente
- Columnas: Fecha/Hora, Nivel, Temperatura, Presión, Estado

#### Modo Simulación

- 📋 Instrucciones de uso
- 💡 Consejos para experimentar
- 🎯 Guía de funcionalidades

---

## 🎨 Características Visuales

### Diseño Moderno

- 🎨 CSS personalizado con gradientes
- 🌈 Esquema de colores profesional
- 📦 Cards con sombras y bordes redondeados
- 🎯 Botones con efectos hover
- 📱 Diseño responsive

### Métricas en Tiempo Real (KPIs)

**4 Métricas Principales:**
1. 💧 **Nivel Actual**
   - Valor en cm
   - Delta (cambio respecto a 10 muestras atrás)

2. 🚦 **Estado del Sistema**
   - ✅ NORMAL
   - 🟡 ALERTA_BAJA
   - 🔴 ALERTA_ALTA

3. 🌡️ **Temperatura**
   - Valor en °C

4. 🔽 **Presión Barométrica**
   - Valor en hPa

---

## 💡 Casos de Uso

### 📚 Caso 1: Demostración Educativa

**Objetivo:** Explicar el funcionamiento del sistema de control

**Pasos:**
1. Abre el dashboard: `./dashboard_3d.sh`
2. Selecciona **"🎮 Simulación Interactiva"**
3. Configura parámetros iniciales:
   - Altura: 200 cm
   - Diámetro: 100 cm
   - Caudal entrada: 5 L/min
   - Caudal salida: 3 L/min
4. Presiona **▶️ Iniciar**
5. Observa el tanque 3D llenándose
6. Explica los umbrales cuando se activen

**Resultado:** Visualización clara del comportamiento del sistema

---

### 🧪 Caso 2: Experimentación con Parámetros

**Objetivo:** Entender el efecto de diferentes caudales

**Pasos:**
1. Modo: **"🎮 Simulación Interactiva"**
2. Inicia simulación con valores por defecto
3. **Durante la simulación**, cambia:
   - Aumenta caudal de entrada a 8 L/min
   - Observa cómo el nivel sube más rápido
   - Disminuye a 2 L/min
   - Observa cómo el nivel baja
4. Experimenta con diferentes combinaciones
5. Observa el tanque 3D respondiendo en tiempo real

**Resultado:** Comprensión intuitiva de la dinámica del sistema

---

### 🎯 Caso 3: Ajuste de Umbrales

**Objetivo:** Encontrar umbrales óptimos

**Pasos:**
1. Modo: **"🎮 Simulación Interactiva"**
2. Establece umbrales iniciales:
   - Bajo: 40 cm
   - Alto: 160 cm
3. Inicia simulación
4. Observa cuándo se activan las alertas
5. Ajusta los umbrales hasta encontrar valores óptimos
6. Observa en el tanque 3D las líneas de umbral

**Resultado:** Umbrales calibrados según necesidades

---

### 🔬 Caso 4: Análisis de Datos Históricos

**Objetivo:** Revisar resultados de simulaciones previas

**Pasos:**
1. Ejecuta primero el SCE: `./run.sh --solo-sce -t 300`
2. Abre dashboard 3D: `./dashboard_3d.sh`
3. Selecciona **"📊 Visualización"**
4. Navega por las tabs:
   - **Tanque 3D:** Ve el último nivel
   - **Gráficas:** Analiza tendencias
   - **Análisis:** Revisa estadísticas
5. Activa **Auto-refresh** para ver datos en vivo

**Resultado:** Análisis completo de datos históricos

---

### 🎮 Caso 5: Control Manual

**Objetivo:** Operar el sistema manualmente

**Pasos:**
1. Modo: **"🎮 Simulación Interactiva"**
2. Desmarca **"Válvula Entrada"** → Nivel empieza a bajar
3. Activa **"Bomba Salida"** → Nivel baja más rápido
4. Marca **"Válvula Entrada"** de nuevo → Nivel sube
5. Desactiva **"Bomba Salida"** → Nivel sube más rápido
6. Observa el tanque 3D respondiendo a tus comandos

**Resultado:** Control total manual del sistema

---

## 🎓 Experimentos Sugeridos

### Experimento 1: Llenado Rápido

**Configuración:**
- Caudal entrada: 10 L/min (máximo)
- Caudal salida: 0 L/min
- Válvula entrada: ON
- Bomba salida: OFF

**Observar:** Tiempo que tarda en alcanzar el umbral alto

---

### Experimento 2: Vaciado Rápido

**Configuración:**
- Caudal entrada: 0 L/min
- Caudal salida: 10 L/min (máximo)
- Válvula entrada: OFF
- Bomba salida: ON

**Observar:** Tiempo que tarda en alcanzar el umbral bajo

---

### Experimento 3: Equilibrio Perfecto

**Objetivo:** Mantener nivel constante

**Configuración:**
- Caudal entrada: 5 L/min
- Caudal salida: 5 L/min
- Ambas válvulas: ON

**Observar:** Nivel debería mantenerse estable

---

### Experimento 4: Oscilación

**Configuración:**
- Caudal entrada: 7 L/min
- Caudal salida: 5 L/min
- Umbral bajo: 50 cm
- Umbral alto: 150 cm

**Observar:** Sistema oscilando entre umbrales

---

## ⚙️ Configuración Avanzada

### Personalizar Colores

Editar `dashboard/dashboard_3d_interactivo.py` línea 71-76:

```python
streamlit run dashboard/dashboard_3d_interactivo.py \
    --theme.primaryColor "#TU_COLOR" \
    --theme.backgroundColor "#TU_FONDO"
```

### Cambiar Puerto

```bash
streamlit run dashboard/dashboard_3d_interactivo.py --server.port 8502
```

---

## 🐛 Solución de Problemas

### El tanque 3D no se muestra

**Solución:**
```bash
pip install plotly --upgrade
```

### La simulación se congela

**Solución:**
- Reduce la velocidad de actualización (slider a 1.0-2.0s)
- Verifica que no haya procesos pesados ejecutándose

### Los datos históricos no aparecen

**Solución:**
```bash
# Genera datos primero
./run.sh --solo-sce -t 120
# Luego abre el dashboard
./dashboard_3d.sh
```

### El navegador no se abre automáticamente

**Solución:**
Abre manualmente: http://localhost:8501

---

## 🎯 Atajos de Teclado (en navegador)

- **Ctrl + R** - Recargar dashboard
- **F11** - Pantalla completa
- **Ctrl + Shift + I** - Abrir DevTools (debug)
- **Ctrl + +/-** - Zoom in/out

---

## 📊 Comparación con Dashboard Original

| Característica | Dashboard Original | Dashboard 3D Interactivo |
|----------------|-------------------|-------------------------|
| Visualización 3D | ❌ No | ✅ Sí |
| Simulación en vivo | ❌ No | ✅ Sí |
| Controles interactivos | ⚠️ Limitados | ✅ Completos |
| Modificar parámetros | ❌ No | ✅ Sí |
| Control manual | ❌ No | ✅ Sí |
| Tanque animado | ❌ No | ✅ Sí |
| Gauge de nivel | ❌ No | ✅ Sí |
| Tabs organizados | ⚠️ Básico | ✅ Avanzado |
| CSS personalizado | ⚠️ Básico | ✅ Completo |

---

## 👥 Créditos

**Desarrollado por:**
- Ing. Torres Rousemery
- Ing. Pinto Adrian
- Ing. Cova Luis

**🎓 Universidad de Oriente - Núcleo Anzoátegui**
Postgrado en Ingeniería Eléctrica
Especialización en Automatización e Informática Industrial

**📅 Diciembre 2024**

---

## 📚 Referencias

- **Streamlit:** https://streamlit.io/
- **Plotly 3D:** https://plotly.com/python/3d-charts/
- **Ecuaciones del Tanque:** Basadas en ecuaciones diferenciales de flujo

---

**¡Disfruta explorando el sistema! 🌊**
