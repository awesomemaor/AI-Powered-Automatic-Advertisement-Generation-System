import sys
import random
import os
import math
from PyQt5.QtWidgets import QWidget, QMessageBox, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QGraphicsDropShadowEffect, QFrame
from PyQt5.QtGui import QFont, QColor, QPainter, QLinearGradient, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer, QPointF, QThread, pyqtSignal
from Backend.logic.login_logic import logout_user_request
from Backend.logic.generate_ad_logic import handle_generate
from guis.ad_preview_screen import AdPreviewScreen

# threading class for ad generation process
class GenerateThread(QThread):
    finished = pyqtSignal(dict)

    def __init__(self, prompt, user_id, mode):
        super().__init__()
        self.prompt = prompt
        self.user_id = user_id
        self.mode = mode

    def run(self):
        result = handle_generate(
            prompt=self.prompt,
            user_id=self.user_id,
            mode=self.mode
        )
        self.finished.emit(result)

# מחלקת חלקיקים
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

class UserHomeScreen(QWidget):
    def __init__(self, parent, username):
        super().__init__()
        self.parent = parent
        self.username = username
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
        self.setWindowTitle("InstaAD | Dashboard")
        self.setMinimumSize(1200, 800)

        # Layout ראשי שממרכז את הכרטיס
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # כרטיס הזכוכית שאהבת
        self.card = QFrame()
        self.card.setFixedWidth(650)
        # שים לב: הורדתי setFixedHeight כדי שהכרטיס יגדל אם צריך והטקסט לא ייחתך
        self.card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.07);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 40px;
            }
        """)
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(50, 50, 50, 50)
        card_layout.setSpacing(20)

        # --- המרכוז הפנימי שמונע חיתוך ---
        card_layout.addStretch() 

        # כותרת
        self.welcome_label = QLabel(f"Welcome, {self.username}!")
        self.welcome_label.setFont(QFont("Segoe UI", 32, QFont.Bold))
        self.welcome_label.setStyleSheet("color: white; background: transparent; border: none;")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setWordWrap(True) # מאפשר לטקסט לרדת שורה אם השם ארוך
        card_layout.addWidget(self.welcome_label)

        subtitle = QLabel("Choose your advertising action")
        subtitle.setFont(QFont("Segoe UI", 14)) # הגדלתי טיפה שיהיה ברור
        subtitle.setStyleSheet("color: #a0aec0; background: transparent; border: none; padding: 5px;")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True) # זה ימנע את החיתוך!
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(20)

        # כפתורים
        actions = [
            ("✨ Start New Ad", self.start_new_ad),
            ("🤖 Recommended Ad", self.generate_recommended),
            ("📂 Ad History", self.advertisement_history)
        ]

        for text, func in actions:
            btn = QPushButton(text)
            btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
            btn.setMinimumHeight(65)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(func)
            
            if "Start" in text:
                style = """
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00f2fe, stop:1 #4facfe);
                        color: #0d1117; border-radius: 15px; font-weight: 900;
                    }
                    QPushButton:hover { background: white; }
                """
            else:
                style = """
                    QPushButton {
                        background: rgba(255, 255, 255, 0.08);
                        color: white; border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 15px;
                    }
                    QPushButton:hover { background: rgba(255, 255, 255, 0.15); border: 1px solid white; }
                """
            btn.setStyleSheet(style)
            card_layout.addWidget(btn)

        # כפתור Logout
        self.logout_button = QPushButton("Logout")
        self.logout_button.setCursor(Qt.PointingHandCursor)
        self.logout_button.clicked.connect(self.logout_clicked)
        self.logout_button.setStyleSheet("""
            QPushButton {
                color: #e74c3c; background: transparent; font-size: 14px; 
                font-weight: bold; border: none; margin-top: 10px;
            }
            QPushButton:hover { color: #ff5e57; text-decoration: underline; }
        """)
        card_layout.addWidget(self.logout_button, alignment=Qt.AlignCenter)

        card_layout.addStretch() # סוגר את המרכוז מלמטה

        # צל
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(80)
        shadow.setColor(QColor(0, 0, 0, 200))
        self.card.setGraphicsEffect(shadow)

        main_layout.addWidget(self.card)

        # Loading overlay
        self.loading_overlay = QLabel("✨ Creating your ad...")
        self.loading_overlay.setAlignment(Qt.AlignCenter)
        self.loading_overlay.setStyleSheet("""
            background: rgba(0, 0, 0, 0.6);
            color: white;
            font-size: 20px;
            border-radius: 20px;
        """)
        self.loading_overlay.setParent(self)
        self.loading_overlay.hide()

    def start_new_ad(self):
        self.parent.generate_screen.username = self.username
        self.parent.setCurrentWidget(self.parent.generate_screen)

    # recommended ad creation flow
    def generate_recommended(self):
        self.loading_overlay.show()

        self.gen_thread = GenerateThread(
            prompt=None,
            user_id=self.username,
            mode="recommended"
        )

        self.gen_thread.finished.connect(self.on_generate_finished)
        self.gen_thread.start()

    def on_generate_finished(self, result):
        self.loading_overlay.hide()

        if not result.get("success"):
            QMessageBox.warning(self, "Error", result.get("message"))
            return

        data = result["data"]

        self.preview_window = AdPreviewScreen(
            task_id=data["task_id"],
            keywords=data.get("keywords", []),
            username=self.username,
            go_back_callback=self.return_from_preview
        )

        self.hide()
        self.preview_window.show()

    def return_from_preview(self):
        """נקראת כשהמשתמש לוחץ Try Again"""
        if self.preview_window:
            self.preview_window.close()
            self.preview_window = None
        self.show()

    def advertisement_history(self):
        self.parent.ad_history_screen.load_ads(self.username)
        self.parent.setCurrentWidget(self.parent.ad_history_screen)

    def logout_clicked(self):
        result = logout_user_request(self.username)
        if result["success"]:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setText("Logged out successfully!")
            msg.exec_()
            self.parent.setCurrentWidget(self.parent.welcome_screen)