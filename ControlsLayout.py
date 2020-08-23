from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSlider, QLabel, QPushButton
from PyQt5.QtCore import Qt
from ControlFader import GenericControlFader, ColorControlFader

class ControlsLayout(QHBoxLayout):
    def __init__(self, buttons):
        super().__init__()
        self.buttonList = buttons

        self.intensityFader = GenericControlFader(buttons, "intensity")
        self.addLayout(self.intensityFader)
        self.panFader = GenericControlFader(buttons, "pan")
        self.addLayout(self.panFader)
        self.tiltFader = GenericControlFader(buttons, "tilt")
        self.addLayout(self.tiltFader)
        self.zoom = GenericControlFader(buttons, "zoom")
        self.addLayout(self.zoom)
        self.colorFaders = ColorControlFader(buttons)
        self.addLayout(self.colorFaders)

    def zero(self):
        self.intensityFader.zeroButtonPush()
        self.panFader.zeroButtonPush()
        self.tiltFader.zeroButtonPush()
        self.zoom.zeroButtonPush()
        self.colorFaders.zero()
