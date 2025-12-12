# 🚀 Guía de Instalación y Uso - SCE Gemelo Digital 3D

## 📦 Contenido del Paquete

Este archivo ZIP contiene todo lo necesario para ejecutar el Sistema de Control de Tanque con Gemelo Digital 3D.

---

## ⚡ Instalación Rápida (3 pasos)

### Linux / macOS

```bash
# 1. Descomprimir y entrar a la carpeta
unzip evaluacion3_sce.zip
cd evaluacion3_sce

# 2. Instalar (crear entorno virtual e instalar dependencias)
chmod +x instalar.sh
./instalar.sh

# 3. Ejecutar
./iniciar_dashboard.sh
```

### Windows

```cmd
REM 1. Descomprimir el ZIP y abrir CMD/PowerShell en la carpeta

REM 2. Crear entorno virtual e instalar
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

REM 3. Ejecutar
venv\Scripts\activate
streamlit run dashboard/dashboard_3d_interactivo.py
```

---

## 📋 Requisitos Previos

- **Python 3.8 o superior** ([Descargar](https://www.python.org/downloads/))
- **Navegador moderno** (Chrome recomendado)
- **Conexión a Internet** (solo para instalación de dependencias)

**Verificar Python:**
```bash
python --version  # o python3 --version
```

---

## 🌐 Acceso a la Aplicación

Una vez iniciada, la aplicación estará disponible en:
```
http://localhost:8501
```

El navegador debería abrirse automáticamente. Si no, copia y pega la URL anterior.

---

## 🎮 Uso Básico

### Modo Control Manual (Recomendado para empezar)

1. En el sidebar izquierdo, selecciona **"🎮 Control Manual Total"**
2. Usa los sliders para:
   - **💧 Nivel del Tanque:** Cambia el nivel directamente
   - **🌡️ Temperatura:** Ajusta temperatura ambiente
   - **🔽 Presión:** Modifica presión barométrica
3. Prueba los botones de **Escenarios Rápidos**
4. Observa el tanque 3D actualizarse en tiempo real

### Modo Simulación Física

1. Selecciona **"🔄 Simulación Física"**
2. Configura:
   - Caudal de Entrada: 20 L/min
   - Caudal de Salida: 5 L/min
   - Activa Válvula de Entrada
3. Presiona **"▶️ Iniciar"**
4. Observa el nivel subir automáticamente

**Tip:** Usa velocidad de 0.5-0.7s para mejor balance entre fluidez y rendimiento.

---

## 🔧 Solución de Problemas

### Problema: "ModuleNotFoundError"

```bash
# Activar entorno virtual
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstalar dependencias
pip install -r requirements.txt
```

### Problema: "Puerto 8501 ya en uso"

```bash
# Detener proceso anterior
pkill -f streamlit  # Linux/macOS

# O ejecutar en otro puerto
streamlit run dashboard/dashboard_3d_interactivo.py --server.port 8502
```

### Problema: No se ve el tanque 3D

1. Haz **hard refresh:** `Ctrl+Shift+R` (o `Cmd+Shift+R` en Mac)
2. Abre una ventana de **incógnito**
3. Verifica que WebGL esté habilitado en tu navegador

### Problema: Flickering visible

- Aumenta la velocidad de actualización a 0.7-1.0s en el slider
- Usa Google Chrome para mejor rendimiento

---

## 📁 Estructura de Archivos

```
evaluacion3_sce/
├── dashboard/              # Dashboards web
│   └── dashboard_3d_interactivo.py  ← DASHBOARD PRINCIPAL
├── simuladores/            # Física y sensores
├── sce/                    # Sistema embebido
├── ml/                     # Machine Learning
├── datos/                  # Base de datos
├── instalar.sh             # Script de instalación (Linux/Mac)
├── iniciar_dashboard.sh    # Script de inicio (Linux/Mac)
├── reiniciar_dashboard.sh  # Script de reinicio (Linux/Mac)
├── requirements.txt        # Dependencias Python
└── README.md              # Documentación completa
```

---

## 📚 Documentación Adicional

- **`README.md`** - Documentación completa del proyecto
- **`OPTIMIZACIONES_REALIZADAS.md`** - Detalles técnicos de optimizaciones
- **`SOLUCION_PROBLEMAS.md`** - Guía completa de troubleshooting
- **`DASHBOARD_3D_GUIA.md`** - Guía técnica del dashboard

---

## ✅ Verificación de Instalación

Ejecuta este comando para verificar que todo está instalado:

```bash
source venv/bin/activate
python -c "import streamlit; import plotly; import numpy; print('✅ Instalación correcta')"
```

Deberías ver: `✅ Instalación correcta`

---

## 🆘 Ayuda

Si tienes problemas:

1. ✅ Lee `SOLUCION_PROBLEMAS.md`
2. ✅ Verifica los requisitos previos
3. ✅ Usa el script `reiniciar_dashboard.sh`

---

## 🎯 Próximos Pasos

1. ✅ Instalar usando `instalar.sh`
2. ✅ Ejecutar con `iniciar_dashboard.sh`
3. ✅ Explorar el Modo Control Manual
4. ✅ Probar la Simulación Física
5. ✅ Leer la documentación completa

---

**¡Disfruta del sistema! 🌊🎉**
