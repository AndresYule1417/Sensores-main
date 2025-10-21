#!/bin/bash
# Script para configurar auto-inicio de servicios en Raspberry Pi
# Fecha: 21 de octubre de 2025

echo "========================================"
echo "CONFIGURANDO AUTO-INICIO DE SERVICIOS"
echo "========================================"
echo ""

# Colores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Crear directorio de logs si no existe
echo -e "${YELLOW}[1/6]${NC} Creando directorio de logs..."
mkdir -p /home/innovasic/galpon/logs
echo -e "${GREEN}✓${NC} Directorio de logs creado"
echo ""

# Detener servicios existentes si están corriendo
echo -e "${YELLOW}[2/6]${NC} Deteniendo servicios existentes..."
sudo systemctl stop fastapi_backend.service 2>/dev/null || true
sudo systemctl stop servidor_tcp.service 2>/dev/null || true
echo -e "${GREEN}✓${NC} Servicios detenidos"
echo ""

# Copiar archivos de servicio a systemd
echo -e "${YELLOW}[3/6]${NC} Instalando archivos de servicio systemd..."
sudo cp /home/innovasic/galpon/raspberry_backend/servidor_tcp.service /etc/systemd/system/
sudo cp /home/innovasic/galpon/raspberry_backend/fastapi_backend.service /etc/systemd/system/
sudo chmod 644 /etc/systemd/system/servidor_tcp.service
sudo chmod 644 /etc/systemd/system/fastapi_backend.service
echo -e "${GREEN}✓${NC} Archivos de servicio instalados"
echo ""

# Recargar systemd
echo -e "${YELLOW}[4/6]${NC} Recargando configuración systemd..."
sudo systemctl daemon-reload
echo -e "${GREEN}✓${NC} Configuración recargada"
echo ""

# Habilitar servicios para auto-inicio
echo -e "${YELLOW}[5/6]${NC} Habilitando auto-inicio de servicios..."
sudo systemctl enable servidor_tcp.service
sudo systemctl enable fastapi_backend.service
echo -e "${GREEN}✓${NC} Servicios habilitados para auto-inicio"
echo ""

# Iniciar servicios
echo -e "${YELLOW}[6/6]${NC} Iniciando servicios..."
sudo systemctl start servidor_tcp.service
sleep 3
sudo systemctl start fastapi_backend.service
sleep 3
echo -e "${GREEN}✓${NC} Servicios iniciados"
echo ""

# Verificar estado
echo "========================================"
echo "ESTADO DE LOS SERVICIOS"
echo "========================================"
echo ""

echo -e "${YELLOW}Servidor TCP (puerto 8889):${NC}"
sudo systemctl status servidor_tcp.service --no-pager -l | head -n 15
echo ""

echo -e "${YELLOW}FastAPI Backend (puerto 8000):${NC}"
sudo systemctl status fastapi_backend.service --no-pager -l | head -n 15
echo ""

echo "========================================"
echo "COMANDOS ÚTILES"
echo "========================================"
echo ""
echo "Ver logs en tiempo real:"
echo "  sudo journalctl -u servidor_tcp.service -f"
echo "  sudo journalctl -u fastapi_backend.service -f"
echo ""
echo "Detener servicios:"
echo "  sudo systemctl stop servidor_tcp.service"
echo "  sudo systemctl stop fastapi_backend.service"
echo ""
echo "Reiniciar servicios:"
echo "  sudo systemctl restart servidor_tcp.service"
echo "  sudo systemctl restart fastapi_backend.service"
echo ""
echo "Deshabilitar auto-inicio:"
echo "  sudo systemctl disable servidor_tcp.service"
echo "  sudo systemctl disable fastapi_backend.service"
echo ""
echo -e "${GREEN}✓ Configuración completada!${NC}"
echo "Los servicios se iniciarán automáticamente al reiniciar la Raspberry Pi"
