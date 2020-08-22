from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt

class FixtureButton(QPushButton):
    def __init__(self, number, changeFunction):
        super().__init__()
        self.callback = changeFunction
        self.setCheckable(True)
        self.fixtureNum = number
        self.setText(str(self.fixtureNum))
        self.clicked.connect(self.fixtureClicked)
        self.setAutoDefault(False)
        self.setFocusPolicy(Qt.NoFocus)
        self.setMaximumHeight(30)

    def setFixtureNumber(self, number):
        self.fixtureNum = number

    def getFixtureNumber(self):
        return self.fixtureNum

    def fixtureClicked(self):
        self.callback(self.fixtureNum)