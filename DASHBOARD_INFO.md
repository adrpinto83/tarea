# 📊 Información del Dashboard

## Mensaje de Bienvenida Personalizado

Al abrir el dashboard, los usuarios verán el siguiente mensaje en español:

---

### 🌊 Sistema de Monitoreo de Nivel - Gemelo Digital
**Simulación de SCE con Raspberry Pi 3 + Fusión de Datos + Machine Learning**

> **📚 Evaluación 3 - Microprocesadores Aplicados a Control**
>
> Sistema Computacional Empotrado (SCE) implementado con:
> ✅ Programación Orientada a Objetos (POO)
> ✅ Planificador Ejecutivo Cíclico (Tiempo Real)
> ✅ Fusión de Datos Multisensor
> ✅ Machine Learning con Random Forest
> ✅ Dashboard Interactivo Web
>
> ---
>
> **👥 Desarrollado por:**
> - Ing. Torres Rousemery
> - Ing. Pinto Adrian
> - Ing. Cova Luis
>
> **🎓 Universidad de Oriente - Núcleo Anzoátegui**
> Postgrado en Ingeniería Eléctrica
> Especialización en Automatización e Informática Industrial
>
> *Diciembre 2024*

---

## Panel Lateral (Sidebar)

El sidebar incluye:

### ⚙️ Configuración
- 🔄 Auto-refresh (cada 2s)
- 📊 Muestras a mostrar (50-1000)

### 📘 Acerca del Proyecto

> **Evaluación 3**
> Microprocesadores Aplicados a Control
>
> **👥 Equipo de Desarrollo:**
> - Ing. Torres Rousemery
> - Ing. Pinto Adrian
> - Ing. Cova Luis
>
> **🎓 Institución:**
> Universidad de Oriente
> Núcleo Anzoátegui
> Postgrado en Ingeniería Eléctrica
>
> **📅 Fecha:** Diciembre 2024

---

## Características del Dashboard

### 📌 Indicadores en Tiempo Real (KPIs)
- 💧 Nivel Actual (cm)
- 🚦 Estado del Sistema
- 🌡️ Temperatura (°C)
- 🔽 Presión Barométrica (hPa)

### 📊 Gráficas Interactivas
1. **Nivel del Tanque en Tiempo Real**
   - Serie temporal con umbrales de alarma
   - Umbral Alto: 170 cm (línea roja)
   - Umbral Bajo: 30 cm (línea naranja)

2. **Sensores Ambientales**
   - Temperatura vs tiempo
   - Presión barométrica vs tiempo

3. **Distribución de Estados**
   - Gráfica de barras con frecuencia de estados
   - Estados: NORMAL, ALERTA_BAJA, ALERTA_ALTA

### 📈 Estadísticas del Sistema
- Estadísticas descriptivas del nivel
- Estadísticas de temperatura
- Estadísticas de presión

### 📋 Tabla de Datos
- Últimas 20 mediciones
- Columnas: Fecha/Hora, Nivel, Temperatura, Presión, Estado

---

## Configuración Técnica

### Archivos de Configuración Streamlit

**`.streamlit/config.toml`**
```toml
[browser]
gatherUsageStats = false

[runner]
magicEnabled = true
fastReruns = true

[client]
showErrorDetails = true
toolbarMode = "minimal"

[server]
headless = true
port = 8501
enableCORS = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

**`.streamlit/credentials.toml`**
```toml
[general]
email = ""
```

Estos archivos evitan que Streamlit solicite el email al usuario.

---

## Cómo Ejecutar

```bash
# Opción 1: Script rápido
./dashboard.sh

# Opción 2: Manual
source venv/bin/activate
streamlit run dashboard/dashboard_streamlit.py

# Opción 3: Como parte del flujo completo
./start.sh 300
```

El dashboard se abrirá automáticamente en: **http://localhost:8501**

---

## Capturas de Pantalla (Descripción)

El dashboard muestra:

1. **Parte Superior:**
   - Título principal
   - Mensaje de bienvenida con información del proyecto
   - KPIs en 4 columnas

2. **Parte Central:**
   - Gráfica grande del nivel del tanque
   - Dos columnas: Sensores ambientales | Distribución de estados

3. **Parte Inferior:**
   - Estadísticas en 3 columnas
   - Tabla de últimas mediciones
   - Footer con métricas de resumen

4. **Sidebar Izquierdo:**
   - Logo/Banner del proyecto
   - Controles de configuración
   - Información del equipo
