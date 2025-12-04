from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from Backend.logic.login_logic import login_user
from Backend.logic.login_logic import logout_user_request

class LoginScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("InstaAD - Login")
        self.setGeometry(400, 400, 600, 450)

        # רקע גרדיאנט אחיד
        self.setStyleSheet("""
            LoginScreen {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea,
                    stop:1 #764ba2
                );
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # כרטיס לבן למרכז
        card_widget = QWidget()
        card_widget.setStyleSheet("""
            background-color: white;
            border-radius: 20px;
        """)
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(20)
        card_layout.setAlignment(Qt.AlignCenter)

        # כפתור Back
        self.back_button = QPushButton("Back")
        self.back_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setStyleSheet("""
            QPushButton {
                background: #e74c3c;
                color: white;
                border-radius: 10px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #c0392b;
            }
        """)
        card_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # כותרת
        title_label = QLabel("Login to InstaAD")
        title_label.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)

        # שדות Username ו-Password
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username...")
        self.username_input.setFont(QFont("Segoe UI", 14))
        self.username_input.setFixedWidth(300)
        self.username_input.setMinimumHeight(40)
        self.username_input.setAlignment(Qt.AlignCenter)
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #667eea;
                border-radius: 10px;
                padding: 6px 10px;
            }
            QLineEdit:focus {
                border: 2px solid #5568d3;
            }
        """)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter password...")
        self.password_input.setFont(QFont("Segoe UI", 14))
        self.password_input.setFixedWidth(300)
        self.password_input.setMinimumHeight(40)
        self.password_input.setAlignment(Qt.AlignCenter)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #667eea;
                border-radius: 10px;
                padding: 6px 10px;
            }
            QLineEdit:focus {
                border: 2px solid #5568d3;
            }
        """)

        card_layout.addWidget(self.username_input, alignment=Qt.AlignCenter)
        card_layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        # Login button
        self.log_button = QPushButton("Login")
        self.log_button.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.log_button.setMinimumHeight(50)
        self.log_button.setCursor(Qt.PointingHandCursor)
        self.log_button.clicked.connect(self.try_login)
        self.log_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea,
                    stop:1 #764ba2
                );
                color: white;
                border-radius: 12px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3,
                    stop:1 #6a3f8f
                );
            }
            QPushButton:pressed {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4e5dc8,
                    stop:1 #5d3782
                );
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(102, 126, 234, 150))
        self.log_button.setGraphicsEffect(shadow)
        card_layout.addWidget(self.log_button)

        card_widget.setLayout(card_layout)
        main_layout.addWidget(card_widget, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)

    def go_back(self):
        self.parent.setCurrentWidget(self.parent.welcome_screen)

    def try_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        result = login_user(username, password)

        msg = QMessageBox()
        if result["success"]:
            msg.setText(result["message"])
            msg.setIcon(QMessageBox.Information)
            msg.exec_()

            # יצירת מסך בית עם שם המשתמש
            from guis.userHome_screen import UserHomeScreen
            user_home = UserHomeScreen(self.parent, username)
            # Update generate_screen to use this user_home instance
            self.parent.generate_screen.user_home_screen = user_home
            #self.parent.user_home_screen = user_home
            self.parent.addWidget(user_home)
      
            self.parent.setCurrentWidget(user_home)

        else:
            if result["message"] == "User already logged in.":
                msg = QMessageBox()
                msg.setWindowTitle("User Already Logged In")
                msg.setText("User already logged in.\nWould you like to sign out now?")
                msg.setIcon(QMessageBox.Question)
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

                choice = msg.exec_()

                if choice == QMessageBox.Yes:
                    logout_user_request(username)

                    msg = QMessageBox()
                    msg.setWindowTitle("Logged Out")
                    msg.setText("You have been logged out. Please log in again.")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()

                    self.parent.setCurrentWidget(self.parent.welcome_screen)
                    return
                
                else:
                    return
            
            else:
                msg = QMessageBox()
                msg.setText("Login failed: " + result["message"])
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()