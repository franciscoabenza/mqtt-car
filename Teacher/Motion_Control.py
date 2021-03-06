# The Motion Control Class definitions
from enum import Enum
import paho.mqtt.client as mqtt



def on_connect(client, userdata, flags, rc):
  print("connected  with code" + str(rc))
  client.subscribe("robocar")

def on_message(client, userdata, msg):
  print(msg.topic + "  " + str(msg.payload))

clientName = "fran"
client = mqtt.Client(clientName)

client.on_connect = on_connect
client.on_message = on_message

client.connect("10.120.0.81", 1883, 60)



class DriveStates(Enum):
  STOP     = 0
  FORWARD  = 1
  BACKWARD = 2
  
class Motion_Control:

  def __init__(self):
    self.__Left_DriveUnit = Drive_Unit('LeftDrive')
    #self.__Left_DriveUnit.Set_Drive_State(DriveStates.FORWARD, 0.3) #For test
    self.__Right_DriveUnit = Drive_Unit('RightDrive')
    #self.__Right_DriveUnit.Set_Drive_State(DriveStates.BACKWARD, 0.7) #For test

  def Stop(self):
    self.__Left_DriveUnit.Set_Drive_State(DriveStates.STOP, 1) 
    self.__Right_DriveUnit.Set_Drive_State(DriveStates.STOP, 1) 
    
  def Forward(self, speed):
    self.__Left_DriveUnit.Set_Drive_State(DriveStates.FORWARD, speed) 
    self.__Right_DriveUnit.Set_Drive_State(DriveStates.FORWARD, speed) 

  def Backward(self, speed):
    self.__Left_DriveUnit.Set_Drive_State(DriveStates.BACKWARD, speed) 
    self.__Right_DriveUnit.Set_Drive_State(DriveStates.BACKWARD, speed) 
    
  def Left(self):
    self.__Left_DriveUnit.Set_Drive_State(DriveStates.BACKWARD, 0) 
    self.__Right_DriveUnit.Set_Drive_State(DriveStates.FORWARD, 1) 

  def Right(self):
    self.__Left_DriveUnit.Set_Drive_State(DriveStates.FORWARD, 1) 
    self.__Right_DriveUnit.Set_Drive_State(DriveStates.BACKWARD, 0) 

class Drive_Unit:

  def __init__(self, Name):
    self.__Drive_State = DriveStates.STOP
    self.__Last_Drive_State = DriveStates.STOP
    self.__Speed = 1
    self.__Name = Name
        
  def Set_Drive_State(self, Drive_State, Speed):
  
    DriveActions = {DriveStates.STOP     : self.__Drive_Stop,
                    DriveStates.FORWARD  : self.__Motor_forward,
                    DriveStates.BACKWARD : self.__Motor_backward}

    self.__Drive_State = Drive_State
    self.__Speed = Speed
    
    if Drive_State != self.__Last_Drive_State: #To avoid multiple calls to the motors
      action = DriveActions.get(Drive_State)
      action(Speed)
      self.__Last_Drive_State = Drive_State

  def __Drive_Stop(self, speed):    #This function made with a dummy speed because the action lookup 
    self.__speed = speed

    isLeft = self.__Name == "LeftDrive"
    isRight = self.__Name == "RightDrive"
    self.__speed = speed
    if isLeft:
      print("SL")
      client.publish("robocar","LS")
    elif isRight:
      print("SR")
      client.publish("robocar","RS")
      
    
  def __Motor_forward(self, speed):
    print('Motor Forward')
    isLeft = self.__Name == "LeftDrive"
    isRight = self.__Name == "RightDrive"
    self.__speed = speed
    if isLeft:
      print("FL")
      client.publish("robocar","LF")
    elif isRight:
      print("FR")
      client.publish("robocar","RF")


  def __Motor_backward(self, speed):
    print('Motor Backward')
    self.__speed = speed
    isLeft = self.__Name == "LeftDrive"
    isRight = self.__Name == "RightDrive"

    if isLeft:
      print("BL")
      client.publish("robocar","LB")
    elif isRight:
      print("BR")
      client.publish("robocar","RB")


  def Get_Drive_State(self):
    return self.__Drive_State

  def Get_Drive_Speed(self):
    return self.__Speed
