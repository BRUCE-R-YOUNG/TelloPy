import time
import cv2
import tellopy

#connect
tello = tellopy.Tello()
tello.connect()

#takeoff
tello.takeoff()

#land
time.sleep(5)
tello.land()