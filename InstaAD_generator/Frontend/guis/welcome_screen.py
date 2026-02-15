import sys
import random
import os
import math
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect, 
    QFrame, QHBoxLayout, QDialog, QScrollArea, QGridLayout
)
from PyQt5.QtGui import QFont, QPixmap, QColor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QPointF

# --- חלון עזרה מעוצב ומלוטש ---
class HelpWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("InstaAD | Guide")
        self.setFixedSize(700, 650)  # הגדלתי קצת את החלון שיהיה מרווח
        
        # עיצוב כללי - כהה, נקי ומקצועי
        self.setStyleSheet("""
            QDialog {
                background-color: #151525; 
                color: #e0e0e0;
                border: 1px solid #333;
            }
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { width: 6px; background: #222; }
            QScrollBar::handle:vertical { background: #555; border-radius: 3px; }
        """)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # כותרת ראשית של החלון - קצת יותר קטנה ומעודנת
        header = QLabel("User Guide")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Segoe UI", 18, QFont.Bold))
        header.setStyleSheet("background-color: #0f0c29; color: #00f2fe; padding: 12px; border-bottom: 1px solid #333;")
        layout.addWidget(header)

        # אזור גלילה
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(15) # רווח עדין בין אלמנטים
        content_layout.setContentsMargins(30, 20, 30, 20)

        # פונקציה ליצירת סקשן מעוצב
        def add_section(title, text):
            # מסגרת לכל הסבר
            container = QFrame()
            container.setStyleSheet("""
                QFrame {
                    background-color: #1e1e2d; 
                    border-radius: 8px; 
                    border: 1px solid #2a2a3a;
                }
            """)
            c_layout = QVBoxLayout(container)
            c_layout.setContentsMargins(15, 12, 15, 12)
            c_layout.setSpacing(5)

            # כותרת הסקשן - גודל 13 (מודגש)
            lbl_title = QLabel(title)
            lbl_title.setFont(QFont("Segoe UI", 13, QFont.Bold))
            lbl_title.setStyleSheet("color: #ffffff; border: none;")
            lbl_title.setAlignment(Qt.AlignLeft) 
            
            # טקסט הסבר - גודל 11 (קריא ונקי)
            lbl_text = QLabel(text)
            lbl_text.setFont(QFont("Segoe UI", 11))
            lbl_text.setStyleSheet("color: #b0b0c0; border: none;")
            lbl_text.setWordWrap(True)
            lbl_text.setAlignment(Qt.AlignLeft) 

            c_layout.addWidget(lbl_title)
            c_layout.addWidget(lbl_text)
            
            content_layout.addWidget(container)

        # --- תוכן ההסברים (טקסט קצר ולעניין) ---
        
        add_section("🌟 General Overview", 
                    "InstaAD is an AI-powered platform for creating video ads in seconds. "
                    "Analyze products and target audiences to generate unique content effortlessly.")

        add_section("🔐 Login & Access", 
                    "• Login: Access your dashboard with existing credentials.\n"
                    "• Register: Create a new account to unlock AI features and save projects.")

        add_section("✨ Start New Ad", 
                    "Input product details, select a style, and let the AI generate a complete video ad tailored to your brand.")

        add_section("🤖 Recommended Ad", 
                    "Receive AI-driven suggestions based on current market trends and your past successful campaigns.")

        add_section("📂 Ad History", 
                    "Manage your library. View, download, or delete previously generated advertisements.")

        # הוספת הודעת תודה בסוף
        add_section("💙 Thank You!", 
                    "Thank you for choosing InstaAD! We're committed to revolutionizing your marketing workflow with cutting-edge AI technology. "
                    "Your creativity drives us forward. If you have any feedback or suggestions, we'd love to hear from you. "
                    "Happy creating! 🚀")

        content_layout.addStretch()
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

        # כפתור סגירה
        close_btn = QPushButton("Close Guide")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a2a3a; color: white; border: none;
                padding: 10px; font-weight: bold; font-size: 12px;
            }
            QPushButton:hover { background-color: #3a3a4a; color: #00f2fe; }
        """)
        layout.addWidget(close_btn)

# --- מחלקת חלקיקים ---
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

# --- המסך הראשי ---
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
        
        # רקע
        grad = QLinearGradient(0, 0, self.width(), self.height())
        grad.setColorAt(0, QColor(15, 12, 41))   
        grad.setColorAt(0.5 + (0.1 * math.sin(self.gradient_offset * math.pi * 2)), QColor(48, 43, 99)) 
        grad.setColorAt(1, QColor(36, 36, 62))   
        painter.fillRect(self.rect(), grad)
        
        # חלקיקים
        painter.setPen(Qt.NoPen)
        for p in self.particles:
            painter.setBrush(QColor(0, 242, 254, p.alpha)) 
            painter.drawEllipse(QPointF(p.x, p.y), p.size, p.size)

    def initUI(self):
        self.setWindowTitle("InstaAD | AI Marketing Evolution")
        self.setMinimumSize(1200, 800)

        # שימוש ב-GRID כדי לשים דברים אחד על השני
        # שכבה 0: התוכן המרכזי (לוגו וכו')
        # שכבה 1: הכפתור למעלה (צף)
        grid_layout = QGridLayout(self)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # --- שכבה 1: התוכן המרכזי (בדיוק כמו שהיה, ממורכז) ---
        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        content_h_layout = QHBoxLayout(content_widget)
        content_h_layout.setContentsMargins(0, 0, 0, 0)
        content_h_layout.setSpacing(0)

        # >>> צד שמאל: הויז'ואל והלוגו
        left_side = QFrame()
        left_side.setStyleSheet("background: transparent;")
        left_layout = QVBoxLayout(left_side)
        left_layout.setAlignment(Qt.AlignCenter)
        
        self.logo_label = QLabel()
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
        image_path = os.path.join(base_path, "InstaADlogo.png")
        if os.path.exists(image_path):
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

        # >>> צד ימין: ממשק המשתמש
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

        welcome_text = QLabel("Start Creating.")
        welcome_text.setFont(QFont("Segoe UI", 32, QFont.Bold))
        welcome_text.setStyleSheet("color: white; border: none; background: transparent;")
        
        desc_text = QLabel("The world's most advanced AI ad generation platform.")
        desc_text.setWordWrap(True)
        desc_text.setFont(QFont("Segoe UI", 12))
        desc_text.setStyleSheet("color: #a0aec0; border: none; background: transparent; margin-bottom: 25px;")

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
            QPushButton:hover { background: white; margin-top: -2px; }
        """)

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
            QPushButton:hover { color: #00f2fe; }
        """)

        right_layout.addStretch(1)
        right_layout.addWidget(welcome_text)
        right_layout.addWidget(desc_text)
        right_layout.addSpacing(10)
        right_layout.addWidget(self.login_button)
        right_layout.addWidget(self.register_button)
        right_layout.addStretch(1)

        content_h_layout.addWidget(left_side, 1)
        content_h_layout.addWidget(right_side)

        # --- הוספת התוכן המרכזי לגריד (תופס את כל המסך) ---
        grid_layout.addWidget(content_widget, 0, 0)

        # --- שכבה 2: כפתור העזרה "צף" בפינה הימנית העליונה ---
        # אנחנו יוצרים מיכל קטן רק לכפתור כדי למקם אותו
        help_container = QWidget()
        help_container.setStyleSheet("background: transparent;")
        help_layout = QHBoxLayout(help_container)
        help_layout.setContentsMargins(0, 20, 30, 0) # מרווחים מהקצוות: 20 מלמעלה, 30 מימין
        help_layout.addStretch() # דוחף את הכפתור ימינה

        self.help_btn = QPushButton("❓ Help / Guide")
        self.help_btn.setCursor(Qt.PointingHandCursor)
        self.help_btn.clicked.connect(self.show_help)
        self.help_btn.setFixedSize(155, 42)
        self.help_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 0, 0, 0.4);
                color: #a0aec0;
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 21px;
                font-size: 12px;
                font-weight: bold;
                padding: 0px 15px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.6);
                color: white;
                border-color: #00f2fe;
            }
        """)
        help_layout.addWidget(self.help_btn)

        # הוספת כפתור העזרה לגריד, באותו מקום (0,0) אבל עם יישור למעלה
        grid_layout.addWidget(help_container, 0, 0, Qt.AlignTop)

    def go_to_Login(self):
        self.parent.setCurrentWidget(self.parent.login_screen)
    
    def go_to_Register(self):
        self.parent.setCurrentWidget(self.parent.register_screen)

    def show_help(self):
        dialog = HelpWindow(self)
        dialog.exec_()