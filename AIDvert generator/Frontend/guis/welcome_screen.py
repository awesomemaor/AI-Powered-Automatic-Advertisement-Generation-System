from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class WelcomeScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle("InstaAD - Welcome")
        self.setGeometry(400, 400, 600, 400)

        layout = QVBoxLayout()

        self.title = QLabel("Welcome to InstaAD")
        self.title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.go_to_Login)
        layout.addWidget(self.login_button)

        self.register_button = QPushButton("Register")
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def go_to_Login(self):
        self.parent.setCurrentWidget(self.parent.login_screen)
