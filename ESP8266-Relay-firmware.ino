// Script for ESP8266 for control Relay by api requests
// To work check go to http://ip_of_esp
// 

#include "ESP8266WiFi.h"
#include "ESP8266WebServer.h"

#define RELAY_PIN 2
#define ON HIGH
#define OFF LOW

ESP8266WebServer server(80);
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
byte tries = 10;  // Wi-Fi connect retries
bool STATE = false;

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
  update_relay();  // Turn off, becouse STATE = false

  WiFi.begin(ssid, password);

  while (--tries && WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  server.on("/set", set);
  server.on("/get", get);
  server.on("/uptime", uptime);
  server.on("/switch", switch_state);
  server.on("/", handleRootPath);
  server.onNotFound(handleNotFound);

  server.begin();
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


void switch_state() {
  STATE = !STATE;
  String response = "State changed from " + String(!STATE) + " to " + String(STATE);
  server.send(200, "text/plain", response);
  update_relay();
}


void get() {
  String response = "State:" + String(STATE);
  server.send(200, "text/plain", response);
}


void uptime() {
  unsigned long sec = millis() / 1000;
  unsigned long min = sec / 60;
  unsigned long hr = min / 60;
  unsigned long days = hr / 24;

  sec %= 60;
  min %= 60;
  hr %= 24;

  String response = "Uptime:" + String(days) + "d " +  String(hr) + ":" + String(min) + ":" + String(sec);
  server.send(200, "text/plain", response);
}



void handleRootPath() {
  server.send(200, "text/html", "<p>Hello from home Wi-Fi relay!</p><p>This is WebSerber on ESP-01 that controls Relay v4.0</p><p>Here you will find a <a href=\"https://github.com/SmartThinksDIY\">project site</a></p><p>Credits: <a href=\"https://annndruha.space\">annndruha.space</a></p>");
}


void handleNotFound() {
  String response = "Page not Found\n\n";
  server.send(404, "text/plain", response);
}