/**
 *  Autor: Ivan Camilo Leiton Murcia
 *  Proyecto: Medición de variables en galpón de gallinas en la finca Pensil de la UCC. 
 *  
 *  MODIFICADO: Actualizado para funcionar con nueva Raspberry Pi
 *  Fecha: Octubre 2025
 */
 
#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

/*
* ==================== CONFIGURACIÓN WiFi ====================
* Digita las credenciales de tu red WiFi 2.4GHz
*/
#ifndef STASSID
#define STASSID "TU_WIFI_SSID"        // ← CAMBIAR: Tu red WiFi
#define STAPSK  "TU_WIFI_PASSWORD"     // ← CAMBIAR: Tu contraseña WiFi
#endif

const char* ssid     = STASSID;
const char* password = STAPSK;

/*
* ==================== CONFIGURACIÓN SERVIDOR TCP ====================
* Digitar IP de servidor TCP destino (Raspberry Pi)
*/
const char* host = "192.168.20.33";   // ← IP de la Raspberry Pi
const uint16_t port = 8889;           // Puerto TCP

/*
* ==================== CONFIGURACIÓN DISPOSITIVO ====================
* Importante: Declarar DeviceID con un ID reconocible
*/
const char DeviceID[] = "ESP8266_GALPON_001";   // ← ID del dispositivo

// ==================== VARIABLES GLOBALES ====================

const int dataLength = 5;
const char separator = ',';
float data[dataLength];
boolean flag = 1;

unsigned long previousMillis = 0;
const long interval = 50;
DynamicJsonDocument doc(1024);
int ledState = LOW;

/*
* Constantes de conversión para sensores
*/
const float conv = (3.95/1023.0) / 0.01;  // Conversión humedad suelo
const float ATOV = 3.95 / 1023.0;          // ADC to Voltage

// ==================== FUNCIONES ====================

/**
 * Parpadeo del LED integrado (indicador visual)
 */
void Blink() {
  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;
    if (ledState == HIGH) {
      ledState = LOW;  
    } else {
      ledState = HIGH;
    }
    digitalWrite(LED_BUILTIN, ledState);
  }
}

/**
 * Leer datos del puerto Serial y actualizar JSON
 * Formato esperado: "LUX,NH3_ADC,HS_ADC,H_ADC,T_ADC\n"
 * 
 * Los datos vienen de un Arduino/microcontrolador conectado
 * por Serial que lee los sensores físicos:
 * - BH1750 (luminosidad)
 * - MQ135 (gases NH3)
 * - Sensor humedad suelo
 * - DHT22/sensor analógico (humedad aire)
 * - Thermistor (temperatura)
 */
void set_payload() {
  delay(300);
  
  if (Serial.available() > 0) {
    String str = Serial.readStringUntil('\n');
    
    // Parsear datos separados por comas
    for (byte i = 0; i < dataLength ; i++) {
      int index = str.indexOf(separator);
      data[i] = str.substring(0, index).toFloat(); 
      str = str.substring(index + 1);     
    }
  } 

  // ==================== PROCESAMIENTO DE SENSORES ====================

  // 1. BH1750 - Luminosidad (ya viene en lux)
  doc["LUX"].set(data[0]);
  
  // 2. MQ135 - Conversión de ADC a NH3 (ppm)
  float v = data[1] * 3.95 / 1023.0;      // Voltaje
  float RS = 1000 * ((4 - v) / v);         // Resistencia del sensor
  double NH3 = 6.8449 * pow(RS / 2809, -0.41);  // Concentración NH3
  doc["NH3"].set(NH3);
  
  // 3. Humedad del suelo (conversión ADC)
  doc["HS"].set(data[2] * conv);
  
  // 4. Humedad del aire (conversión ADC a %)
  doc["H"].set(data[3] * 33.33333 * 3.95 / 1023.0);
  
  // 5. Temperatura - Thermistor (conversión ADC a °C)
  float Temp = log(10000.0 * ((1024.0 / data[4] - 1))); 
  Temp = 1 / (0.001269148 + (0.000234125 + (0.0000000876741 * Temp * Temp)) * Temp);
  Temp = Temp - 273.15;  // Kelvin a Celsius
  doc["T"].set(Temp);   
}

// ==================== SETUP ====================

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  
  Serial.begin(9600);
  
  Serial.println("\n\n╔════════════════════════════════════════╗");
  Serial.println("║  ESP8266 - Galpón Avícola UCC         ║");
  Serial.println("║  Código Original (Sensores Reales)    ║");
  Serial.println("╚════════════════════════════════════════╝");
  
  /*
  * Conexión a la red WiFi
  */
  Serial.print("\n🌐 Conectando a WiFi: ");
  Serial.println(ssid);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  /*
  * Indicador visual de estado de conexión
  */    
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    Blink();
  }
  
  Serial.println("\n✅ WiFi conectado");
  Serial.print("📍 IP del ESP8266: ");
  Serial.println(WiFi.localIP());
  
  Serial.print("🖥️  Servidor TCP: ");
  Serial.print(host);
  Serial.print(":");
  Serial.println(port);
  
  Serial.print("📡 Device ID: ");
  Serial.println(DeviceID);
  
  Blink();

  /*
  * Inicializar estructura JSON
  */            
  doc["Device"] = DeviceID;
  doc["IP"] = WiFi.localIP().toString();
  doc["LUX"] = 0.0;
  doc["NH3"] = 0.0;
  doc["HS"] = 0.0;
  doc["H"] = 0.0;
  doc["T"] = 0.0;
  
  Serial.println("\n✅ Inicialización completa");
  Serial.println("📨 Esperando datos por Serial (9600 baud)...");
  Serial.println("   Formato: LUX,NH3_ADC,HS_ADC,H_ADC,T_ADC");
  Serial.println("\n────────────────────────────────────────\n");
}

// ==================== LOOP ====================

void loop() {   
  static bool wait = false;
  WiFiClient client;
  
  /*
  * Conexión al servidor TCP
  */
  if (!client.connect(host, port)) {
    Serial.println("❌ Error conectando al servidor TCP");
    Blink();
    delay(5000);
    return;
  } 
  
  Serial.println("✅ Conectado al servidor TCP");
  
  /*
  * Esperar respuesta del servidor (comando)
  */
  unsigned long timeout = millis();
  while (client.available() == 0) {
    if (millis() - timeout > 5000) {
      Serial.println("⏱️ Timeout esperando comando del servidor");
      client.stop();
      Blink(); 
      return;
    }
  }
  
  /*
  * Recepción de comandos por parte del servidor
  */ 
  char ch = ' ';
  while (client.available()) {
    ch = static_cast<char>(client.read());
  } 
  
  Serial.print("📥 Comando recibido del servidor: '");
  Serial.print(ch);
  Serial.println("'");
  
  /*
  * Procesamiento de la instrucción
  */
  switch(ch) {
    case 'a':
      // Comando 'a': Enviar datos de sensores
      Serial.print(ch);  // Enviar 'a' por Serial al Arduino
      delay(20);

      Serial.println("⏳ Esperando datos de sensores por Serial...");
      
      // Esperar datos del Arduino por Serial
      while (Serial.available() == 0) {
        // Esperar datos
      }        

      // Leer y procesar datos
      set_payload();
      
      // Mostrar datos que se van a enviar
      Serial.println("📤 Enviando JSON al servidor:");
      serializeJsonPretty(doc, Serial);
      Serial.println();
      
      // Enviar JSON al servidor TCP
      serializeJson(doc, client);    
      
      Serial.println("✅ Datos enviados correctamente");
      break;

    case 'b':
      // Comando 'b': Enviar JSON actual sin actualizar sensores
      if (client.connected()) {
        Serial.println("📤 Enviando JSON actual (sin actualizar):");
        serializeJsonPretty(doc, Serial);
        Serial.println();
        
        serializeJson(doc, client);
        
        Serial.println("✅ JSON enviado");
      }
      break;
      
    default:
      Serial.print("⚠️ Comando desconocido: '");
      Serial.print(ch);
      Serial.println("'");
      break;
  }
  
  // Cerrar conexión
  client.stop(); 
  Serial.println("🔌 Conexión TCP cerrada");
  Serial.println("────────────────────────────────────────\n");
  
  if (wait) {
    delay(10000);  // Esperar 10 segundos antes de la próxima conexión
  }

  wait = true;    
}
