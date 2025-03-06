import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QColor, QPalette
import numpy as np
import math
import sched

import marcher

size = (40, 40)
windowSize = (700, 700)

colors = ["#009900", "#77CC00", "#CCEE00", "#CCCC00", "#EEBB00", "#FFAA00", "#FF9900", "#FF7700", "#FF5500", "#FF0000"]

class IndexButton(QPushButton):
    def __init__(self, x : int, y : int, **kwargs):
        self.posX = x
        self.posY = y
        self.active = False
        super().__init__(**kwargs)

class ClickableGrid(QWidget):
    def __init__(self, rows, cols, targetSizeX, targetSizeY):
        super().__init__()
        self.rows = rows
        self.cols = cols
        self.targetSizeX = targetSizeX
        self.targetSizeY = targetSizeY
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Clickable Squares")
        self.setGeometry(100, 100, *windowSize)

        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()
        

        self.buttons = []
        self.lock = False

        buttonSize = (self.targetSizeX // self.cols, self.targetSizeY // self.rows)

        for row in range(self.rows):
            button_row = []
            for col in range(self.cols):
                button = IndexButton(col, row)
                button.setFixedSize(*buttonSize)
                button.setStyleSheet("background-color: white;")
                button.clicked.connect(lambda _, b=button: self.buttonPressed(b))
                grid_layout.addWidget(button, row, col)
                button_row.append(button)
            self.buttons.append(button_row)

        main_layout.addLayout(grid_layout)
        
        button_layout = QHBoxLayout()

        grid_layout.setSpacing(1)  # Adjust spacing between grid buttons
        button_layout.setSpacing(5)  # Adjust spacing between bottom buttons

        self.calculate_button = QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.calculate)
        button_layout.addWidget(self.calculate_button)
        
        self.simulate_button = QPushButton("Simulate")
        self.simulate_button.clicked.connect(self.simulate)
        button_layout.addWidget(self.simulate_button)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)

    def buttonPressed(self, button):
        if self.lock:
            return
        button.active = not button.active
        self.updateButton(button)

    def updateButton(self, button):
        color = "black" if button.active else "white"
        self.changeButtonColor(button, color)

    def changeButtonColor(self, button, color : str):
        button.setStyleSheet(f"background-color: {color};")

    def simulate(self):
        #self.calculate_button.setEnabled(False)
        #self.simulate_button.setEnabled(False)
        converted = []
        for y in range(self.rows):
            converted.append([])
            for x in range(self.cols):
                but = self.buttons[y][x]
                but : IndexButton
                converted[y].append(but.active)
        res = marcher.Simulate(converted)
        for y in range(self.rows):
            for x in range(self.cols):
                but = self.buttons[y][x]
                but : IndexButton
                but.active = res[y][x]
                self.updateButton(but)
        #self.lock = True

    def calculate(self):
        #self.calculate_button.setEnabled(False)
        #self.simulate_button.setEnabled(False)
        converted = []
        for y in range(self.rows):
            converted.append([])
            for x in range(self.cols):
                but = self.buttons[y][x]
                but : IndexButton
                converted[y].append(but.active)
        #res = marcher.CalculateProbabilities(converted)
        #maxProb = 0.5
        #res = marcher.MarkovChainProbabilitesToMaxProb(converted, maxProb)
        res = marcher.VoidHoleProbabilities(converted)
        maximum = res.max()
        for y in range(self.rows):
            for x in range(self.cols):
                but = self.buttons[y][x]
                but : IndexButton
                isNeighbour = marcher._NeighbourExists(converted, y, x)
                if but.active or not isNeighbour:
                    continue
                #but.setText(str(res[y][x]))
                val = res[y][x] / maximum
                col = colors[min(math.floor((1-math.pow(1-val, 5)) * len(colors)), len(colors)-1)]
                self.changeButtonColor(but, col)
        #self.lock = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClickableGrid(*size, *windowSize)
    window.show()
    app.exec()
    #sys.exit()
