import face_recognition
from PIL import Image, ImageDraw

import requests
from io import BytesIO
from numpy import asarray
import base64
import os


DETECTED_IMG_DIR = 'static/detected_person_img'
KNWON_IMG_DIR = 'static/knwon_faces_img'


# Decode images from URL safe base64
def decode_url(url):
	im64 = base64.b64decode(url)
	imageFile = Image.open(BytesIO(im64))
	image = imageFile.convert('RGB')
	return image

# Encode sample image an return encoding
def recognize_sample_face(img_url):
	img = face_recognition.load_image_file(img_url)
	img_encoding = face_recognition.face_encodings(img)[0]
	return img_encoding


def face_rec(img_arr, known_face_encodings, known_face_names):
	# Drawing set
	pil_image = Image.fromarray(img_arr)
	draw = ImageDraw.Draw(pil_image)
	# Get faces encodings
	face_locations = face_recognition.face_locations(img_arr)
	face_encodings = face_recognition.face_encodings(img_arr, face_locations)
	
	# Recognice faces
	names = ["Posible intruso"]
	recognized_people = []
	for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
		# See if the face is a match for the known face(s)
		matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

		name = "Posible intruso"
		if True in matches:
			first_match_index = matches.index(True)
			name = known_face_names[first_match_index]
		names.append(name)

		# Draw a box around the face using the Pillow module
		draw.rectangle(((left, top), (right, bottom)), outline=(48, 63, 159))
		text_width, text_height = draw.textsize(name)
		draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(48, 63, 159), outline=(48, 63, 159))
		draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 0))
	
	# Save image
	pil_image.save(os.path.join(DETECTED_IMG_DIR, f'{names[0]}_detected.jpg'))
	# Remove the drawing library from memory as per the Pillow docs
	del draw

	return names