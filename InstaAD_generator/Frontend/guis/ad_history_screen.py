from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout,
    QScrollArea, QGridLayout, QPushButton, QFrame, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.QtMultimediaWidgets import QVideoWidget

from Backend.logic.save_ad_logic import handle_get_ad, handle_delete_ad

import vlc
import requests
import tempfile
import os
import sys


class AdHistoryScreen(QWidget):
    def __init__(self, parent, username):
        super().__init__()
        self.parent = parent
        self.username = username

        # ======================
        # Main Layout
        # ======================
        self.main_layout = QVBoxLayout(self)

        # Top layout: Back button + Title
        top_layout = QHBoxLayout()

        # Back button
        back_btn = QPushButton("← Back")
        back_btn.setFixedSize(80, 32)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """)
        back_btn.clicked.connect(self.go_back)
        top_layout.addWidget(back_btn, alignment=Qt.AlignLeft)

        # Title label
        title = QLabel("Saved Advertisements")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(title)
        top_layout.addStretch()  # דוחף את ה־Title למרכז

        # הוספה של top_layout ל־main_layout
        self.main_layout.addLayout(top_layout)

        # ======================
        # Scroll Area
        # ======================
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()
        self.grid = QGridLayout()
        self.grid.setSpacing(20)

        self.container.setLayout(self.grid)
        self.scroll.setWidget(self.container)

        self.main_layout.addWidget(self.scroll)

    # ======================
    # Load Ads
    # ======================
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

    # ======================
    # Card Creation
    # ======================
    def create_ad_card(self, ad: dict):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 12px;
            }
        """)

        card.layout = QVBoxLayout(card)
        card.ad_id = ad["_id"]
        card.video_url = ad["video_url"]
        card.saved_at = ad["saved_at"]

        card.vlc_instance = vlc.Instance("--no-xlib", "--quiet", "--no-plugins-cache")
        card.vlc_player = card.vlc_instance.media_player_new()

        self._build_card_normal(card)
        return card

    # ======================
    # Normal Card State
    # ======================
    # card in normal state, shows saved at, view and delete buttons
    def _build_card_normal(self, card):
        self._clear_layout(card.layout)

        label = QLabel(f"Saved at:\n{card.saved_at}")
        label.setAlignment(Qt.AlignCenter)

        view_btn = QPushButton("▶ View")
        delete_btn = QPushButton("🗑 Delete")

        view_btn.clicked.connect(
            lambda: self._build_card_video(card)
        )
        delete_btn.clicked.connect(
            lambda: self.delete_ad(card)
        )

        card.layout.addWidget(label)
        card.layout.addWidget(view_btn)
        card.layout.addWidget(delete_btn)

    # ======================
    # Video Card State
    # ======================
    # card when a video is playing, it switches the Qt card layout to show the video widget
    def _build_card_video(self, card):
        self._clear_layout(card.layout)

        top = QHBoxLayout()
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(24, 24)
        close_btn.setStyleSheet("""
            QPushButton {
                border: none;
                font-size: 14px;
            }
            QPushButton:hover {
                color: red;
            }
        """)

        close_btn.clicked.connect(
            lambda: self._close_card_video(card)
        )

        top.addStretch()
        top.addWidget(close_btn)
        card.layout.addLayout(top)

        card.video_widget = QVideoWidget()
        card.video_widget.setMinimumHeight(220)
        card.layout.addWidget(card.video_widget)

        temp_path = os.path.join(
            tempfile.gettempdir(),
            f"history_{card.ad_id}.mp4"
        )

        if not os.path.exists(temp_path):
            r = requests.get(card.video_url, stream=True)
            with open(temp_path, "wb") as f:
                for chunk in r.iter_content(1024 * 1024):
                    f.write(chunk)

        media = card.vlc_instance.media_new(temp_path)
        media.add_option("input-repeat=9999")  # LOOP FOREVER
        card.vlc_player.set_media(media)

        self._bind_vlc(card)
        card.vlc_player.play()

    # ======================
    # Close Video
    # ======================
    def _close_card_video(self, card):
        if card.vlc_player.is_playing():
            card.vlc_player.stop()
        self._build_card_normal(card)

    # ======================
    # Delete Ad
    # ======================
    def delete_ad(self, card):
        confirm = QMessageBox.question(
            self,
            "Delete Ad",
            "Are you sure you want to delete this ad?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            if card.vlc_player.is_playing():
                card.vlc_player.stop()

            success = handle_delete_ad(card.ad_id)
            if success:
                self.load_ads(self.username)

    # ======================
    # VLC Binding
    # ======================
    def _bind_vlc(self, card):
        win_id = int(card.video_widget.winId())

        if sys.platform.startswith("win"):
            card.vlc_player.set_hwnd(win_id)
        elif sys.platform.startswith("linux"):
            card.vlc_player.set_xwindow(win_id)
        elif sys.platform == "darwin":
            card.vlc_player.set_nsobject(win_id)

    # ======================
    # Utils
    # ======================
    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def go_back(self):
        self.parent.setCurrentWidget(self.parent.user_home_screen)

    # ======================
    # Cleanup
    # ======================
    def closeEvent(self, event):
        for i in range(self.grid.count()):
            w = self.grid.itemAt(i).widget()
            if hasattr(w, "vlc_player") and w.vlc_player.is_playing():
                w.vlc_player.stop()
        event.accept()
