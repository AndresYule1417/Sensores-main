/*
 * 🐔 Configuración ESP32 - Galpón Avícola UCC
 * 
 * CONFIGURACIÓN PERSONAL - Edita estos valores con tus datos reales
 */

#ifndef CONFIG_H
#define CONFIG_H

// =====================================================================
// CONFIGURACIÓN WIFI - CAMBIAR CON TUS DATOS
// =====================================================================
#define WIFI_SSID "WIFI_UCC_ESTUDIANTES"    // 🔧 CAMBIAR: Nombre de tu red WiFi
#define WIFI_PASSWORD "5stud14nt3s_BplC00r*" // 🔧 CAMBIAR: Contraseña WiFi

// =====================================================================
// CONFIGURACIÓN MQTT - MÚLTIPLES OPCIONES
// =====================================================================
// Opción 1: Mosquitto público (más confiable)
#define MQTT_SERVER "test.mosquitto.org"    // 🔧 Broker MQTT público confiable
#define MQTT_PORT 1883                      // Puerto MQTT estándar

// Opción 2: Si test.mosquitto.org no funciona, usar:
// #define MQTT_SERVER "broker.hivemq.com"
// #define MQTT_PORT 1883

// Opción 3: Para uso local (cambiar a tu servidor):
// #define MQTT_SERVER "192.168.1.100"
// #define MQTT_PORT 1883

#define MQTT_USER ""                        // Usuario MQTT (vacío para brokers públicos)
#define MQTT_PASSWORD ""                    // Contraseña MQTT (vacío para brokers públicos)

// =====================================================================
// IDENTIFICACIÓN DEL SISTEMA
// =====================================================================
#define GALPON_ID "galpon_prueba"           // ID único del galpón
#define DEVICE_ID "ESP32_001"               // ID único de este ESP32

// =====================================================================
// CONFIGURACIÓN DE SENSORES (CALIBRACIÓN)
// =====================================================================

// DHT22 - Temperatura y Humedad
#define DHT_TEMP_OFFSET 0.0                 // Offset temperatura °C
#define DHT_HUM_OFFSET 0.0                  // Offset humedad %

// LDR - Sensor de luz
#define LDR_MIN_LUX 0                       // LUX mínimo en oscuridad
#define LDR_MAX_LUX 1000                    // LUX máximo en luz directa

// MQ135 - Sensor NH3 (Amoniaco)
#define MQ135_MIN_PPM 0                     // PPM mínimo
#define MQ135_MAX_PPM 50                    // PPM máximo esperado

// MQ136 - Sensor H2S (Sulfuro de hidrógeno)  
#define MQ136_MIN_PPM 0                     // PPM mínimo
#define MQ136_MAX_PPM 20                    // PPM máximo esperado

// =====================================================================
// CONFIGURACIÓN AVANZADA
// =====================================================================
#define PUBLISH_INTERVAL_MS 30000           // Intervalo publicación (30s)
#define WIFI_TIMEOUT_MS 10000               // Timeout conexión WiFi
#define MQTT_KEEPALIVE 60                   // Keep alive MQTT (segundos)

// Configuración de calidad de aire (umbrales de alarma)
#define NH3_ALARM_THRESHOLD 20.0            // Alarma NH3 > 20 ppm
#define HS_ALARM_THRESHOLD 10.0             // Alarma H2S > 10 ppm
#define TEMP_MIN_ALARM 15.0                 // Alarma temperatura < 15°C
#define TEMP_MAX_ALARM 30.0                 // Alarma temperatura > 30°C
#define HUMIDITY_MIN_ALARM 40.0             // Alarma humedad < 40%
#define HUMIDITY_MAX_ALARM 80.0             // Alarma humedad > 80%

// =====================================================================
// INFORMACIÓN DEL DISPOSITIVO
// =====================================================================
#define FIRMWARE_VERSION "1.0.0"
#define HARDWARE_VERSION "ESP32_DHT22_MQ135_MQ136"
#define INSTITUTION "Universidad Cooperativa de Colombia"
#define CAMPUS "Neiva"
#define PROJECT "Sistema Monitoreo Galpón Avícola"

#endif // CONFIG_