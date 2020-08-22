from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QFileDialog, QMessageBox, QDialog, QDialogButtonBox, QVBoxLayout
from android_receiver import android_receiver
import socket


class SensorDialog(QDialog):

    def __init__(self, parent, pinspotworld, currentPin):
        super().__init__(parent)
        self.setWindowTitle("Sensor Control Mode")

        self.pinspots = pinspotworld
        self.currentPin = currentPin

        self.message = QMessageBox()
        self.message.setText("Press Start to Activate Sensor Control Mode\nServer Address " + str(socket.gethostbyname(socket.gethostname)) + "\nDo Not Press OK")

        layout = QVBoxLayout()
        layout.addWidget(self.message)
        self.setLayout(layout)

        self.startStopButton = QPushButton("Start")
        self.startStopButton.setCheckable(True)
        self.startStopButton.clicked.connect(self.sensorControl)
        layout.addWidget(self.startStopButton)

        self.closeButton = QPushButton("Close")
        self.closeButton.clicked.connect(self.hide)
        layout.addWidget(self.closeButton)



    def sensorControl(self):
        receiver = android_receiver()

        if self.startStopButton.isChecked() == True:
            self.startStopButton.setText("Stop")
            self.startStopButton.repaint()

            receiver.start(self.pinspots, self.currentPin)

        else:
            self.startStopButton.setText("Start")
            receiver.stop()
            self.startStopButton.repaint()