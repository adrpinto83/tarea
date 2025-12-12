#!/bin/bash

echo "════════════════════════════════════════════════════════════"
echo "  🌊 SCE Gemelo Digital 3D - Script de Instalación"
echo "════════════════════════════════════════════════════════════"
echo ""

# Verificar Python
echo "1️⃣  Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ ERROR: Python no encontrado"
    echo "   Por favor instala Python 3.8 o superior"
    echo "   Descargar desde: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | awk '{print $2}')
echo "   ✅ Python encontrado: $PYTHON_VERSION"
echo ""

# Verificar versión de Python
PYTHON_MAJOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$($PYTHON_CMD -c "import sys; print(sys.version_info.minor)")

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo "❌ ERROR: Python 3.8 o superior requerido"
    echo "   Tu versión: $PYTHON_VERSION"
    exit 1
fi

# Crear entorno virtual
echo "2️⃣  Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "   ⚠️  Entorno virtual ya existe"
    read -p "   ¿Deseas recrearlo? (s/N): " respuesta
    if [ "$respuesta" = "s" ] || [ "$respuesta" = "S" ]; then
        rm -rf venv
        $PYTHON_CMD -m venv venv
        echo "   ✅ Entorno virtual recreado"
    else
        echo "   ℹ️  Usando entorno virtual existente"
    fi
else
    $PYTHON_CMD -m venv venv
    echo "   ✅ Entorno virtual creado"
fi
echo ""

# Activar entorno virtual
echo "3️⃣  Activando entorno virtual..."
source venv/bin/activate
echo "   ✅ Entorno virtual activado"
echo ""

# Actualizar pip
echo "4️⃣  Actualizando pip..."
pip install --upgrade pip --quiet
echo "   ✅ pip actualizado"
echo ""

# Instalar dependencias
echo "5️⃣  Instalando dependencias..."
echo "   Esto puede tomar varios minutos..."
pip install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo "   ✅ Dependencias instaladas correctamente"
else
    echo "   ❌ ERROR: Falló la instalación de dependencias"
    echo "   Intenta ejecutar manualmente: pip install -r requirements.txt"
    exit 1
fi
echo ""

# Verificar instalación
echo "6️⃣  Verificando instalación..."
$PYTHON_CMD -c "import streamlit; import plotly; import numpy; import pandas" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "   ✅ Todas las dependencias verificadas"
else
    echo "   ⚠️  Algunas dependencias podrían no estar instaladas correctamente"
fi
echo ""

# Dar permisos a scripts
echo "7️⃣  Configurando scripts..."
chmod +x *.sh 2>/dev/null
echo "   ✅ Permisos de ejecución configurados"
echo ""

# Verificar base de datos
if [ ! -f "datos/datos_sce.db" ]; then
    echo "   ℹ️  Base de datos no encontrada (se creará automáticamente)"
fi
echo ""

echo "════════════════════════════════════════════════════════════"
echo "  ✅ ¡Instalación completada exitosamente!"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📝 Próximos pasos:"
echo ""
echo "  1. Ejecutar la aplicación:"
echo "     ./iniciar_dashboard.sh"
echo ""
echo "  2. La aplicación se abrirá en:"
echo "     http://localhost:8501"
echo ""
echo "  3. Si tienes problemas:"
echo "     ./reiniciar_dashboard.sh"
echo ""
echo "📚 Documentación:"
echo "  - README.md - Guía completa"
echo "  - README_INSTALACION.md - Instalación rápida"
echo "  - SOLUCION_PROBLEMAS.md - Troubleshooting"
echo ""
echo "════════════════════════════════════════════════════════════"
