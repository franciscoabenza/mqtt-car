/*
 Converted to esp32 listening on
 
 Basic ESP8266 MQTT example

 This sketch demonstrates the capabilities of the pubsub library in combination
 with the ESP8266 board/library.

 It connects to an MQTT server then:
  - publishes "hello world" to the topic "outTopic" every two seconds
  - subscribes to the topic "inTopic", printing out any messages
    it receives. NB - it assumes the received payloads are strings not binary
  - If the first character of the topic "inTopic" is an 1, switch ON the ESP Led,
    else switch it off

 It will reconnect to the server if the connection is lost using a blocking
 reconnect function. See the 'mqtt_reconnect_nonblocking' example for how to
 achieve the same result without blocking the main loop.

 To install the ESP8266 board, (using Arduino 1.6.4+):
  - Add the following 3rd party board manager under "File -> Preferences -> Additional Boards Manager URLs":
       http://arduino.esp8266.com/stable/package_esp8266com_index.json
  - Open the "Tools -> Board -> Board Manager" and click install for the ESP8266"
  - Select your ESP8266 in "Tools -> Board"

*/
//#include <ESP8266WiFi.h>   commented
#include <WiFi.h>  //new
#include <PubSubClient.h>


#define Right_Mot_Forw 13
#define Right_Mot_Backw 12
#define Left_Mot_Forw 2
#define Left_Mot_Backw 14

int BUILTIN_LED = 2;  //new

// Update these with values suitable for your network.
const char* ssid = "ITEK 1st";
const char* password = "ITEK.cabana.E21a";
const char* mqtt_server = "test.mosquitto.org";
const char* inTopic = "eaaa/itek/e21a/carx";
//const char* ssid = "Waoo4920_S3N3";
//const char* password = "pcty7937";
//const char* mqtt_server = "test.mosquitto.org";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  if ((char)payload[0] == 'L') {
      if ((char)payload[1] == 'F') {
        digitalWrite(Left_Mot_Forw,HIGH);
        digitalWrite(Left_Mot_Backw,LOW);
      }
      if ((char)payload[1] == 'B') {
        digitalWrite(Left_Mot_Forw,LOW);
        digitalWrite(Left_Mot_Backw,HIGH);
      }
      if ((char)payload[1] == 'S') {
        digitalWrite(Left_Mot_Forw,LOW);
        digitalWrite(Left_Mot_Backw,LOW);
      }
  } 
  if ((char)payload[0] == 'R') {
      if ((char)payload[1] == 'F') {
        digitalWrite(Right_Mot_Forw,HIGH);
        digitalWrite(Right_Mot_Backw,LOW);
      }
      if ((char)payload[1] == 'B') {
        digitalWrite(Right_Mot_Forw,LOW);
        digitalWrite(Right_Mot_Backw,HIGH);
      }
      if ((char)payload[1] == 'S') {
        digitalWrite(Right_Mot_Forw,LOW);
        digitalWrite(Right_Mot_Backw,LOW);
      }
  } 

}

void setup() {
  pinMode(Left_Mot_Forw,OUTPUT);
  pinMode(Left_Mot_Backw,OUTPUT);
  pinMode(Right_Mot_Forw,OUTPUT);
  pinMode(Right_Mot_Backw,OUTPUT);
        digitalWrite(Left_Mot_Forw,LOW);
        digitalWrite(Left_Mot_Backw,LOW);
        digitalWrite(Right_Mot_Forw,LOW);
        digitalWrite(Right_Mot_Backw,LOW);
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }

  long now = millis();

   client.loop();

  if (millis() - now > 7)
  {
      Serial.print("duration of  mqtt.loop()  is  : milisec  ->");
       Serial.println(millis() - now);
  }

  now = millis();
  if (now - lastMsg > 20000) {
    lastMsg = now;
    ++value;
    snprintf (msg, 50, "hello world #%ld", value);
    Serial.print("Publish message: ");
    Serial.println(msg);
    client.publish("outTopic", msg);
  }
}
