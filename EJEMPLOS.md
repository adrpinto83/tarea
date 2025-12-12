# 🚀 EJEMPLOS DE USO RÁPIDO

## Caso de Uso 1: Demo Rápida (2 minutos)
```bash
./start.sh
# Ejecuta simulación de 120 segundos
# Entrena ML automáticamente
# Abre dashboard en http://localhost:8501
```

## Caso de Uso 2: Simulación Larga (10 minutos)
```bash
./start.sh 600
# Simulación de 10 minutos para más datos
```

## Caso de Uso 3: Ejecutar Solo Componentes Específicos

### Solo generar datos del SCE:
```bash
./run.sh --solo-sce -t 300
```

### Solo entrenar Machine Learning:
```bash
./run.sh --solo-ml
```

### Solo ver Dashboard:
```bash
./run.sh --solo-dashboard
# o simplemente:
./dashboard.sh
```

## Caso de Uso 4: Flujo Completo Manual

### Paso 1: Activar entorno virtual
```bash
source venv/bin/activate
```

### Paso 2: Generar datos (5 minutos)
```bash
python sce/sce_gemelo_digital.py -t 300
```

### Paso 3: Entrenar modelo ML
```bash
python ml/ml_prediccion.py
```

### Paso 4: Ver resultados en Dashboard
```bash
streamlit run dashboard/dashboard_streamlit.py
```

## Caso de Uso 5: Generar Múltiples Datasets

```bash
# Primera ejecución
./run.sh --solo-sce -t 300

# Segunda ejecución (acumula más datos)
./run.sh --solo-sce -t 300

# Tercera ejecución
./run.sh --solo-sce -t 300

# Ahora entrenar con todos los datos acumulados
./run.sh --solo-ml
```

## Caso de Uso 6: Experimentación con Parámetros

### Modificar parámetros del tanque:
```bash
# Editar sce/sce_gemelo_digital.py línea ~389
# Cambiar altura_max, diametro, caudal_entrada, caudal_salida

# Luego ejecutar:
./run.sh --solo-sce -t 300
./run.sh --solo-ml
./dashboard.sh
```

## Caso de Uso 7: Ver Ayuda

```bash
./run.sh --help
```

## Caso de Uso 8: Ejecución en Background

### Terminal 1: Dashboard en background
```bash
./dashboard.sh &
```

### Terminal 2: Continuar trabajando
```bash
./run.sh --solo-sce -t 600
```

## 📊 Archivos Generados

Después de ejecutar encontrarás:

```
evaluacion3_sce/
├── datos/
│   └── datos_sce.db                    # Base de datos SQLite con mediciones
├── ml/
│   └── modelo_rf.pkl                   # Modelo Random Forest entrenado
└── resultados/
    ├── prediccion_ml.png               # Gráfica de predicciones vs reales
    └── importancia_features.png        # Importancia de características
```

## 🎯 Tips

- **Primera vez**: Usa `./start.sh` para ver todo el flujo completo
- **Experimentos**: Usa `./run.sh --solo-sce` múltiples veces, luego `--solo-ml`
- **Presentación**: Ejecuta con `-t 600` para tener muchos datos y buenos gráficos
- **Debug**: Revisa `datos/datos_sce.db` con herramientas SQLite

## 🐛 Solución Rápida de Problemas

### Error: "No module named 'simuladores'"
```bash
# Asegúrate de ejecutar desde el directorio raíz
cd /home/adrpinto/evaluacion3_sce
./run.sh --solo-sce
```

### Error: "No hay datos"
```bash
# Genera datos primero
./run.sh --solo-sce -t 120
```

### Dashboard no carga datos
```bash
# Verifica que exista la base de datos
ls -lh datos/datos_sce.db

# Si no existe, genera datos
./run.sh --solo-sce -t 120
```

## ⚡ Comandos Más Usados

```bash
# Lo más común - Ejecutar todo
./start.sh

# Generar más datos
./run.sh --solo-sce -t 300

# Re-entrenar modelo
./run.sh --solo-ml

# Ver dashboard
./dashboard.sh

# Ayuda
./run.sh --help
```

---

**¡Listo para experimentar! 🎉**
