# screens/user_home_screen.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class UserHomeScreen(QWidget):
    def __init__(self, parent, username):
        super().__init__()
        self.parent = parent
        self.username = username
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("InstaAD - Home")
        self.setGeometry(400, 400, 600, 400)

        layout = QVBoxLayout()

        welcome_label = QLabel(f"Welcome, {self.username}!")
        welcome_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(welcome_label)

        # Example placeholder button
        self.next_button = QPushButton("Start New Ad")
        self.next_button.setFont(QFont("Segoe UI", 16))
        layout.addWidget(self.next_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
