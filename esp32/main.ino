/*
 * 🐔 Sistema de Monitoreo Galpón Avícola
 * Universidad Cooperativa de Colombia - Campus Neiva
 * 
 * ESP8266 - Sensor de condiciones ambientales
 * Publica datos vía MQTT cada 5 segundos
 * 
 * Sensores:
 * - DHT22: Temperatura y Humedad
 * - LDR: Iluminación (LUX)
 * - MQ135: Amoniaco (NH3) aproximado
 * - MQ136: Sulfuro de hidrógeno (H2S) aproximado
 */

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <DHT.h>
#include "config.h"

// =====================================================================
// CONFIGURACIÓN DE PINES Y MODO DE OPERACIÓN
// =====================================================================
#define SIMULATION_MODE true        // true = simular sensores, false = sensores reales

#define DHT_PIN 4           // Pin DHT22 (Temperatura y Humedad)
#define DHT_TYPE DHT22      // Tipo de sensor DHT
#define LDR_PIN 34          // Pin analógico LDR (Luz)
#define MQ135_PIN 35        // Pin analógico MQ135 (NH3)
#define MQ136_PIN 32        // Pin analógico MQ136 (H2S)
#define LED_PIN 2           // LED integrado ESP32

// Variables para simulación
float sim_base_temp = 22.0;     // Temperatura base
float sim_base_humidity = 60.0;  // Humedad base
float sim_base_lux = 150.0;      // Luz base
float sim_base_nh3 = 5.0;        // NH3 base
float sim_base_hs = 2.0;         // H2S base

// =====================================================================
// OBJETOS Y VARIABLES
// =====================================================================
DHT dht(DHT_PIN, DHT_TYPE);
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// Variables de tiempo
unsigned long lastPublish = 0;
const unsigned long PUBLISH_INTERVAL = 30000; // 30 segundos

// Variables de sensores
float temperature = 0.0;
float humidity = 0.0;
float lux = 0.0;
float nh3_ppm = 0.0;
float hs_ppm = 0.0;

// Estado de conexión
bool wifiConnected = false;
bool mqttConnected = false;

// =====================================================================
// SETUP INICIAL
// =====================================================================
void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("🐔 Iniciando ESP32 - Sensor Galpón Avícola");
  Serial.println("Universidad Cooperativa de Colombia");
  Serial.println("==========================================");
  
  if (SIMULATION_MODE) {
    Serial.println("🎭 MODO SIMULACIÓN ACTIVADO");
    Serial.println("📊 Generando datos realistas de galpón avícola");
  } else {
    Serial.println("🔬 MODO SENSORES REALES");
  }
  
  // Configurar pines
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  
  // Inicializar DHT22 solo si no está en modo simulación
  if (!SIMULATION_MODE) {
    dht.begin();
  }
  
  // Configurar MQTT
  mqttClient.setServer(MQTT_SERVER, MQTT_PORT);
  mqttClient.setCallback(mqttCallback);
  
  // Conectar WiFi
  connectWiFi();
  
  // Conectar MQTT
  connectMQTT();
  
  Serial.println("✅ Setup completado");
  digitalWrite(LED_PIN, HIGH); // LED encendido = sistema listo
  
  // Mostrar información del dispositivo
  Serial.println("\n📋 Configuración del dispositivo:");
  Serial.printf("🏷️ ID Galpón: %s\n", GALPON_ID);
  Serial.printf("📱 ID Dispositivo: %s\n", DEVICE_ID);
  Serial.printf("🎯 Modo: %s\n", SIMULATION_MODE ? "Simulación" : "Sensores Reales");
}

// =====================================================================
// LOOP PRINCIPAL
// =====================================================================
void loop() {
  // Verificar conexiones
  if (!WiFi.isConnected()) {
    wifiConnected = false;
    connectWiFi();
  }
  
  if (!mqttClient.connected()) {
    mqttConnected = false;
    connectMQTT();
  }
  
  // Mantener conexión MQTT
  mqttClient.loop();
  
  // Publicar datos cada 30 segundos
  unsigned long now = millis();
  if (now - lastPublish >= PUBLISH_INTERVAL) {
    readSensors();
    publishSensorData();
    lastPublish = now;
  }
  
  delay(100);
}

// =====================================================================
// CONEXIÓN WIFI MEJORADA CON DEBUG DETALLADO
// =====================================================================
void connectWiFi() {
  if (wifiConnected) return;
  
  Serial.println("📡 Conectando a WiFi...");
  Serial.print("🌐 Red: ");
  Serial.println(WIFI_SSID);
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
    
    // Mostrar estado cada 5 intentos
    if (attempts % 5 == 0) {
      Serial.print(" [Intento ");
      Serial.print(attempts);
      Serial.print("/20] Estado: ");
      Serial.print(WiFi.status());
      Serial.println();
    }
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    wifiConnected = true;
    Serial.println();
    Serial.println("✅ WiFi conectado exitosamente");
    Serial.print("📍 IP asignada: ");
    Serial.println(WiFi.localIP());
    Serial.print("📶 Intensidad señal: ");
    Serial.print(WiFi.RSSI());
    Serial.println(" dBm");
  } else {
    Serial.println();
    Serial.println("❌ Error conectando WiFi");
    Serial.print("🔍 Estado final: ");
    Serial.println(WiFi.status());
    Serial.println("💡 Verifica SSID y contraseña en config.h");
    delay(5000);
  }
}

// =====================================================================
// CONEXIÓN MQTT MEJORADA CON DEBUG DETALLADO
// =====================================================================
void connectMQTT() {
  if (mqttConnected || !wifiConnected) return;
  
  Serial.println("🔌 Intentando conexión MQTT...");
  Serial.print("📡 Servidor: ");
  Serial.print(MQTT_SERVER);
  Serial.print(":");
  Serial.println(MQTT_PORT);
  
  // Generar Client ID único más corto para evitar problemas
  String clientId = "ESP32_";
  clientId += String(random(1000, 9999));  // ID más corto
  
  Serial.print("🆔 Cliente ID: ");
  Serial.println(clientId);
  
  if (mqttClient.connect(clientId.c_str(), MQTT_USER, MQTT_PASSWORD)) {
    mqttConnected = true;
    Serial.println("✅ MQTT conectado exitosamente");
    
    // Suscribirse a tópico de comandos (opcional)
    String commandTopic = "galpon/" + String(GALPON_ID) + "/command/" + String(DEVICE_ID);
    mqttClient.subscribe(commandTopic.c_str());
    Serial.print("📥 Suscrito a: ");
    Serial.println(commandTopic);
    
    // Publicar mensaje de conexión
    publishStatusMessage("online");
    
  } else {
    int errorCode = mqttClient.state();
    Serial.print("❌ Error MQTT, código: ");
    Serial.print(errorCode);
    
    // Explicar el código de error
    switch(errorCode) {
      case -4: Serial.println(" (Timeout de conexión)"); break;
      case -3: Serial.println(" (Conexión perdida)"); break;
      case -2: Serial.println(" (Conexión rechazada - ID cliente incorrecto)"); break;
      case -1: Serial.println(" (Error de protocolo)"); break;
      case 1: Serial.println(" (Versión de protocolo incorrecta)"); break;
      case 2: Serial.println(" (ID cliente rechazado)"); break;
      case 3: Serial.println(" (Servidor no disponible)"); break;
      case 4: Serial.println(" (Credenciales incorrectas)"); break;
      case 5: Serial.println(" (No autorizado)"); break;
      default: Serial.println(" (Error desconocido)"); break;
    }
    
    Serial.println("🔄 Reintentando en 5 segundos...");
    delay(5000);
  }
}

// =====================================================================
// LECTURA DE SENSORES
// =====================================================================
void readSensors() {
  Serial.println("📊 Leyendo sensores...");
  
  if (SIMULATION_MODE) {
    // 🎭 MODO SIMULACIÓN - Generar datos realistas
    generateSimulatedData();
  } else {
    // 🔬 MODO SENSORES REALES
    readRealSensors();
  }
  
  // Imprimir valores leídos
  Serial.println("📈 Valores de sensores:");
  Serial.printf("  🌡️ Temperatura: %.2f°C\n", temperature);
  Serial.printf("  💧 Humedad: %.2f%%\n", humidity);
  Serial.printf("  💡 Luz: %.0f LUX\n", lux);
  Serial.printf("  🟢 NH3: %.2f ppm\n", nh3_ppm);
  Serial.printf("  🔴 H2S: %.2f ppm\n", hs_ppm);
}

// =====================================================================
// GENERADOR DE DATOS SIMULADOS
// =====================================================================
void generateSimulatedData() {
  unsigned long now = millis();
  
  // Simular ciclo diario (24 horas = 86400000 ms, pero acelerado)
  float hourOfDay = (now / 60000.0); // 1 minuto = 1 hora simulada
  hourOfDay = fmod(hourOfDay, 24.0);
  
  // 🌡️ TEMPERATURA - Varía según "hora del día"
  // Más fría en la madrugada (4-6 AM), más caliente al mediodía
  float temp_variation = 3.0 * sin((hourOfDay - 6.0) * PI / 12.0);
  temperature = sim_base_temp + temp_variation + random(-150, 150) / 100.0; // ±1.5°C ruido
  
  // 💧 HUMEDAD - Inversa a temperatura
  float hum_variation = -2.0 * sin((hourOfDay - 6.0) * PI / 12.0);
  humidity = sim_base_humidity + hum_variation + random(-200, 200) / 100.0; // ±2% ruido
  
  // 💡 LUZ - Ciclo día/noche realista
  if (hourOfDay >= 6.0 && hourOfDay <= 18.0) {
    // Día: luz variable
    float light_curve = sin((hourOfDay - 6.0) * PI / 12.0);
    lux = sim_base_lux * light_curve + random(-20, 20);
  } else {
    // Noche: luz mínima
    lux = random(0, 10);
  }
  
  // 🟢 NH3 - Aumenta con actividad de las aves (día) y temperatura
  float activity_factor = (hourOfDay >= 6.0 && hourOfDay <= 20.0) ? 1.5 : 0.7;
  float temp_factor = (temperature > 25.0) ? 1.3 : 1.0;
  nh3_ppm = sim_base_nh3 * activity_factor * temp_factor + random(-50, 100) / 100.0;
  
  // 🔴 H2S - Relacionado con NH3 pero menor concentración
  hs_ppm = sim_base_hs * (nh3_ppm / sim_base_nh3) * 0.6 + random(-20, 50) / 100.0;
  
  // Aplicar límites realistas
  temperature = constrain(temperature, 15.0, 35.0);
  humidity = constrain(humidity, 40.0, 90.0);
  lux = constrain(lux, 0.0, 800.0);
  nh3_ppm = constrain(nh3_ppm, 0.0, 30.0);
  hs_ppm = constrain(hs_ppm, 0.0, 15.0);
  
  // Mostrar hora simulada
  Serial.printf("  🕐 Hora simulada: %.1fh (ciclo acelerado)\n", hourOfDay);
}

// =====================================================================
// LECTURA DE SENSORES REALES
// =====================================================================
void readRealSensors() {
  // DHT22 - Temperatura y Humedad
  temperature = dht.readTemperature();
  humidity = dht.readHumidity();
  
  // Validar lecturas DHT22
  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("⚠️ Error leyendo DHT22");
    temperature = -999.0;
    humidity = -999.0;
  }
  
  // LDR - Luz (convertir a LUX aproximado)
  int ldrValue = analogRead(LDR_PIN);
  lux = map(ldrValue, 0, 4095, 0, 1000); // Mapeo aproximado a LUX
  
  // MQ135 - NH3 (conversión aproximada a PPM)
  int mq135Value = analogRead(MQ135_PIN);
  nh3_ppm = mapFloat(mq135Value, 0, 4095, 0, 50); // Rango 0-50 ppm
  
  // MQ136 - H2S (conversión aproximada a PPM)
  int mq136Value = analogRead(MQ136_PIN);
  hs_ppm = mapFloat(mq136Value, 0, 4095, 0, 20); // Rango 0-20 ppm
}

// =====================================================================
// PUBLICAR DATOS VÍA MQTT
// =====================================================================
void publishSensorData() {
  if (!mqttConnected) {
    Serial.println("⚠️ MQTT desconectado, no se pueden enviar datos");
    return;
  }
  
  // Crear JSON con datos de sensores
  StaticJsonDocument<200> doc;
  doc["device"] = DEVICE_ID;
  doc["t"] = round(temperature * 100) / 100.0;  // 2 decimales
  doc["h"] = round(humidity * 100) / 100.0;     // 2 decimales
  doc["lux"] = round(lux);                      // Sin decimales
  doc["nh3"] = round(nh3_ppm * 100) / 100.0;   // 2 decimales
  doc["hs"] = round(hs_ppm * 100) / 100.0;     // 2 decimales
  doc["ts"] = getTimestamp();
  doc["rssi"] = WiFi.RSSI();
  doc["ip"] = WiFi.localIP().toString();
  
  // Convertir a string
  String jsonString;
  serializeJson(doc, jsonString);
  
  // Tópico MQTT
  String topic = "galpon/" + String(GALPON_ID) + "/sensor/" + String(DEVICE_ID);
  
  // Publicar
  if (mqttClient.publish(topic.c_str(), jsonString.c_str())) {
    Serial.println("✅ Datos publicados:");
    Serial.println("📝 Tópico: " + topic);
    Serial.println("📊 Datos: " + jsonString);
    
    // Parpadear LED para indicar envío exitoso
    digitalWrite(LED_PIN, LOW);
    delay(100);
    digitalWrite(LED_PIN, HIGH);
  } else {
    Serial.println("❌ Error publicando datos");
  }
}

// =====================================================================
// FUNCIONES AUXILIARES
// =====================================================================

// Callback para mensajes MQTT recibidos
void mqttCallback(char* topic, byte* payload, unsigned int length) {
  Serial.print("📨 Mensaje recibido en: ");
  Serial.println(topic);
  
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  Serial.println("💬 Contenido: " + message);
  
  // Procesar comandos (opcional)
  if (message == "status") {
    publishStatusMessage("online");
  } else if (message == "reboot") {
    Serial.println("🔄 Reiniciando ESP32...");
    ESP.restart();
  } else if (message == "simulate") {
    Serial.println("🎭 Cambiando a modo simulación");
    // Cambiar modo dinámicamente (se puede implementar)
  } else if (message == "real") {
    Serial.println("🔬 Cambiando a modo sensores reales");
    // Cambiar modo dinámicamente (se puede implementar)
  }
}

// Publicar mensaje de estado
void publishStatusMessage(String status) {
  String topic = "galpon/" + String(GALPON_ID) + "/status/" + String(DEVICE_ID);
  
  StaticJsonDocument<150> doc;
  doc["device"] = DEVICE_ID;
  doc["status"] = status;
  doc["mode"] = SIMULATION_MODE ? "simulation" : "real";
  doc["uptime"] = millis();
  doc["rssi"] = WiFi.RSSI();
  doc["ts"] = getTimestamp();
  doc["firmware"] = "1.0.0";
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  mqttClient.publish(topic.c_str(), jsonString.c_str());
}

// Mapeo de float
float mapFloat(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

// Timestamp simple (sin RTC)
String getTimestamp() {
  unsigned long uptime = millis();
  unsigned long hours = uptime / 3600000;
  unsigned long minutes = (uptime % 3600000) / 60000;
  unsigned long seconds = (uptime % 60000) / 1000;
  
  String timestamp = String(hours) + ":" + String(minutes) + ":" + String(seconds);
  return timestamp;
}