import face_recognition
from PIL import Image, ImageDraw

import requests
from io import BytesIO
from numpy import asarray
import base64, os
from datetime import datetime


DETECTED_IMG_DIR = os.path.join('static', 'detected_person_img')
KNWON_IMG_DIR = os.path.join('static', 'knwon_faces_img')


# Decode images from URL safe base64
def decode_url(url):
	im64 = base64.b64decode(url)
	imageFile = Image.open(BytesIO(im64))
	image = imageFile.convert('RGB')
	print('- Imagen decodificada')
	return image


# Encode sample image an return encoding
def recognize_sample_face(img_url):
	img = face_recognition.load_image_file(img_url)
	encodings = face_recognition.face_encodings(img)
	if not len(encodings):
		return []
	img_encoding = encodings[0]
	print(f'- Encodeado imagen de usuario {img_url} registrado')
	return img_encoding


def save_image(pil_image, name):
	print('- Guardando imagen')
	pil_image.save(os.path.join(DETECTED_IMG_DIR, f'_{datetime.today().strftime("%H%M%S")}_{name}.jpg'))


# Face recognition algorithm
def face_rec(img_arr, known_face_encodings, known_face_names):
	print('- Empieza proceso de reconocimiento facial')
	# Stop when no face detected
	if not len(known_face_encodings):
		raise Exception('no se recibió buen enconding de la imagen nueva')
		return ["Posible intruso"]
	if not len(known_face_encodings[0]):
		raise Exception('no se recibió buen enconding de la imagen nueva')
		return ["Posible intruso"]
	# Upload image
	pil_image = Image.fromarray(img_arr)
	# Draw sets
	draw = ImageDraw.Draw(pil_image)
	# Get faces encodings
	face_locations = face_recognition.face_locations(img_arr)
	face_encodings = face_recognition.face_encodings(img_arr, face_locations)
	
	# Recognice faces
	names = ["Posible intruso"]
	save_name = ''
	img_sent = False
	recognized_people = []
	for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
		# See if the face is a match for the known face(s)
		matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

		name = "Posible intruso"
		if True in matches:
			first_match_index = matches.index(True)
			name = known_face_names[first_match_index]
			save_image(pil_image, name)
			img_sent = True
		names.append(name)

	# Save image if noone was detected
	if not img_sent:
		save_image(pil_image, 'Intruso')
	# Remove the drawing library from memory as per the Pillow docs
	del draw

	print('Reconocimiento facial terminado')
	return names