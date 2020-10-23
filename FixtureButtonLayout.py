from PyQt5.QtWidgets import QGridLayout, QSpacerItem, QSizePolicy
import csv

''' FixtureButtonLayout arranges the buttons according to the
    layout in layout.csv. Any numeric value will be treated
    as a fixture number and any alphabetic value will be
    treated as a spacer. '''

class FixtureButtonLayout(QGridLayout):

    def __init__(self, buttons):
        super().__init__()
        self.buttonList = buttons

        # Open csv file with fixture layout
        with open('layout.csv') as layoutFile:
            layoutReader = csv.reader(layoutFile)
            rowCount = 1

            # Loop through each cell. If cell contains a number,
            # add the appropriate fixture button to the grid.
            # If it does not contain a number, add a spacer
            for row in layoutReader:
                colCount = 1
                for column in row:
                    if column.isnumeric():
                        self.addWidget(self.buttonList[int(column) - 1], rowCount, colCount)
                    else:
                        spacer = QSpacerItem(10, 10, QSizePolicy.Expanding)
                        self.addItem(spacer, rowCount, colCount)
                    colCount += 1
                rowCount += 1