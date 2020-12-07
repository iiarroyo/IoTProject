import face_recognition
from PIL import Image, ImageDraw
import numpy as np

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import requests
from io import BytesIO
from numpy import asarray
import base64

# Fetch the service account key JSON file contents
cred = credentials.Certificate('private/iotv2-a811e-firebase-adminsdk-lo9wt-1a8ea97452.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iotv2-a811e.firebaseio.com/'
})
ref = db.reference('esp32-cam')
#dict = {u'-MNGnGyD8BkFvCkFFwql': {u'photo': u'data_quetal'}, u'-MNGnJOoFB5lR3arOSUV': {u'photo': u'data_hola'}}

url_lists = list(range(10))

dict = ref.get()
for p_id, p_info in dict.items():
    for key in p_info:
#        print(p_info[key])
        url_lists.append(p_info[key]) 


url = url_lists[-1][23:] # last url from realtime database
#LIMPIAR STRING
# print(url)

url = url.replace('%2B','+')
url = url.replace('%2F','/')
url = url.replace('%3D','=')

im64 = base64.b64decode(url)
# print(data3)
imageFile = Image.open(BytesIO(im64))
#
image = imageFile.convert('RGB')
# image.save('audacious.jpg')




# Load an image with an unknown face
#unknown_image = face_recognition.load_image_file("testUnknownImages/index.jpg") # de archivo
unknown_image=asarray(image)# de URL

# Load a sample picture and learn how to recognize it.
isidra_image = face_recognition.load_image_file("knownImages/Isidra.jpg")
isidra_face_encoding = face_recognition.face_encodings(isidra_image)[0]

# Load a second sample picture and learn how to recognize it.
macaria_image = face_recognition.load_image_file("knownImages/Macaria.jpg")
macaria_face_encoding = face_recognition.face_encodings(macaria_image)[0]

israel_image = face_recognition.load_image_file("knownImages/Israel.jpg")
israel_face_encoding = face_recognition.face_encodings(israel_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    isidra_face_encoding,
    macaria_face_encoding,
    israel_face_encoding
]
known_face_names = [
    "Isidra",
    "Macaria",
    "Israel"
]


# Find all the faces and face encodings in the unknown image
face_locations = face_recognition.face_locations(unknown_image)
face_encodings = face_recognition.face_encodings(unknown_image, face_locations)


pil_image = Image.fromarray(unknown_image)
draw = ImageDraw.Draw(pil_image)

# Loop through each face found in the unknown image
for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
    # See if the face is a match for the known face(s)
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    name = "Posible intruso"

    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]

    # Draw a box around the face using the Pillow module
    draw.rectangle(((left, top), (right, bottom)), outline=(48, 63, 159))

    # Draw a label with a name below the face
    text_width, text_height = draw.textsize(name)
    draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(48, 63, 159), outline=(48, 63, 159))
    draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 0))


# Remove the drawing library from memory as per the Pillow docs
del draw

pil_image.show()
