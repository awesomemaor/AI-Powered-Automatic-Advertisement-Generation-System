import sys
import random
import os
import math
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, 
    QMessageBox, QGraphicsDropShadowEffect, QFrame, QComboBox, QDateEdit
)
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter, QLinearGradient, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer, QPointF, QDate, QThread, pyqtSignal
from Backend.logic.register_logic import register_user

# threading class for registration process
class RegisterWorker(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, username, password, birthdate, business_type, business_field):
        super().__init__()
        self.username = username
        self.password = password
        self.birthdate = birthdate
        self.business_type = business_type
        self.business_field = business_field

    def run(self):
        result = register_user(
            self.username,
            self.password,
            self.birthdate,
            self.business_type,
            self.business_field
        )
        self.finished.emit(result)

# מחלקת חלקיקים (להמשכיות העיצוב)
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

class RegisterScreen(QWidget):
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
        self.setWindowTitle("InstaAD | Register")
        self.setMinimumSize(1200, 850)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        self.card = QFrame()
        self.card.setFixedWidth(500)
        self.card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.07);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 30px;
            }
        """)
        
        # צמצום ה-Spacing של ה-Layout הכללי
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(50, 40, 50, 40)
        card_layout.setSpacing(5) # רווח קטן מאוד בין האלמנטים

        # כותרות
        title = QLabel("Join the Future")
        title.setFont(QFont("Segoe UI", 32, QFont.Bold))
        title.setStyleSheet("color: white; border: none; background: transparent;")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        subtitle = QLabel("Create your InstaAD account")
        subtitle.setStyleSheet("color: #a0aec0; font-size: 14px; border: none; background: transparent; margin-bottom: 10px;")
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(subtitle)

        # סטייל לשדות הקלט
        input_style = """
            QLineEdit, QDateEdit, QComboBox {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 12px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
                border: 1px solid #00f2fe;
            }
        """
        
        # סטייל ספציפי לכותרות הקטגוריות
        category_label_style = """
            QLabel {
                color: white; 
                font-size: 16px; 
                font-weight: bold; 
                border: none; 
                background: transparent; 
                margin-top: 10px;
                padding: 0px;
            }
        """

        # --- שדות ---
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("👤 Username")
        self.username_input.setStyleSheet(input_style)
        self.username_input.setFixedHeight(50)
        card_layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("🔒 Password")
        self.password_input.setStyleSheet(input_style)
        self.password_input.setFixedHeight(50)
        card_layout.addWidget(self.password_input)

        # קטגוריית תאריך לידה
        dob_label = QLabel("📅 Birthdate")
        dob_label.setStyleSheet(category_label_style)
        card_layout.addWidget(dob_label)
        
        self.birthdate_input = QDateEdit()
        self.birthdate_input.setCalendarPopup(True)
        self.birthdate_input.setDate(QDate.currentDate())
        self.birthdate_input.setStyleSheet(input_style)
        self.birthdate_input.setFixedHeight(50)
        
        # --- תיקון העיצוב של לוח השנה ---
        calendar_style = """
            QCalendarWidget QWidget {
                alternate-background-color: #1e1e36;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #0f0c29;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                padding: 5px;
            }
            QCalendarWidget QToolButton {
                color: white;
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
                border: none;
                border-radius: 5px;
                padding: 5px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: rgba(0, 242, 254, 0.2);
            }
            QCalendarWidget QMenu {
                background-color: #1a1a2e;
                color: white;
                border: 1px solid #00f2fe;
            }
            QCalendarWidget QSpinBox {
                background-color: #1a1a2e;
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 3px;
                selection-background-color: #00f2fe;
                selection-color: black;
            }
            /* עיצוב רשת הימים */
            QCalendarWidget QAbstractItemView:enabled {
                color: white;
                background-color: #15152b;
                selection-background-color: #00f2fe;
                selection-color: #0d1117;
                outline: none;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: #4a4a6a;
            }
        """
        self.birthdate_input.calendarWidget().setStyleSheet(calendar_style)
        # ---------------------------------
        
        card_layout.addWidget(self.birthdate_input)

        # קטגוריית סוג עסק
        type_label = QLabel("💼 Business Type")
        type_label.setStyleSheet(category_label_style)
        card_layout.addWidget(type_label)
        
        self.type_input = QComboBox()
        self.type_input.addItems(["Self-employed", "Salaried employee"])
        self.type_input.setStyleSheet(input_style)
        self.type_input.setFixedHeight(50)
        card_layout.addWidget(self.type_input)

        # שדה תחום עסק
        self.field_input = QLineEdit()
        self.field_input.setPlaceholderText("🏢 Business Field (e.g., Food, Gym)")
        self.field_input.setStyleSheet(input_style)
        self.field_input.setFixedHeight(50)
        card_layout.addWidget(self.field_input)

        # כפתור רישום
        card_layout.addSpacing(20)
        self.reg_button = QPushButton("CREATE ACCOUNT")
        self.reg_button.setFixedHeight(60)
        self.reg_button.setCursor(Qt.PointingHandCursor)
        self.reg_button.clicked.connect(self.register)
        self.reg_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00f2fe, stop:1 #4facfe);
                color: #000; font-weight: 800; font-size: 14px; border-radius: 12px;
            }
            QPushButton:hover { background: white; }
        """)
        card_layout.addWidget(self.reg_button)

        # קישור חזרה
        self.back_button = QPushButton("← Already have an account? Login")
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.clicked.connect(self.back_clicked)
        self.back_button.setStyleSheet("color: #94a3b8; background: transparent; font-size: 13px; border: none;")
        card_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)

        card_layout.addStretch()

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(60)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.card.setGraphicsEffect(shadow)
        
        main_layout.addWidget(self.card)

        # --- Loading overlay ---
        self.loading_overlay = QLabel("Registering account...", self)
        self.loading_overlay.setAlignment(Qt.AlignCenter)
        self.loading_overlay.setStyleSheet("""
            background-color: rgba(0,0,0,160);
            color: white;
            font-size: 18px;
            border-radius: 20px;
        """)
        self.loading_overlay.hide()
        self.loading_overlay.raise_()

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        birthdate = self.birthdate_input.date().toString("yyyy-MM-dd")
        business_type = self.type_input.currentText()
        business_field = self.field_input.text()

        self.loading_overlay.show()

        self.worker = RegisterWorker(username, password, birthdate, business_type, business_field)
        self.worker.finished.connect(self.register_finished)
        self.worker.start()
    
    def register_finished(self, result):
        self.loading_overlay.hide()

        if result["success"]:
            QMessageBox.information(self, "Success", result["message"])
            self.parent.setCurrentWidget(self.parent.welcome_screen)
        else:
            QMessageBox.warning(self, "Error", result["message"])

    def back_clicked(self):
        self.parent.setCurrentWidget(self.parent.welcome_screen)