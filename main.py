from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_ngrok import run_with_ngrok
from flask_socketio import SocketIO, emit
import external_connections as db
import mqtt
from reconocimiento_facial import decode_url, recognize_sample_face, face_rec, save_image

import os, sys, json, time
import numpy as np 
from PIL import Image


app = Flask(__name__)
socket = SocketIO(app)
# run_with_ngrok(app)

# Constants
KNOWN_FACES_IMG = os.path.join('static', 'knwon_faces_img')
DETECTED_PERSON_IMG = os.path.join('static', 'detected_person_img')


def open_close_door():
	context = {}
	db.set_door_opened()
	context['times_opened'] = db.get_times_opened()
	context['times_known_faces'] = db.times_known_faces()
	context['times_unknown_faces'] = db.times_unknown_faces()
	context['door_status'] = True

	socket.emit('announce door', context, broadcast=True)
	mqtt.open_door()
	context['door_status'] = False
	socket.emit('announce door', context, broadcast=True)



@app.route('/')
def index():
	context = {}
	context['door_status'] = db.get_door_status()
	context['alarm_status'] = db.get_alarm_status()
	context['door_opened'] = db.get_times_opened()
	context['face_recogniced'] = db.times_known_faces()
	context['face_unrecogniced'] = db.times_unknown_faces()
	return render_template('index.html', data=context)


@app.route('/register_user', methods=['POST'])
def register_user():
	name = request.form.get('name')
	# Open from detected folder
	img = Image.open(request.form.get('img_src'))
	print('Image from detected folder readed:', name, img)
	# Save in new directory
	img.save(os.path.join(KNOWN_FACES_IMG, f'{name}.jpg'))
	# Add name to firebase
	db.set_known_people_name(name)
	return redirect(url_for('index'))


@app.route('/recfacial', methods=['POST', 'GET'])
def check_image():
	print('\nFuncion reconocimiento facial: API servidor\n')
	# Que tome la ultima foto de firebase
	video_bytes_url = db.get_last_video_url()
	if not video_bytes_url:
		return jsonify({'error': 'no hay imagen en servidor'}), 404
	# Decode de base64
	img = decode_url(video_bytes_url)

	# Que le aplique reconocimiento facial
		## Obtener los nombre de las personas registradas en firebase
	names = db.get_known_people_names()
		## Encodear las imagenes de las personas conocidas
	known_imgs_dirs = os.listdir(KNOWN_FACES_IMG)
	known_encodings = [recognize_sample_face(os.path.join(KNOWN_FACES_IMG, dir_)) for dir_ in known_imgs_dirs]
	result = ['Posible intruso']
		## Reconocer cara con la img desconocida y las conocidas
	if not len(known_encodings):
		print('\nNo se detecta la cara de nadie registrado o no hay nadie registrado\n')
		img_pil = Image.fromarray(np.asarray(img))
		save_image(img_pil, 'desconocido')
	else:
		result = face_rec(np.asarray(img), known_encodings, names)

	# Publique a traves de mqtt
	open_door = False
	person_name = result[0]
	for name in result:
		if name != 'Posible intruso':
			open_door = True
			person_name = name
	if open_door:
		print(f'Detectado a: {result}')
		open_close_door()
	else:
		print('Detectado intruso')
		alarm = mqtt.intruder()

	# Actualice interfaz de la aplicación
	try:
		img_dir = os.listdir(DETECTED_PERSON_IMG)[-1]
		socket.emit('announce image', 
		{'img_src': f'static/detected_person_img/{img_dir}', 
		'registered': open_door,
		'person': person_name})
		print(f'\nInterfaz de usuario actualizada con la imagen en {img_dir}\n')
	except Exception as e:
		print(f'\nNo hay imagen registrada o ocurrio un error:\n {e}\n')

	# Actualice base de datos de firebase
	db.set_register(open_door, person_name)
	if open_door:
		db.set_door_opened()
	print('\nBase de datos de firebase actualizada\n')
	return jsonify(0)


@app.route('/stats')
def stats():
	registers = db.get_registers()
	known_registers = []
	unknown_registers = []

	for val in registers:
		if val['registrado']:
			known_registers.append(val)
		else:
			unknown_registers.append(val)
	chart1 = {'known': len(known_registers), 'unknown': len(unknown_registers)}

	chart2 = []
	for name in db.get_known_people_names():
		y = 0
		for val in registers:
			if val['persona'] == name:
				y += 1
		chart2.append({'name': name, 'y': y})
	

	return render_template('stats.html', chart1=chart1, chart2=json.dumps(chart2))


@socket.on('open close door')
def open_close_door_socket(data):
	print('Abir y cerrar puerta')
	open_close_door()


@socket.on('change alarm')
def change_buzzer(data):
	context = {'alarm_status': data['alarm_status']}
	db.set_alarm_status(data['alarm_status'])
	emit('announce alarm', context, broadcast=True)


@socket.on('change image')
def change_cam_image(data):
	context = {}
	context['img_dir'] = data['img_dir']
	emit('announce image', context, broadcast=True)




if __name__ == "__main__":
	app.run(debug=True)
	socket.run(app)