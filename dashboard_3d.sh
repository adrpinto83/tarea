#!/bin/bash

###############################################################################
# Script de Lanzamiento - Dashboard 3D Interactivo
# Sistema: SCE Gemelo Digital
# Descripción: Inicia el dashboard 3D con simulación en tiempo real
###############################################################################

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Banner
echo -e "${BLUE}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║      🌊 SCE GEMELO DIGITAL - DASHBOARD 3D INTERACTIVO 🌊     ║
║                                                               ║
║            Sistema de Monitoreo Avanzado                      ║
║         con Simulación en Tiempo Real                         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Verificar entorno virtual
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Entorno virtual no encontrado${NC}"
    echo -e "${YELLOW}   Ejecute primero: bash setup_proyecto.sh${NC}"
    exit 1
fi

# Activar entorno virtual
echo -e "${GREEN}🔧 Activando entorno virtual...${NC}"
source venv/bin/activate

# Verificar instalación de streamlit
if ! command -v streamlit &> /dev/null; then
    echo -e "${YELLOW}⚠️  Streamlit no encontrado. Instalando...${NC}"
    pip install streamlit plotly > /dev/null 2>&1
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ Lanzando Dashboard 3D Interactivo...${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${BLUE}📊 Características:${NC}"
echo -e "   ${GREEN}✓${NC} Visualización 3D del tanque en tiempo real"
echo -e "   ${GREEN}✓${NC} Controles interactivos (sliders)"
echo -e "   ${GREEN}✓${NC} Simulación física en vivo"
echo -e "   ${GREEN}✓${NC} Modificación de parámetros en tiempo real"
echo -e "   ${GREEN}✓${NC} Gráficas animadas"
echo ""
echo -e "${BLUE}🎮 Modos disponibles:${NC}"
echo -e "   1. ${GREEN}Visualización${NC} - Ver datos históricos"
echo -e "   2. ${GREEN}Simulación Interactiva${NC} - Controlar el sistema en vivo"
echo ""
echo -e "${YELLOW}💡 El navegador se abrirá automáticamente en:${NC}"
echo -e "   ${GREEN}http://localhost:8501${NC}"
echo ""
echo -e "${YELLOW}⌨️  Presione Ctrl+C para detener el dashboard${NC}"
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo ""

# Lanzar dashboard
streamlit run dashboard/dashboard_3d_interactivo.py \
    --server.port 8501 \
    --server.headless true \
    --browser.gatherUsageStats false \
    --theme.primaryColor "#1f77b4" \
    --theme.backgroundColor "#ffffff"
