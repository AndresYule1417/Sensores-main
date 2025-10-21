#!/bin/bash
# Script para limpiar y reiniciar servicios
# Fecha: 21 de octubre de 2025

echo "========================================="
echo "LIMPIEZA Y REINICIO DE SERVICIOS"
echo "========================================="
echo ""

# Matar todos los procesos uvicorn y Servidor.py
echo "[1/4] Deteniendo procesos duplicados..."
pkill -f uvicorn 2>/dev/null
pkill -f Servidor.py 2>/dev/null
sleep 2
echo "✓ Procesos antiguos detenidos"
echo ""

# Detener servicios systemd
echo "[2/4] Deteniendo servicios systemd..."
sudo systemctl stop fastapi_backend.service 2>/dev/null
sudo systemctl stop servidor_tcp.service 2>/dev/null
sleep 1
echo "✓ Servicios systemd detenidos"
echo ""

# Reiniciar servicios
echo "[3/4] Iniciando servicios..."
sudo systemctl start servidor_tcp.service
sleep 3
sudo systemctl start fastapi_backend.service
sleep 5
echo "✓ Servicios iniciados"
echo ""

# Verificar estado
echo "[4/4] Verificando estado..."
echo ""
echo "Estado de servicios:"
sudo systemctl is-active servidor_tcp.service fastapi_backend.service
echo ""

echo "Procesos corriendo:"
ps aux | grep -E 'Servidor.py|uvicorn' | grep -v grep
echo ""

echo "Prueba de API:"
curl http://localhost:8000/status
echo ""
echo ""

echo "========================================="
echo "✓ SERVICIOS REINICIADOS"
echo "========================================="
