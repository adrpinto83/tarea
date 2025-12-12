#!/bin/bash

# Script para solo lanzar el Dashboard
echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║          🌐 LANZANDO DASHBOARD WEB INTERACTIVO                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "⚠️  IMPORTANTE: Abre tu NAVEGADOR WEB"
echo ""
echo "📍 Ve a esta URL en tu navegador:"
echo "   http://localhost:8501"
echo ""
echo "🎯 Allí verás:"
echo "   ✅ Mensaje personalizado en español"
echo "   ✅ Firmas de los participantes (Torres, Pinto, Cova)"
echo "   ✅ Información de la Universidad de Oriente"
echo "   ✅ Gráficas interactivas del sistema"
echo "   ✅ KPIs y estadísticas en tiempo real"
echo ""
echo "ℹ️  La terminal solo muestra el servidor ejecutándose."
echo "   El contenido COMPLETO se ve en el NAVEGADOR WEB."
echo ""
echo "Presione Ctrl+C para detener el servidor"
echo ""
echo "══════════════════════════════════════════════════════════════════"
echo ""

source venv/bin/activate
streamlit run dashboard/dashboard_streamlit.py
