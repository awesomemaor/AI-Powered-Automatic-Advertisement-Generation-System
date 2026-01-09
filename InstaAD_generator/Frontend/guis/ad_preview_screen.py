from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtMultimediaWidgets import QVideoWidget

import requests
import tempfile
import os
import sys
import vlc


class AdPreviewScreen(QWidget):
    def __init__(self, task_id: str, keywords: list[str], go_back_callback):
        super().__init__()

        self.task_id = task_id
        self.keywords = keywords
        self.go_back_callback = go_back_callback

        self.setWindowTitle("Ad Preview")
        self.setMinimumSize(600, 450)

        self.init_ui()
        self.start_polling()

    # ======================
    # UI
    # ======================
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        self.title = QLabel("AI Video Advertisement")
        self.title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title)

        self.status_label = QLabel("Status: Generating video...")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        # ---- Video Widget ----
        self.video_widget = QVideoWidget()
        self.video_widget.hide()
        layout.addWidget(self.video_widget)

        # ---- Keywords ----
        if self.keywords:
            kw = QLabel("Keywords:\n" + ", ".join(self.keywords))
            kw.setAlignment(Qt.AlignCenter)
            layout.addWidget(kw)

        # ---- Buttons ----
        btns = QHBoxLayout()
        self.try_again_btn = QPushButton("Try Again")
        self.save_btn = QPushButton("Save Ad")
        self.save_btn.setEnabled(False)

        btns.addWidget(self.try_again_btn)
        btns.addWidget(self.save_btn)
        layout.addLayout(btns)

        self.setLayout(layout)

        self.try_again_btn.clicked.connect(self.on_try_again)
        self.save_btn.clicked.connect(self.save_ad)

        # ---- VLC Player ----
        self.vlc_instance = vlc.Instance()
        self.vlc_player = self.vlc_instance.media_player_new()

    # ======================
    # Polling
    # ======================
    def start_polling(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_status)
        self.timer.start(3000)

    def check_status(self):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/check-video-status",
                json={"task_id": self.task_id},
                timeout=10
            )

            data = response.json()
            status = data.get("status", "UNKNOWN")

            if status == "PROCESSING":
                self.status_label.setText("Status: Still generating...")

            elif status == "FAILED":
                self.timer.stop()
                self.status_label.setText("❌ Generation failed")

            elif status == "SUCCESS":
                self.timer.stop()
                video_url = data.get("video_url")
                if video_url:
                    self.load_video(video_url)
                else:
                    self.status_label.setText("❌ Video URL missing")

            else:
                self.status_label.setText(f"Status: {status}")

        except Exception as e:
            self.status_label.setText(f"Error: {e}")

    # ======================
    # Video (VLC)
    # ======================
    def load_video(self, url: str):
        self.status_label.setText("✅ Video ready!")

        # Download video locally
        r = requests.get(url, stream=True)
        temp_path = os.path.join(
            tempfile.gettempdir(),
            f"{self.task_id}.mp4"
        )

        with open(temp_path, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                f.write(chunk)

        print("VIDEO SAVED TO:", temp_path)

        self.video_widget.show()

        media = self.vlc_instance.media_new(temp_path)
        self.vlc_player.set_media(media)
        self._bind_vlc_to_widget()
        self.vlc_player.play()

        self.save_btn.setEnabled(True)

    def _bind_vlc_to_widget(self):
        win_id = int(self.video_widget.winId())

        if sys.platform.startswith("win"):
            self.vlc_player.set_hwnd(win_id)
        elif sys.platform.startswith("linux"):
            self.vlc_player.set_xwindow(win_id)
        elif sys.platform == "darwin":
            self.vlc_player.set_nsobject(win_id)

    # ======================
    # Events
    # ======================
    def on_try_again(self):
        self.timer.stop()
        if self.vlc_player.is_playing():
            self.vlc_player.stop()
        self.close()
        self.go_back_callback()

    def save_ad(self):
        print(f"Saved video task: {self.task_id}")

    def closeEvent(self, event):
        if self.vlc_player.is_playing():
            self.vlc_player.stop()
        event.accept()
