from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QPixmap, QColor
from PyQt5.QtCore import Qt
import os

class WelcomeScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle("InstaAD - Welcome")
        self.setGeometry(400, 400, 600, 500)

        # רקע עם גרדיאנט מודרני
        self.setStyleSheet("""
            WelcomeScreen {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea,
                    stop:1 #764ba2
                );
            }
        """)

        # Layout ראשי
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 40, 50, 40)
        main_layout.setSpacing(0)  # מאפס את הרווחים האוטומטיים
        main_layout.setAlignment(Qt.AlignCenter)

        # כרטיס מרכזי לבן
        card_widget = QWidget()
        card_widget.setObjectName("card")
        card_widget.setStyleSheet("""
            QWidget#card {
                background-color: white;
                border-radius: 25px;
            }
        """)
        
        # צל לכרטיס
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setXOffset(0)
        shadow.setYOffset(15)
        shadow.setColor(QColor(0, 0, 0, 100))
        card_widget.setGraphicsEffect(shadow)
        
        # Layout של הכרטיס
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(50, 40, 50, 40)
        card_layout.setSpacing(15)  # רווח קטן יותר בין האלמנטים
        card_layout.setAlignment(Qt.AlignCenter)

        # Title
        self.title = QLabel("Welcome to InstaAD")
        self.title.setFont(QFont("Segoe UI", 32, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #2c3e50; background: transparent;")
        self.title.setWordWrap(True)
        card_layout.addWidget(self.title)

        # Subtitle
        subtitle = QLabel("Your Advertising Solution")
        subtitle.setFont(QFont("Segoe UI", 5))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #7f8c8d; background: transparent;")
        card_layout.addWidget(subtitle)

     # Logo
        self.logo_label = QLabel()

        # נתיב תקין לתמונה מתוך הקובץ הנוכחי
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
        image_path = os.path.join(base_path, "InstaADlogo.png")

        print("IMAGE PATH:", image_path)
        print("EXISTS:", os.path.exists(image_path))

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print("ERROR: Could not load image!")

        pixmap = pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setStyleSheet("background: transparent;")
        card_layout.addWidget(self.logo_label)

        # Login Button
        self.login_button = QPushButton("Login to Your Account")
        self.login_button.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.login_button.setMinimumHeight(55)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.go_to_Login)
        self.login_button.setStyleSheet("""
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
        
        # צל לכפתור Login
        login_shadow = QGraphicsDropShadowEffect()
        login_shadow.setBlurRadius(20)
        login_shadow.setXOffset(0)
        login_shadow.setYOffset(5)
        login_shadow.setColor(QColor(102, 126, 234, 120))
        self.login_button.setGraphicsEffect(login_shadow)
        
        card_layout.addWidget(self.login_button)

        # Register Button
        self.register_button = QPushButton("Create New Account")
        self.register_button.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.register_button.setMinimumHeight(55)
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.clicked.connect(self.go_to_Register)
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #667eea;
                border: 2px solid #667eea;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f0f3ff;
                border: 2px solid #5568d3;
                color: #5568d3;
            }
            QPushButton:pressed {
                background-color: #e0e7ff;
            }
        """)
        card_layout.addWidget(self.register_button)

        card_widget.setLayout(card_layout)
        main_layout.addWidget(card_widget)

        self.setLayout(main_layout)

    def go_to_Login(self):
        self.parent.setCurrentWidget(self.parent.login_screen)
    
    def go_to_Register(self):
        self.parent.setCurrentWidget(self.parent.register_screen)