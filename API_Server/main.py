from flask import Flask, render_template, jsonify, request
from flask_ngrok import run_with_ngrok
from flask_socketio import SocketIO, emit
import external_connections as db
import mqtt
# from reconocimiento_facial import decode_url, recognize_sample_face, face_rec

import os, sys, json, time


app = Flask(__name__)
socket = SocketIO(app)
run_with_ngrok(app)


@app.route('/')
def index():
	context = {}
	context['door_status'] = db.get_door_status()
	context['alarm_status'] = db.get_alarm_status()
	context['times_opened'] = db.get_times_opened()
	context['times_known_faces'] = db.times_known_faces()
	context['times_unknown_faces'] = db.times_unknown_faces()
	return render_template('index.html', data=context)


@app.route('/recfacial', methods=['POST', 'GET'])
def check_image():
	print('Funcion reconocimiento facial: API servidor')
	"""
	# Que tome la ultima foto de firebase
	video_bytes_url = db.get_last_video_url()
	# Decode de base64
	img = decode_url(video_bytes_url)
	# Que le aplique reconocimiento facial
		## Obtener los nombre de las personas registradas en firebase
	names = db.get_known_people_names()
		## Encodear las imagenes de las personas conocidas con el dir de la img: '/isra.jpg'
	known_imgs_dirs = os.listdir('knwon_faces_img')
	known_encodings = [recognize_sample_face(dir_) for dir_ in known_imgs_dirs]
		## Reconocer cara con la img desconocida y las conocidas
	result = face_rec(img, known_encodings, names)
	"""
	result = ['Javier']
	# Publique a traves de mqtt
	open_door = False
	person_name = result[0]
	for name in result:
		if name != 'Posible intruso':
			open_door = True
			person_name = ''
	if open_door:
		opened = mqtt.open_door()
	else:
		alarm = mqtt.intruder()
	# Actualice interfaz de la aplicación
	try:
		img_dir = os.listdir('static/detected_person_img')[-1]
		socket.emit('announce image', {'img_src': f'static/detected_person_img/{img_dir}', 'registered': open_door})
	except Exception as e:
		print(f'No hay imagen registrada o ocurrio un error:\n {e}')
	# Actualice base de datos de firebase
	db.set_register(open_door, person_name)

	if request.method == 'GET':
		return jsonify(0)


@app.route('/stats')
def stats():
	chart1 = {'known': 13, 'unknown': 6}
	chart2 = [{'name': 'Israel', 'y': 6},
			{'name': 'Javier', 'y': 5},
			{'name': 'Gerardo', 'y': 8},
			{'name': 'Luis', 'y': 6}]
	return render_template('stats.html', chart1=chart1, chart2=json.dumps(chart2))


@socket.on('change door')
def open_close_door(data):
	context = {'door_status': data['door_status']}
	db.set_door_status(data['door_status'])
	context['times_opened'] = db.get_times_opened()
	context['times_known_faces'] = db.times_known_faces()
	context['times_unknown_faces'] = db.times_unknown_faces()
	emit('announce door', context, broadcast=True)


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
	app.run()
	socket.run(app)