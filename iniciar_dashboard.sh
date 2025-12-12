#!/bin/bash

echo "════════════════════════════════════════════════════════════"
echo "  🌊 SCE Gemelo Digital 3D"
echo "════════════════════════════════════════════════════════════"
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo "❌ ERROR: Entorno virtual no encontrado"
    echo ""
    echo "Por favor ejecuta primero:"
    echo "  ./instalar.sh"
    echo ""
    exit 1
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Verificar que streamlit esté instalado
if ! python -c "import streamlit" 2>/dev/null; then
    echo "❌ ERROR: Streamlit no está instalado"
    echo ""
    echo "Por favor ejecuta:"
    echo "  ./instalar.sh"
    echo ""
    exit 1
fi

echo "✅ Entorno virtual activado"
echo ""

# Verificar archivo del dashboard
if [ ! -f "dashboard/dashboard_3d_interactivo.py" ]; then
    echo "❌ ERROR: Dashboard no encontrado"
    echo "   Archivo faltante: dashboard/dashboard_3d_interactivo.py"
    exit 1
fi

echo "🚀 Iniciando Dashboard 3D Interactivo..."
echo ""
echo "════════════════════════════════════════════════════════════"
echo "  📱 La aplicación se abrirá en tu navegador"
echo "  🌐 URL: http://localhost:8501"
echo ""
echo "  ⚠️  Si no se abre automáticamente, copia la URL de arriba"
echo ""
echo "  Para detener: Presiona Ctrl+C"
echo "════════════════════════════════════════════════════════════"
echo ""

# Ejecutar streamlit
streamlit run dashboard/dashboard_3d_interactivo.py
