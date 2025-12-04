from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices

class AdPreviewScreen(QWidget):
    def __init__(self, video_data, go_back_callback):
        super().__init__()
        self.video_data = video_data
        self.go_back_callback = go_back_callback

        self.setWindowTitle("Video Preview")
        layout = QVBoxLayout()

        self.web = QWebEngineView()
        video_id = video_data["videoId"]
        embed_url = f"https://www.youtube.com/embed/{video_id}"
        self.web.load(QUrl(embed_url))
        #QDesktopServices.openUrl(QUrl(f"https://www.youtube.com/watch?v={video_id}"))
        layout.addWidget(self.web)

        self.save_btn = QPushButton("Save this video")
        self.try_again_btn = QPushButton("Try Again")

        layout.addWidget(self.save_btn)
        layout.addWidget(self.try_again_btn)

        self.setLayout(layout)

        # FIXED
        self.try_again_btn.clicked.connect(self.on_try_again)
        self.save_btn.clicked.connect(self.save_video)

    def on_try_again(self):
        self.close()
        self.go_back_callback()

    def save_video(self):
        print("Video saved:", self.video_data)
 
