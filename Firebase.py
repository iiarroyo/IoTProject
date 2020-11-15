import pyrebase
#import firebase
settings ={
    'apiKey': "AIzaSyCG4Hn0vp7hV11PYU93xjIhxc996Ivj3C4",
    'authDomain': "iothola.firebaseapp.com",
    'databaseURL': "https://iothola.firebaseio.com",
    'projectId': "iothola",
    'storageBucket': "iothola.appspot.com",
    'messagingSenderId': "514308252039",
    'appId': "1:514308252039:web:08d6bccb6944f3bf5cf322",
    'measurementId': "G-5BG9G1ED5Y"}


firebase = pyrebase.initialize_app(settings)
db = firebase.database()
#storage = firebase.storage()
db.child("").push({'prueba1' : 1, 'hola': 2})
