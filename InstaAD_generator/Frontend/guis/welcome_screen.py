import sys
import random
import os
import math
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect, QFrame, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter, QLinearGradient, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer, QRectF, QPointF

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

class WelcomeScreen(QWidget):
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

    def initUI(self):
        self.setWindowTitle("InstaAD | AI Marketing Evolution")
        self.setMinimumSize(1200, 800)

        main_h_layout = QHBoxLayout(self)
        main_h_layout.setContentsMargins(0, 0, 0, 0)
        main_h_layout.setSpacing(0)

        # --- צד שמאל: הויז'ואל והלוגו (ללא שינוי) ---
        left_side = QFrame()
        left_side.setStyleSheet("background: transparent;")
        left_layout = QVBoxLayout(left_side)
        left_layout.setAlignment(Qt.AlignCenter)
        
        self.logo_label = QLabel()
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
        image_path = os.path.join(base_path, "InstaADlogo.png")
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
        
        logo_glow = QGraphicsDropShadowEffect()
        logo_glow.setBlurRadius(120)
        logo_glow.setColor(QColor(0, 242, 254, 100))
        self.logo_label.setGraphicsEffect(logo_glow)
        
        left_layout.addWidget(self.logo_label)
        
        brand_title = QLabel("Advertisement AI Generator")
        brand_title.setFont(QFont("Orbitron", 50, QFont.Bold)) 
        brand_title.setStyleSheet("color: white; margin-top: 20px; background: transparent;")
        left_layout.addWidget(brand_title, alignment=Qt.AlignCenter)

        # --- צד ימין: ממשק המשתמש (מעודכן למרכז) ---
        right_side = QFrame()
        right_side.setFixedWidth(500)
        right_side.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.05);
                border-left: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)
        
        right_layout = QVBoxLayout(right_side)
        right_layout.setContentsMargins(60, 0, 60, 0) 
        right_layout.setSpacing(15)

        # טקסט כניסה
        welcome_text = QLabel("Start Creating.")
        welcome_text.setFont(QFont("Segoe UI", 32, QFont.Bold))
        welcome_text.setStyleSheet("color: white; border: none; background: transparent;")
        
        desc_text = QLabel("The world's most advanced AI ad generation platform.")
        desc_text.setWordWrap(True)
        desc_text.setFont(QFont("Segoe UI", 12))
        desc_text.setStyleSheet("color: #a0aec0; border: none; background: transparent; margin-bottom: 25px;")

        # כפתור Login הפרימיום
        self.login_button = QPushButton("LOGIN TO DASHBOARD")
        self.login_button.setMinimumHeight(65)
        self.login_button.setCursor(Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.go_to_Login)
        self.login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00f2fe, stop:1 #4facfe);
                color: #000;
                font-weight: 800;
                font-size: 14px;
                border-radius: 12px;
                letter-spacing: 1px;
            }
            QPushButton:hover {
                background: white;
                margin-top: -2px;
            }
        """)

        # כפתור Create Account החדש
        self.register_button = QPushButton("New here? Create account")
        self.register_button.setMinimumHeight(50)
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.clicked.connect(self.go_to_Register)
        self.register_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #94a3b8;
                font-size: 14px;
                border: none;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #00f2fe;
            }
        """)

        # --- המרכוז החדש ---
        right_layout.addStretch(1) # דוחף מלמעלה
        right_layout.addWidget(welcome_text)
        right_layout.addWidget(desc_text)
        right_layout.addSpacing(10)
        right_layout.addWidget(self.login_button)
        right_layout.addWidget(self.register_button)
        right_layout.addStretch(1) # דוחף מלמטה - התוצאה: הכל באמצע!

        main_h_layout.addWidget(left_side, 1)
        main_h_layout.addWidget(right_side)

    def go_to_Login(self):
        self.parent.setCurrentWidget(self.parent.login_screen)
    
    def go_to_Register(self):
        self.parent.setCurrentWidget(self.parent.register_screen)