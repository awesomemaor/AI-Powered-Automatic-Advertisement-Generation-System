from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from Backend.logic.login_logic import login_user

class LoginScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("AIDvert - Login")
        self.setGeometry(400, 400, 600, 400)

        main_layout = QVBoxLayout()  # Main layout for the widget

        # Top layout for the back button
        top_layout = QHBoxLayout()
        self.back_button = QPushButton("Back")
        self.back_button.setFont(QFont("Segoe UI", 16))
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setObjectName("backButton")
        top_layout.addWidget(self.back_button)
        top_layout.addStretch()  

        main_layout.addLayout(top_layout)  

        # Title
        self.title = QLabel("Login to AIDvert")
        self.title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)

        # Username input
        self.username_input = QLineEdit()  
        self.username_input.setPlaceholderText("Enter username...")  
        self.username_input.setFont(QFont("Segoe UI", 12))  
        self.username_input.setFixedWidth(300)  
        self.username_input.setAlignment(Qt.AlignCenter) 
        main_layout.addWidget(self.username_input, alignment=Qt.AlignCenter)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password...")  
        self.password_input.setFont(QFont("Segoe UI", 12))  
        self.password_input.setFixedWidth(300)  
        self.password_input.setAlignment(Qt.AlignCenter) 
        main_layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        # Login button
        self.log_button = QPushButton("Login")
        self.log_button.setFont(QFont("Segoe UI", 16))
        self.log_button.clicked.connect(self.try_login)
        main_layout.addWidget(self.log_button)

        self.setLayout(main_layout)
    
    def go_back(self):
        self.parent.setCurrentWidget(self.parent.welcome_screen)

    # Add this method to LoginScreen:
    def try_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        result = login_user(username, password)
        
        msg = QMessageBox()
        if result["success"]:
            msg.setText(result["message"])
            msg.setIcon(QMessageBox.Information)
            # TODO: Navigate to next screen here
        else:
            msg.setText("Login failed: " + result["message"])
            msg.setIcon(QMessageBox.Critical)
        msg.exec_()