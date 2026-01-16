# screens/user_home_screen.py

from PyQt5.QtWidgets import QWidget, QMessageBox ,QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from Backend.logic.login_logic import logout_user_request
from Backend.logic.generate_ad_logic import handle_generate
from guis.ad_preview_screen import AdPreviewScreen

class UserHomeScreen(QWidget):
    def __init__(self, parent, username):
        super().__init__()
        self.parent = parent
        self.username = username
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("InstaAD - Home")
        self.setGeometry(400, 400, 600, 500)

        # רקע עם גרדיאנט מודרני
        self.setStyleSheet("""
            UserHomeScreen {
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
        main_layout.setAlignment(Qt.AlignCenter)

        # כרטיס לבן למרכז המסך
        card_widget = QWidget()
        card_widget.setStyleSheet("""
            background-color: white;
            border-radius: 20px;
        """)
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(20)
        card_layout.setAlignment(Qt.AlignCenter)

        # כותרת בולטת
        welcome_label = QLabel(f"Welcome, {self.username}!")
        welcome_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        welcome_label.setStyleSheet("color: #2c3e50;")  # צבע בולט, כהה
        welcome_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(welcome_label)

        # כפתור Logout בחלק העליון של הכרטיס
        self.logout_button = QPushButton("Logout")
        self.logout_button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.logout_button.setCursor(Qt.PointingHandCursor)
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 12px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.logout_button.clicked.connect(self.logout_clicked)
        card_layout.addWidget(self.logout_button, alignment=Qt.AlignRight)

        # כפתורים מרכזיים
        buttons = [
            ("Start New Ad", self.start_new_ad),
            ("Generate Recommended Advertisement", self.generate_recommended),
            ("Advertisement History", self.advertisement_history)
        ]

        for text, func in buttons:
            btn = QPushButton(text)
            btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
            btn.setMinimumHeight(50)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(func)
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
            # צל לכפתור
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setXOffset(0)
            shadow.setYOffset(5)
            shadow.setColor(QColor(102, 126, 234, 120))
            btn.setGraphicsEffect(shadow)
            card_layout.addWidget(btn)

        card_widget.setLayout(card_layout)
        main_layout.addWidget(card_widget, alignment=Qt.AlignCenter)
        self.setLayout(main_layout)

    def start_new_ad(self):
        self.parent.generate_screen.username = self.username
        self.parent.setCurrentWidget(self.parent.generate_screen)

    def generate_recommended(self):
        result = handle_generate(
            prompt=None,
            user_id=self.username,
            mode="recommended"
        )

        if result.get("success"):
            data = result["data"]

            self.preview_window = AdPreviewScreen(
                task_id=data["task_id"],
                keywords=data.get("keywords", []),
                username=self.username,
                go_back_callback=self.return_from_preview
            )

            self.hide()
            self.preview_window.show()
    
    def return_from_preview(self):
        """נקראת כשהמשתמש לוחץ Try Again"""
        if self.preview_window:
            self.preview_window.close()
            self.preview_window = None
        self.show()

    def advertisement_history(self):
        self.parent.ad_history_screen.load_ads(self.username)
        self.parent.setCurrentWidget(self.parent.ad_history_screen)

    def logout_clicked(self):
        result = logout_user_request(self.username)

        if result["success"]:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Logout")
            msg.setText("You have been logged out successfully!")
            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec_()  

            #self.parent.user_home_screen = None
            #self.parent.current_user = None

            self.parent.setCurrentWidget(self.parent.welcome_screen)