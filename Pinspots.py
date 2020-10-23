from lib.StupidArtnet import StupidArtnet
from Config import Config
import time, random, os, json

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

        # Get channels for fixture
        with open("profiles/" + config["fixtureType"] + ".json", 'r') as p:
            self.profile = json.load(p)

        # Important constants - currently from config, eventually from fixture profile
        self.controllerIP = config["enodeIP"]
        self.numUniverses = config["numUniverses"]
        self.numPinspots = config["numFixtures"]
        self.bytesPerPacket = config["channelsPerPacket"]
        self.bytesPerFixture = self.profile["channelCount"]
        self.fixturesPerUniverse = config["fixturesPerUniverse"]

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



    def setLight(self, fixtureNum, attribute, newValue):
        # universeIndex is the index into the universes list that defines
        # which universe the fixture is in
        universeIndex = int((fixtureNum - 1) / self.fixturesPerUniverse)

        # The offset into the universe's array is the first channel of the
        # fixture plus the channel offset from the fixture profile
        offset = (((fixtureNum - 1) * self.bytesPerFixture) + (self.profile["channels"][attribute] - 1))
        
        # Correct the offset for universes above 1
        while offset >= (self.profile["channelCount"] * self.fixturesPerUniverse):
            offset -= (self.profile["channelCount"] * self.fixturesPerUniverse)

        # Debug print
        print("Offset: " + str(offset) + " Fixture: " + str(fixtureNum) + " Attribute: " + attribute + " New Value: " + str(newValue))

        # Update channel with new value
        self.universe_arrays[universeIndex][offset] = newValue

        # Commit changes to DMX
        self.update()



    def setColor(self, fixtureNum, newRedValue, newGreenValue, newBlueValue, newWhiteValue):
        # Verify that fixture supports each channel before changing them

        if "red" in self.profile["channels"]:
            self.setLight(fixtureNum, "red", newRedValue)

        if "green" in self.profile["channels"]:
            self.setLight(fixtureNum, "green", newGreenValue)

        if "blue" in self.profile["channels"]:
            self.setLight(fixtureNum, "blue", newBlueValue)

        if "white" in self.profile["channels"]:
            self.setLight(fixtureNum, "white", newWhiteValue)



    def autoTarget(self, fixtureNum):
        # Get configuration
        atConfig = Config.getConfig()["autoTarget"]

        # Set up max values
        maxBrightness = 0
        maxPan = 0
        maxTilt = 0
        currentTilt = atConfig["startTilt"]
        
        # Increment through tilt values in preconfigured steps
        while currentTilt <= atConfig["maxTilt"]:
            self.setLight(fixtureNum, "tilt", currentTilt)

            # Increment through pan values in steps of 7
            for pan in range(self.profile["channelMin"], self.profile["channelMax"], int(atConfig["panStep"] + 0.25 * (currentTilt - atConfig["startTilt"]))):
                self.setLight(fixtureNum, "pan", pan)

                # Wait for sensor value to update
                time.sleep(atConfig["waitSeconds"])

                # Get value from light sensor
                currentBrightness = int(os.popen('./getsensorvalue').read())
                print("Current brightness " + str(currentBrightness))

                # Check if new position is brightest yet
                if currentBrightness > maxBrightness:
                    maxBrightness = currentBrightness
                    maxPan = pan
                    maxTilt = currentTilt

            # Advance tilt by configured amount
            currentTilt += atConfig["tiltStep"]

        # Commit calculated best position
        print("Max values: Brightness: " + str(maxBrightness) + " Pan: " + str(maxPan) + " Tilt: " + str(maxTilt))
        self.setLight(fixtureNum, "tilt", maxTilt)
        self.setLight(fixtureNum, "pan", maxPan)



    def reset(self):
        # Populate all status arrays with zeros (lights are off)
        for universeNum in range(self.numUniverses):
            for x in range(self.bytesPerPacket):
                self.universe_arrays[universeNum][x] = self.profile["channelMin"]

        # Apply startup procedure from fixture profile
        startupSteps = self.profile["startupProcedure"]
        for fixture in range(1, self.numPinspots + 1):
            for attribute in startupSteps:
                self.setLight(fixture, attribute, startupSteps[attribute])



    def getUniverses(self):
        universes = list()
        for u in self.universe_arrays:
            universes.append(u)
        return universes



    def setUniverses(self, universes):
        for u in range(len(universes)):
            self.universe_arrays[u] = universes[u]
        self.update()
        print("Successfully updated " + str(len(universes)) + " universes")