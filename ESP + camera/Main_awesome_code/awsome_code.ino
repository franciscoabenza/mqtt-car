#include <WiFi.h>  //new
#include <PubSubClient.h>


#define Right_Mot_Forw 13 //IN 3
#define Right_Mot_Backw 32 //IN 4
#define Left_Mot_Forw 2 //IN 1
#define Left_Mot_Backw 33 //IN 2


int BUILTIN_LED = 2;  //new



// Update these with values suitable for your network.
//const char* ssid = "ITEK 2nd";
//const char* password = "Four_Sprints_F21v";
const char* mqtt_server = "10.120.0.81";
const char* inTopic = "robocar";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;




void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  

}

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
      digitalWrite(Left_Mot_Forw, HIGH);
      digitalWrite(Left_Mot_Backw, LOW);
    }
    if ((char)payload[1] == 'B') {
      digitalWrite(Left_Mot_Forw, LOW);
      digitalWrite(Left_Mot_Backw, HIGH);
    }
    if ((char)payload[1] == 'S') {
      digitalWrite(Left_Mot_Forw, LOW);
      digitalWrite(Left_Mot_Backw, LOW);
    }
  }
  if ((char)payload[0] == 'R') {
    if ((char)payload[1] == 'F') {
      digitalWrite(Right_Mot_Forw, HIGH);
      digitalWrite(Right_Mot_Backw, LOW);
    }
    if ((char)payload[1] == 'B') {
      digitalWrite(Right_Mot_Forw, LOW);
      digitalWrite(Right_Mot_Backw, HIGH);
    }
    if ((char)payload[1] == 'S') {
      digitalWrite(Right_Mot_Forw, LOW);
      digitalWrite(Right_Mot_Backw, LOW);
    }
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str(),"username","password")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe(inTopic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
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
  camera_setup();

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
  camera_loop();
}
