from lib.StupidArtnet import StupidArtnet
import time
import random
import os

'''Pinspots implements a Singleton pattern. getPinspotWorld() can be called from anywhere'''

class Pinspots:

    instance = None


    @staticmethod
    def getPinspotWorld():
        if Pinspots.instance == None:
            Pinspots()
        return Pinspots.instance





    def __init__(self, *args, **kwargs):
        if Pinspots.instance != None:
            raise Exception("Error: Class is Singleton - Use getPinspotWorld()")
        else:
            Pinspots.instance = self
        super().__init__(*args, **kwargs)

        # Important constants - THESE WILL COME FROM CONFIG EVENTUALLY
        self.numPinspots = 48
        self.bytesPerPacket = 512    # each byte is one DMX channel
        self.bytesPerFixture = 21    # each ZCL360i in extended mode has 21 channels of DMX control
        # Create bytearrays for each universe's status
        self.universe1status = bytearray(self.bytesPerPacket)
        self.universe2status = bytearray(self.bytesPerPacket)
        # Create universes using StupidArtnet(eNode IP Address, universe, packet size) - FROM CONFIG
        self.universe1 = StupidArtnet('2.10.10.2', 0, self.bytesPerPacket)
        self.universe2 = StupidArtnet('2.10.10.2', 1, self.bytesPerPacket)
        # Print universes for testing
        print(self.universe1)
        print(self.universe2)
        # Set all lights to zero using reset method
        self.reset()
        # Start threads for each universe
        self.universe1.start()
        self.universe2.start()





    def __del__(self):
        # Reset lights and stop threads for both universes
        self.reset()
        self.universe1.stop()
        self.universe2.stop()





    def update(self):
        # Set each universe with the current status array
        self.universe1.set(self.universe1status)
        self.universe2.set(self.universe2status)





    def setIntensity(self, fixtureNum, newIntensityValue):
        # If fixture is in universe 1
        if fixtureNum < 24:
            offsets = self.getOffsetsForFixture(fixtureNum)
            self.universe1status[offsets["intensity"]] = newIntensityValue
        # Otherwise fixture is in universe 2
        else:
            offsets = self.getOffsetsForFixture(fixtureNum-24)
            self.universe2status[offsets["intensity"]] = newIntensityValue
        # Commit changes
        self.update()
        # Debug print
        print("Intensity of fixture " + str(fixtureNum) + " changed to " + str(newIntensityValue))





    def setPan(self, fixtureNum, newPanValue):
        # If fixture is in universe 1
        if fixtureNum < 24:
            offsets = self.getOffsetsForFixture(fixtureNum)
            self.universe1status[offsets["pan"]] = newPanValue
        # Otherwise fixture is in universe 2
        else:
            offsets = self.getOffsetsForFixture(fixtureNum-24)
            self.universe2status[offsets["pan"]] = newPanValue
        # Commit changes
        self.update()
        # Debug print
        print("Pan of fixture " + str(fixtureNum) + " changed to " + str(newPanValue))





    def setTilt(self, fixtureNum, newTiltValue):
        # If fixture is in universe 1
        if fixtureNum < 24:
            offsets = self.getOffsetsForFixture(fixtureNum)
            self.universe1status[offsets["tilt"]] = newTiltValue
        # Otherwise fixture is in universe 2
        else:
            offsets = self.getOffsetsForFixture(fixtureNum-24)
            self.universe2status[offsets["tilt"]] = newTiltValue
        # Commit changes
        self.update()
        # Debug print
        print("Tilt of fixture " + str(fixtureNum) + " changed to " + str(newTiltValue))





    def setZoom(self, fixtureNum, newZoomValue):
        # If fixture is in universe 1
        if fixtureNum < 24:
            offsets = self.getOffsetsForFixture(fixtureNum)
            self.universe1status[offsets["zoom"]] = newZoomValue
        # Otherwise fixture is in universe 2
        else:
            offsets = self.getOffsetsForFixture(fixtureNum-24)
            self.universe2status[offsets["zoom"]] = newZoomValue
        # Commit changes
        self.update()
        # Debug print
        print("Zoom of fixture " + str(fixtureNum) + " changed to " + str(newZoomValue))


    


    def setColor(self, fixtureNum, newRedValue, newGreenValue, newBlueValue, newWhiteValue):
        # If fixture is in universe 1
        if fixtureNum < 24:
            offsets = self.getOffsetsForFixture(fixtureNum)
            self.universe1status[offsets["red"]] = newRedValue
            self.universe1status[offsets["green"]] = newGreenValue
            self.universe1status[offsets["blue"]] = newBlueValue
            self.universe1status[offsets["white"]] = newWhiteValue
        # Otherwise fixture is in universe 2
        else:
            offsets = self.getOffsetsForFixture(fixtureNum-24)
            self.universe2status[offsets["red"]] = newRedValue
            self.universe2status[offsets["green"]] = newGreenValue
            self.universe2status[offsets["blue"]] = newBlueValue
            self.universe2status[offsets["white"]] = newWhiteValue
        # Commit changes
        self.update()





    def autoTarget(self, fixtureNum):
        # Set up max values
        maxBrightness = 0
        maxPan = 0
        maxTilt = 0
        currentTilt = 63
        # Increment through tilt values in steps of 5
        while currentTilt <= 127:
            self.setTilt(fixtureNum, currentTilt)
            print("Setting tilt to " + str(currentTilt))
            # Increment through pan values in steps of 7
            for pan in range(1,256,int(7 + 0.25*(currentTilt-63))):
                self.setPan(fixtureNum, pan)
                print("Setting pan to " + str(pan))
                time.sleep(.5)
                currentBrightness = int(os.popen('./getsensorvalue').read())
                print("Current brightness " + str(currentBrightness))
                if currentBrightness > maxBrightness:
                    maxBrightness = currentBrightness
                    maxPan = pan
                    maxTilt = currentTilt
            currentTilt += 7
        print("Max values: Brightness: " + str(maxBrightness) + " Pan: " + str(maxPan) + " Tilt: " + str(maxTilt))
        self.setTilt(fixtureNum, maxTilt)
        self.setPan(fixtureNum, maxPan)





    def reset(self):
        # Populate both status arrays with zeros (lights are off)
        for x in range(self.bytesPerPacket):
            self.universe1status[x] = 0
            self.universe2status[x] = 0

        # All values are reasonable when set to zero except shutter,
        # which will close the shutter. Open all shutters by setting to 255
        shutterIndex = 11
        while shutterIndex < (self.numPinspots/2)*self.bytesPerFixture:
            self.universe1status[shutterIndex] = 255
            self.universe2status[shutterIndex] = 255
            shutterIndex += self.bytesPerFixture

        # Send settings to lights
        self.universe1.set(self.universe1status)
        self.universe2.set(self.universe2status)





    # percentToByte takes in a percentage (0-100 inclusive)
    # and returns the corresponding value in (0-255 inclusive)
    def percentToByte(self, percent):
        percentAsFloat = float(percent/100)
        return int(percentAsFloat*255)





    # getOffsetsForFixture returns a dictionary with the bytearray index values for each fixture's parameters
    def getOffsetsForFixture(self, fixtureNum):
        # Determine first byte for fixture
        startByte = (fixtureNum - 1)*self.bytesPerFixture
        fixtureOffsets = {
            "pan" : startByte,
            "tilt" : startByte+2,
            "red" : startByte+6,
            "green" : startByte+7,
            "blue" : startByte+8,
            "white" : startByte+9,
            "shutter" : startByte+11,
            "intensity" : startByte+12,
            "zoom" : startByte+14
        }
        return fixtureOffsets


    


    def getUniverse1Status(self):
        return self.universe1status





    def getUniverse2Status(self):
        return self.universe2status





    def setUniverse1Status(self, universe1new):
        self.universe1status = universe1new
        self.update()
        print("successfully loaded universe 1")





    def setUniverse2Status(self, universe2new):
        self.universe2status = universe2new
        self.update()
        print("successfully loaded universe 2")