import time
import cv2
from djitellopy import Tello

#connect
tello = Tello()
tello.connect()

#takeoff
tello.takeoff()

#land
time.sleep(5)
tello.land()