import sys
import random
import os
import math
import requests
import tempfile
import vlc
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit, QMessageBox, QFrame, QGraphicsDropShadowEffect
)
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QFont, QColor, QPainter, QLinearGradient
from PyQt5.QtMultimediaWidgets import QVideoWidget
from Backend.logic.save_ad_logic import handle_save_ad
from Backend.logic.generate_ad_logic import handle_submit_feedback

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

class AdPreviewScreen(QWidget):
    def __init__(self, task_id: str, keywords: list[str], username: str, go_back_callback):
        super().__init__()
        self.task_id = task_id
        self.keywords = keywords
        self.username = username
        self.go_back_callback = go_back_callback
        self.current_video_url = None
        self.feedback_text = ""
        
        self.particles = [Particle(1200, 800) for _ in range(60)]
        self.initUI()
        self.start_polling()
        
        # אנימציה לרקע
        self.gradient_offset = 0
        self.timer_anim = QTimer(self)
        self.timer_anim.timeout.connect(self.update_frame)
        self.timer_anim.start(30)

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
        self.setWindowTitle("InstaAD | Ad Preview")
        self.setMinimumSize(800, 700)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # כרטיס הזכוכית
        self.card = QFrame()
        self.card.setFixedWidth(700)
        self.card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.07);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 30px;
            }
            QLabel { border: none; background: transparent; color: white; }
        """)
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)

        # כותרת וסטטוס
        header_layout = QVBoxLayout()
        self.title = QLabel("AI Video Premiere")
        self.title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        
        self.status_label = QLabel("Status: Generating magic...")
        self.status_label.setFont(QFont("Segoe UI", 12))
        self.status_label.setStyleSheet("color: #00f2fe;")
        self.status_label.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(self.title)
        header_layout.addWidget(self.status_label)
        card_layout.addLayout(header_layout)

        # נגן הוידאו (מוסתר בהתחלה)
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumHeight(300)
        self.video_widget.setStyleSheet("background-color: black; border-radius: 15px; border: 1px solid rgba(255,255,255,0.1);")
        self.video_widget.hide()
        card_layout.addWidget(self.video_widget)

        # כפתורי פעולה
        btns_layout = QHBoxLayout()
        self.try_again_btn = QPushButton("↺ Regenerate")
        self.save_btn = QPushButton("💾 Save to Gallery")
        self.save_btn.setEnabled(False)

        btn_style = """
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                color: white; border-radius: 12px;
                padding: 12px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background: rgba(255, 255, 255, 0.2); }
            QPushButton:disabled { color: rgba(255,255,255,0.2); background: transparent; }
        """
        self.try_again_btn.setStyleSheet(btn_style)
        self.save_btn.setStyleSheet(btn_style.replace("rgba(255, 255, 255, 0.1)", "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #00f2fe, stop:1 #4facfe)").replace("color: white", "color: #0d1117"))
        
        btns_layout.addWidget(self.try_again_btn)
        btns_layout.addWidget(self.save_btn)
        card_layout.addLayout(btns_layout)

        # אזור פידבק
        feedback_container = QVBoxLayout()
        feedback_label = QLabel("Improve next results:")
        feedback_label.setStyleSheet("color: #a0aec0; font-size: 11px; font-weight: bold;")
        
        self.feedback_input = QTextEdit()
        self.feedback_input.setPlaceholderText("Notes for the AI (e.g. 'Make it more energetic', 'Change lighting')...")
        self.feedback_input.setFixedHeight(80)
        self.feedback_input.setEnabled(False)
        self.feedback_input.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 0, 0, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                color: white;
                padding: 10px;
            }
        """)
        
        self.submit_feedback_btn = QPushButton("Submit Optimization")
        self.submit_feedback_btn.setEnabled(False)
        self.submit_feedback_btn.setCursor(Qt.PointingHandCursor)
        self.submit_feedback_btn.setStyleSheet("""
            QPushButton {
                background: transparent; color: #00f2fe; border: 1px solid #00f2fe; 
                border-radius: 8px; font-size: 12px; font-weight: bold; padding: 5px;
            }
            QPushButton:hover { background: rgba(0, 242, 254, 0.1); }
        """)
        
        feedback_container.addWidget(feedback_label)
        feedback_container.addWidget(self.feedback_input)
        feedback_container.addWidget(self.submit_feedback_btn)
        card_layout.addLayout(feedback_container)

        self.submit_feedback_btn.clicked.connect(self.submit_feedback)
        self.try_again_btn.clicked.connect(self.on_try_again)
        self.save_btn.clicked.connect(self.save_ad)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(80)
        shadow.setColor(QColor(0, 0, 0, 180))
        self.card.setGraphicsEffect(shadow)
        main_layout.addWidget(self.card)

        # VLC
        self.vlc_instance = vlc.Instance("--no-xlib", "--quiet")
        self.vlc_player = self.vlc_instance.media_player_new()

    # ======================
    # הלוגיקה שלך (ללא שינוי)
    # ======================
    def start_polling(self):
        self.poll_timer = QTimer()
        self.poll_timer.timeout.connect(self.check_status)
        self.poll_timer.start(3000)

    def check_status(self):
        try:
            response = requests.post("http://127.0.0.1:8000/check-video-status", json={"task_id": self.task_id}, timeout=10)
            data = response.json()
            status = data.get("status", "UNKNOWN")
            if status == "PROCESSING": self.status_label.setText("Status: Finalizing frames...")
            elif status == "FAILED":
                self.poll_timer.stop()
                self.status_label.setText("❌ Generation failed")
            elif status == "SUCCESS":
                self.poll_timer.stop()
                video_url = data.get("video_url")
                if video_url: self.load_video(video_url)
                else: self.status_label.setText("❌ Video URL missing")
            else: self.status_label.setText(f"Status: {status}")
        except Exception as e: self.status_label.setText(f"Error: {e}")

    def load_video(self, url: str):
        self.current_video_url = url
        self.status_label.setText("✅ Masterpiece Ready!")
        r = requests.get(url, stream=True)
        temp_path = os.path.join(tempfile.gettempdir(), f"{self.task_id}.mp4")
        with open(temp_path, "wb") as f:
            for chunk in r.iter_content(1024 * 1024): f.write(chunk)
        self.video_widget.show()
        media = self.vlc_instance.media_new(temp_path)
        media.add_option("input-repeat=9999")
        self.vlc_player.set_media(media)
        self._bind_vlc_to_widget()
        self.vlc_player.play()
        self.save_btn.setEnabled(True)
        self.feedback_input.setEnabled(True)
        self.submit_feedback_btn.setEnabled(True)

    def _bind_vlc_to_widget(self):
        win_id = int(self.video_widget.winId())
        if sys.platform.startswith("win"): self.vlc_player.set_hwnd(win_id)
        elif sys.platform.startswith("linux"): self.vlc_player.set_xwindow(win_id)
        elif sys.platform == "darwin": self.vlc_player.set_nsobject(win_id)

    def on_try_again(self):
        self.poll_timer.stop()
        if self.vlc_player.is_playing(): self.vlc_player.stop()
        self.close()
        self.go_back_callback()

    def save_ad(self):
        result = handle_save_ad(username=self.username, task_id=self.task_id, video_url=self.current_video_url)
        self.status_label.setText(result["message"])

    def submit_feedback(self):
        self.feedback_text = self.feedback_input.toPlainText().strip()
        if not self.feedback_text:
            QMessageBox.warning(self, "Feedback", "Please enter feedback before submitting.")
            return
        result = handle_submit_feedback(user_id=self.username, feedback=self.feedback_text)
        if result["success"]:
            QMessageBox.information(self, "Feedback", result["message"])
            self.feedback_input.clear()
            self.submit_feedback_btn.setEnabled(False)
        else: QMessageBox.warning(self, "Feedback", result["message"])

    def closeEvent(self, event):
        if self.vlc_player.is_playing(): self.vlc_player.stop()
        event.accept()