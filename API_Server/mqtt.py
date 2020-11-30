import paho.mqtt.client as mqtt


## MQTT BROKER CREDENTIALS ------------

def on_connect(client, userdata, flags, rc):
	print('Connected to MQTT broker with code:'+str(rc))
	client.subscribe('') # <-- name string

def on_message(client, userdata, msg):
	# do something
	pass
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
servername = ''
port = 1883
username = ''
password = ''
client.connect(servername, port, 60)
client.username_pw_set(username, password)

client.loop_forever()