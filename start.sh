#!/bin/bash

# Script de Inicio Rápido - SCE Gemelo Digital
# Uso: ./start.sh [tiempo_simulacion]

TIEMPO=${1:-120}  # Default: 120 segundos

echo "🚀 Iniciando SCE Gemelo Digital..."
echo "⏱️  Tiempo de simulación: ${TIEMPO}s"
echo ""

# Ejecutar todo
./run.sh -t $TIEMPO
