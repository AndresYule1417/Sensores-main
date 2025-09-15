# 🤖 PROMPT PARA IA - IMPLEMENTACIÓN RASPBERRY PI
**Para: innovasicrasp en GitHub**  
**Proyecto: Sistema de Monitoreo Galpón Avícola - Universidad Cooperativa de Colombia**

---

## 🎯 CONTEXTO DEL PROYECTO

Eres una IA que debe ayudar a **innovasicrasp** a implementar un sistema de monitoreo de galpón avícola en una **Raspberry Pi 4B**. El proyecto ya tiene código funcional que debe ser adaptado para funcionar localmente en Raspberry Pi con acceso público.

### 📋 ARQUITECTURA OBJETIVO:
```
ESP32 Sensores → Raspberry Pi (PostgreSQL + FastAPI) → Dashboard Web Público
                        ↓
                   Streamlit Dashboard + Autenticación @campusucc.edu.co
                        ↓
                   Acceso Público (Cloudflare Tunnel o Vercel)
```

### 🏛️ INFORMACIÓN INSTITUCIONAL:
- **Universidad:** Universidad Cooperativa de Colombia
- **Campus:** Neiva
- **Email autorizado:** Solo @campusucc.edu.co
- **Proyecto:** Monitoreo ambiental para galpón avícola

---

## 📁 ARCHIVOS DISPONIBLES EN EL REPOSITORIO

### ✅ Archivos Base (Código Existente - REUTILIZAR):
- `streamlit_app.py` - Dashboard original funcional
- `main.py` - API FastAPI original funcional  
- `min_tabla.py` - Tablas con sparklines (mantener sin cambios)
- `styles.css` - Estilos CSS personalizados (mantener sin cambios)

### 🆕 Archivos Adaptados para Raspberry Pi:
- `streamlit_app_raspberry.py` - Dashboard con autenticación @campusucc.edu.co
- `main_raspberry.py` - API adaptada para PostgreSQL local
- `POSTGRESQL_RASPBERRY.md` - Guía de configuración de base de datos
- `ACCESO_PUBLICO_GRATUITO.md` - Opciones de túneles gratuitos
- `INSTALACION_COMPLETA_RASPBERRY.md` - Manual paso a paso
- `ARQUITECTURA_SIMPLIFICADA.md` - Documentación técnica

---

## 🎯 TAREAS ESPECÍFICAS PARA INNOVASICRASP

### 🗄️ FASE 1: Configuración de PostgreSQL (30 min)

**INSTRUCCIONES PRECISAS:**

1. **Actualizar Raspberry Pi:**
   ```bash
   sudo apt update && sudo apt upgrade -y
   sudo reboot
   ```

2. **Instalar PostgreSQL:**
   ```bash
   sudo apt install -y postgresql postgresql-contrib python3-pip python3-venv
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```

3. **Configurar Base de Datos (EXACTAMENTE COMO SE MUESTRA):**
   ```bash
   sudo -u postgres psql
   
   # Ejecutar en psql:
   CREATE DATABASE galpon_db;
   CREATE USER galpon_user WITH PASSWORD 'UCC2024_Galpon!';
   GRANT ALL PRIVILEGES ON DATABASE galpon_db TO galpon_user;
   ALTER USER galpon_user CREATEDB;
   \q
   ```

4. **Crear Tabla de Sensores:**
   ```bash
   psql -h localhost -U galpon_user -d galpon_db
   
   # Ejecutar en psql:
   CREATE TABLE sensors3 (
       id SERIAL PRIMARY KEY,
       device VARCHAR(50) NOT NULL,
       lux FLOAT NOT NULL,
       nh3 FLOAT NOT NULL,
       hs FLOAT NOT NULL,
       h FLOAT NOT NULL,
       t FLOAT NOT NULL,
       time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       ip VARCHAR(45)
   );
   
   CREATE INDEX idx_sensors3_device ON sensors3(device);
   CREATE INDEX idx_sensors3_time ON sensors3(time DESC);
   \q
   ```

### 🐍 FASE 2: Configuración del Proyecto Python (15 min)

**INSTRUCCIONES EXACTAS:**

1. **Crear Directorio del Proyecto:**
   ```bash
   mkdir -p /home/pi/galpon
   cd /home/pi/galpon
   ```

2. **Clonar Repositorio:**
   ```bash
   git clone https://github.com/AndresYule1417/Sensores-main.git .
   ```

3. **Crear Entorno Virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Instalar Dependencias:**
   ```bash
   pip install streamlit==1.31.0 fastapi==0.104.1 uvicorn[standard]==0.24.0
   pip install pandas==2.1.4 plotly==5.17.0 sqlalchemy==2.0.23 psycopg2-binary==2.9.9
   pip install python-multipart==0.0.6 pydantic==2.5.2 python-dotenv==1.0.0
   ```

5. **Crear Archivo .env:**
   ```bash
   cat > .env << 'EOF'
   DB_USER=galpon_user
   DB_PASSWORD=UCC2024_Galpon!
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=galpon_db
   DATABASE_URL=postgresql://galpon_user:UCC2024_Galpon!@localhost:5432/galpon_db
   EOF
   ```

### 🚀 FASE 3: Configuración de Servicios (20 min)

**CREAR SERVICIOS SYSTEMD EXACTAMENTE ASÍ:**

1. **Servicio FastAPI:**
   ```bash
   sudo nano /etc/systemd/system/galpon-api.service
   
   # Copiar EXACTAMENTE:
   [Unit]
   Description=Galpon Avicola FastAPI
   After=postgresql.service network.target
   
   [Service]
   Type=simple
   User=pi
   WorkingDirectory=/home/pi/galpon
   Environment=PATH=/home/pi/galpon/venv/bin
   ExecStart=/home/pi/galpon/venv/bin/python -m uvicorn main_raspberry:app --host 0.0.0.0 --port 8000
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

2. **Servicio Streamlit:**
   ```bash
   sudo nano /etc/systemd/system/galpon-dashboard.service
   
   # Copiar EXACTAMENTE:
   [Unit]
   Description=Galpon Avicola Dashboard
   After=galpon-api.service
   
   [Service]
   Type=simple
   User=pi
   WorkingDirectory=/home/pi/galpon
   Environment=PATH=/home/pi/galpon/venv/bin
   ExecStart=/home/pi/galpon/venv/bin/python -m streamlit run streamlit_app_raspberry.py --server.port 8501 --server.address 0.0.0.0
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

3. **Habilitar Servicios:**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable galpon-api galpon-dashboard
   sudo systemctl start galpon-api galpon-dashboard
   ```

### 🌐 FASE 4: Acceso Público (Elegir UNA opción)

**OPCIÓN A: Cloudflare Tunnel (GRATIS PERMANENTE - RECOMENDADO)**

1. **Instalar Cloudflared:**
   ```bash
   wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
   sudo dpkg -i cloudflared-linux-arm64.deb
   ```

2. **Configurar Túnel:**
   ```bash
   cloudflared tunnel login  # Seguir instrucciones en pantalla
   cloudflared tunnel create galpon-ucc
   ```

3. **Crear Configuración:**
   ```bash
   mkdir -p ~/.cloudflared
   nano ~/.cloudflared/config.yml
   
   # Reemplazar TU-TUNNEL-ID por el ID que apareció:
   tunnel: TU-TUNNEL-ID
   credentials-file: /home/pi/.cloudflared/TU-TUNNEL-ID.json
   
   ingress:
     - hostname: galpon-ucc.tudominio.com
       service: http://localhost:8501
     - service: http_status:404
   ```

**OPCIÓN B: Vercel para Frontend + Túnel para API**

Si necesitas mayor rendimiento para el frontend:

1. **Adaptar Streamlit para Vercel:**
   - Convertir `streamlit_app_raspberry.py` a Next.js
   - Usar API de Raspberry Pi como backend
   - Configurar variables de entorno en Vercel

2. **Mantener API en Raspberry Pi:**
   - Solo exponer FastAPI vía túnel
   - Frontend en Vercel consume API remota

### ✅ FASE 5: Verificación (10 min)

**COMANDOS DE VERIFICACIÓN OBLIGATORIOS:**

1. **Verificar PostgreSQL:**
   ```bash
   sudo systemctl status postgresql
   psql -h localhost -U galpon_user -d galpon_db -c "SELECT COUNT(*) FROM sensors3;"
   ```

2. **Verificar Servicios:**
   ```bash
   sudo systemctl status galpon-api galpon-dashboard
   curl http://localhost:8000/health
   ```

3. **Probar API:**
   ```bash
   curl -X POST http://localhost:8000/api/sensores \
     -H "Content-Type: application/json" \
     -d '{"device":"TEST_PI","lux":50,"nh3":15,"hs":5,"h":65,"t":22}'
   ```

4. **Verificar Dashboard:**
   - Abrir navegador: `http://IP_RASPBERRY:8501`
   - Probar login con email @campusucc.edu.co
   - Contraseña: `hello` (temporalmente)

---

## 🔧 PERSONALIZACIÓN REQUERIDA

### 🔐 Autenticación:
- **Email permitido:** Solo dominios @campusucc.edu.co
- **Contraseña temporal:** `hello` (cambiar en producción)
- **Hash MD5:** `5e884898da28047151d0e56f8dc6292d`

### 🎨 Branding UCC:
- **Universidad:** Universidad Cooperativa de Colombia
- **Campus:** Neiva
- **Colores:** Verde UCC (#2E7D32, #4CAF50)
- **Logo:** 🐔 (emoji de pollo para galpón avícola)

### 📊 Sensores ESP32:
- **Dispositivos esperados:** ESP32_001, ESP32_002, ESP32_003
- **Parámetros:** lux, nh3, hs, h, t (iluminación, amoniaco, sulfuro, humedad, temperatura)
- **Frecuencia:** Cada 30 segundos por sensor

---

## 🚨 PUNTOS CRÍTICOS DE ATENCIÓN

### ⚠️ ERRORES COMUNES A EVITAR:

1. **NO cambiar el esquema de la tabla sensors3** - Los ESP32 ya están configurados
2. **NO modificar main_raspberry.py** sin entender el endpoint `/api/sensores`
3. **NO exponer PostgreSQL al exterior** - Solo conexiones locales
4. **NO usar HTTP en producción** - Siempre HTTPS con túneles
5. **NO hardcodear IPs** - Usar variables de entorno

### ✅ VALIDACIONES OBLIGATORIAS:

1. **PostgreSQL debe aceptar conexiones locales:**
   ```bash
   psql -h localhost -U galpon_user -d galpon_db -c "SELECT 1;"
   ```

2. **FastAPI debe responder correctamente:**
   ```bash
   curl http://localhost:8000/health
   # Debe retornar: {"status": "✅ Sistema operativo"}
   ```

3. **Streamlit debe cargar con autenticación:**
   - Pantalla de login visible
   - Redirección tras login exitoso
   - Datos de sensores mostrados

4. **Túnel público debe funcionar:**
   ```bash
   curl -I https://tu-dominio-publico.com
   # Debe retornar: HTTP/2 200
   ```

---

## 📱 RESULTADO ESPERADO

Al finalizar, debes tener:

- ✅ **PostgreSQL funcionando** con datos de sensores
- ✅ **FastAPI recibiendo datos** de ESP32 en `/api/sensores`
- ✅ **Dashboard Streamlit accesible** con autenticación UCC
- ✅ **Acceso público HTTPS** vía túnel gratuito
- ✅ **Servicios auto-iniciables** en boot de Raspberry Pi
- ✅ **Logs y monitoreo** funcionando correctamente

### 🌐 URLs Finales:
- **Dashboard:** `https://galpon-ucc.tudominio.com`
- **API:** `https://galpon-ucc.tudominio.com` (mismo dominio, puerto 8000)
- **Documentación:** `https://galpon-ucc.tudominio.com/api/docs`

---

## 📞 SOPORTE Y CONTACTO

- **Repositorio:** https://github.com/AndresYule1417/Sensores-main
- **Colaborador Principal:** AndresYule1417
- **Implementador:** innovasicrasp
- **Universidad:** Universidad Cooperativa de Colombia
- **Campus:** Neiva

### 📋 CHECKLIST FINAL:

- [ ] PostgreSQL instalado y funcionando
- [ ] Base de datos galpon_db creada con tabla sensors3
- [ ] Entorno Python configurado con dependencias
- [ ] Servicios systemd creados y habilitados
- [ ] API FastAPI respondiendo en puerto 8000
- [ ] Dashboard Streamlit funcionando en puerto 8501
- [ ] Autenticación @campusucc.edu.co implementada
- [ ] Túnel público configurado y funcionando
- [ ] Pruebas de conectividad exitosas
- [ ] Sistema auto-iniciable configurado

**⏱️ Tiempo total estimado: 75 minutos**

---

## 🎯 COMANDO RÁPIDO DE VERIFICACIÓN FINAL

```bash
# Ejecutar este comando al final para verificar todo:
echo "🐔 Verificación Sistema Galpón Avícola UCC"
echo "=========================================="
sudo systemctl is-active postgresql && echo "✅ PostgreSQL: Activo" || echo "❌ PostgreSQL: Error"
sudo systemctl is-active galpon-api && echo "✅ FastAPI: Activo" || echo "❌ FastAPI: Error"  
sudo systemctl is-active galpon-dashboard && echo "✅ Streamlit: Activo" || echo "❌ Streamlit: Error"
curl -s http://localhost:8000/health > /dev/null && echo "✅ API: Respondiendo" || echo "❌ API: Error"
psql -h localhost -U galpon_user -d galpon_db -c "SELECT COUNT(*) FROM sensors3;" 2>/dev/null && echo "✅ Base de datos: Conectada" || echo "❌ Base de datos: Error"
echo "🏛️ Universidad Cooperativa de Colombia - Sistema Operativo"
```

**¡IMPORTANTE:** Si algo falla, revisar logs con:
```bash
sudo journalctl -u galpon-api -f
sudo journalctl -u galpon-dashboard -f
```

¡Con este prompt, innovasicrasp tendrá todo lo necesario para implementar el sistema exitosamente! 🚀
