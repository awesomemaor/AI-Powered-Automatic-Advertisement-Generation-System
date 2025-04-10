from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
import os

class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Window setup
        self.setWindowTitle("AIDvert - Welcome")
        self.setGeometry(400, 400, 600, 400)

        layout = QVBoxLayout()

        # Project title
        self.title = QLabel("Welcome to AIDvert")
        self.title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Login button
        self.login_button = QPushButton("Login")
        layout.addWidget(self.login_button)

        # Register button
        self.register_button = QPushButton("Register")
        layout.addWidget(self.register_button)

        self.setLayout(layout)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Load external QSS style
    qss_path = os.path.join(os.path.dirname(__file__), "style.qss")
    with open(qss_path, "r") as file:
        app.setStyleSheet(file.read())  # <- זה מה שחסר

    window = WelcomeScreen()
    window.show()
    sys.exit(app.exec_())

