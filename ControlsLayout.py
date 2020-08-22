from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSlider, QLabel, QPushButton
from PyQt5.QtCore import Qt
from ControlFader import GenericControlFader, ColorControlFader

class ControlsLayout(QHBoxLayout):
    def __init__(self, pinspotWorld, buttons):
        super().__init__()
        self.pinspots = pinspotWorld
        self.buttonList = buttons

        self.intensityFader = GenericControlFader(pinspotWorld, buttons, "intensity")
        self.addLayout(self.intensityFader)
        self.panFader = GenericControlFader(pinspotWorld, buttons, "pan")
        self.addLayout(self.panFader)
        self.tiltFader = GenericControlFader(pinspotWorld, buttons, "tilt")
        self.addLayout(self.tiltFader)
        self.zoom = GenericControlFader(pinspotWorld, buttons, "zoom")
        self.addLayout(self.zoom)
        self.colorFaders = ColorControlFader(pinspotWorld, buttons)
        self.addLayout(self.colorFaders)

    def zero(self):
        self.intensityFader.zeroButtonPush()
        self.panFader.zeroButtonPush()
        self.tiltFader.zeroButtonPush()
        self.zoom.zeroButtonPush()
        self.colorFaders.zero()
