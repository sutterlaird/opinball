from PyQt5.QtWidgets import QGridLayout, QSpacerItem, QSizePolicy

class FixtureButtonLayout(QGridLayout):
    def __init__(self, buttons):
        super().__init__()
        self.buttonList = buttons

        # Spacers
        for x in range(1,9):
            spacer = QSpacerItem(10,10,QSizePolicy.Expanding)
            self.addItem(spacer, x, 8)
            self.addItem(spacer, x, 4)
        for x in range(1,12):
            spacer = QSpacerItem(10,20,QSizePolicy.Expanding)
            self.addItem(spacer, 4, x)


        # First soffit service wall
        self.addWidget(self.buttonList[0], 7, 11)
        self.addWidget(self.buttonList[1], 6, 11)
        self.addWidget(self.buttonList[2], 5, 11)
        self.addWidget(self.buttonList[3], 5, 10)
        self.addWidget(self.buttonList[4], 5, 9)
        self.addWidget(self.buttonList[5], 6, 9)
        self.addWidget(self.buttonList[6], 7, 9)
        self.addWidget(self.buttonList[7], 7, 10)

        # Second soffit service wall
        self.addWidget(self.buttonList[8], 7, 7)
        self.addWidget(self.buttonList[9], 6, 7)
        self.addWidget(self.buttonList[10], 5, 7)
        self.addWidget(self.buttonList[11], 5, 6)
        self.addWidget(self.buttonList[12], 5, 5)
        self.addWidget(self.buttonList[13], 6, 5)
        self.addWidget(self.buttonList[14], 7, 5)
        self.addWidget(self.buttonList[15], 7, 6)

        # Third soffit service wall
        self.addWidget(self.buttonList[16], 7, 3)
        self.addWidget(self.buttonList[17], 6, 3)
        self.addWidget(self.buttonList[18], 5, 3)
        self.addWidget(self.buttonList[19], 5, 2)
        self.addWidget(self.buttonList[20], 5, 1)
        self.addWidget(self.buttonList[21], 6, 1)
        self.addWidget(self.buttonList[22], 7, 1)
        self.addWidget(self.buttonList[23], 7, 2)



        # First soffit gallery wall
        self.addWidget(self.buttonList[24], 3, 11)
        self.addWidget(self.buttonList[25], 2, 11)
        self.addWidget(self.buttonList[26], 1, 11)
        self.addWidget(self.buttonList[27], 1, 10)
        self.addWidget(self.buttonList[28], 1, 9)
        self.addWidget(self.buttonList[29], 2, 9)
        self.addWidget(self.buttonList[30], 3, 9)
        self.addWidget(self.buttonList[31], 3, 10)

        # Second soffit gallery wall
        self.addWidget(self.buttonList[32], 3, 7)
        self.addWidget(self.buttonList[33], 2, 7)
        self.addWidget(self.buttonList[34], 1, 7)
        self.addWidget(self.buttonList[35], 1, 6)
        self.addWidget(self.buttonList[36], 1, 5)
        self.addWidget(self.buttonList[37], 2, 5)
        self.addWidget(self.buttonList[38], 3, 5)
        self.addWidget(self.buttonList[39], 3, 6)

        # Third soffit gallery wall
        self.addWidget(self.buttonList[40], 3, 3)
        self.addWidget(self.buttonList[41], 2, 3)
        self.addWidget(self.buttonList[42], 1, 3)
        self.addWidget(self.buttonList[43], 1, 2)
        self.addWidget(self.buttonList[44], 1, 1)
        self.addWidget(self.buttonList[45], 2, 1)
        self.addWidget(self.buttonList[46], 3, 1)
        self.addWidget(self.buttonList[47], 3, 2)