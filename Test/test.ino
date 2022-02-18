
/*
 IN
 */

#define Left_Mot_Forw 15
#define Left_Mot_Backw 12
#define Right_Mot_Forw 2
#define Right_Mot_Backw 14

void setup() {
  // set up as output pins
 pinMode(15,OUTPUT); //Connected to IN1
 pinMode(12,OUTPUT); //Connected to IN2
 pinMode(2,OUTPUT); // Connected to IN3
 pinMode(14,OUTPUT); // Connected to IN4

}

void loop() {
  //digitalWrite(Left_Mot_Forw,HIGH);
  //digitalWrite(Right_Mot_Forw,HIGH);
  
  digitalWrite(Right_Mot_Forw, HIGH);
  //delay(1000);

}