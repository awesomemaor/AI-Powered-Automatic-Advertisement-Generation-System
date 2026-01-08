# guis/generate_screen.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QGraphicsDropShadowEffect, QMessageBox
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from Backend.logic.login_logic import logout_user_request
from Backend.logic.generate_ad_logic import handle_generate
from guis.ad_preview_screen import AdPreviewScreen

class GenerateScreen(QWidget):
    def __init__(self, parent, username, user_home_screen=None):
        super().__init__()
        self.parent = parent
        self.username = username
        self.user_home_screen = user_home_screen  # Reference to the login-created user_home
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Generate Advertisement")
        self.setGeometry(400, 400, 600, 500)

        # רקע עם גרדיאנט מודרני
        self.setStyleSheet("""
            GenerateScreen {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea,
                    stop:1 #764ba2
                );
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 40, 50, 40)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # כרטיס לבן במרכז
        card_widget = QWidget()
        card_widget.setStyleSheet("""
            background-color: white;
            border-radius: 20px;
        """)
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(20)
        card_layout.setAlignment(Qt.AlignCenter)

        # כותרת מסך
        title_label = QLabel("Generate Advertisement")
        title_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)

        # Back & Logout buttons
        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.parent.setCurrentWidget(self.user_home_screen or self.parent.user_home_screen))
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.on_logout)
        for btn in [back_btn, logout_btn]:
            btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #667eea,
                        stop:1 #764ba2
                    );
                    color: white;
                    border-radius: 12px;
                    border: none;
                    padding: 6px 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5568d3,
                        stop:1 #6a3f8f
                    );
                }
                QPushButton:pressed {
                    background: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4e5dc8,
                        stop:1 #5d3782
                    );
                }
            """)
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setXOffset(0)
            shadow.setYOffset(5)
            shadow.setColor(QColor(102, 126, 234, 120))
            btn.setGraphicsEffect(shadow)
            card_layout.addWidget(btn)

        # Prompt input
        self.prompt_input = QLineEdit()
        self.prompt_input.setPlaceholderText("Enter prompt")
        self.prompt_input.setFont(QFont("Segoe UI", 14))
        self.prompt_input.setMinimumHeight(40)
        self.prompt_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #667eea;
                border-radius: 10px;
                padding: 6px 10px;
            }
            QLineEdit:focus {
                border: 2px solid #5568d3;
            }
        """)
        card_layout.addWidget(self.prompt_input)

        # Generate button
        generate_btn = QPushButton("Generate")
        generate_btn.setFont(QFont("Segoe UI", 16, QFont.Bold))
        generate_btn.setMinimumHeight(50)
        generate_btn.setCursor(Qt.PointingHandCursor)
        generate_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea,
                    stop:1 #764ba2
                );
                color: white;
                border-radius: 12px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5568d3,
                    stop:1 #6a3f8f
                );
            }
            QPushButton:pressed {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4e5dc8,
                    stop:1 #5d3782
                );
            }
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(102, 126, 234, 150))
        generate_btn.setGraphicsEffect(shadow)

        generate_btn.clicked.connect(self.on_generate_clicked)
        card_layout.addWidget(generate_btn)

        card_widget.setLayout(card_layout)
        main_layout.addWidget(card_widget, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)
    
    def on_logout(self):
        logout_user_request(self.username)
        self.parent.setCurrentWidget(self.parent.welcome_screen)

    def on_generate_clicked(self):
        prompt = self.prompt_input.text().strip()
        if not prompt:
            QMessageBox.warning(self, "Error", "Please enter a prompt")
            return

        result = handle_generate(prompt, self.username)

        if result.get("success"):
            data = result.get("data", {})

            task_id = data.get("task_id")
            if task_id:
                # יוצרים מסך Preview שיודע לעבוד עם task_id
                self.preview_window = AdPreviewScreen(
                    task_id=task_id,
                    keywords=data.get("keywords", []),
                    go_back_callback=self.return_from_preview
                )
                
                self.hide()
                self.preview_window.show()
                return

        # fallback
        QMessageBox.critical(
            self,
            "Error",
            result.get("message", "Video generation failed")
        )

    # הסבר בשילנו: כשבחלון הסרטון לוחצים אחורה הוא סוגר אותו וזוכר לחזור ל self.show שזה בעצם החלון של האפליקציה הראשי
    def return_from_preview(self):
        """נקראת כשהמשתמש לוחץ Try Again"""
        if self.preview_window:
            self.preview_window.close()
            self.preview_window = None
        self.show()
