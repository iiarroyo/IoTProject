from flask import Flask, render_template
from flask_ngrok import run_with_ngrok
from flask_socketio import SocketIO, emit
from external_connections import *
# from reconocimiento_facial import decode_url, recognize_sample_face, face_rec

import os, sys, json


app = Flask(__name__)
socket = SocketIO(app)
# run_with_ngrok(app)


@app.route('/')
def index():
	context = {}
	context['door_status'] = get_door_status()
	context['alarm_status'] = get_alarm_status()
	context['times_opened'] = get_times_opened()
	context['times_known_faces'] = times_known_faces()
	context['times_unknown_faces'] = times_unknown_faces()
	return render_template('index.html', data=context)


@app.route('/recfacial', methods=['POST'])
def check_image(data):
	# Encode known faces

	video_bytes_url = get_last_video_url()

	set_door_status(data['status'])


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
	set_door_status(data['door_status'])
	context['times_opened'] = get_times_opened()
	context['times_known_faces'] = times_known_faces()
	context['times_unknown_faces'] = times_unknown_faces()
	emit('announce door', context, broadcast=True)


@socket.on('change alarm')
def change_buzzer(data):
	context = {'alarm_status': data['alarm_status']}
	set_alarm_status(data['alarm_status'])
	emit('announce alarm', context, broadcast=True)


@socket.on('change image')
def change_cam_image(data):
	context = {}
	context['img_dir'] = data['img_dir']
	emit('announce image', context, broadcast=True)



if __name__ == "__main__":
	app.run(debug=True)
	socket.run(app)