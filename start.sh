#!/bin/bash

# Script de inicio para Render
echo "🚀 Iniciando Semillero Digital Dashboard..."

# Instalar dependencias si es necesario
pip install -r requirements.txt

# Iniciar la aplicación
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
