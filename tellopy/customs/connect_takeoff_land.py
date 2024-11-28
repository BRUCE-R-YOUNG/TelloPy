import time
import cv2
import tellopy

#connect
tello = tellopy.Tello()
tello.connect()

time.sleep(2)
#takeoff
tello.takeoff()

#land
time.sleep(10)
tello.land()