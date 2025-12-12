# 📖 GUÍA DE USO - SCE Gemelo Digital

## 🚀 Inicio Rápido

### Opción 1: Ejecución Completa Automática (Recomendado)
```bash
./start.sh          # Simulación de 120 segundos (default)
./start.sh 300      # Simulación de 300 segundos
```

Esto ejecutará automáticamente:
1. ✅ Gemelo Digital del SCE (genera datos)
2. ✅ Entrenamiento de Machine Learning
3. ✅ Dashboard Web Interactivo

---

## 🎯 Opciones Avanzadas

### Script Principal con Opciones
```bash
# Ejecución completa personalizada
./run.sh -t 300                    # 300 segundos de simulación

# Ejecutar solo componentes específicos
./run.sh --solo-sce                # Solo el SCE
./run.sh --solo-ml                 # Solo entrenar ML
./run.sh --solo-dashboard          # Solo dashboard

# Ver ayuda
./run.sh --help
```

### Scripts Individuales
```bash
# Solo Dashboard
./dashboard.sh

# Componentes manuales
source venv/bin/activate
python sce/sce_gemelo_digital.py -t 300
python ml/ml_prediccion.py
streamlit run dashboard/dashboard_streamlit.py
```

---

## 📊 Flujo de Trabajo

```
┌─────────────────────────────────────────────────────────────┐
│                  FLUJO DE EJECUCIÓN                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. 🔧 Activar Entorno Virtual                              │
│     └─> source venv/bin/activate                            │
│                                                             │
│  2. 🌊 Ejecutar SCE Gemelo Digital                          │
│     ├─> Simula tanque físico                                │
│     ├─> Lee sensores (ultrasónico + ambiental)              │
│     ├─> Fusiona datos                                       │
│     ├─> Ejecuta control con planificador cíclico            │
│     └─> Guarda en BD: datos/datos_sce.db                    │
│                                                             │
│  3. 🤖 Entrenar Modelo ML                                   │
│     ├─> Carga datos de BD                                   │
│     ├─> Crea features temporales                            │
│     ├─> Entrena Random Forest                               │
│     ├─> Evalúa métricas (MSE, R², MAE)                      │
│     ├─> Guarda modelo: ml/modelo_rf.pkl                     │
│     └─> Genera gráficas en resultados/                      │
│                                                             │
│  4. 📊 Lanzar Dashboard                                     │
│     ├─> Carga datos de BD                                   │
│     ├─> Visualiza KPIs en tiempo real                       │
│     ├─> Gráficas interactivas (Plotly)                      │
│     └─> URL: http://localhost:8501                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Archivos Generados

Después de ejecutar, encontrarás:

```
evaluacion3_sce/
├── datos/
│   └── datos_sce.db                    # 📊 Base de datos SQLite
├── ml/
│   └── modelo_rf.pkl                   # 🤖 Modelo Random Forest
└── resultados/
    ├── prediccion_ml.png               # 📈 Gráfica predicciones
    └── importancia_features.png        # 📊 Importancia features
```

---

## 🎓 Ejemplos de Uso

### Caso 1: Demo Rápida (2 minutos)
```bash
./start.sh 120
# Dashboard se abre automáticamente en http://localhost:8501
```

### Caso 2: Simulación Larga para Análisis (10 minutos)
```bash
./run.sh -t 600
```

### Caso 3: Re-entrenar ML con Datos Nuevos
```bash
./run.sh --solo-sce -t 300    # Generar más datos
./run.sh --solo-ml            # Re-entrenar con datos nuevos
```

### Caso 4: Solo Visualizar Datos Existentes
```bash
./dashboard.sh
```

---

## 🐛 Solución de Problemas

### Error: "Entorno virtual no encontrado"
```bash
# Instalar la aplicación primero
bash setup_proyecto.sh
source venv/bin/activate
pip install -r requirements.txt
```

### Error: "No hay datos en la base de datos"
```bash
# Ejecutar primero el SCE para generar datos
./run.sh --solo-sce
```

### Error: "Modelo no encontrado"
```bash
# Entrenar el modelo
./run.sh --solo-ml
```

### Dashboard no se abre
```bash
# Verificar que Streamlit esté instalado
source venv/bin/activate
pip install streamlit

# Ejecutar manualmente
streamlit run dashboard/dashboard_streamlit.py --server.port 8501
```

---

## ⚙️ Configuración Personalizada

### Modificar Tiempo de Simulación por Defecto
Editar `start.sh`:
```bash
TIEMPO=${1:-300}  # Cambiar 120 a 300 segundos
```

### Modificar Parámetros del Tanque
Editar `sce/sce_gemelo_digital.py`:
```python
self.tanque = TanqueSimulado(
    altura_max=200,     # Altura máxima del tanque (cm)
    diametro=100,       # Diámetro (cm)
    caudal_entrada=5,   # Caudal entrada (L/min)
    caudal_salida=3     # Caudal salida (L/min)
)
```

### Modificar Umbrales de Control
Editar `sce/sce_gemelo_digital.py`:
```python
self.controlador = ControladorNivel(
    H_max=200,
    umbral_bajo=30,     # Cambiar umbral bajo
    umbral_alto=170     # Cambiar umbral alto
)
```

---

## 📞 Soporte

**Equipo de Desarrollo:**
- Ing. Torres Rousemery
- Ing. Pinto Adrian
- Ing. Cova Luis

**Universidad de Oriente - Núcleo Anzoátegui**
Postgrado en Ingeniería Eléctrica

---

## 🎯 Tips y Mejores Prácticas

1. **Primera ejecución**: Usa `./start.sh` para ver todo el flujo
2. **Análisis detallado**: Ejecuta con `-t 600` o más para más datos
3. **Re-entrenar ML**: Ejecuta varias veces el SCE con `--solo-sce` y luego `--solo-ml`
4. **Comparar resultados**: Guarda las gráficas de `resultados/` con diferentes nombres
5. **Dashboard en background**: Ejecuta `./dashboard.sh` en una terminal separada

---

## 📚 Documentación Adicional

- **README.md**: Descripción general del proyecto
- **sce/sce_gemelo_digital.py**: Código documentado del SCE
- **ml/ml_prediccion.py**: Código documentado de ML
- **dashboard/dashboard_streamlit.py**: Código del dashboard

---

**¡Listo para usar! 🚀**
