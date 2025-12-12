# 🌐 INSTRUCCIONES PARA VER EL DASHBOARD

## ⚠️ IMPORTANTE

El dashboard es una **aplicación web** que se visualiza en el **navegador**, NO en la terminal.

---

## 🎯 Cómo Visualizar el Dashboard

### Paso 1: Ejecutar el servidor
```bash
./dashboard.sh
```

O con el script completo:
```bash
./start.sh
```

### Paso 2: Lo que verás en la TERMINAL
```
════════════════════════════════════════════════════════════════
  PASO 3: LANZANDO DASHBOARD WEB INTERACTIVO
════════════════════════════════════════════════════════════════

🌐 Abriendo dashboard en el navegador...
📍 URL: http://localhost:8501

You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://172.23.195.162:8501
```

**Esto es SOLO el servidor ejecutándose.**
**El contenido NO se ve en la terminal.**

### Paso 3: Abrir el NAVEGADOR WEB

1. Abre tu navegador (Chrome, Firefox, Edge, Safari, etc.)

2. Ve a una de estas direcciones:
   - **Local:** `http://localhost:8501`
   - **Red local:** `http://172.23.195.162:8501`

3. **ALLÍ** verás el dashboard completo con:

---

## 🎨 Lo que VERÁS en el NAVEGADOR

### Parte Superior del Dashboard

```
═══════════════════════════════════════════════════════════════
🌊 Sistema de Monitoreo de Nivel - Gemelo Digital
═══════════════════════════════════════════════════════════════

Simulación de SCE con Raspberry Pi 3 + Fusión de Datos + Machine Learning

┌─────────────────────────────────────────────────────────────┐
│ ℹ️ Mensaje de Información (azul)                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 📚 Evaluación 3 - Microprocesadores Aplicados a Control    │
│                                                             │
│ Sistema Computacional Empotrado (SCE) implementado con:    │
│ ✅ Programación Orientada a Objetos (POO)                  │
│ ✅ Planificador Ejecutivo Cíclico (Tiempo Real)            │
│ ✅ Fusión de Datos Multisensor                             │
│ ✅ Machine Learning con Random Forest                      │
│ ✅ Dashboard Interactivo Web                               │
│                                                             │
│ ───────────────────────────────────────────────────────────│
│                                                             │
│ 👥 Desarrollado por:                                       │
│ - Ing. Torres Rousemery                                     │
│ - Ing. Pinto Adrian                                         │
│ - Ing. Cova Luis                                            │
│                                                             │
│ 🎓 Universidad de Oriente - Núcleo Anzoátegui              │
│    Postgrado en Ingeniería Eléctrica                        │
│    Especialización en Automatización e Informática          │
│                                                             │
│ Diciembre 2024                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════════
📌 Indicadores en Tiempo Real
═══════════════════════════════════════════════════════════════

┌──────────────┬──────────────┬──────────────┬──────────────┐
│ 💧 Nivel     │ 🚦 Estado    │ 🌡️ Temp      │ 🔽 Presión   │
│ 50.52 cm     │ ✅ NORMAL    │ 25.0°C       │ 1013.2 hPa   │
└──────────────┴──────────────┴──────────────┴──────────────┘

[Gráfica interactiva del nivel del tanque]
[Gráficas de temperatura y presión]
[Distribución de estados]
[Estadísticas]
[Tabla de datos]
```

### Panel Lateral (Sidebar)

```
┌──────────────────────────────────┐
│ SCE UDO [Logo]                   │
│                                  │
│ ⚙️ Configuración                 │
│ □ 🔄 Auto-refresh (cada 2s)      │
│ ━━━━━━━━━━                       │
│ 📊 Muestras: 500                 │
│                                  │
│ ─────────────────────────────────│
│                                  │
│ 📘 Acerca del Proyecto           │
│                                  │
│ Evaluación 3                     │
│ Microprocesadores Aplicados      │
│                                  │
│ 👥 Equipo de Desarrollo:         │
│ - Ing. Torres Rousemery          │
│ - Ing. Pinto Adrian              │
│ - Ing. Cova Luis                 │
│                                  │
│ 🎓 Universidad de Oriente        │
│    Núcleo Anzoátegui             │
│    Postgrado en Ingeniería       │
│                                  │
│ 📅 Diciembre 2024                │
└──────────────────────────────────┘
```

---

## 🔧 Si Estás en WSL/Linux sin Interfaz Gráfica

Si estás en WSL (Windows Subsystem for Linux) o un servidor sin interfaz gráfica:

### Opción 1: Abrir desde Windows
1. Deja el servidor corriendo en la terminal WSL
2. Abre un navegador en **Windows**
3. Ve a: `http://localhost:8501`

### Opción 2: Usar la IP de red
1. Usa la Network URL que aparece en la terminal:
   `http://172.23.195.162:8501`
2. Abre esta URL desde cualquier dispositivo en la misma red

### Opción 3: Generar captura de pantalla
```bash
# Instalar navegador headless y capturador
sudo apt update
sudo apt install -y chromium-browser

# Capturar screenshot del dashboard (ejemplo)
chromium-browser --headless --screenshot=dashboard.png http://localhost:8501
```

---

## 📸 Crear Capturas del Dashboard

Si quieres documentar cómo se ve, puedes:

1. Abrir el dashboard en el navegador
2. Presionar `F12` para abrir DevTools
3. Usar la herramienta de captura de pantalla del navegador
4. O simplemente usar `Print Screen`

---

## ✅ Checklist de Verificación

- [ ] Ejecuté `./dashboard.sh` o `./start.sh`
- [ ] Vi el mensaje "You can now view your Streamlit app in your browser"
- [ ] Copié la URL: `http://localhost:8501`
- [ ] Abrí mi NAVEGADOR WEB
- [ ] Pegué la URL en la barra de direcciones
- [ ] Presioné ENTER
- [ ] ✅ **AHORA SÍ veo el dashboard completo**

---

## 🐛 Solución de Problemas

### "No puedo abrir el navegador"
- Estás en WSL: Abre el navegador en Windows y usa `localhost:8501`
- Estás en servidor remoto: Usa la Network URL desde otro dispositivo

### "La página no carga"
```bash
# Verifica que el servidor esté corriendo
ps aux | grep streamlit

# Verifica el puerto
netstat -tulpn | grep 8501

# Si hay problemas, usa otro puerto
streamlit run dashboard/dashboard_streamlit.py --server.port 8502
```

### "Solo veo la terminal"
- **Normal.** El contenido está en el navegador web, no en la terminal.

---

## 📞 Preguntas Frecuentes

**P: ¿Dónde veo el mensaje personalizado?**
R: En el navegador web, no en la terminal.

**P: ¿Por qué no se ve en la terminal?**
R: Porque Streamlit es una aplicación web. La terminal solo muestra el servidor.

**P: ¿Cómo detengo el servidor?**
R: Presiona `Ctrl+C` en la terminal.

**P: ¿Puedo verlo desde otro dispositivo?**
R: Sí, usa la Network URL: `http://172.23.195.162:8501`

---

**Recuerda:** El dashboard es una **aplicación WEB** 🌐
Debes verlo en un **NAVEGADOR** 🖥️, no en la **TERMINAL** 💻
