import time
import cv2
import tellopy

def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print(data)


#connect
drone  = tellopy.Tello()
drone.connect()
drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)


time.sleep(2)
#takeoff
drone.takeoff()
drone.down(70)

time.sleep(5)
drone.forward
time.sleep(5)
drone.counter_clockwise(90)

#land
time.sleep(10)
drone.land()