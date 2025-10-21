#!/bin/bash

# ============================================
# Script de Verificación Completa del Sistema
# ============================================
# Ejecuta: ./verificar_sistema.sh
# O desde Windows: ssh innovasic@192.168.0.180 "/home/innovasic/galpon/raspberry_backend/verificar_sistema.sh"

echo "🔍 ===== VERIFICACIÓN DEL SISTEMA IoT GALPÓN ====="
echo ""

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================
# 1. DETENER SERVICIOS
# ============================================
echo "🛑 [1/6] Deteniendo servicios systemd..."
sudo systemctl stop servidor_tcp.service
sudo systemctl stop fastapi_backend.service
echo -e "${GREEN}✅ Servicios detenidos${NC}"
echo ""

# ============================================
# 2. LIMPIAR PROCESOS DUPLICADOS
# ============================================
echo "🧹 [2/6] Limpiando procesos duplicados..."
pkill -f "Servidor.py" 2>/dev/null
pkill -f "uvicorn" 2>/dev/null
sleep 2
echo -e "${GREEN}✅ Procesos limpiados${NC}"
echo ""

# ============================================
# 3. REINICIAR SERVICIOS
# ============================================
echo "🚀 [3/6] Reiniciando servicios..."
sudo systemctl start servidor_tcp.service
sleep 3
sudo systemctl start fastapi_backend.service
sleep 8  # Dar tiempo para que FastAPI inicie completamente
echo -e "${GREEN}✅ Servicios reiniciados${NC}"
echo ""

# ============================================
# 4. VERIFICAR ESTADO DE SERVICIOS
# ============================================
echo "📊 [4/6] Verificando estado de servicios systemd..."
SERVIDOR_STATUS=$(sudo systemctl is-active servidor_tcp.service)
FASTAPI_STATUS=$(sudo systemctl is-active fastapi_backend.service)

if [ "$SERVIDOR_STATUS" == "active" ]; then
    echo -e "   ${GREEN}✅ servidor_tcp.service: $SERVIDOR_STATUS${NC}"
else
    echo -e "   ${RED}❌ servidor_tcp.service: $SERVIDOR_STATUS${NC}"
fi

if [ "$FASTAPI_STATUS" == "active" ]; then
    echo -e "   ${GREEN}✅ fastapi_backend.service: $FASTAPI_STATUS${NC}"
else
    echo -e "   ${RED}❌ fastapi_backend.service: $FASTAPI_STATUS${NC}"
fi
echo ""

# ============================================
# 5. VERIFICAR PROCESOS EN EJECUCIÓN
# ============================================
echo "🔍 [5/6] Verificando procesos en ejecución..."
SERVIDOR_PROC=$(ps aux | grep "Servidor.py" | grep -v grep | wc -l)
UVICORN_PROC=$(ps aux | grep "uvicorn main:app" | grep -v grep | wc -l)

echo "   📌 Procesos Servidor.py encontrados: $SERVIDOR_PROC"
echo "   📌 Procesos uvicorn encontrados: $UVICORN_PROC"

if [ "$SERVIDOR_PROC" -eq 1 ]; then
    echo -e "   ${GREEN}✅ Servidor TCP corriendo (1 instancia)${NC}"
elif [ "$SERVIDOR_PROC" -gt 1 ]; then
    echo -e "   ${YELLOW}⚠️  Múltiples instancias de Servidor.py ($SERVIDOR_PROC)${NC}"
else
    echo -e "   ${RED}❌ Servidor TCP no está corriendo${NC}"
fi

if [ "$UVICORN_PROC" -eq 1 ]; then
    echo -e "   ${GREEN}✅ FastAPI corriendo (1 instancia)${NC}"
elif [ "$UVICORN_PROC" -gt 1 ]; then
    echo -e "   ${YELLOW}⚠️  Múltiples instancias de uvicorn ($UVICORN_PROC)${NC}"
else
    echo -e "   ${RED}❌ FastAPI no está corriendo${NC}"
fi

# Mostrar detalles de procesos
echo ""
echo "   Detalles de procesos:"
ps aux | grep -E "Servidor.py|uvicorn main:app" | grep -v grep | awk '{print "   - " $11 " " $12 " " $13 " " $14 " " $15 " (PID: " $2 ")"}'
echo ""

# ============================================
# 6. PROBAR CONECTIVIDAD API
# ============================================
echo "🌐 [6/6] Probando conectividad de la API..."

# Esperar un poco más para asegurar que FastAPI esté listo
sleep 5

# Intentar varias veces antes de fallar
MAX_RETRIES=3
RETRY_COUNT=0
API_RESPONSE=""

while [ $RETRY_COUNT -lt $MAX_RETRIES ] && [ -z "$API_RESPONSE" ]; do
    API_RESPONSE=$(curl -s http://localhost:8000/status 2>/dev/null)
    if [ -z "$API_RESPONSE" ]; then
        RETRY_COUNT=$((RETRY_COUNT + 1))
        if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
            echo "   Intento $RETRY_COUNT fallido, reintentando..."
            sleep 3
        fi
    fi
done

if [ -n "$API_RESPONSE" ]; then
    echo -e "${GREEN}✅ API respondiendo correctamente${NC}"
    echo "   Respuesta: $API_RESPONSE"
else
    echo -e "${RED}❌ API no responde después de $MAX_RETRIES intentos${NC}"
    echo "   Intentando diagnóstico..."
    
    # Verificar si el puerto está en uso
    PORT_CHECK=$(sudo netstat -tlnp | grep ":8000" 2>/dev/null)
    if [ -n "$PORT_CHECK" ]; then
        echo "   Puerto 8000 en uso por:"
        echo "   $PORT_CHECK"
    else
        echo "   Puerto 8000 no está en uso"
    fi
fi
echo ""

# ============================================
# RESUMEN FINAL
# ============================================
echo "📋 ===== RESUMEN DE VERIFICACIÓN ====="
echo ""

ALL_OK=true

if [ "$SERVIDOR_STATUS" != "active" ]; then
    ALL_OK=false
fi

if [ "$FASTAPI_STATUS" != "active" ]; then
    ALL_OK=false
fi

if [ "$SERVIDOR_PROC" -ne 1 ]; then
    ALL_OK=false
fi

if [ "$UVICORN_PROC" -ne 1 ]; then
    ALL_OK=false
fi

if [ -z "$API_RESPONSE" ]; then
    ALL_OK=false
fi

if [ "$ALL_OK" = true ]; then
    echo -e "${GREEN}✅✅✅ SISTEMA COMPLETAMENTE FUNCIONAL ✅✅✅${NC}"
    echo ""
    echo "🌐 Dashboard puede conectarse a: http://192.168.0.180:8000"
    echo "📊 Datos almacenados en: /home/innovasic/galpon/raspberry_backend/galpon.db"
    echo "📁 Archivo Excel: /home/innovasic/galpon/AppIoTEsp8266-UCC-main/Servidor/data_test_14.xlsx"
else
    echo -e "${RED}❌ SISTEMA CON PROBLEMAS - Revisar logs arriba${NC}"
    echo ""
    echo "📝 Comandos útiles para diagnóstico:"
    echo "   - Ver logs TCP: sudo journalctl -u servidor_tcp.service -n 50"
    echo "   - Ver logs API: sudo journalctl -u fastapi_backend.service -n 50"
    echo "   - Procesos: ps aux | grep -E 'Servidor|uvicorn'"
fi

echo ""
echo "============================================"
