from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLineEdit, QLabel

class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Start Visualization Button
        self.start_button = QPushButton("Start Visualization")
        self.start_button.clicked.connect(self.start_visualization)
        layout.addWidget(self.start_button)
        
        # Add Probabilities Button
        self.add_probabilities_button = QPushButton("Add Probabilities")
        self.add_probabilities_button.clicked.connect(self.add_probabilities)
        layout.addWidget(self.add_probabilities_button)
        
        # Simulate Button with Steps Input
        self.simulate_layout = QHBoxLayout()
        self.simulate_button = QPushButton("Simulate")
        self.simulate_button.clicked.connect(self.simulate)
        self.simulate_layout.addWidget(self.simulate_button)
        
        self.steps_label = QLabel("Steps:")
        self.simulate_layout.addWidget(self.steps_label)
        
        self.steps_input = QLineEdit()
        self.simulate_layout.addWidget(self.steps_input)
        
        layout.addLayout(self.simulate_layout)
        
        # Set layout
        self.setLayout(layout)
        self.setWindowTitle("Control Panel")

    def start_visualization(self):

        pass  # Placeholder method

    def add_probabilities(self):
        pass  # Placeholder method

    def simulate(self):
        pass  # Placeholder method

if __name__ == "__main__":
    from multiprocessing import Process
    app = QApplication([])
    window = ControlPanel()
    window.show()
    app.exec()
