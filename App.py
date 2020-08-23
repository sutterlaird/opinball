from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QVBoxLayout, QWidget, QGridLayout, QHBoxLayout, QInputDialog, QLineEdit, QFileDialog
from FixtureButton import FixtureButton
from Pinspots import Pinspots
from FixtureButtonLayout import FixtureButtonLayout
from ControlsLayout import ControlsLayout
from MainAppButtons import StopButton, SaveShowButton, LoadShowButton, SingleMultiButton, SelectAllButton, DeselectAllButton, AutoTargetButton, PhoneControlButton
import time

# Initialize application and window
app = QApplication([])
window = QWidget()
window.setStyleSheet(open("style.qss", "r").read())
window.setWindowTitle("Sutter's Pinspot Controller")

# Create pinspot model
pinspotWorld = Pinspots.getPinspotWorld()





# ButtonClick is called whenever a fixture button is clicked
# Enforces single or multi select policy
def buttonClick(buttonNum):
    # If single/multi select button is not set to multi, uncheck all other buttons
    if not singlemulti.isChecked():
        for button in buttonList:
            if button.isChecked() and button.getFixtureNumber() != buttonNum:
                button.setChecked(False)
                button.repaint()





# Create list of buttons, one per fixture
buttonList = list()
for x in range(pinspotWorld.numPinspots):
    button = FixtureButton(x+1, buttonClick)
    buttonList.append(button)

# Create grid layout for room map
grid = FixtureButtonLayout(buttonList)
controls = ControlsLayout(buttonList)

# Create vertical layout for elements
verticalLayout = QVBoxLayout()

# Create horizontal layout for bottom elements
bottomHorizLayout1 = QHBoxLayout()
bottomHorizLayout2 = QHBoxLayout()
stop = StopButton(buttonList, controls.zero)
save = SaveShowButton()
load = LoadShowButton()
singlemulti = SingleMultiButton()
selectAll = SelectAllButton(buttonList, singlemulti)
deselectAll = DeselectAllButton(buttonList)
autotarget = AutoTargetButton(buttonList)
phone = PhoneControlButton(buttonList)

bottomHorizLayout1.addWidget(autotarget)
bottomHorizLayout1.addWidget(selectAll)
bottomHorizLayout1.addWidget(deselectAll)
bottomHorizLayout1.addWidget(singlemulti)
bottomHorizLayout2.addWidget(stop)
bottomHorizLayout2.addWidget(save)
bottomHorizLayout2.addWidget(load)
bottomHorizLayout2.addWidget(phone)


# Add layouts to master layout
# verticalLayout.addLayout(topHorizLayout)
verticalLayout.addLayout(grid)
verticalLayout.addLayout(bottomHorizLayout1)
verticalLayout.addLayout(bottomHorizLayout2)

verticalLayout.addLayout(controls)


# Add master layout and make it all happen
window.setLayout(verticalLayout)
window.show()
app.exec_()