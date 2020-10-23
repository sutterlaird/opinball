from PyQt5.QtWidgets import QVBoxLayout, QSlider, QLabel, QPushButton
from PyQt5.QtCore import Qt
from Pinspots import Pinspots





# GenericControlFader is used to generate an intensity, pan, tilt, or zoom fader
class GenericControlFader(QVBoxLayout):
    # Constants
    sliderMax = 255
    sliderMin = 0



    def __init__(self, buttons, newType):
        super().__init__()
        self.pinspots = Pinspots.getPinspotWorld()
        self.buttonList = buttons
        self.sliderType = newType

        # Create label for slider
        faderLabel = QLabel(self.sliderType.title())
        self.addWidget(faderLabel)

        # Create Max Button for slider
        fullButton = QPushButton("Full")
        fullButton.setAutoDefault(False)
        fullButton.setFocusPolicy(Qt.NoFocus)
        fullButton.clicked.connect(self.fullButtonPush)
        fullButton.setFixedWidth(70)
        self.addWidget(fullButton)

        # Create Zero Button for slider
        zeroButton = QPushButton("Zero")
        zeroButton.setAutoDefault(False)
        zeroButton.setFocusPolicy(Qt.NoFocus)
        zeroButton.clicked.connect(self.zeroButtonPush)
        self.addWidget(zeroButton)

        # Setup slider
        self.slider = QSlider(Qt.Vertical)
        self.slider.setFocusPolicy(Qt.NoFocus)
        self.slider.setTickPosition(QSlider.NoTicks)
        self.slider.setSingleStep(1)
        self.slider.valueChanged.connect(self.sliderChange)
        self.slider.setMinimum(self.sliderMin)
        self.slider.setMaximum(self.sliderMax)
        self.slider.setMinimumHeight(200)
        self.addWidget(self.slider)

        # Setup label
        self.valueLabel = QLabel("0")
        self.addWidget(self.valueLabel)

        self.setAlignment(faderLabel, Qt.AlignCenter)
        self.setAlignment(self.slider, Qt.AlignCenter)
        self.setAlignment(self.valueLabel, Qt.AlignCenter)



    # sliderChange handles the movement of the slider,
    # changing the value of the selected fixtures
    def sliderChange(self):
        newValue = self.slider.value()
        self.valueChange(newValue)



    # fullButtonPush is called when the full button is pushed
    def fullButtonPush(self):
        self.slider.setValue(self.slider.maximum())



    # zeroButtonPush is called when the zero button is pushed
    def zeroButtonPush(self):
        self.slider.setValue(self.slider.minimum())



    # valueChange updates the correct value for all checked fixtures
    def valueChange(self, newValue):
        self.valueLabel.setText(str(newValue))
        self.valueLabel.repaint()
        for button in self.buttonList:
            if button.isChecked():
                self.pinspots.setLight(button.getFixtureNumber(), self.sliderType, newValue)





# ColorControlFader generates a QVBoxLayout with four sliders for color
class ColorControlFader(QVBoxLayout):
    def __init__(self, buttons):
        super().__init__()
        self.pinspots = Pinspots.getPinspotWorld()
        self.buttonList = buttons
        self.colorValues = list()

        # Constants
        self.sliderMin = self.pinspots.profile["channelMin"]
        self.sliderMax = self.pinspots.profile["channelMax"]

        # Populate colorValues with four zeros
        for x in range(4):
            self.colorValues.append(self.sliderMin)

        # Create label for section
        faderLabel = QLabel("Color")
        self.addWidget(faderLabel)

        # Create label for red slider
        redLabel = QLabel("Red")
        self.addWidget(redLabel)

        # Setup red slider
        self.redSlider = QSlider(Qt.Horizontal)
        self.redSlider.setFocusPolicy(Qt.NoFocus)
        self.redSlider.setTickPosition(QSlider.NoTicks)
        self.redSlider.setSingleStep(1)
        self.redSlider.valueChanged.connect(self.anySliderChange)
        self.redSlider.setMinimum(self.sliderMin)
        self.redSlider.setMaximum(self.sliderMax)
        self.addWidget(self.redSlider)

        # Create label for green slider
        greenLabel = QLabel("Green")
        self.addWidget(greenLabel)

        # Setup green slider
        self.greenSlider = QSlider(Qt.Horizontal)
        self.greenSlider.setFocusPolicy(Qt.NoFocus)
        self.greenSlider.setTickPosition(QSlider.NoTicks)
        self.greenSlider.setSingleStep(1)
        self.greenSlider.valueChanged.connect(self.anySliderChange)
        self.greenSlider.setMinimum(self.sliderMin)
        self.greenSlider.setMaximum(self.sliderMax)
        self.addWidget(self.greenSlider)

        # Create label for blue slider
        blueLabel = QLabel("Blue")
        self.addWidget(blueLabel)

        # Setup blue slider
        self.blueSlider = QSlider(Qt.Horizontal)
        self.blueSlider.setFocusPolicy(Qt.NoFocus)
        self.blueSlider.setTickPosition(QSlider.NoTicks)
        self.blueSlider.setSingleStep(1)
        self.blueSlider.valueChanged.connect(self.anySliderChange)
        self.blueSlider.setMinimum(self.sliderMin)
        self.blueSlider.setMaximum(self.sliderMax)
        self.addWidget(self.blueSlider)

        # Create label for white slider
        whiteLabel = QLabel("White")
        self.addWidget(whiteLabel)

        # Setup white slider
        self.whiteSlider = QSlider(Qt.Horizontal)
        self.whiteSlider.setFocusPolicy(Qt.NoFocus)
        self.whiteSlider.setTickPosition(QSlider.NoTicks)
        self.whiteSlider.setSingleStep(1)
        self.whiteSlider.valueChanged.connect(self.anySliderChange)
        self.whiteSlider.setMinimum(self.sliderMin)
        self.whiteSlider.setMaximum(self.sliderMax)
        self.addWidget(self.whiteSlider)

        # Setup label
        self.valueLabel = QLabel("R: 000  G: 000  B: 000  W: 000  Hex: #000000")
        self.addWidget(self.valueLabel)



    # anySliderChange is called whenever a slider is moved
    def anySliderChange(self):
        self.colorValues[0] = self.redSlider.value()
        self.colorValues[1] = self.greenSlider.value()
        self.colorValues[2] = self.blueSlider.value()
        self.colorValues[3] = self.whiteSlider.value()
        self.update()



    def zero(self):
        self.redSlider.setValue(self.redSlider.minimum())
        self.greenSlider.setValue(self.greenSlider.minimum())
        self.blueSlider.setValue(self.blueSlider.minimum())
        self.whiteSlider.setValue(self.whiteSlider.minimum())



    # Update updates the color value label and pushes the color changes to the fixtures
    def update(self):
        hexValue = "#" + str(hex(self.colorValues[0])[2:].zfill(2)) + str(hex(self.colorValues[1])[2:].zfill(2)) + str(hex(self.colorValues[2])[2:].zfill(2))
        self.valueLabel.setText("R: " + str(self.colorValues[0]).zfill(3) + "  G: " + str(self.colorValues[1]).zfill(3) + "  B: " + str(self.colorValues[2]).zfill(3) + "  W: " + str(self.colorValues[3]).zfill(3) + "  Hex: " + hexValue)
        self.valueLabel.repaint()
        for button in self.buttonList:
            if button.isChecked():
                self.pinspots.setColor(button.getFixtureNumber(), self.colorValues[0], self.colorValues[1], self.colorValues[2], self.colorValues[3])