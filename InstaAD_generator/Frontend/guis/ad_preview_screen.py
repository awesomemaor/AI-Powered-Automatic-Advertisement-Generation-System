from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class AdPreviewScreen(QWidget):
    def __init__(self, ad_data: dict, go_back_callback):
        super().__init__()

        self.ad_data = ad_data
        self.go_back_callback = go_back_callback

        self.setWindowTitle("Ad Preview")
        self.setMinimumSize(500, 400)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignTop)

        # ---- Title ----
        title = QLabel("AI Advertisement Preview")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # ---- Status ----
        status = QLabel("Status: Generated successfully")
        status.setFont(QFont("Segoe UI", 12))
        status.setAlignment(Qt.AlignCenter)
        layout.addWidget(status)

        # ---- Placeholder for video ----
        preview_box = QLabel("🎬 Video Preview Placeholder\n(Google AI Studio output)")
        preview_box.setAlignment(Qt.AlignCenter)
        preview_box.setStyleSheet("""
            QLabel {
                background-color: #f2f2f2;
                border: 2px dashed #aaa;
                border-radius: 12px;
                padding: 40px;
                color: #555;
            }
        """)
        preview_box.setMinimumHeight(180)
        layout.addWidget(preview_box)

        # ---- Prompt / keywords ----
        if "keywords" in self.ad_data:
            keywords_label = QLabel(
                "Keywords used:\n" + ", ".join(self.ad_data["keywords"])
            )
            keywords_label.setWordWrap(True)
            keywords_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(keywords_label)

        # ---- Buttons ----
        btn_layout = QHBoxLayout()

        self.save_btn = QPushButton("Save Ad")
        self.try_again_btn = QPushButton("Try Again")

        for btn in (self.save_btn, self.try_again_btn):
            btn.setMinimumHeight(40)
            btn.setCursor(Qt.PointingHandCursor)

        btn_layout.addWidget(self.try_again_btn)
        btn_layout.addWidget(self.save_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # ---- Events ----
        self.try_again_btn.clicked.connect(self.on_try_again)
        self.save_btn.clicked.connect(self.save_ad)

    def on_try_again(self):
        self.close()
        self.go_back_callback()

    def save_ad(self):
        print("Saved ad:", self.ad_data)
