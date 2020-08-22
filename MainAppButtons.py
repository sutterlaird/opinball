from PyQt5.QtWidgets import QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from SensorDialog import SensorDialog





class StopButton(QPushButton):
    def __init__(self, pinspotWorld, buttonlist, callback):
        super().__init__()
        self.callback = callback
        self.pinspots = pinspotWorld
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
    def __init__(self, pinspotWorld):
        super().__init__()
        self.pinspots = pinspotWorld
        self.setText("Save Show")
        self.clicked.connect(self.onSaveClicked)
        self.setAutoDefault(False)
        self.setFocusPolicy(Qt.NoFocus)



    def onSaveClicked(self):
        # Open file chooser dialog and get new file name
        options = QFileDialog.Options()
        newFileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","Pinspot Show Files (*.suttershow)", options=options)
        if newFileName:
            newSaveFile = open(newFileName, "w+b")
            newSaveFile.write(self.pinspots.getUniverse1Status())
            newSaveFile.write(self.pinspots.getUniverse2Status())





class LoadShowButton(QPushButton):
    def __init__(self, pinspotWorld):
        super().__init__()
        self.pinspots = pinspotWorld
        self.setText("Load Show")
        self.clicked.connect(self.onLoadClicked)
        self.setAutoDefault(False)
        self.setFocusPolicy(Qt.NoFocus)



    def onLoadClicked(self):
        print("Load clicked")
        options = QFileDialog.Options()
        loadFileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Pinspot Show Files (*.suttershow)", options=options)
        if loadFileName:
            print(loadFileName)
            newLoadFile = open(loadFileName, "r+b")
            universe1 = bytearray(newLoadFile.read(self.pinspots.bytesPerPacket))
            universe2 = bytearray(newLoadFile.read(self.pinspots.bytesPerPacket))
            self.pinspots.setUniverse1Status(universe1)
            self.pinspots.setUniverse2Status(universe2)





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
    def __init__(self, pinspotWorld, buttonList):
        super().__init__()
        self.buttons = buttonList
        self.pinspots = pinspotWorld
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
    def __init__(self, pinspotWorld, buttonList):
        super().__init__()
        self.buttons = buttonList
        self.pinspots = pinspotWorld
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
            dialog = SensorDialog(self, self.pinspots, checkedButtonNumbers[0])
            dialog.show()