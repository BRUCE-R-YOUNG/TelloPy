import time
import cv2
from djitellopy import Tello

#connect
tello = Tello()
tello.connect()

#takeoff
tello.takeoff()

#moveup
time.sleep(5)
tello.move_up(50)

#movedown
time.sleep(5)
tello.move_down(50)

#land
time.sleep(5)
tello.land()