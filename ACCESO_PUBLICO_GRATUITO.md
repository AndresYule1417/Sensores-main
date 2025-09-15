# 🌐 ACCESO PÚBLICO GRATUITO - RASPBERRY PI

## 🎯 Opciones de Túneles Gratuitos

### 🚀 1. Cloudflare Tunnel (RECOMENDADO)

**✅ Ventajas:**
- 100% gratuito permanente
- Sin límites de ancho de banda
- HTTPS automático con certificados
- Sin exponer puertos del router
- Dominio personalizado gratis

```bash
# 1. Instalar cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
sudo dpkg -i cloudflared-linux-arm64.deb

# 2. Autenticar con Cloudflare
cloudflared tunnel login

# 3. Crear túnel
cloudflared tunnel create galpon-ucc

# 4. Configurar DNS (en dashboard Cloudflare)
# Agregar registro CNAME: galpon.tudominio.com -> UUID.cfargotunnel.com

# 5. Archivo de configuración
mkdir -p ~/.cloudflared
nano ~/.cloudflared/config.yml
```

**config.yml:**
```yaml
tunnel: TU-TUNNEL-ID
credentials-file: /home/pi/.cloudflared/TU-TUNNEL-ID.json

ingress:
  # Streamlit Dashboard
  - hostname: galpon.tudominio.com
    service: http://localhost:8501
  
  # FastAPI Backend
  - hostname: api.galpon.tudominio.com  
    service: http://localhost:8000
    
  # Catch-all rule
  - service: http_status:404
```

```bash
# 6. Crear servicio systemd
sudo nano /etc/systemd/system/cloudflared.service

[Unit]
Description=Cloudflare Tunnel
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/usr/local/bin/cloudflared tunnel run
Restart=always

[Install]
WantedBy=multi-user.target

# 7. Habilitar servicio
sudo systemctl enable cloudflared
sudo systemctl start cloudflared
```

---

### 🌟 2. Ngrok (Opción Simple)

**✅ Ventajas:**
- Setup súper rápido
- 2 túneles simultáneos gratis
- Subdominio aleatorio incluido

**❌ Limitaciones:**
- Túneles cambian al reiniciar
- Límite de 20,000 requests/mes

```bash
# 1. Instalar ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz
tar xvzf ngrok-v3-stable-linux-arm64.tgz
sudo mv ngrok /usr/local/bin

# 2. Configurar token (registrarse en ngrok.com)
ngrok config add-authtoken TU_TOKEN

# 3. Exponer Streamlit (puerto 8501)
ngrok http 8501 --region=us

# 4. Exponer FastAPI (puerto 8000) en otra terminal
ngrok http 8000 --region=us
```

**Script automático:**
```bash
#!/bin/bash
# start_tunnels.sh

# Iniciar Streamlit
cd /home/pi/galpon
python -m streamlit run streamlit_app_raspberry.py --server.port 8501 &

# Iniciar FastAPI  
python -m uvicorn main_raspberry:app --host 0.0.0.0 --port 8000 &

# Esperar 5 segundos
sleep 5

# Iniciar túneles ngrok
ngrok http 8501 --log=stdout > ngrok_streamlit.log &
ngrok http 8000 --log=stdout > ngrok_api.log &

echo "✅ Servicios iniciados!"
echo "📊 Dashboard: Ver ngrok_streamlit.log para URL"
echo "🚀 API: Ver ngrok_api.log para URL"
```

---

### 🏠 3. DuckDNS + Port Forwarding

**✅ Ventajas:**
- Dominio fijo gratis
- Control total
- Sin intermediarios

**❌ Limitaciones:**
- Requiere configurar router
- Necesita IP pública

```bash
# 1. Registrarse en duckdns.org
# 2. Crear subdominio: galpon-ucc.duckdns.org

# 3. Instalar cliente DuckDNS
mkdir ~/duckdns
cd ~/duckdns
nano duck.sh

#!/bin/bash
echo url="https://www.duckdns.org/update?domains=galpon-ucc&token=TU_TOKEN&ip=" | curl -k -o ~/duckdns/duck.log -K -

# 4. Hacer ejecutable y automatizar
chmod 700 duck.sh
crontab -e
# Agregar: */5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1

# 5. Configurar nginx como proxy reverso
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/galpon

server {
    listen 80;
    server_name galpon-ucc.duckdns.org;
    
    # Dashboard Streamlit
    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # API FastAPI
    location /api/ {
        proxy_pass http://localhost:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# 6. Habilitar sitio
sudo ln -s /etc/nginx/sites-available/galpon /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# 7. Configurar port forwarding en router:
# Puerto 80 -> 192.168.1.X:80 (IP de Raspberry Pi)
```

---

## 🔐 Configuración de Seguridad

### 🛡️ 1. Fail2Ban (Protección contra ataques)

```bash
# Instalar fail2ban
sudo apt install fail2ban -y

# Configurar
sudo nano /etc/fail2ban/jail.local

[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3
ignoreip = 127.0.0.1/8 192.168.1.0/24

[nginx-http-auth]
enabled = true
port = http,https
logpath = /var/log/nginx/error.log

# Reiniciar servicio
sudo systemctl restart fail2ban
```

### 🔥 2. Firewall UFW

```bash
# Configurar firewall
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 8501/tcp  # Solo si necesitas acceso directo
sudo ufw status
```

### 🔒 3. HTTPS con Let's Encrypt (Para DuckDNS)

```bash
# Instalar certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtener certificado
sudo certbot --nginx -d galpon-ucc.duckdns.org

# Renovación automática
sudo crontab -e
# Agregar: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 🚀 Scripts de Arranque Automático

### 📜 startup.sh
```bash
#!/bin/bash
# /home/pi/galpon/startup.sh

echo "🐔 Iniciando Sistema Galpón Avícola UCC..."

# Activar entorno virtual
source /home/pi/galpon/venv/bin/activate

# Verificar PostgreSQL
sudo systemctl start postgresql
sleep 3

# Iniciar FastAPI
cd /home/pi/galpon
python -m uvicorn main_raspberry:app --host 0.0.0.0 --port 8000 &
echo "🚀 API FastAPI iniciada en puerto 8000"

# Esperar 5 segundos
sleep 5

# Iniciar Streamlit
python -m streamlit run streamlit_app_raspberry.py --server.port 8501 --server.address 0.0.0.0 &
echo "📊 Dashboard Streamlit iniciado en puerto 8501"

# Iniciar túnel (elige uno)
echo "🌐 Iniciando túnel público..."

# OPCIÓN A: Cloudflare Tunnel
sudo systemctl start cloudflared

# OPCIÓN B: Ngrok (comentar línea anterior y descomentar estas)
# ngrok http 8501 --log=stdout > /home/pi/galpon/logs/ngrok_streamlit.log &
# ngrok http 8000 --log=stdout > /home/pi/galpon/logs/ngrok_api.log &

echo "✅ Sistema iniciado completamente!"
echo "📱 URLs disponibles:"
echo "   Dashboard: https://galpon.tudominio.com"
echo "   API: https://api.galpon.tudominio.com"
```

### 🔄 Servicio systemd completo
```bash
# /etc/systemd/system/galpon-system.service
[Unit]
Description=Sistema Galpon Avicola UCC
After=postgresql.service network.target

[Service]
Type=forking
User=pi
WorkingDirectory=/home/pi/galpon
ExecStart=/home/pi/galpon/startup.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Habilitar
sudo systemctl enable galpon-system
sudo systemctl start galpon-system
```

---

## 📱 URLs de Acceso Final

### 🏛️ Cloudflare Tunnel (Recomendado)
- **Dashboard:** `https://galpon.tudominio.com`
- **API:** `https://api.galpon.tudominio.com`
- **Docs API:** `https://api.galpon.tudominio.com/api/docs`

### 🌟 Ngrok
- **Dashboard:** `https://abc123.ngrok.io` (cambia cada restart)
- **API:** `https://def456.ngrok.io` (cambia cada restart)

### 🏠 DuckDNS + Router
- **Dashboard:** `https://galpon-ucc.duckdns.org`
- **API:** `https://galpon-ucc.duckdns.org/api`

---

## 🔍 Verificación y Monitoreo

```bash
# Ver logs del sistema
sudo journalctl -u galpon-system -f

# Verificar servicios activos
sudo systemctl status postgresql
sudo systemctl status galpon-system
sudo systemctl status cloudflared

# Probar conectividad externa
curl -I https://galpon.tudominio.com
curl https://api.galpon.tudominio.com/health

# Ver estadísticas de túnel
cloudflared tunnel info galpon-ucc
```

---

## 📊 Dashboard de Monitoreo

Puedes agregar este endpoint a tu FastAPI para monitorear el sistema:

```python
@app.get("/api/system-status")
async def system_status():
    import psutil
    import subprocess
    
    # Stats del sistema
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    # Verificar túnel
    tunnel_status = "🔴 Desconectado"
    try:
        result = subprocess.run(['pgrep', 'cloudflared'], capture_output=True)
        if result.returncode == 0:
            tunnel_status = "🟢 Conectado"
    except:
        pass
    
    return {
        "timestamp": datetime.now().isoformat(),
        "system": {
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "disk_percent": (disk.used / disk.total) * 100,
            "uptime": "Ver logs"
        },
        "services": {
            "postgresql": "🟢 Activo",
            "fastapi": "🟢 Activo", 
            "tunnel": tunnel_status
        },
        "university": "Universidad Cooperativa de Colombia",
        "campus": "Neiva"
    }
```

¡Con esto tendrás acceso público completamente funcional y gratuito! 🎉

**Mi recomendación:** Usa **Cloudflare Tunnel** para producción - es más estable y profesional. 💪