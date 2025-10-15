# 📱 ESP32 - Código de Sensores

## 🔧 Hardware Requerido

### **Componentes principales:**
- **ESP32 DevKit V1** (recomendado)
- **DHT22** - Temperatura y humedad
- **LDR** - Sensor de luz
- **MQ135** - Sensor de gases (NH3 aproximado)
- **MQ136** - Sensor H2S (opcional, o usar MQ135)
- **Resistencias:** 10kΩ (pull-up DHT22), 10kΩ (divisor LDR)

### **Conexiones:**

```
ESP32          Sensor
-----          ------
GPIO 4    →    DHT22 Data
GPIO 34   →    LDR (con divisor de voltaje)
GPIO 35   →    MQ135 Analog Out
GPIO 32   →    MQ136 Analog Out
3.3V      →    VCC sensores
GND       →    GND sensores
```

## 📋 Instalación

### 1. **Arduino IDE Setup:**
```bash
# Instalar Arduino IDE 2.x
# Agregar URL de ESP32 en Preferencias:
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json

# Instalar Board ESP32 en Board Manager
# Seleccionar: ESP32 Dev Module
```

### 2. **Librerías necesarias:**
```cpp
// Instalar desde Library Manager:
- DHT sensor library (by Adafruit)
- ArduinoJson (by Benoit Blanchon)
- PubSubClient (by Nick O'Leary)
```

### 3. **Configuración:**
```bash
# Copiar template de configuración
cp config.h.template config.h

# Editar config.h con tus datos:
# - WiFi SSID y password
# - IP de Raspberry Pi
# - ID del dispositivo
```

## 🚀 Carga del código

### **Pasos para cargar:**
1. Abrir `main.ino` en Arduino IDE
2. Configurar `config.h` con tus credenciales
3. Seleccionar Board: **ESP32 Dev Module**
4. Seleccionar Puerto COM correcto
5. Click **Upload** (Ctrl+U)

### **Monitor Serial:**
```bash
# Abrir Serial Monitor (Ctrl+Shift+M)
# Velocidad: 115200 baud
# Verás logs como:
🐔 Iniciando ESP32 - Sensor Galpón Avícola
📡 Conectando a WiFi...
✅ WiFi conectado. IP: 192.168.1.150
🔌 Conectando a MQTT...
✅ MQTT conectado
📊 Leyendo sensores...
✅ Datos publicados
```

## 📊 Formato de Datos

### **Tópico MQTT:**
```
galpon/galpon_ucc_neiva/sensor/ESP32_001
```

### **JSON enviado cada 30s:**
```json
{
  "device": "ESP32_001",
  "t": 23.45,        // Temperatura °C
  "h": 65.2,         // Humedad %
  "lux": 120,        // Iluminación LUX
  "nh3": 1.2,        // Amoniaco ppm (aproximado)
  "hs": 0.05,        // H2S ppm (aproximado)
  "ts": "2:30:45",   // Timestamp uptime
  "rssi": -65,       // Señal WiFi
  "ip": "192.168.1.150"
}
```

## 🔧 Calibración de Sensores

### **DHT22 - Temperatura/Humedad:**
```cpp
// Generalmente no necesita calibración
// Si hay offset, ajustar en config.h:
#define DHT_TEMP_OFFSET -1.5  // Si lee 1.5°C alto
#define DHT_HUM_OFFSET 2.0    // Si lee 2% bajo
```

### **LDR - Luz:**
```cpp
// Calibrar con luxómetro profesional
// Ajustar mapeo en código según lecturas reales
lux = map(ldrValue, 0, 4095, 0, 1000);  // Ajustar rango
```

### **MQ135/MQ136 - Gases:**
```cpp
// ⚠️ IMPORTANTE: Solo valores aproximados
// Para mediciones precisas usar sensores calibrados
// Los valores son relativos para tendencias
```

## 🐛 Troubleshooting

### **Error WiFi:**
```
❌ Error conectando WiFi
```
**Solución:**
- Verificar SSID y password en `config.h`
- Asegurar que WiFi está en 2.4GHz (ESP32 no soporta 5GHz)
- Verificar alcance de señal

### **Error MQTT:**
```
❌ Error MQTT, código: -2
```
**Solución:**
- Verificar IP de Raspberry Pi en `config.h`
- Asegurar que Mosquitto está corriendo en Pi
- Verificar credenciales MQTT

### **Valores de sensores -999:**
```
🌡️ Temperatura: -999.00°C
```
**Solución:**
- Verificar conexiones DHT22
- Revisar alimentación 3.3V
- Comprobar resistencia pull-up 10kΩ

## 📱 Comandos Remotos

### **Vía MQTT:**
```bash
# Tópico de comandos:
galpon/galpon_ucc_neiva/command/ESP32_001

# Comandos disponibles:
"status"    # Envía estado actual
"reboot"    # Reinicia ESP32
```

### **Test desde PC:**
```bash
# Instalar mosquitto clients en Windows:
choco install mosquitto

# Enviar comando:
mosquitto_pub -h 192.168.1.100 -t "galpon/galpon_ucc_neiva/command/ESP32_001" -m "status"

# Escuchar datos:
mosquitto_sub -h 192.168.1.100 -t "galpon/galpon_ucc_neiva/sensor/+"
```

## 🔋 Consumo de Energía

### **Típico:**
- **Activo (WiFi + sensores):** ~150-200mA
- **Deep sleep (futuro):** ~10µA
- **Alimentación:** 3.3V/5V, fuente mínimo 500mA

### **Optimizaciones futuras:**
```cpp
// Para operación con batería:
esp_sleep_enable_timer_wakeup(30 * 1000000); // 30s
esp_deep_sleep_start();
```

---

**🐔 Universidad Cooperativa de Colombia - Campus Neiva**  
*Código ESP32 optimizado para galpón avícola con conectividad intermitente*