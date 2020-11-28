# import the necessary packages
import numpy as np
import urllib
import cv2
# METHOD #1: OpenCV, NumPy, and urllib
url="http://192.168.1.95/capture"
def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format
    resp = urllib.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    # return the image
    return image

url="http://192.168.1.95/capture"
