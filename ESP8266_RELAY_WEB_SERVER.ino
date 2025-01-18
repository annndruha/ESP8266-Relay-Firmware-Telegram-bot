// Generic ESP8266 with CH340 bootloader

#include "ESP8266WiFi.h"
#include "ESP8266WebServer.h"

#define RELAY_PIN 2
#define ON HIGH
#define OFF LOW

ESP8266WebServer server(80);
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
bool STATE = false;

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  update_relay();  // Turn off, because STATE = false

  Serial.begin(9600);

  Serial.println("Start...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Non Connecting to WiFi..");
  } else {
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

    // Sensors
    server.on("/lamp_state", lamp_state);

    // Actions
    server.on("/set", set);
    server.on("/switch", _switch);

    // Other
    server.on("/", handleRootPath);
    server.on("/json", json);
    server.on("/uptime", uptime);
    server.on("/reboot", reboot);
    server.onNotFound(handleNotFound);

    server.begin();
    Serial.println("Server listening............");
  }
}

void loop() {
  server.handleClient();
}

void update_relay() {
  if (STATE) {
    digitalWrite(RELAY_PIN, ON);
  } else {
    digitalWrite(RELAY_PIN, OFF);
  }
  delay(500);
}

void set() {
  Serial.println("[" + String(server.client().remoteIP().toString())+ "] Request set");
  String response = "";
  if (server.arg("value") == "") {
    response = "Parameter not found";
  } else {
    if (server.arg("value") == "1") {
      if (STATE) {
        response = "Nothing changed. State:1";
      } else {
        response = "Value set to 1";
      }
      STATE = true;
    } else if (server.arg("value") == "0") {
      if (!STATE) {
        response = "Nothing changed. State:0";
      } else {
        response = "Value set to 0";
      }
      STATE = false;
    } else {
      response = "Only value=0 or value=1 accepted";
    }
  }
  server.send(200, "text/plain", response);
  update_relay();
}


void _switch() {
  Serial.println("[" + String(server.client().remoteIP().toString())+ "] Request switch");
  STATE = !STATE;
  String response = "State changed from " + String(!STATE) + " to " + String(STATE);
  server.send(200, "text/plain", response);
  update_relay();
}

String read_lamp_state(){
  return String(STATE);
}

void lamp_state() {
  Serial.println("[" + String(server.client().remoteIP().toString())+ "] Request get_state");
  server.send(200, "text/plain", read_lamp_state());
}

String getUptime(){
  unsigned long sec = millis() / 1000;
  unsigned long min = sec / 60;
  unsigned long hr = min / 60;
  unsigned long days = hr / 24;
  sec %= 60;
  min %= 60;
  hr %= 24;
  String response = String(days) + "d " +  String(hr) + ":" + String(min) + ":" + String(sec);
  return response;
}

void uptime() {
  Serial.println("[" + String(server.client().remoteIP().toString())+ "] Request uptime");
  server.send(200, "text/plain", getUptime());
}

void reboot() {
  Serial.println("[" + String(server.client().remoteIP().toString())+ "] Request reboot");
  server.send(200, "text/plain", "Reboot in progress...");
  ESP.restart();
}

void json() {
  Serial.println("[" + String(server.client().remoteIP().toString())+ "] Request json");
  String json;
  json = "{\"states\":{";
  json += "\"lamp_state\":\"" + read_lamp_state() + "\"";
  json += "}}";
  server.send(200, "application/json", json);
}

void handleRootPath() {
  Serial.println("[" + String(server.client().remoteIP().toString())+ "] Request handleRootPath");
  String response = """<h3>Hello from ESP-01 Relay v4.0!</h3>""" \
                    """States:""" \
                    """<br><a href=\"/lamp_state\">/lamp_state</a> (""" + read_lamp_state() + ")" + \
                    """<br><br>Actions:""" + \
                    """<br><a href=\"/set?value=1\">/set?value=1</a> (Turn on)""" + \
                    """<br><a href=\"/set?value=0\">/set?value=0</a> (Turn off)""" + \
                    """<br><a href=\"/switch\">/switch</a>  (Invert state)""" + \
                    """<br><br>Debug:""" + \
                    """<br><a href=\"/json\">/json</a> (Sensor values in json format)" + \
                    """<br><a href=\"/reboot\">/reboot</a>  (Reboot NodeMCU)" + \
                    """<br><a href=\"/uptime\">/uptime</a>  (""" + String(getUptime()) + ")";
  server.send(200, "text/html", response);
}


void handleNotFound() {
  Serial.println("[" + String(server.client().remoteIP().toString())+ "] Request handleNotFound:" + String(server.uri()));
  String response ="""<p>Hello from ESP-01 Relay v4.0!</p>""" \
                   """<p><a href=\"/\">Go to main page</a></p>""";
  server.send(404, "text/html", response);
}