import sys
import random
import os
import math
import tempfile
import requests
import vlc
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QScrollArea, QGridLayout, QPushButton, QFrame, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor, QPainter, QLinearGradient
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtMultimediaWidgets import QVideoWidget

from Backend.logic.save_ad_logic import handle_get_ad, handle_delete_ad

# מחלקת חלקיקים להמשכיות העיצוב
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

class AdHistoryScreen(QWidget):
    def __init__(self, parent, username):
        super().__init__()
        self.parent = parent
        self.username = username
        self.particles = [Particle(1200, 800) for _ in range(60)]
        
        self.initUI()
        
        # אנימציה לרקע
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
        self.setWindowTitle("InstaAD | Saved Ads")
        self.setMinimumSize(1200, 850)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(40, 40, 40, 40)
        self.main_layout.setSpacing(25)

        # Header: Back Button + Title
        header_layout = QHBoxLayout()
        
        back_btn = QPushButton("← Back")
        back_btn.setFixedSize(100, 40)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover { background: rgba(255, 255, 255, 0.2); }
        """)
        back_btn.clicked.connect(self.go_back)
        header_layout.addWidget(back_btn)
        
        header_layout.addStretch()

        title = QLabel("Advertisement Gallery")
        title.setFont(QFont("Segoe UI", 28, QFont.Bold))
        title.setStyleSheet("color: white; border: none; background: transparent;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        # מרווח בצד ימין כדי שהכותרת תהיה במרכז באמת
        header_layout.addSpacing(100) 

        self.main_layout.addLayout(header_layout)

        # Scroll Area Styling (שקיפות היא המפתח כאן)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.05);
                width: 10px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical {
                background: #00f2fe;
                min-height: 20px;
                border-radius: 5px;
            }
        """)

        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")
        self.grid = QGridLayout()
        self.grid.setSpacing(30)
        self.container.setLayout(self.grid)
        self.scroll.setWidget(self.container)
        
        self.main_layout.addWidget(self.scroll)

    def load_ads(self, username: str):
        self.username = username
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        ads = handle_get_ad(self.username)
        row = col = 0
        for ad in ads:
            card = self.create_ad_card(ad)
            self.grid.addWidget(card, row, col)
            col += 1
            if col == 2:
                col = 0
                row += 1

    def create_ad_card(self, ad: dict):
        card = QFrame()
        card.setMinimumHeight(350)
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.07);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
            }
        """)
        card.layout = QVBoxLayout(card)
        card.layout.setContentsMargins(20, 20, 20, 20)
        card.layout.setSpacing(15)
        
        card.ad_id = ad["_id"]
        card.video_url = ad["video_url"]
        card.saved_at = ad["saved_at"]
        card.is_playing = False

        card.vlc_instance = vlc.Instance("--no-xlib", "--quiet")
        card.vlc_player = card.vlc_instance.media_player_new()

        self._build_card_normal(card)
        
        # צל עדין לכרטיס
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 100))
        card.setGraphicsEffect(shadow)
        
        return card

    def _build_card_normal(self, card):
        self._clear_layout(card.layout)
        
        # תצוגת תאריך
        date_label = QLabel(f"Generated on:\n{card.saved_at}")
        date_label.setFont(QFont("Segoe UI", 11))
        date_label.setStyleSheet("color: #a0aec0; border: none; background: transparent;")
        date_label.setAlignment(Qt.AlignCenter)
        card.layout.addWidget(date_label)

        card.layout.addStretch()

        # כפתור צפייה
        view_btn = QPushButton("▶ PLAY VIDEO")
        view_btn.setFixedHeight(50)
        view_btn.setCursor(Qt.PointingHandCursor)
        view_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00f2fe, stop:1 #4facfe);
                color: #0d1117;
                font-weight: 800;
                border-radius: 12px;
            }
            QPushButton:hover { background: white; }
        """)
        view_btn.clicked.connect(lambda: self._on_view_clicked(card))
        card.layout.addWidget(view_btn)

        # כפתור מחיקה
        delete_btn = QPushButton("🗑 Delete Ad")
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setStyleSheet("""
            QPushButton {
                color: #e74c3c;
                background: transparent;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover { color: #ff5e57; text-decoration: underline; }
        """)
        delete_btn.clicked.connect(lambda: self.delete_ad(card))
        card.layout.addWidget(delete_btn)

    def _build_card_video(self, card):
        self._clear_layout(card.layout)

        # כפתור סגירה (X)
        top_bar = QHBoxLayout()
        close_btn = QPushButton("✕ Close")
        close_btn.setStyleSheet("color: #a0aec0; background: transparent; border: none; font-weight: bold;")
        close_btn.clicked.connect(lambda: self._close_card_video(card))
        top_bar.addStretch()
        top_bar.addWidget(close_btn)
        card.layout.addLayout(top_bar)

        # ווידג'ט הוידאו
        card.video_widget = QVideoWidget()
        card.video_widget.setStyleSheet("background-color: black; border-radius: 10px;")
        card.video_widget.setMinimumHeight(220)
        card.layout.addWidget(card.video_widget)

        # הורדה וטעינה של הוידאו
        temp_path = os.path.join(tempfile.gettempdir(), f"history_{card.ad_id}.mp4")
        if not os.path.exists(temp_path):
            try:
                r = requests.get(card.video_url, stream=True)
                with open(temp_path, "wb") as f:
                    for chunk in r.iter_content(1024 * 1024):
                        f.write(chunk)
            except: pass

        media = card.vlc_instance.media_new(temp_path)
        media.add_option("input-repeat=9999")
        card.vlc_player.set_media(media)
        self._bind_vlc(card)
        card.vlc_player.play()

    # --- שאר הלוגיקה שלך (ללא שינוי) ---
    def _on_view_clicked(self, card):
        if not card.is_playing:
            card.is_playing = True
            self._build_card_video(card)

    def _close_card_video(self, card):
        if card.vlc_player.is_playing():
            card.vlc_player.stop()
        card.is_playing = False
        self._build_card_normal(card)

    def delete_ad(self, card):
        confirm = QMessageBox.question(self, "Delete Ad", "Are you sure you want to delete this ad?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            if card.vlc_player.is_playing(): card.vlc_player.stop()
            if handle_delete_ad(card.ad_id): self.load_ads(self.username)

    def _bind_vlc(self, card):
        win_id = int(card.video_widget.winId())
        if sys.platform.startswith("win"): card.vlc_player.set_hwnd(win_id)
        elif sys.platform.startswith("linux"): card.vlc_player.set_xwindow(win_id)
        elif sys.platform == "darwin": card.vlc_player.set_nsobject(win_id)

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            elif item.layout(): self._clear_layout(item.layout())

    def go_back(self):
        self.parent.setCurrentWidget(self.parent.user_home_screen)

    def closeEvent(self, event):
        for i in range(self.grid.count()):
            w = self.grid.itemAt(i).widget()
            if hasattr(w, "vlc_player"): w.vlc_player.stop()
        event.accept()