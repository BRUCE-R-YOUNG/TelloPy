import time
import cv2
import tellopy

def handler(event, sender, data, **args):
    tello = sender
    if event is tello.EVENT_FLIGHT_DATA:
        print(data)

#connect
tello  = tellopy.Tello()
tello.connect()
tello.subscribe(tello.EVENT_FLIGHT_DATA, handler)

#takeoff
time.sleep(2)
tello.takeoff()
tello.down(70)

#forward&counter_clockwise
time.sleep(2)
tello.forward
time.sleep(2)
tello.counter_clockwise(90)

#land
time.sleep(5)
tello.land()