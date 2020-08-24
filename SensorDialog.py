from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QFileDialog, QMessageBox, QDialog, QDialogButtonBox, QVBoxLayout
from sensor_receiver import sensor_receiver
import socket


class SensorDialog(QDialog):

    def __init__(self, parent, currentPin):
        super().__init__(parent)
        self.setWindowTitle("Sensor Control Mode")

        self.currentPin = currentPin
        self.receiver = sensor_receiver()

        self.message = QMessageBox()
        self.message.setText("Press Start to Activate Sensor Control Mode\nConnect on Port 50000")

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

        if self.startStopButton.isChecked() == True:
            self.startStopButton.setText("Stop")
            self.startStopButton.repaint()
            # Start receiver daemon
            self.receiver.startLoop(self.currentPin)

        else:
            self.startStopButton.setText("Start")
            self.receiver.stopLoop()
            self.startStopButton.repaint()