import socket, traceback, threading
from numpy import interp
from Pinspots import Pinspots





class android_receiver():
    host = ''
    port = 50000
    running = False
    xPos = 0.0
    yPos = 0.0





    # getVal returns the current position values
    def getVal(self):
        return (self.xPos, self.yPos)





    # Initalize and bind the socket, then start the loop
    def start(self, pinNumber):
        self.pinspots = Pinspots.getPinspotWorld()
        self.pinNumber = pinNumber

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.bind((self.host, self.port))
        print("Socket bound successfully")

        self.running = True
        self.daemon = threading.Thread(target=self.loop, args=None)
        self.daemon.start()





    # Stop loop and close the socket
    def stop(self):
        self.running = False
        self.daemon.join()
        self.s.close()





    def loop(self):
        while self.running:
            message, address = self.s.recvfrom(8192)
            messageString = message.decode("utf-8")
            valSplit = messageString.split(",")
            self.xPos = float(valSplit[2])
            self.yPos = float(valSplit[3])

            panVal = interp(self.xPos, [-10,10], [64,192])
            tiltVal = interp(self.yPos, [-10,10], [64,192])

            print("Changing pan of fixture " + str(self.pinNumber) + " to " + str(int(panVal)))
            self.pinspots.setPan(self.pinNumber, int(panVal))
            print("Changing tilt of fixture " + str(self.pinNumber) + " to " + str(int(tiltVal)))
            self.pinspots.setTilt(self.pinNumber, int(tiltVal))