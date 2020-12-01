
import time
import paho.mqtt.client as mqtt

client = mqtt.Client()

client.connect("ioticos.org", 1883, 15)
client.username_pw_set("BQXJgocKs8eNR5U", "yypASF385flrctX")


# client.loop_forever()
client.loop_start()
time.sleep(1)
while True:
    client.publish("t4OrO5P0Ph83409/input","Javier")
    print ("Message Sent")
    time.sleep(15)

client.loop_stop()
client.disconnect()
