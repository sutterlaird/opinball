from sensor_receiver import sensor_receiver
import time, socket, json


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 50000))

for x in range(500):
    message, address = s.recvfrom(8192)
    dictionary = json.loads(message.decode('utf-8'))
    print(dictionary["accelerometerAccelerationX"])


# receiver = sensor_receiver()

# receiver.startLoop(1)
# print("Loop started")
# time.sleep(30)
# print("Stopping loop")
# receiver.stopLoop()