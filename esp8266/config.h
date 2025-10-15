// CODIGO ESP826 - Publica datos simulados de sensores a un broker MQTT:


#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <PubSubClient.h>

ESP8266WiFiMulti wifiMulti;
WiFiClient espClient;
PubSubClient client(espClient);

// Broker MQTT (Raspberry Pi) 
const char* mqtt_server = "192.168.20.33";
const int mqtt_port = 1883;

unsigned long lastMsg = 0;

void setup_wifi() {
  Serial.println();
  Serial.println("Buscando y conectando a las redes guardadas...");
  // Espera hasta estar conectado a alguna de las redes añadidas
  while (wifiMulti.run() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.println("✅ WiFi conectado!");
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());
  Serial.print("IP asignada: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Intentando conexión MQTT...");
    String clientId = "ESP8266-";
    clientId += String(ESP.getChipId()); // ID único por dispositivo
    if (client.connect(clientId.c_str())) {
      Serial.println("Conectado al broker");
    } else {
      Serial.print("Error, rc=");
      Serial.print(client.state());
      Serial.println(" - reintentando en 5s");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  delay(10);
  randomSeed(analogRead(A0)); // semillas pseudoaleatorias

  // Agrega aquí tus redes (en el orden que quieras)
  wifiMulti.addAP("WIFI_UCC_ESTUDIANTES", "E5tud14nt3s_BplC00r*");
  wifiMulti.addAP("FLIA_BARRIOS", "1082920252");

  setup_wifi();

  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 5000) { // cada 5 segundos
    lastMsg = now;

    // Simulación de sensores
    float temperatura = random(200, 350) / 10.0;  // 20.0 - 35.0
    float humedad = random(400, 900) / 10.0;      // 40.0 - 90.0
    int luz = random(300, 800);                   // 300 - 800 lux
    float nh3 = random(0, 30) / 10.0;             // 0.0 - 3.0
    float h2s = random(0, 20) / 10.0;             // 0.0 - 2.0

    // JSON con los datos
    String payload = "{";
    payload += "\"timestamp\":"; payload += now / 1000; payload += ",";
    payload += "\"temperatura\":"; payload += temperatura; payload += ",";
    payload += "\"humedad\":"; payload += humedad; payload += ",";
    payload += "\"luz\":"; payload += luz; payload += ",";
    payload += "\"nh3\":"; payload += nh3; payload += ",";
    payload += "\"h2s\":"; payload += h2s;
    payload += "}";

    Serial.print("Publicando: ");
    Serial.println(payload);

    client.publish("galpon/esp32/sensor/data", payload.c_str());
  }
}