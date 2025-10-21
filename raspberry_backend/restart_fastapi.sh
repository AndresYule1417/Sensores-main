#!/bin/bash
# Script para detener FastAPI, reinicializar la base de datos e iniciar nuevamente

echo "=========================================="
echo "  REINICIO COMPLETO DE FASTAPI"
echo "=========================================="

cd /home/innovasic/galpon/raspberry_backend

echo ""
echo "[1/4] Deteniendo FastAPI..."
pkill -f "python3 main.py" 2>/dev/null || echo "      (No estaba corriendo)"
sleep 2
echo "      ✅ Detenido"

echo ""
echo "[2/4] Activando entorno virtual..."
source venv/bin/activate
echo "      ✅ Activado"

echo ""
echo "[3/4] Inicializando base de datos..."
python3 init_database.py <<EOF
s
EOF
echo "      ✅ Base de datos creada"

echo ""
echo "[4/4] Iniciando FastAPI en segundo plano..."
nohup python3 main.py > logs_api.log 2>&1 &
FASTAPI_PID=$!
sleep 3

# Verificar que está corriendo
if ps -p $FASTAPI_PID > /dev/null; then
    echo "      ✅ FastAPI iniciado (PID: $FASTAPI_PID)"
    echo ""
    echo "=========================================="
    echo "  ✅ FASTAPI CORRIENDO"
    echo "=========================================="
    echo ""
    echo "URL: http://192.168.0.180:8000"
    echo "Docs: http://192.168.0.180:8000/docs"
    echo ""
    echo "Ver logs: tail -f ~/galpon/raspberry_backend/logs_api.log"
    echo "Detener: pkill -f 'python3 main.py'"
else
    echo "      ❌ Error al iniciar FastAPI"
    echo ""
    echo "Ver errores:"
    tail -20 logs_api.log
fi
