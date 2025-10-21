#!/bin/bash
# Script para instalar todas las dependencias del backend en Raspberry Pi

echo "========================================"
echo "  INSTALACION DE DEPENDENCIAS"
echo "========================================"

# Verificar que estamos en el directorio correcto
if [ ! -f "main.py" ]; then
    echo "❌ Error: No se encuentra main.py"
    echo "   Ejecuta este script desde: ~/galpon/raspberry_backend/"
    exit 1
fi

echo ""
echo "[1/4] Activando entorno virtual..."
source venv/bin/activate
echo "      ✅ Entorno activado"

echo ""
echo "[2/4] Instalando FastAPI y Uvicorn..."
pip install fastapi uvicorn
echo "      ✅ FastAPI instalado"

echo ""
echo "[3/4] Instalando SQLAlchemy..."
pip install sqlalchemy
echo "      ✅ SQLAlchemy instalado"

echo ""
echo "[4/4] Instalando pandas y openpyxl (para importar Excel)..."
pip install pandas openpyxl xlrd
echo "      ✅ pandas y openpyxl instalados"

echo ""
echo "========================================"
echo "  ✅ INSTALACION COMPLETA"
echo "========================================"
echo ""
echo "Ahora puedes:"
echo "1. Importar datos: python3 import_excel_to_sqlite.py"
echo "2. Iniciar API:    python3 main.py"
echo ""
