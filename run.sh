#!/bin/bash

# Script de Ejecución Automática - SCE Gemelo Digital
# Autor: Equipo Torres, Pinto, Cova
# Universidad de Oriente

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Banner
clear
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                                                              ║"
echo "║        🌊  SCE GEMELO DIGITAL - SISTEMA AUTOMÁTICO  🌊       ║"
echo "║                                                              ║"
echo "║              Sistema de Monitoreo de Nivel                  ║"
echo "║          Universidad de Oriente - Núcleo Anzoátegui         ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Función para verificar si el entorno virtual existe
verificar_venv() {
    if [ ! -d "venv" ]; then
        echo -e "${RED}❌ Error: Entorno virtual no encontrado${NC}"
        echo -e "${YELLOW}💡 Ejecute primero: bash setup_proyecto.sh${NC}"
        exit 1
    fi
}

# Función para activar entorno virtual
activar_venv() {
    echo -e "${BLUE}🔧 Activando entorno virtual...${NC}"
    source venv/bin/activate
    echo -e "${GREEN}✓ Entorno virtual activado${NC}"
    echo ""
}

# Función para ejecutar el SCE
ejecutar_sce() {
    local duracion=$1
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  PASO 1: EJECUTANDO GEMELO DIGITAL DEL SCE${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}⏱️  Duración de simulación: ${duracion} segundos${NC}"
    echo ""

    python sce/sce_gemelo_digital.py -t $duracion

    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ SCE ejecutado exitosamente${NC}"
        echo -e "${GREEN}📊 Datos guardados en: datos/datos_sce.db${NC}"
    else
        echo -e "${RED}❌ Error al ejecutar el SCE${NC}"
        exit 1
    fi
}

# Función para entrenar ML
entrenar_ml() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  PASO 2: ENTRENANDO MODELO DE MACHINE LEARNING${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo ""

    python ml/ml_prediccion.py

    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ Modelo ML entrenado exitosamente${NC}"
        echo -e "${GREEN}💾 Modelo guardado en: ml/modelo_rf.pkl${NC}"
        echo -e "${GREEN}📈 Gráficas guardadas en: resultados/${NC}"
    else
        echo -e "${RED}❌ Error al entrenar el modelo ML${NC}"
        exit 1
    fi
}

# Función para lanzar dashboard
lanzar_dashboard() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  PASO 3: LANZANDO DASHBOARD WEB INTERACTIVO${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${YELLOW}🌐 Dashboard iniciándose...${NC}"
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ⚠️  IMPORTANTE: Abre tu NAVEGADOR WEB                   ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${YELLOW}📍 URL del Dashboard:${NC}"
    echo -e "   ${GREEN}http://localhost:8501${NC}"
    echo ""
    echo -e "${YELLOW}🎯 Lo que verás en el navegador:${NC}"
    echo "   ✅ Mensaje personalizado en español"
    echo "   ✅ Firmas: Torres, Pinto, Cova"
    echo "   ✅ Información de la UDO"
    echo "   ✅ Gráficas interactivas en tiempo real"
    echo "   ✅ KPIs y estadísticas"
    echo ""
    echo -e "${BLUE}ℹ️  Lo que ves AQUÍ (terminal) es solo el servidor.${NC}"
    echo -e "${BLUE}   El contenido COMPLETO está en el NAVEGADOR WEB.${NC}"
    echo ""
    echo -e "${GREEN}Presione Ctrl+C para detener el servidor${NC}"
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo ""

    streamlit run dashboard/dashboard_3d_interactivo.py
}

# Función para mostrar ayuda
mostrar_ayuda() {
    echo "Uso: $0 [opciones]"
    echo ""
    echo "Opciones:"
    echo "  -t, --tiempo SEGUNDOS    Duración de la simulación (default: 120)"
    echo "  --solo-sce               Solo ejecutar el SCE"
    echo "  --solo-ml                Solo entrenar ML (requiere datos previos)"
    echo "  --solo-dashboard         Solo lanzar dashboard (requiere datos previos)"
    echo "  -h, --help               Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0                       # Ejecutar todo con 120s de simulación"
    echo "  $0 -t 300                # Ejecutar todo con 300s de simulación"
    echo "  $0 --solo-dashboard      # Solo mostrar dashboard"
    echo ""
}

# Función para mostrar resumen final
mostrar_resumen() {
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✅ EJECUCIÓN COMPLETADA EXITOSAMENTE${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BLUE}📁 Archivos generados:${NC}"
    echo "   • datos/datos_sce.db           - Base de datos SQLite"
    echo "   • ml/modelo_rf.pkl              - Modelo Random Forest"
    echo "   • resultados/prediccion_ml.png  - Gráfica de predicciones"
    echo "   • resultados/importancia_features.png - Importancia de features"
    echo ""
    echo -e "${BLUE}🚀 Próximos pasos:${NC}"
    echo "   • El dashboard se abrirá automáticamente"
    echo "   • Puedes re-ejecutar: $0 --solo-dashboard"
    echo ""
}

# ==================== MAIN ====================

# Valores por defecto
DURACION=120
MODO="completo"

# Parsear argumentos
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--tiempo)
            DURACION="$2"
            shift 2
            ;;
        --solo-sce)
            MODO="solo-sce"
            shift
            ;;
        --solo-ml)
            MODO="solo-ml"
            shift
            ;;
        --solo-dashboard)
            MODO="solo-dashboard"
            shift
            ;;
        -h|--help)
            mostrar_ayuda
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Opción desconocida: $1${NC}"
            mostrar_ayuda
            exit 1
            ;;
    esac
done

# Verificar entorno virtual
verificar_venv

# Activar entorno virtual
activar_venv

# Ejecutar según modo
case $MODO in
    completo)
        ejecutar_sce $DURACION
        entrenar_ml
        mostrar_resumen
        lanzar_dashboard
        ;;
    solo-sce)
        ejecutar_sce $DURACION
        echo -e "${GREEN}✅ SCE ejecutado. Para entrenar ML: $0 --solo-ml${NC}"
        ;;
    solo-ml)
        if [ ! -f "datos/datos_sce.db" ]; then
            echo -e "${RED}❌ Error: No hay datos. Ejecute primero: $0 --solo-sce${NC}"
            exit 1
        fi
        entrenar_ml
        echo -e "${GREEN}✅ ML entrenado. Para ver dashboard: $0 --solo-dashboard${NC}"
        ;;
    solo-dashboard)
        if [ ! -f "datos/datos_sce.db" ]; then
            echo -e "${RED}❌ Error: No hay datos. Ejecute primero: $0 --solo-sce${NC}"
            exit 1
        fi
        lanzar_dashboard
        ;;
esac
