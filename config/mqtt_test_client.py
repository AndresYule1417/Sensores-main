# 🐔 Cliente MQTT de Prueba - Galpón Avícola UCC
# Para verificar que el ESP32 está enviando datos correctamente

import paho.mqtt.client as mqtt
import json
from datetime import datetime
import sys

# Configuración MQTT (misma que ESP32)
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPICS = [
    "galpon/galpon_prueba/sensor/ESP32_001",
    "galpon/galpon_prueba/status/ESP32_001"
]

print("🐔 Cliente MQTT de Prueba - Galpón Avícola UCC")
print("=" * 50)
print(f"📡 Conectando a: {MQTT_BROKER}:{MQTT_PORT}")
print(f"👂 Escuchando tópicos:")
for topic in MQTT_TOPICS:
    print(f"   • {topic}")
print("=" * 50)

def on_connect(client, userdata, flags, rc):
    """Callback cuando se conecta al broker MQTT"""
    if rc == 0:
        print("✅ Conectado al broker MQTT")
        print("📡 Suscribiéndose a tópicos...")
        
        for topic in MQTT_TOPICS:
            client.subscribe(topic)
            print(f"   ✅ Suscrito a: {topic}")
        
        print("\n🎯 Esperando datos del ESP32...")
        print("   (Presiona Ctrl+C para salir)")
        print("-" * 50)
        
    else:
        print(f"❌ Error conectando al broker MQTT: {rc}")
        sys.exit(1)

def on_message(client, userdata, msg):
    """Callback cuando llega un mensaje"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    topic = msg.topic
    
    try:
        # Decodificar JSON
        data = json.loads(msg.payload.decode())
        
        print(f"\n📨 [{timestamp}] Mensaje recibido:")
        print(f"📝 Tópico: {topic}")
        
        if "/sensor/" in topic:
            # Datos de sensores
            print("📊 Datos de sensores:")
            print(f"   🌡️  Temperatura: {data.get('t', 'N/A')}°C")
            print(f"   💧 Humedad: {data.get('h', 'N/A')}%")
            print(f"   ☀️  Luz: {data.get('lux', 'N/A')} LUX")
            print(f"   🟢 NH3: {data.get('nh3', 'N/A')} ppm")
            print(f"   🔴 H2S: {data.get('hs', 'N/A')} ppm")
            print(f"   📶 RSSI: {data.get('rssi', 'N/A')} dBm")
            print(f"   🌐 IP: {data.get('ip', 'N/A')}")
            print(f"   ⏰ Timestamp: {data.get('ts', 'N/A')}")
            
        elif "/status/" in topic:
            # Datos de estado
            print("📱 Estado del dispositivo:")
            print(f"   🔌 Estado: {data.get('status', 'N/A')}")
            print(f"   🎭 Modo: {data.get('mode', 'N/A')}")
            print(f"   ⏱️  Uptime: {data.get('uptime', 'N/A')} ms")
            print(f"   🔧 Firmware: {data.get('firmware', 'N/A')}")
        
        print(f"📄 JSON completo: {json.dumps(data, indent=2)}")
        
    except json.JSONDecodeError:
        print(f"⚠️  Mensaje no JSON: {msg.payload.decode()}")
    except Exception as e:
        print(f"❌ Error procesando mensaje: {e}")
    
    print("-" * 50)

def on_disconnect(client, userdata, rc):
    """Callback cuando se desconecta"""
    print(f"\n⚠️  Desconectado del broker MQTT (código: {rc})")

def main():
    """Función principal"""
    try:
        # Crear cliente MQTT
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        
        # Conectar al broker
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        # Mantener conexión activa
        client.loop_forever()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo cliente MQTT...")
        client.disconnect()
        print("✅ Cliente desconectado correctamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()