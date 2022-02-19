import keyboard
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

client.connect("192.168.1.60", 1883, 60)


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


def call_stop(char):
    print('STOP')

    client.publish("robocar", "S")


def call_forward(char):
    print('FORWARDS')
    client.publish("robocar","F")

def call_backward(char):
    print('BACK')
    client.publish("robocar","B")

def call_left(char):
    print('LEFT')
    client.publish("robocar","L")

def call_right(char):
    print('RIGHT')
    client.publish("robocar", "R")

def call_quit():
    print('quit')
    call_stop('x')
    quit(0)

main()

client.loop_forever()