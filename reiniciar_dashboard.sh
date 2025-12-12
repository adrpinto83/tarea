#!/bin/bash

echo "🔄 Reiniciando Dashboard 3D Interactivo..."

# Matar procesos de streamlit anteriores
echo "1. Deteniendo procesos anteriores de Streamlit..."
pkill -f "streamlit run dashboard/dashboard_3d_interactivo.py" 2>/dev/null
pkill -f "streamlit" 2>/dev/null
sleep 2

# Limpiar caché de Streamlit
echo "2. Limpiando caché de Streamlit..."
rm -rf ~/.streamlit/cache 2>/dev/null
rm -rf .streamlit/cache 2>/dev/null

# Activar entorno virtual
echo "3. Activando entorno virtual..."
source venv/bin/activate

# Ejecutar dashboard
echo "4. Iniciando dashboard optimizado..."
echo ""
echo "✅ Dashboard iniciándose en http://localhost:8501"
echo ""
echo "⚠️  IMPORTANTE: En tu navegador:"
echo "   1. Presiona Ctrl+Shift+R (o Cmd+Shift+R en Mac) para hard refresh"
echo "   2. O abre una ventana de incógnito"
echo ""
echo "Para detener: Presiona Ctrl+C"
echo "═══════════════════════════════════════════════════════════"
echo ""

streamlit run dashboard/dashboard_3d_interactivo.py
