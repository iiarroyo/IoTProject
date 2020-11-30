import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import random
from datetime import datetime, date


## FIREBASE CREDENTIALS ---------------
cred = credentials.Certificate('private/iotv2-a811e-firebase-adminsdk-lo9wt-1a8ea97452.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iotv2-a811e.firebaseio.com/'
})
root_ref = db.reference('/')
esp32_ref = db.reference('esp32-cam')
known_people_ref = db.reference('personas_registradas')
register_ref = db.reference('registro')
door_opened_ref = db.reference('puerta_abierta')


## ESTADO DE LOS REGISTROS ------------
def get_registers():
	query_set = register_ref.get()
	return query_set.items()

def set_register(known_boolean, person_id):
	new_register = {
		'registrado': known_boolean,
		'persona': person_id,
		'hora_entrada':  str(datetime.now().time()),
		'facha_entrada': date.today().strftime('%d/%m/%Y')
	}
	return register_ref.push(new_register)

def get_knwon_people_names():
	query_set = known_people_ref.get()
	return query_set.items()

def set_known_people(name):
	new_people = {'name': name}
	return known_people_ref.push(new_people)

def get_door_opened():
	query_set = door_opened_ref.get()
	return query_set.items()

def set_door_opened():
	new_door_opened = {
		'hora':  str(datetime.now().time()),
		'facha': date.today().strftime('%d/%m/%Y') 
	}
	return door_opened_ref.push(new_door_opened)


## ESTADO DE LOS ACTUADORES --------
DOOR_STATUS = False
ALARM_STATUS = False
def get_door_status():
	# Connect to mqtt broker
	return DOOR_STATUS

def set_door_status(status):
	# Connect to mqtt broker
	DOOR_STATUS = status

def get_alarm_status():
	# Connect to mqtt broker
	return ALARM_STATUS

def set_alarm_status(status):
	# Connect to mqtt broker
	ALARM_STATUS = status


## ESTADO DE LAS STATS --------------
def get_times_opened():
	return len(get_door_opened())

def times_known_faces():
	counter = 0
	for id, data in get_registers():
		for key in data:
			if data[key]['registrado'] == True:
				counter += 1
	return counter

def times_unknown_faces():
	counter = 0
	for id, data in get_registers():
		for key in data:
			if data[key]['registrado'] == False:
				counter += 1
	return counter


## ESTADO DE LAS IMÁGENES ----------
def get_last_video_url():
	# Get the list of all videos from RTDB
	url_lists = list(range(10))
	dict = esp32_ref.get()
	for p_id, p_info in dict.items():
		for key in p_info:
			url_lists.append(p_info[key])

	# Get last url
	url = url_lists[-1][23:]

	# Clean image bytes
	url = url.replace('%2B','+')
	url = url.replace('%2F','/')
	url = url.replace('%3D','=')

	return url