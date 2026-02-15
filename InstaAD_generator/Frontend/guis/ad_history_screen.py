import sys
import random
import os
import math
import tempfile
import requests
import vlc
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QScrollArea, QGridLayout, QPushButton, QFrame, QMessageBox, 
    QGraphicsDropShadowEffect, QSizePolicy
)
from PyQt5.QtGui import QFont, QColor, QPainter, QLinearGradient, QCursor
from PyQt5.QtCore import Qt, QTimer, QPointF

# ייבוא הלוגיקה מהבאקנד שלך
from Backend.logic.save_ad_logic import handle_get_ad, handle_delete_ad

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

        # Header
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
        header_layout.addSpacing(100) 

        self.main_layout.addLayout(header_layout)

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { background: rgba(255, 255, 255, 0.05); width: 10px; border-radius: 5px; }
            QScrollBar::handle:vertical { background: #00f2fe; min-height: 20px; border-radius: 5px; }
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

    def format_date_string(self, date_str):
        try:
            clean_date = date_str.split('.')[0] 
            dt_obj = datetime.strptime(clean_date, "%Y-%m-%dT%H:%M:%S")
            return dt_obj.strftime("%d %b %Y | %H:%M")
        except Exception:
            return date_str

    def create_ad_card(self, ad: dict):
        card = QFrame()
        card.setMinimumHeight(380)
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(30, 30, 40, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
            }
        """)
        card.layout = QVBoxLayout(card)
        card.layout.setContentsMargins(15, 15, 15, 15)
        card.layout.setSpacing(10)
        
        card.ad_id = ad["_id"]
        card.video_url = ad["video_url"]
        card.saved_at = self.format_date_string(ad["saved_at"])
        card.is_playing = False

        card.vlc_instance = vlc.Instance("--no-xlib", "--quiet")
        card.vlc_player = card.vlc_instance.media_player_new()

        self._build_card_normal(card)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        card.setGraphicsEffect(shadow)
        
        return card

    def _build_card_normal(self, card):
        self._clear_layout(card.layout)
        
        # --- Header Section ---
        header = QHBoxLayout()
        
        # תאריך עם אייקון שעון במקום לוח שנה
        date_lbl = QLabel(f"🕒  {card.saved_at}")
        date_lbl.setFont(QFont("Segoe UI", 10, QFont.Bold))
        date_lbl.setStyleSheet("color: #a0aec0; background: transparent; border: none;")
        header.addWidget(date_lbl)
        
        header.addStretch()
        
        # כפתור מחיקה
        delete_btn = QPushButton("🗑")
        delete_btn.setFixedSize(30, 30)
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setStyleSheet("""
            QPushButton {
                color: #ff5e57;
                background: rgba(255, 94, 87, 0.1);
                border-radius: 6px;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover { background: rgba(255, 94, 87, 0.2); }
        """)
        delete_btn.clicked.connect(lambda: self.delete_ad(card))
        header.addWidget(delete_btn)
        
        card.layout.addLayout(header)

        # --- Preview Section (Styled Placeholder) ---
        # עיצוב מחדש של הריבוע השחור שיהיה יפה
        preview_frame = QFrame()
        preview_frame.setCursor(Qt.PointingHandCursor)
        preview_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #2b32b2, stop:1 #1488cc);
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.1);
            }
            QFrame:hover {
                border: 1px solid #00f2fe;
            }
        """)
        preview_frame.setFixedHeight(220)
        
        # מאפשר לחיצה על הפריים עצמו
        preview_frame.mousePressEvent = lambda event: self._on_view_clicked(card)
        
        preview_layout = QVBoxLayout(preview_frame)
        
        # הוספת אייקון באמצע כדי שלא יהיה רק "שחור"
        icon_lbl = QLabel("🎬")
        icon_lbl.setAlignment(Qt.AlignCenter)
        icon_lbl.setStyleSheet("font-size: 50px; background: transparent; border: none;")
        
        play_lbl = QLabel("Click to Play")
        play_lbl.setAlignment(Qt.AlignCenter)
        play_lbl.setStyleSheet("color: rgba(255,255,255,0.7); font-weight: bold; background: transparent; border: none;")

        preview_layout.addStretch()
        preview_layout.addWidget(icon_lbl)
        preview_layout.addWidget(play_lbl)
        preview_layout.addStretch()
        
        card.layout.addWidget(preview_frame)

        # --- Action Buttons Section (Big Buttons) ---
        btns_layout = QHBoxLayout()
        btns_layout.setSpacing(10)
        
        # כפתור Play גדול
        watch_btn = QPushButton("▶ PLAY")
        watch_btn.setFixedHeight(45)
        watch_btn.setCursor(Qt.PointingHandCursor)
        watch_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        watch_btn.setStyleSheet("""
            QPushButton {
                background: white;
                color: #0d1117;
                font-weight: 800;
                border-radius: 10px;
                font-size: 14px;
            }
            QPushButton:hover { background: #e0e0e0; }
        """)
        watch_btn.clicked.connect(lambda: self._on_view_clicked(card))
        btns_layout.addWidget(watch_btn)

        # כפתור הורדה גדול
        download_btn = QPushButton("⬇ DOWNLOAD")
        download_btn.setFixedHeight(45)
        download_btn.setCursor(Qt.PointingHandCursor)
        download_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        download_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                font-weight: bold;
                border-radius: 10px;
                border: 1px solid rgba(255,255,255,0.2);
                font-size: 13px;
            }
            QPushButton:hover { background: rgba(255, 255, 255, 0.2); color: #00f2fe; border: 1px solid #00f2fe; }
        """)
        download_btn.clicked.connect(lambda: os.startfile(card.video_url) if sys.platform.startswith("win") else os.system(f"open {card.video_url}"))
        btns_layout.addWidget(download_btn)

        card.layout.addLayout(btns_layout)

    def _build_card_video(self, card):
        self._clear_layout(card.layout)

        # Header with Playing text and Close button
        top_bar = QHBoxLayout()
        playing_lbl = QLabel("▶ Now Playing")
        playing_lbl.setStyleSheet("color: #00f2fe; font-weight: bold; border: none; background: transparent;")
        
        close_btn = QPushButton("✕ STOP")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setFixedSize(70, 28)
        close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 0, 0, 0.2);
                color: #ff5e57;
                border-radius: 6px;
                font-weight: bold;
                border: none;
                font-size: 12px;
            }
            QPushButton:hover { background: rgba(255, 0, 0, 0.4); }
        """)
        close_btn.clicked.connect(lambda: self._close_card_video(card))
        
        top_bar.addWidget(playing_lbl)
        top_bar.addStretch()
        top_bar.addWidget(close_btn)
        card.layout.addLayout(top_bar)

        # Video Frame
        video_frame = QFrame()
        video_frame.setFixedHeight(300) 
        video_frame.setStyleSheet("""
            QFrame {
                background-color: black;
                border-radius: 12px;
                border: 1px solid #333;
            }
        """)
        card.layout.addWidget(video_frame)
        card.video_widget = video_frame 

        # Load Video Logic
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
        
        win_id = int(video_frame.winId())
        if sys.platform.startswith("win"): card.vlc_player.set_hwnd(win_id)
        elif sys.platform.startswith("linux"): card.vlc_player.set_xwindow(win_id)
        elif sys.platform == "darwin": card.vlc_player.set_nsobject(win_id)
        
        card.vlc_player.play()

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

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()
            elif item.layout(): self._clear_layout(item.layout())

    def go_back(self):
        for i in range(self.grid.count()):
            w = self.grid.itemAt(i).widget()
            if hasattr(w, "vlc_player"): w.vlc_player.stop()
        self.parent.setCurrentWidget(self.parent.user_home_screen)

    def closeEvent(self, event):
        for i in range(self.grid.count()):
            w = self.grid.itemAt(i).widget()
            if hasattr(w, "vlc_player"): w.vlc_player.stop()
        event.accept()