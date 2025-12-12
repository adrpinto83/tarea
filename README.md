# 🌊 SCE Gemelo Digital - Sistema de Monitoreo de Nivel

**Evaluación 3 - Microprocesadores Aplicados a Control**

Sistema Computacional Empotrado (SCE) completamente simulado con:
- ✅ Gemelo Digital del sistema físico
- ✅ Programación Orientada a Objetos (POO)
- ✅ Planificador Ejecutivo Cíclico (Tiempo Real)
- ✅ Fusión de Datos Multisensor
- ✅ Machine Learning (Predicción con Random Forest)
- ✅ Dashboard Web Interactivo
- ✨ **NUEVO:** Dashboard 3D Interactivo con Simulación en Vivo

---

## 👥 Equipo

- **Ing. Torres Rousemery**
- **Ing. Pinto Adrian**
- **Ing. Cova Luis**

**Universidad de Oriente - Núcleo Anzoátegui**
Postgrado en Ingeniería Eléctrica
Especialización en Automatización e Informática Industrial

---

## 🚀 Inicio Rápido

### Opción 1: Dashboard 3D Interactivo (NUEVO) ⭐

```bash
./dashboard_3d.sh
```

Características:
- 🌊 Tanque 3D con agua animada en tiempo real
- 🎛️ Controles interactivos (sliders para todos los parámetros)
- 🎮 Simulación física en vivo dentro del dashboard
- 📊 Gráficas animadas y métricas actualizadas
- ⚙️ Control manual de válvulas y bombas
- 🔄 Pausa/reanudación de simulación

**📖 [Ver Guía Completa del Dashboard 3D](DASHBOARD_3D_GUIA.md)**

---

### Opción 2: Ejecución Completa Tradicional

```bash
./start.sh          # Simulación de 120 segundos (default)
./start.sh 300      # Simulación de 300 segundos
```

Ejecuta automáticamente:
1. ✅ Gemelo Digital del SCE (genera datos)
2. ✅ Entrenamiento de Machine Learning
3. ✅ Dashboard Web Tradicional

---

### Opción 3: Componentes Individuales

```bash
# Solo SCE
./run.sh --solo-sce -t 300

# Solo ML
./run.sh --solo-ml

# Solo Dashboard tradicional
./dashboard.sh

# Dashboard 3D Interactivo
./dashboard_3d.sh
```

---

## 📊 Comparación de Dashboards

| Característica | Dashboard Tradicional | Dashboard 3D Interactivo |
|----------------|----------------------|--------------------------|
| Visualización 3D | ❌ No | ✅ Sí |
| Simulación en vivo | ❌ No | ✅ Sí |
| Controles interactivos | ⚠️ Limitados | ✅ Completos |
| Modificar parámetros | ❌ No | ✅ Sí |
| Datos históricos | ✅ Sí | ✅ Sí |
| Animaciones | ⚠️ Básicas | ✅ Avanzadas |

---

## 📁 Estructura del Proyecto

```
evaluacion3_sce/
├── 📄 start.sh                          # Inicio rápido
├── 📄 run.sh                            # Script principal
├── 📄 dashboard.sh                      # Dashboard tradicional
├── 📄 dashboard_3d.sh                   # Dashboard 3D (NUEVO)
│
├── 📚 COMO_USAR.md                      # Guía de uso
├── 📚 DASHBOARD_3D_GUIA.md              # Guía Dashboard 3D (NUEVO)
├── 📚 EJEMPLOS.md                       # Casos de uso
├── 📚 README.md                         # Este archivo
│
├── 🌊 simuladores/                      # Simulador físico
│   └── simulador_tanque.py
│
├── 🤖 sce/                              # Sistema embebido
│   └── sce_gemelo_digital.py
│
├── 🧠 ml/                               # Machine Learning
│   ├── ml_prediccion.py
│   └── modelo_rf.pkl
│
├── 📊 dashboard/                        # Dashboards web
│   ├── dashboard_streamlit.py           # Dashboard tradicional
│   └── dashboard_3d_interactivo.py      # Dashboard 3D (NUEVO)
│
├── 💾 datos/                            # Base de datos
│   └── datos_sce.db
│
└── 📈 resultados/                       # Gráficas ML
    ├── prediccion_ml.png
    └── importancia_features.png
```

---

## 🎮 Características del Dashboard 3D Interactivo

### Modos de Operación

1. **📊 Modo Visualización**
   - Ver datos históricos de la base de datos
   - Gráficas y estadísticas de ejecuciones previas
   - Análisis de tendencias

2. **🎮 Modo Simulación Interactiva**
   - Simulación física en tiempo real
   - Controles para modificar parámetros al vuelo
   - Visualización 3D animada
   - Control manual de actuadores

### Controles Disponibles

- **Parámetros del Tanque:** Altura, Diámetro
- **Caudales:** Entrada (0-10 L/min), Salida (0-10 L/min)
- **Umbrales:** Nivel bajo, Nivel alto
- **Control Manual:** Válvula entrada, Bomba salida
- **Simulación:** Iniciar/Pausar, Reiniciar
- **Velocidad:** Ajustar frecuencia de actualización

### Visualizaciones

- 🌊 **Tanque 3D Interactivo**
  - Rotación con mouse
  - Zoom interactivo
  - Agua animada en tiempo real
  - Líneas de umbrales

- 📊 **Medidor Gauge**
  - Indicador tipo velocímetro
  - Zonas de color según estado
  - Porcentaje de capacidad

- 📈 **Gráficas Dinámicas**
  - Nivel vs tiempo
  - Sensores ambientales
  - Distribución de estados

---

## 💡 Casos de Uso

### Para Demostración
```bash
./dashboard_3d.sh
# Seleccionar "Simulación Interactiva"
# Ajustar parámetros con sliders
# Presionar "Iniciar"
```

### Para Análisis de Datos
```bash
./run.sh --solo-sce -t 600  # Generar datos
./dashboard_3d.sh           # Abrir dashboard
# Seleccionar "Visualización"
```

### Para Experimentación
```bash
./dashboard_3d.sh
# Modo "Simulación Interactiva"
# Cambiar caudales en tiempo real
# Observar respuesta del sistema
```

---

## 📖 Documentación

- **[COMO_USAR.md](COMO_USAR.md)** - Guía de uso general
- **[DASHBOARD_3D_GUIA.md](DASHBOARD_3D_GUIA.md)** - Guía completa del Dashboard 3D
- **[EJEMPLOS.md](EJEMPLOS.md)** - Casos de uso y ejemplos
- **[RESUMEN_FINAL.md](RESUMEN_FINAL.md)** - Estado del proyecto

---

## 🛠️ Requisitos

- Python 3.8+
- Streamlit
- Plotly
- NumPy
- Pandas
- SQLite3
- Scikit-learn

**Instalación automática:**
```bash
bash setup_proyecto.sh
```

---

## 🎯 URLs de Acceso

- **Dashboard 3D Interactivo:** http://localhost:8501
- **Dashboard Tradicional:** http://localhost:8501

*(Solo uno puede ejecutarse a la vez en el puerto 8501)*

---

## 🐛 Solución de Problemas

### Dashboard 3D no muestra el tanque
```bash
pip install plotly --upgrade
```

### Datos históricos no aparecen
```bash
./run.sh --solo-sce -t 120  # Genera datos primero
```

### Puerto ocupado
```bash
# Cambiar puerto en dashboard_3d.sh
streamlit run ... --server.port 8502
```

---

## 🎓 Características Técnicas

- **Planificador Cíclico:** T_menor = 100ms, T_mayor = 2000ms
- **Sensores:** JSN-SR04T (ultrasónico), BME280 (ambiental)
- **Fusión de Datos:** Promedio móvil con ventana de 5 muestras
- **Control:** Histéresis con umbrales configurables
- **ML:** Random Forest Regressor para predicción
- **Simulación:** Ecuaciones diferenciales de flujo

---

## 📞 Contacto

**Equipo de Desarrollo:**
- Ing. Torres Rousemery
- Ing. Pinto Adrian
- Ing. Cova Luis

**🎓 Universidad de Oriente - Núcleo Anzoátegui**
Postgrado en Ingeniería Eléctrica
Especialización en Automatización e Informática Industrial

**📅 Diciembre 2024**

---

**¡Explora el sistema con el nuevo Dashboard 3D Interactivo! 🌊🎮**
