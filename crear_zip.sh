#!/bin/bash

echo "════════════════════════════════════════════════════════════"
echo "  📦 Empaquetando SCE Gemelo Digital 3D"
echo "════════════════════════════════════════════════════════════"
echo ""

# Nombre del archivo ZIP
ZIP_NAME="evaluacion3_sce_v3.0.zip"
TEMP_DIR="evaluacion3_sce"

# Limpiar archivos temporales y caché
echo "🧹 Limpiando archivos temporales..."

# Eliminar caché de Python
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null

# Eliminar caché de Streamlit
rm -rf ~/.streamlit/cache 2>/dev/null
rm -rf .streamlit/cache 2>/dev/null

# Eliminar archivos de sistema
find . -type f -name ".DS_Store" -delete 2>/dev/null
find . -type f -name "Thumbs.db" -delete 2>/dev/null

echo "   ✅ Archivos temporales eliminados"
echo ""

# Crear estructura temporal
echo "📁 Preparando estructura de archivos..."

# Archivos y carpetas a incluir
INCLUDE_FILES=(
    "dashboard/"
    "simuladores/"
    "sce/"
    "ml/"
    "datos/"
    "requirements.txt"
    "README.md"
    "README_INSTALACION.md"
    "OPTIMIZACIONES_REALIZADAS.md"
    "OPTIMIZACIONES_ANTI_FLICKERING.md"
    "ERROR_CORREGIDO.md"
    "SOLUCION_PROBLEMAS.md"
    "MEJORA_PERSISTENCIA_3D.md"
    "DASHBOARD_3D_GUIA.md"
    "instalar.sh"
    "iniciar_dashboard.sh"
    "reiniciar_dashboard.sh"
    "dashboard_3d.sh"
    "run.sh"
)

# Crear lista de exclusiones
EXCLUDE_PATTERNS=(
    "__pycache__"
    "*.pyc"
    "*.pyo"
    ".DS_Store"
    "Thumbs.db"
    ".git"
    ".gitignore"
    "venv"
    "*.zip"
    ".streamlit/cache"
    "*.log"
)

echo "   ✅ Estructura preparada"
echo ""

# Crear archivo ZIP
echo "🗜️  Creando archivo ZIP..."
echo "   Archivo: $ZIP_NAME"
echo ""

# Construir comando de exclusión
EXCLUDE_CMD=""
for pattern in "${EXCLUDE_PATTERNS[@]}"; do
    EXCLUDE_CMD="$EXCLUDE_CMD -x \"*/$pattern/*\" -x \"*/$pattern\""
done

# Crear ZIP excluyendo archivos innecesarios
zip -r "$ZIP_NAME" . \
    -x "*/venv/*" \
    -x "*/__pycache__/*" \
    -x "*.pyc" \
    -x "*.pyo" \
    -x "*/.DS_Store" \
    -x "*/Thumbs.db" \
    -x "*/.git/*" \
    -x "*.zip" \
    -x "*/.streamlit/cache/*" \
    -x "*.log" \
    -x "./crear_zip.sh" \
    -q

if [ $? -eq 0 ]; then
    echo "   ✅ ZIP creado exitosamente"
else
    echo "   ❌ ERROR: Falló la creación del ZIP"
    exit 1
fi
echo ""

# Mostrar información del archivo
echo "📊 Información del archivo:"
ls -lh "$ZIP_NAME" | awk '{print "   Tamaño: " $5}'
echo "   Ubicación: $(pwd)/$ZIP_NAME"
echo ""

# Verificar contenido
echo "📝 Verificando contenido..."
NUM_FILES=$(unzip -l "$ZIP_NAME" | tail -1 | awk '{print $2}')
echo "   Archivos incluidos: $NUM_FILES"
echo ""

echo "════════════════════════════════════════════════════════════"
echo "  ✅ ¡Empaquetado completado!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📦 Archivo creado: $ZIP_NAME"
echo ""
echo "📝 Contenido incluido:"
echo "  ✅ Código fuente (dashboard, simuladores, sce, ml)"
echo "  ✅ Base de datos SQLite"
echo "  ✅ Modelo ML entrenado"
echo "  ✅ Scripts de instalación y ejecución"
echo "  ✅ Documentación completa"
echo "  ✅ Archivo requirements.txt"
echo ""
echo "❌ Excluido:"
echo "  • Entorno virtual (venv)"
echo "  • Caché de Python (__pycache__)"
echo "  • Archivos temporales"
echo ""
echo "🚀 Para usar el paquete:"
echo "  1. Descomprimir: unzip $ZIP_NAME"
echo "  2. Instalar: ./instalar.sh"
echo "  3. Ejecutar: ./iniciar_dashboard.sh"
echo ""
echo "════════════════════════════════════════════════════════════"
