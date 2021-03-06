#The RoboCar Class definitions
from itertools import count
from User_Interface import User_Interface, Terminal_Interface, Web_Interface
from Motion_Control import Motion_Control
from enum import Enum

class States(Enum):
  STOP     = 0
  LEFT     = 1
  RIGHT    = 2
  FORWARD  = 3
  BACKWARD = 4
  #CURVE_L = 5
  #CURVE_R = 6
  
class RoboCar:

  def __init__(self, Name, IF_Type):
    self.__Name = Name
    self.__IF_Type = IF_Type
    self.__State = States.STOP

    # User Interface Object is created and RoboCar object reference is passed down
    if IF_Type == 'Terminal':
      self.MyFace = Terminal_Interface(self)
    elif IF_Type == 'Web':
      self.MyFace = Web_Interface(self)

    # Motion Control Object is created 

    self.MyMotion = Motion_Control()

    #Start the Main RoboCar Loop
    self.Main_Loop()

  def Stop(self):
    self.MyMotion.Stop()

  def GoLeft(self):
    self.MyMotion.Left()

  def GoRight(self):
    self.MyMotion.Right()

  def GoForward(self):
    self.MyMotion.Forward(1)

  def GoBackward(self):
    self.MyMotion.Backward(0)

  def Get_Interface_Type(self):
    return self.__IF_Type

  def Set_Name(self, Name):
    self.__Name = Name

  def Get_Name(self):
    return self.__Name

  def Set_State(self, State):
    self.__State = State

  def Get_State(self):
    return self.__State

  def Main_Loop(self):

    quit = False
    Stop_Count = 0
    STOPLIMIT = 1000 #used to be 1000 🇩🇪
    
    actions = {States.STOP:     self.Stop,
               States.LEFT:     self.GoLeft,
               States.RIGHT:    self.GoRight,
               States.FORWARD:  self.GoForward,
               States.BACKWARD: self.GoBackward,}
               #States.CURVE_L: self.CurveLeft,
               #States.CURVE_R: self.CurveRight}

    while not quit:
      
      key = self.MyFace.Read_Key()
  
      if key == 'esc':
        quit = True
  
      if key == 'Arrow_Up':
        self.Set_State(States.FORWARD)
      elif key == 'Arrow_Down':
        self.Set_State(States.BACKWARD)
      elif key == 'Arrow_Left':
        self.Set_State(States.LEFT)
      elif key == 'Arrow_Right':
        self.Set_State(States.RIGHT)
      #elif key == 'Curve_Left':
      #  self.Set_State(States.CURVE_L)
      #elif key == 'Curve_Right':
      #  self.Set_State(States.CURVE_R)
      
      else:                                    #The problem I got here is that it doesnt enter the else on realese I have to click another key
        Stop_Count += 1
        if Stop_Count > STOPLIMIT:
          self.Set_State(States.STOP)
          Stop_Count = 0
      
      action = actions.get(self.__State)
      action()
