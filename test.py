from sensor_receiver import sensor_receiver
import time

receiver = sensor_receiver()

receiver.startLoop(1)
time.sleep(10)
receiver.stopLoop()