from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys

class WelcomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Window setup
        self.setWindowTitle("AI-vertisement - Welcome")
        self.setGeometry(300, 300, 400, 300)

        layout = QVBoxLayout()

        # Project title
        self.title = QLabel("Welcome to AI-vertisement")
        self.title.setFont(QFont("Arial", 18))
        self.title.setStyleSheet("color: #333;")
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("font-size: 16px; padding: 10px;")
        layout.addWidget(self.login_button)

        # Register button
        self.register_button = QPushButton("Register")
        self.register_button.setStyleSheet("font-size: 16px; padding: 10px;")
        layout.addWidget(self.register_button)

        self.setLayout(layout)

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WelcomeScreen()
    window.show()
    sys.exit(app.exec_())
