import time
import cv2
import tellopy

#connect
tello = tellopy.Tello()
tello.connect()

time.sleep(2)
#takeoff
tello.takeoff()

tello.down(50)

#land
time.sleep(10)
tello.land()