#!/bin/bash

# Script para mostrar comandos principales
# Ejecutar: ./comandos_principales.sh

cat << 'EOF'
╔════════════════════════════════════════════════════════════════╗
║       🐓 COMANDOS PRINCIPALES - GALPÓN IoT RASPBERRY PI       ║
╚════════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────────┐
│ 🔍 VERIFICAR TODO EL SISTEMA (Recomendado)                     │
└─────────────────────────────────────────────────────────────────┘
  ~/galpon/raspberry_backend/verificar_sistema.sh

┌─────────────────────────────────────────────────────────────────┐
│ 🔄 REINICIAR SERVICIOS                                         │
└─────────────────────────────────────────────────────────────────┘
  sudo systemctl restart servidor_tcp.service fastapi_backend.service

┌─────────────────────────────────────────────────────────────────┐
│ 📊 VER ESTADO DE SERVICIOS                                     │
└─────────────────────────────────────────────────────────────────┘
  sudo systemctl status servidor_tcp.service fastapi_backend.service

┌─────────────────────────────────────────────────────────────────┐
│ 📝 VER LOGS EN TIEMPO REAL                                     │
└─────────────────────────────────────────────────────────────────┘
  # Servidor TCP:
  sudo journalctl -u servidor_tcp.service -f -n 50

  # FastAPI:
  sudo journalctl -u fastapi_backend.service -f -n 50

  (Presiona Ctrl+C para salir)

┌─────────────────────────────────────────────────────────────────┐
│ 🌐 PROBAR API                                                  │
└─────────────────────────────────────────────────────────────────┘
  curl http://localhost:8000/status
  curl http://localhost:8000/sensores/ultimos?limit=5

┌─────────────────────────────────────────────────────────────────┐
│ 🗄️  CONSULTAR BASE DE DATOS                                    │
└─────────────────────────────────────────────────────────────────┘
  # Contar registros:
  sqlite3 /home/innovasic/galpon/data/galpon.db "SELECT COUNT(*) FROM sensores"

  # Ver últimos 5:
  sqlite3 /home/innovasic/galpon/data/galpon.db "SELECT * FROM sensores ORDER BY id DESC LIMIT 5"

┌─────────────────────────────────────────────────────────────────┐
│ 🔍 VER PROCESOS ACTIVOS                                        │
└─────────────────────────────────────────────────────────────────┘
  ps aux | grep -E 'Servidor|uvicorn' | grep -v grep

┌─────────────────────────────────────────────────────────────────┐
│ 🌐 VER CONEXIONES ESP8266                                      │
└─────────────────────────────────────────────────────────────────┘
  sudo netstat -anp | grep 8889 | grep ESTABLISHED

┌─────────────────────────────────────────────────────────────────┐
│ 🧹 LIMPIEZA COMPLETA (Si hay problemas)                       │
└─────────────────────────────────────────────────────────────────┘
  sudo systemctl stop servidor_tcp.service fastapi_backend.service
  sudo pkill -f Servidor.py
  sudo pkill -f uvicorn
  sleep 3
  sudo systemctl start servidor_tcp.service fastapi_backend.service

┌─────────────────────────────────────────────────────────────────┐
│ 📖 VER GUÍA COMPLETA                                           │
└─────────────────────────────────────────────────────────────────┘
  cat ~/galpon/GUIA_RASPBERRY_PI.md
  # O abrir en editor:
  nano ~/galpon/GUIA_RASPBERRY_PI.md

╔════════════════════════════════════════════════════════════════╗
║  📂 ARCHIVOS IMPORTANTES                                       ║
╠════════════════════════════════════════════════════════════════╣
║  📊 Base de datos: /home/innovasic/galpon/data/galpon.db      ║
║  📁 Excel: ~/galpon/AppIoTEsp8266-UCC-main/Servidor/          ║
║         data_test_14.xlsx                                      ║
║  ⚙️  Servicios: /etc/systemd/system/servidor_tcp.service     ║
║              /etc/systemd/system/fastapi_backend.service      ║
╚════════════════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════════════════╗
║  🌐 ACCESO DESDE OTROS DISPOSITIVOS                           ║
╠════════════════════════════════════════════════════════════════╣
║  API Docs:   http://192.168.0.180:8000/docs                   ║
║  API Status: http://192.168.0.180:8000/status                 ║
║  Dashboard:  http://localhost:8501 (desde Windows)            ║
╚════════════════════════════════════════════════════════════════╝

✅ Sistema configurado con AUTO-INICIO
   Los servicios se inician automáticamente al encender la Raspberry Pi

EOF
