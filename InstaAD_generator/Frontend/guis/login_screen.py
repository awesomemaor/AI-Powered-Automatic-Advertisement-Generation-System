import sys
import random
import os
import math
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QGraphicsDropShadowEffect, QFrame
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter, QLinearGradient, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer, QPointF, QThread, pyqtSignal
from Backend.logic.login_logic import login_user
from Backend.logic.login_logic import logout_user_request

# threading class for login process
class LoginWorker(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

    def run(self):
        result = login_user(self.username, self.password)
        self.finished.emit(result)

# מחלקת החלקיקים לרקע
class Particle:
    def __init__(self, width, height):
        self.x = random.random() * width
        self.y = random.random() * height
        self.vx = (random.random() - 0.5) * 0.5
        self.vy = (random.random() - 0.5) * 0.5
        self.size = random.uniform(1, 3)
        self.alpha = random.randint(50, 150)

    def move(self, width, height):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0 or self.x > width: self.vx *= -1
        if self.y < 0 or self.y > height: self.vy *= -1

class LoginScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.particles = [Particle(1200, 800) for _ in range(60)]
        self.initUI()
        
        self.gradient_offset = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def update_frame(self):
        self.gradient_offset += 0.005
        if self.gradient_offset > 1: self.gradient_offset = 0
        for p in self.particles:
            p.move(self.width(), self.height())
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # הרקע האנימטיבי שאהבנו
        grad = QLinearGradient(0, 0, self.width(), self.height())
        grad.setColorAt(0, QColor(15, 12, 41))   
        grad.setColorAt(0.5 + (0.1 * math.sin(self.gradient_offset * math.pi * 2)), QColor(48, 43, 99)) 
        grad.setColorAt(1, QColor(36, 36, 62))   
        painter.fillRect(self.rect(), grad)
        
        painter.setPen(Qt.NoPen)
        for p in self.particles:
            painter.setBrush(QColor(0, 242, 254, p.alpha)) 
            painter.drawEllipse(QPointF(p.x, p.y), p.size, p.size)
    
    def resizeEvent(self, event):
        if hasattr(self, "loading_overlay"):
            self.loading_overlay.setGeometry(self.rect())
        super().resizeEvent(event)

    def initUI(self):
        self.setWindowTitle("InstaAD | Login")
        self.setMinimumSize(1200, 800)

        # Layout ראשי - ממרכז את הכל
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # כרטיס ה-Login (זכוכית חלבית)
        self.card = QFrame()
        self.card.setFixedWidth(450)
        self.card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.07);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 30px;
            }
        """)
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(50, 50, 50, 50)
        card_layout.setSpacing(15)

        # כותרת הכרטיס
        title_label = QLabel("Welcome Back")
        title_label.setFont(QFont("Segoe UI", 30, QFont.Bold))
        title_label.setStyleSheet("color: white; background: transparent; border:none;")
        title_label.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Please enter your details")
        subtitle.setStyleSheet("color: #a0aec0; font-size: 14px; background: transparent; margin-bottom: 20px; border:none;")
        subtitle.setAlignment(Qt.AlignCenter)

        # עיצוב השדות (Inputs)
        input_style = """
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 15px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #00f2fe;
                background-color: rgba(255, 255, 255, 0.12);
            }
        """

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet(input_style)
        self.username_input.setMinimumHeight(55)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setStyleSheet(input_style)
        self.password_input.setMinimumHeight(55)

        # כפתור Login המודרני
        self.log_button = QPushButton("LOG IN")
        self.log_button.setMinimumHeight(60)
        self.log_button.setCursor(Qt.PointingHandCursor)
        self.log_button.clicked.connect(self.try_login)
        self.log_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00f2fe, stop:1 #4facfe);
                color: #000;
                font-weight: 800;
                font-size: 14px;
                border-radius: 12px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background: white;
            }
        """)

        # כפתור חזרה (Back)
        self.back_button = QPushButton("← Back to Welcome")
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.clicked.connect(self.go_back)
        self.back_button.setStyleSheet("""
            QPushButton {
                color: #a0aec0;
                background: transparent;
                font-size: 13px;
                border: none;
                margin-top: 10px;
            }
            QPushButton:hover { color: white; }
        """)

        # הוספת אלמנטים לכרטיס
        card_layout.addWidget(title_label)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(self.log_button)
        card_layout.addWidget(self.back_button)

        # אפקט צל לכרטיס ש"יקפוץ" מהרקע
        card_shadow = QGraphicsDropShadowEffect()
        card_shadow.setBlurRadius(80)
        card_shadow.setColor(QColor(0, 0, 0, 180))
        self.card.setGraphicsEffect(card_shadow)

        main_layout.addWidget(self.card)

        self.loading_overlay = QLabel("Connecting...", self)
        self.loading_overlay.setAlignment(Qt.AlignCenter)
        self.loading_overlay.setStyleSheet("""
            background-color: rgba(0, 0, 0, 160);
            color: white;
            font-size: 18px;
            border-radius: 20px;
        """)
        self.loading_overlay.hide()
        self.loading_overlay.raise_()

    # logic functions
    def go_back(self):
        self.parent.setCurrentWidget(self.parent.welcome_screen)

    def try_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return

        # הצגת טעינה
        self.loading_overlay.show()

        # יצירת worker
        self.login_worker = LoginWorker(username, password)
        self.login_worker.finished.connect(self.on_login_finished)
        self.login_worker.start()

    def on_login_finished(self, result):
        self.loading_overlay.hide()
        msg = QMessageBox()

        if result["success"]:
            msg.setText(result["message"])
            msg.setIcon(QMessageBox.Information)
            msg.exec_()

            from guis.userHome_screen import UserHomeScreen
            user_home = UserHomeScreen(self.parent, self.username_input.text())

            self.parent.user_home_screen = user_home
            self.parent.generate_screen.user_home_screen = user_home
            self.parent.addWidget(user_home)
            self.parent.setCurrentWidget(user_home)

        else:
            if result["message"] == "User already logged in.":
                msg.setWindowTitle("User Already Logged In")
                msg.setText("User already logged in.\nWould you like to sign out now?")
                msg.setIcon(QMessageBox.Question)
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                choice = msg.exec_()

                if choice == QMessageBox.Yes:
                    logout_user_request(self.username_input.text())
                    QMessageBox.information(self, "Logged Out", "You have been logged out. Please log in again.")
                    self.parent.setCurrentWidget(self.parent.welcome_screen)
            else:
                QMessageBox.critical(self, "Login failed", result["message"])
