from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtMultimediaWidgets import QVideoWidget
from Backend.logic.save_ad_logic import handle_save_ad
from Backend.logic.generate_ad_logic import handle_submit_feedback

import requests
import tempfile
import os
import sys
import vlc


class AdPreviewScreen(QWidget):
    def __init__(self, task_id: str, keywords: list[str], username: str, go_back_callback):
        super().__init__()

        self.task_id = task_id
        self.keywords = keywords
        self.username = username
        self.go_back_callback = go_back_callback

        self.current_video_url = None
        self.feedback_text = ""

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

        self.title = QLabel("InstaAD Video Advertisement")
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

        # ---- Buttons ----
        btns = QHBoxLayout()
        self.try_again_btn = QPushButton("Regenerate Ad")
        self.save_btn = QPushButton("Save Ad")
        self.save_btn.setEnabled(False)

        btns.addWidget(self.try_again_btn)
        btns.addWidget(self.save_btn)
        layout.addLayout(btns)

        # ---- Feedback Section ----
        self.feedback_input = QTextEdit()
        self.feedback_input.setPlaceholderText(
            "Write notes to improve future ads (style, pacing, tone, etc...)"
        )
        self.feedback_input.setFixedHeight(90)
        self.feedback_input.setEnabled(False)
        layout.addWidget(self.feedback_input)

        self.submit_feedback_btn = QPushButton("Submit Feedback")
        self.submit_feedback_btn.setEnabled(False)
        layout.addWidget(self.submit_feedback_btn)

        self.submit_feedback_btn.clicked.connect(self.submit_feedback)

        self.setLayout(layout)

        self.try_again_btn.clicked.connect(self.on_try_again)
        self.save_btn.clicked.connect(self.save_ad)

        # ---- VLC Player ----
        self.vlc_instance = vlc.Instance("--no-xlib", "--quiet", "--no-plugins-cache")
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
        self.current_video_url = url

        self.status_label.setText("✅ Video ready!")

        r = requests.get(url, stream=True)
        temp_path = os.path.join(tempfile.gettempdir(), f"{self.task_id}.mp4")

        with open(temp_path, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                f.write(chunk)

        self.video_widget.show()

        # enlarge window vertically when video is ready
        current_size = self.size()
        self.resize(current_size.width(), current_size.height() + 220)

        media = self.vlc_instance.media_new(temp_path)
        media.add_option("input-repeat=9999")  # LOOP AD FOREVER

        self.vlc_player.set_media(media)
        self._bind_vlc_to_widget()
        self.vlc_player.play()

        self.save_btn.setEnabled(True)
        self.feedback_input.setEnabled(True)
        self.submit_feedback_btn.setEnabled(True)

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
        result = handle_save_ad(
        username=self.username,
        task_id=self.task_id,
        video_url=self.current_video_url,
        )

        if result["success"]:
            self.status_label.setText(result["message"])
        else:
            self.status_label.setText(result["message"])
    
    def submit_feedback(self):
        self.feedback_text = self.feedback_input.toPlainText().strip()
        
        if not self.feedback_text:
            QMessageBox.warning(self, "Feedback", "Please enter feedback before submitting.")

        result = handle_submit_feedback(
            user_id=self.username,
            feedback=self.feedback_text
            )

        if result["success"]:
            QMessageBox.information(self, "Feedback", result["message"])
            self.feedback_input.clear()
            self.submit_feedback_btn.setEnabled(False)
        else:
            QMessageBox.warning(self, "Feedback", result["message"])

    def closeEvent(self, event):
        if self.vlc_player.is_playing():
            self.vlc_player.stop()
        event.accept()
