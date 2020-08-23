from sensor_receiver import sensor_receiver
import time, socket, json


receiver = sensor_receiver()

receiver.startLoop(1)
print("Loop started")
time.sleep(10)
print("Stopping loop")
receiver.stopLoop()