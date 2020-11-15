# load face_recognition
import face_recognition
import numpy as np
import cv2
import os

# load flask
from flask import Flask, jsonify
#from flask_ngrok import run_with_ngrok

# FIREBASE --------------------------------------------------
def video_from_firebase():
  test_video = "unknown_video/luis.mp4"
  video_capture = cv2.VideoCapture(test_video)
  return video_capture

def init_settings():
  # INITIAL SETTINGS
  
  # Get all the known images filenames
  for file_name in  os.listdir(known_img_dir):
    knownfaces_names.append(file_name[:-5])
    file_path = os.path.join(known_img_dir, file_name)
    # Load the image and encode
    image = face_recognition.load_image_file(file_path)
    known_images_encodings.append(face_recognition.face_encodings(image)[0])
    
#import matplotlib.pyplot as plt


def recognition(video_capture):
  result = False

  while video_capture.isOpened():
    # Read the frame
    ret, frame = video_capture.read()

    # Change from RGB to BGR and Rotate 180 degrees
    frame = cv2.rotate(frame,cv2.cv2.ROTATE_90_CLOCKWISE)
    frame = cv2.rotate(frame,cv2.cv2.ROTATE_90_CLOCKWISE)
    frame = cv2.rotate(frame,cv2.cv2.ROTATE_90_CLOCKWISE)

    # Encode
    face_locations = face_recognition.face_locations(frame, model=model)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Locate the faces
    for face_encoding, face_locations in zip(face_encodings, face_locations):
      # See if the faces are known
      matches = face_recognition.compare_faces(known_images_encodings, face_encoding, model_tolerance)
      name = "Unknown"
      # Check if there are known faces
      if True in matches:
        result = True
        name = knownfaces_names[matches.index(True)]
      print(name)
    # Plot the image
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#    plt.imshow(rgb_frame)
    # plt.show()

    return result

  video_capture.release()

# FLASK -------------------------------------------------
app = Flask(__name__)

@app.route('/')
def index():
  return "HOLA"

@app.route('/api/face_recognition')
def recognition_video():
  context = {}
  # Funcion para cargar la imagen de Firebase
  video = video_from_firebase()
  # Facial recognition
  result = recognition(video)
  # Return result
  context['recognized'] = result
  print(result)
  return jsonify(context)
  
if '__main__' == __name__:
  known_img_dir = "known_images"
  test_video = "unknown_video/luis.mp4"
  model = "cnn"
  model_tolerance = 0.5
  knownfaces_names = []
  known_images_encodings = []
  init_settings()

  app.run()
