
import time
import paho.mqtt.client as mqtt


def intruder():
    client = mqtt.Client()

    client.connect("ioticos.org", 1883, 15)
    client.username_pw_set("BQXJgocKs8eNR5U", "yypASF385flrctX")

    client.loop_start()
    time.sleep(1)

    client.publish("t4OrO5P0Ph83409/input","intruder")
    print ("Message Sent")

    client.loop_stop()
    client.disconnect()
    return True


def open_door(msg):
    client = mqtt.Client()

    client.connect("ioticos.org", 1883, 15)
    client.username_pw_set("BQXJgocKs8eNR5U", "yypASF385flrctX")

    client.loop_start()
    time.sleep(1)

    client.publish("t4OrO5P0Ph83409/input","yes")
    print ("Message Sent")
    time.sleep(15)
    client.publish("t4OrO5P0Ph83409/input","no")

    client.loop_stop()
    client.disconnect()
    return True