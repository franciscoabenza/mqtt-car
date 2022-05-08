import keyboard
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
  print("connected  with code" + str(rc))
  client.subscribe("Nikola")

def on_message(client, userdata, msg):
  print(msg.topic + "  " + str(msg.payload))

clientName = "fran"
client = mqtt.Client(clientName)

client.on_connect = on_connect
client.on_message = on_message

client.connect("10.120.0.225", 1883, 60)


def main():
    keyboard.on_press_key('f', call_forward)
    keyboard.on_press_key('b', call_backward)
    keyboard.on_press_key('s', call_stop)
    keyboard.on_press_key('l', call_left)
    keyboard.on_press_key('r', call_right)
    keyboard.on_press_key('q', call_quit)
    keyboard.on_press_key('up', call_forward)
    keyboard.on_release_key('up', call_stop)
    keyboard.on_press_key('down', call_backward)
    keyboard.on_release_key('down', call_stop)
    keyboard.on_press_key('left', call_left)
    keyboard.on_release_key('left', call_stop)
    keyboard.on_press_key('right', call_right)
    keyboard.on_release_key('right', call_stop)
    keyboard.on_press_key('p', call_right)

def call_stop(char):
    print('STOP')

    client.publish("Nikola", "S")

def call_forward(char):
    print('FORWARDS')
    client.publish("Nikola","B")

def call_backward(char):
    print('BACK')
    client.publish("Nikola","F")

def call_left(char):
    print('LEFT')
    client.publish("Nikola","L")

def call_right(char):
    print('RIGHT')
    client.publish("Nikola", "R")
def call_data(char):
    print('RIGHT')
    client.publish("Nikola", "P")

def call_quit():
    print('quit')
    call_stop('x')
    quit(0)

main()

client.loop_forever()

#this is an edit made from the iPad
