import socket, traceback, threading, select, json
from numpy import interp
from Pinspots import Pinspots





class sensor_receiver():
    host = ''
    port = 50000
    running = False
    xPos = 0.0
    yPos = 0.0





    # getVal returns the current position values
    def getVal(self):
        return (self.xPos, self.yPos)





    # Initalize and bind the socket, then start the loop
    def startLoop(self, pinNumber):
        self.pinspots = Pinspots.getPinspotWorld()
        self.pinNumber = pinNumber

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.settimeout(2)
        self.s.bind((self.host, self.port))
        print("Socket bound successfully")

        self.running = True
        self.receiveDaemon = threading.Thread(target=self.daemon_loop)
        self.receiveDaemon.start()





    # Stop loop and close the socket
    def stopLoop(self):
        self.running = False
        self.receiveDaemon.join()
        self.s.close()





    def daemon_loop(self):
        while self.running:
            try:
                message, address = self.s.recvfrom(8192)
                values = json.loads(message.decode("utf-8"))

                self.xPos = values["accelerometerAccelerationX"]
                self.yPos = values["accelerometerAccelerationY"]

                panVal = interp(self.xPos, [-1,1], [64,192])
                tiltVal = interp(self.yPos, [-1,1], [64,192])

                self.pinspots.setPan(self.pinNumber, int(panVal))
                self.pinspots.setTilt(self.pinNumber, int(tiltVal))
            except:
                print("Receive timeout")