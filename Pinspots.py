from lib.StupidArtnet import StupidArtnet
from Config import Config
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

        config = Config.getConfig()

        # Important constants - currently from config, eventually from fixture profile
        self.controllerIP = config["enodeIP"]
        self.numUniverses = config["numUniverses"]
        self.numPinspots = config["numFixtures"]
        self.bytesPerPacket = config["channelsPerPacket"]
        self.bytesPerFixture = config["channelsPerFixture"]
        self.fixturesPerUniverse = config["fixturesPerUniverse"]
        self.channelMin = config["channelMin"]
        self.channelMax = config["channelMax"]

        # Create bytearrays for each universe's status
        self.universe_arrays = list()
        for x in range(self.numUniverses):
            self.universe_arrays.append(bytearray(self.bytesPerPacket))

        # Create universes using StupidArtnet(eNode IP Address, universe, packet size)
        self.universes = list()
        for x in range(self.numUniverses):
            self.universes.append(StupidArtnet(self.controllerIP, x, self.bytesPerPacket))

            # Print universe for testing
            print(self.universes[x])

            # Start universe
            self.universes[x].start()

        # Reset lights
        self.reset()






    def __del__(self):
        # Reset lights and stop threads for both universes
        self.reset()
        for x in range(self.numUniverses):
            self.universes[x].stop()





    def update(self):
        # Set each universe with the current status array
        for x in range(self.numUniverses):
            self.universes[x].set(self.universe_arrays[x])





    def setIntensity(self, fixtureNum, newIntensityValue):
        # If fixture is in universe 1
        if fixtureNum < self.fixturesPerUniverse:
            offsets = self.getOffsetsForFixture(fixtureNum)
            self.universe_arrays[0][offsets["intensity"]] = newIntensityValue

        # Otherwise fixture is in universe 2
        else:
            offsets = self.getOffsetsForFixture(fixtureNum - self.fixturesPerUniverse)
            self.universe_arrays[1][offsets["intensity"]] = newIntensityValue
        # Commit changes
        self.update()
        # Debug print
        print("Intensity of fixture " + str(fixtureNum) + " changed to " + str(newIntensityValue))





    def setPan(self, fixtureNum, newPanValue):
        # If fixture is in universe 1
        if fixtureNum < self.fixturesPerUniverse:
            offsets = self.getOffsetsForFixture(fixtureNum)
            self.universe_arrays[0][offsets["pan"]] = newPanValue

        # Otherwise fixture is in universe 2
        else:
            offsets = self.getOffsetsForFixture(fixtureNum - self.fixturesPerUniverse)
            self.universe_arrays[1][offsets["pan"]] = newPanValue
        # Commit changes
        self.update()
        # Debug print
        print("Pan of fixture " + str(fixtureNum) + " changed to " + str(newPanValue))





    def setTilt(self, fixtureNum, newTiltValue):
        # If fixture is in universe 1
        if fixtureNum < self.fixturesPerUniverse:
            offsets = self.getOffsetsForFixture(fixtureNum)
            self.universe_arrays[0][offsets["tilt"]] = newTiltValue

        # Otherwise fixture is in universe 2
        else:
            offsets = self.getOffsetsForFixture(fixtureNum - self.fixturesPerUniverse)
            self.universe_arrays[1][offsets["tilt"]] = newTiltValue
        # Commit changes
        self.update()
        # Debug print
        print("Tilt of fixture " + str(fixtureNum) + " changed to " + str(newTiltValue))





    def setZoom(self, fixtureNum, newZoomValue):
        # If fixture is in universe 1
        if fixtureNum < self.fixturesPerUniverse:
            offsets = self.getOffsetsForFixture(fixtureNum)
            self.universe_arrays[0][offsets["zoom"]] = newZoomValue

        # Otherwise fixture is in universe 2
        else:
            offsets = self.getOffsetsForFixture(fixtureNum - self.fixturesPerUniverse)
            self.universe_arrays[1][offsets["zoom"]] = newZoomValue
        # Commit changes
        self.update()
        # Debug print
        print("Zoom of fixture " + str(fixtureNum) + " changed to " + str(newZoomValue))


    


    def setColor(self, fixtureNum, newRedValue, newGreenValue, newBlueValue, newWhiteValue):
        # If fixture is in universe 1
        if fixtureNum < self.fixturesPerUniverse:
            offsets = self.getOffsetsForFixture(fixtureNum)
            self.universe_arrays[0][offsets["red"]] = newRedValue
            self.universe_arrays[0][offsets["green"]] = newGreenValue
            self.universe_arrays[0][offsets["blue"]] = newBlueValue
            self.universe_arrays[0][offsets["white"]] = newWhiteValue

        # Otherwise fixture is in universe 2
        else:
            offsets = self.getOffsetsForFixture(fixtureNum - self.fixturesPerUniverse)
            self.universe_arrays[1][offsets["red"]] = newRedValue
            self.universe_arrays[1][offsets["green"]] = newGreenValue
            self.universe_arrays[1][offsets["blue"]] = newBlueValue
            self.universe_arrays[1][offsets["white"]] = newWhiteValue
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
            for pan in range(1, 256, int(7 + 0.25 * (currentTilt - 63))):
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
            self.universe_arrays[0][x] = self.channelMin
            self.universe_arrays[1][x] = self.channelMin

        # All values are reasonable when set to zero except shutter,
        # which will close the shutter. Open all shutters by setting to self.channelMax
        shutterIndex = 11
        while shutterIndex < (self.numPinspots/2)*self.bytesPerFixture:
            self.universe_arrays[0][shutterIndex] = self.channelMax
            self.universe_arrays[1][shutterIndex] = self.channelMax
            shutterIndex += self.bytesPerFixture

        # Send settings to lights
        for x in range(self.numUniverses):
            self.universes[x].set(self.universe_arrays[x])






    # percentToByte takes in a percentage (0-100 inclusive)
    # and returns the corresponding value in (channelMin-channelMax inclusive)
    def percentToByte(self, percent):
        percentAsFloat = float(percent/100)
        return int(percentAsFloat * self.channelMax)





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
        return self.universe_arrays[0]





    def getUniverse2Status(self):
        return self.universe_arrays[1]





    def setUniverse1Status(self, universe1new):
        self.universe_arrays[0] = universe1new
        self.update()
        print("successfully loaded universe 1")





    def setUniverse2Status(self, universe2new):
        self.universe_arrays[1] = universe2new
        self.update()
        print("successfully loaded universe 2")