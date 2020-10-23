from PyQt5.QtWidgets import QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from SensorDialog import SensorDialog
from Pinspots import Pinspots
from Config import Config





class StopButton(QPushButton):
    def __init__(self, buttonlist, callback):
        super().__init__()
        self.callback = callback
        self.pinspots = Pinspots.getPinspotWorld()
        self.buttons = buttonlist
        self.setText("Stop All")
        self.clicked.connect(self.onGoClicked)
        self.setAutoDefault(False)
        self.setFocusPolicy(Qt.NoFocus)





    def onGoClicked(self):
        print("Stop clicked!")
        self.pinspots.reset()
        for button in self.buttons:
            if button.isChecked():
                button.setChecked(False)
                button.repaint()
        self.callback()





# SaveShowButton creates a Save Show button that opens a file chooser
# and allows the user to save the show
class SaveShowButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.pinspots = Pinspots.getPinspotWorld()
        self.setText("Save Show")
        self.clicked.connect(self.onSaveClicked)
        self.setAutoDefault(False)
        self.setFocusPolicy(Qt.NoFocus)





    def onSaveClicked(self):
        # Open file chooser dialog and get new file name
        newFileName, _ = QFileDialog.getSaveFileName(self,"Save Show File","","Pinspot Show Files (*.opinball)", options=QFileDialog.Options())
        if newFileName:
            newSaveFile = open(newFileName + ".opinball", "w+b")
            for universe in self.pinspots.getUniverses():
                newSaveFile.write(universe)





class LoadShowButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.pinspots = Pinspots.getPinspotWorld()
        self.config = Config.getConfig()
        self.setText("Load Show")
        self.clicked.connect(self.onLoadClicked)
        self.setAutoDefault(False)
        self.setFocusPolicy(Qt.NoFocus)





    def onLoadClicked(self):
        print("Load clicked")
        loadFileName, _ = QFileDialog.getOpenFileName(self,"Select Show File", "","Pinspot Show Files (*.opinball)", options=QFileDialog.Options())
        if loadFileName:
            print("Loading from " + loadFileName)
            newLoadFile = open(loadFileName, "r+b")
            universes = list()
            for u in range(self.config["numUniverses"]):
                universes.append(bytearray(newLoadFile.read(self.config["channelsPerPacket"])))
            self.pinspots.setUniverses(universes)





class SelectAllButton(QPushButton):
    def __init__(self, buttonList, switchButton):
        super().__init__()
        self.singleMulti = switchButton
        self.buttons = buttonList
        self.setText("Select All")
        self.clicked.connect(self.onSelectClicked)
        self.setAutoDefault(False)
        self.setFocusPolicy(Qt.NoFocus)





    def onSelectClicked(self):
        # Change single/multi select mode to multi
        self.singleMulti.setChecked(True)
        self.singleMulti.buttonClicked()
        self.singleMulti.repaint()
        # Check all buttons
        for button in self.buttons:
            button.setChecked(True)
            button.repaint()





class DeselectAllButton(QPushButton):
    def __init__(self, buttonList):
        super().__init__()
        self.buttons = buttonList
        self.setText("Deselect All")
        self.clicked.connect(self.onDeselectClicked)
        self.setAutoDefault(False)
        self.setFocusPolicy(Qt.NoFocus)





    def onDeselectClicked(self):
        for button in self.buttons:
            button.setChecked(False)
            button.repaint()





class SingleMultiButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setCheckable(True)
        self.setText("Single")
        self.clicked.connect(self.buttonClicked)
        self.setAutoDefault(False)
        self.setFocusPolicy(Qt.NoFocus)
        self.setChecked(False)





    def buttonClicked(self):
        if self.isChecked() == True:
            self.setText("Multi")
            self.repaint()
        else:
            self.setText("Single")
            self.repaint()





class AutoTargetButton(QPushButton):
    def __init__(self, buttonList):
        super().__init__()
        self.buttons = buttonList
        self.pinspots = Pinspots.getPinspotWorld()
        self.setText("AutoTarget")
        self.clicked.connect(self.onTargetClicked)
        self.setAutoDefault(False)
        self.setFocusPolicy(Qt.NoFocus)





    def onTargetClicked(self):
        checkedButtonNumbers = list()
        for button in self.buttons:
            if button.isChecked() == True:
                checkedButtonNumbers.append(button.getFixtureNumber())
        if len(checkedButtonNumbers) != 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("AutoTarget Failed")
            msg.setInformativeText("Exactly One Fixture Must Be Selected")
            msg.setWindowTitle("AutoTarget Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            self.pinspots.autoTarget(checkedButtonNumbers[0])





class PhoneControlButton(QPushButton):
    def __init__(self, buttonList):
        super().__init__()
        self.buttons = buttonList
        self.pinspots = Pinspots.getPinspotWorld()
        self.setText("Sensor Control")
        self.clicked.connect(self.onTargetClicked)
        self.setAutoDefault(False)
        self.setFocusPolicy(Qt.NoFocus)





    def onTargetClicked(self):
        checkedButtonNumbers = list()
        for button in self.buttons:
            if button.isChecked() == True:
                checkedButtonNumbers.append(button.getFixtureNumber())
        if len(checkedButtonNumbers) != 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Sensor Control Failed")
            msg.setInformativeText("Exactly One Fixture Must Be Selected")
            msg.setWindowTitle("Sensor Control Error")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            dialog = SensorDialog(self, checkedButtonNumbers[0])
            dialog.show()