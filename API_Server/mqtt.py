
import paho.mqtt.client as mqtt

import time


# Callback Function on Connection with MQTT Server
def on_connect( client, userdata, flags, rc):
    print ("Connected with Code :" +str(rc))
    # Subscribe Topic from here
    client.subscribe("t4OrO5P0Ph83409/input")

# Callback Function on Receiving the Subscribed Topic/Message
def on_message( client, userdata, msg):
    # print the message received from the subscribed topic
    print ( str(msg.payload) )

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("ioticos.org",1883,15) #, 17259, 60
client.username_pw_set("BQXJgocKs8eNR5U", "yypASF385flrctX")


# client.loop_forever()
client.loop_start()
time.sleep(1)
while True:
    client.publish("t4OrO5P0Ph83409/input","Gerardo")
    print ("Message Sent")
    time.sleep(15)

client.loop_stop()
client.disconnect()
