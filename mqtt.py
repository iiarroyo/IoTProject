
import time
import paho.mqtt.client as mqtt


def intruder():
    client = mqtt.Client()

    client.connect("ioticos.org", 1883, 10)
    client.username_pw_set("BQXJgocKs8eNR5U", "yypASF385flrctX")

    client.loop_start()
    time.sleep(10)

    client.publish("t4OrO5P0Ph83409/input","intruder")
    print ("\nMQTT message Sent: intruder\n")

    client.loop_stop()
    client.disconnect()
    return True


def open_door():
    client = mqtt.Client()

    client.connect("ioticos.org", 1883, 10)
    client.username_pw_set("BQXJgocKs8eNR5U", "yypASF385flrctX")

    client.loop_start()
    time.sleep(10)

    client.publish("t4OrO5P0Ph83409/input","yes")
    print ("\nMQTT message Sent: yes\n")
    time.sleep(10)
    client.publish("t4OrO5P0Ph83409/input","no")
    print ("\nMQTT message Sent: no\n")

    client.loop_stop()
    client.disconnect()
    return True