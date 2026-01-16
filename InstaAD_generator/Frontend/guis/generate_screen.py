import sys
import random
import os
import math
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QGraphicsDropShadowEffect, QMessageBox, QFrame, QHBoxLayout
from PyQt5.QtGui import QFont, QColor, QPainter, QLinearGradient, QBrush, QPen
from PyQt5.QtCore import Qt, QTimer, QPointF
from Backend.logic.login_logic import logout_user_request
from Backend.logic.generate_ad_logic import handle_generate
from guis.ad_preview_screen import AdPreviewScreen

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

class GenerateScreen(QWidget):
    def __init__(self, parent, username, user_home_screen=None):
        super().__init__()
        self.parent = parent
        self.username = username
        self.user_home_screen = user_home_screen
        self.particles = [Particle(1200, 800) for _ in range(60)]
        
        # מאגרי נתונים מורחבים
        self.prompts_examples = [
            "A futuristic luxury watch ad with neon lights and deep bass.",
            "Cozy cafe morning vibes with steam rising from a fresh latte.",
            "High-energy sports shoe commercial on a rainy urban track.",
            "Minimalist skincare product reveal with soft, natural shadows.",
            "Cinematic street food festival at night with vibrant colors.",
            "Electric car driving through a mountainous landscape at sunset.",
            "Abstract 3D shapes dancing to a lo-fi hip hop beat.",
            "Premium perfume bottle emerging from a silk background.",
            "Action-packed gaming headset trailer with glitch effects.",
            "Healthy salad bowl preparation with slow-motion splashes."
        ]
        
        self.marketing_quotes = [
            '"Good advertising penetrates the public mind with desires and belief." – William Bernbach',
            '"The best ads come from personal experience." – David Ogilvy',
            '"Creativity is intelligence having fun." – Albert Einstein',
            '"Stopping advertising to save money is like stopping your watch to save time." – Henry Ford',
            '"Design is not just what it looks like. Design is how it works." – Steve Jobs',
            '"Content is king, but engagement is queen, and she rules the house." – Mari Smith',
            '"Don’t find customers for your products, find products for your customers." – Seth Godin',
            '"Advertising is the ability to sense, feel and deposit the very heart-beat of the business." – Leo Burnett',
            '"Make it simple. Make it memorable. Make it inviting to look at." – Leo Burnett',
            '"People don\'t buy what you do; they buy why you do it." – Simon Sinek'
        ]

        self.initUI()
        
        # אנימציה לרקע
        self.gradient_offset = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def showEvent(self, event):
        """פונקציה שרצה בכל פעם שהמסך הופך לנראה - כאן קורה הרנדום"""
        super().showEvent(event)
        self.prompt_input.setPlaceholderText("e.g. " + random.choice(self.prompts_examples))
        self.quote_label.setText(random.choice(self.marketing_quotes))

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
        self.setWindowTitle("InstaAD | AI Generation")
        self.setMinimumSize(1200, 850)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        self.card = QFrame()
        self.card.setFixedWidth(650)
        self.card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.07);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 35px;
            }
            QLabel { border: none; background: transparent; color: white; }
        """)
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(50, 40, 50, 30)
        card_layout.setSpacing(15)

        # Nav
        nav_layout = QHBoxLayout()
        self.back_btn = QPushButton("← Back")
        self.logout_btn = QPushButton("Logout")
        for btn in [self.back_btn, self.logout_btn]:
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("color: #a0aec0; background: transparent; font-size: 13px; border: none;")
        self.back_btn.clicked.connect(lambda: self.parent.setCurrentWidget(self.user_home_screen or self.parent.user_home_screen))
        self.logout_btn.clicked.connect(self.on_logout)
        nav_layout.addWidget(self.back_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.logout_btn)
        card_layout.addLayout(nav_layout)

        # Title
        title_label = QLabel("Create Your Magic")
        title_label.setFont(QFont("Segoe UI", 30, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)

        # Input
        self.prompt_input = QLineEdit()
        self.prompt_input.setMinimumHeight(65)
        self.prompt_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 15px;
                padding: 15px;
                color: white;
                font-size: 15px;
            }
            QLineEdit:focus { border: 1px solid #00f2fe; }
        """)
        card_layout.addWidget(self.prompt_input)

        # Generate Button
        self.generate_btn = QPushButton("GENERATE AD")
        self.generate_btn.setFixedHeight(65)
        self.generate_btn.setCursor(Qt.PointingHandCursor)
        self.generate_btn.clicked.connect(self.on_generate_clicked)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00f2fe, stop:1 #4facfe);
                color: #0d1117; font-weight: 900; font-size: 16px; border-radius: 15px;
            }
            QPushButton:hover { background: white; }
        """)
        
        gen_shadow = QGraphicsDropShadowEffect()
        gen_shadow.setBlurRadius(30)
        gen_shadow.setColor(QColor(0, 242, 254, 100))
        self.generate_btn.setGraphicsEffect(gen_shadow)
        card_layout.addWidget(self.generate_btn)

        self.quote_label = QLabel("")
        # הגדרת הסטייל ישירות ב-CSS מבטיחה שהגודל יישאר קטן (8pt)
        self.quote_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.4); 
                font-size: 20px; 
                font-style: italic;
                background: transparent;
                border: none;
                padding-top: 15px;
            }
        """)
        self.quote_label.setWordWrap(True)
        self.quote_label.setAlignment(Qt.AlignCenter)
        self.quote_label.setMinimumHeight(80) 
        card_layout.addWidget(self.quote_label)

        card_layout.addStretch()
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(70)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.card.setGraphicsEffect(shadow)
        main_layout.addWidget(self.card)

    def on_logout(self):
        logout_user_request(self.username)
        self.parent.setCurrentWidget(self.parent.welcome_screen)

    def on_generate_clicked(self):
        # ... לוגיקה ללא שינוי ...
        prompt = self.prompt_input.text().strip()
        if not prompt:
            QMessageBox.warning(self, "Error", "Please enter a prompt")
            return
        result = handle_generate(prompt, self.username)
        if result.get("success"):
            data = result.get("data", {})
            task_id = data.get("task_id")
            if task_id:
                self.preview_window = AdPreviewScreen(
                    task_id=task_id,
                    keywords=data.get("keywords", []),
                    username=self.username,
                    go_back_callback=self.return_from_preview
                )
                self.hide()
                self.preview_window.show()
                return
        QMessageBox.critical(self, "Error", result.get("message", "Video generation failed"))

    def return_from_preview(self):
        if self.preview_window:
            self.preview_window.close()
            self.preview_window = None
        self.show()