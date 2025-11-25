from Backend.logic.register_logic import register_user, validate_inputs
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, 
    QComboBox, QDateEdit, QGraphicsDropShadowEffect, QMessageBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QDate

class RegisterScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle("InstaAD - Register")
        self.setGeometry(400, 400, 550, 680)

        # רקע גרדיאנט אחיד
        self.setStyleSheet("""
            RegisterScreen {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea,
                    stop:1 #764ba2
                );
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # כרטיס לבן עם צל
        card_widget = QWidget()
        card_widget.setStyleSheet("""
            background-color: white;
            border-radius: 20px;
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0,0,0,80))
        card_widget.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(18)

        # כותרת
        title = QLabel("Create Your Account")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50;")
        title.setWordWrap(True)
        card_layout.addWidget(title)

        subtitle = QLabel("Join InstaAD today")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #7f8c8d;")
        card_layout.addWidget(subtitle)

        # סטייל אחיד לשדות
        input_style = """
            QLineEdit, QDateEdit, QComboBox {
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 12px 15px;
                font-size: 14px;
                color: #2c3e50;
            }
            QLineEdit:focus, QDateEdit:focus, QComboBox:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
            QLineEdit:hover, QDateEdit:hover, QComboBox:hover {
                border: 2px solid #b8c5f2;
            }
        """
        label_style = "color: #495057; font-weight: 600; margin-bottom: 5px;"

        # שדות קלט
        fields = [
            ("👤 Username", QLineEdit, "Enter your username"),
            ("🔒 Password", QLineEdit, "Enter your password", True),
            ("📅 Birthdate", QDateEdit, None),
            ("💼 Business Type", QComboBox, ["Self-employed", "Salaried employee"]),
            ("🏢 Business Field", QLineEdit, "e.g., Cosmetics, Gym, Food")
        ]

        for field in fields:
            label = QLabel(field[0])
            label.setFont(QFont("Segoe UI", 11))
            label.setStyleSheet(label_style)
            card_layout.addWidget(label)

            if field[1] == QLineEdit:
                widget = QLineEdit()
                if len(field) > 3 and field[3]:
                    widget.setEchoMode(QLineEdit.Password)
                widget.setPlaceholderText(field[2])
            elif field[1] == QDateEdit:
                widget = QDateEdit()
                widget.setCalendarPopup(True)
                widget.setDate(QDate.currentDate())
            elif field[1] == QComboBox:
                widget = QComboBox()
                widget.addItems(field[2])

            widget.setFont(QFont("Segoe UI", 13))
            widget.setMinimumHeight(45)
            widget.setStyleSheet(input_style)
            setattr(self, field[0].split(" ")[-1].lower() + "_input", widget)  # לשמור לשימוש בלוגיקה
            card_layout.addWidget(widget)

        # Register button
        register_btn = QPushButton("Create Account")
        register_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        register_btn.setMinimumHeight(50)
        register_btn.setCursor(Qt.PointingHandCursor)
        register_btn.clicked.connect(self.register)
        register_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border-radius: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #5568d3, stop:1 #6a3f8f);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4e5dc8, stop:1 #5d3782);
            }
        """)
        btn_shadow = QGraphicsDropShadowEffect()
        btn_shadow.setBlurRadius(15)
        btn_shadow.setXOffset(0)
        btn_shadow.setYOffset(5)
        btn_shadow.setColor(QColor(102, 126, 234, 100))
        register_btn.setGraphicsEffect(btn_shadow)
        card_layout.addWidget(register_btn)

        # Back Button
        back_btn = QPushButton("← Back to Login")
        back_btn.setFont(QFont("Segoe UI", 12))
        back_btn.setMinimumHeight(45)
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.clicked.connect(self.back_clicked)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #667eea;
                border: 2px solid #667eea;
                border-radius: 10px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #f0f3ff;
                border: 2px solid #5568d3;
                color: #5568d3;
            }
            QPushButton:pressed {
                background-color: #e0e7ff;
            }
        """)
        card_layout.addWidget(back_btn)

        card_widget.setLayout(card_layout)
        main_layout.addWidget(card_widget)
        main_layout.addStretch()
        self.setLayout(main_layout)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        birthdate = self.birthdate_input.date().toString("yyyy-MM-dd")
        business_type = self.type_input.currentText()
        business_field = self.field_input.text()

        success, msg = register_user(username, password, birthdate, business_type, business_field)

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Registration")
        if success:
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setText(msg)
            msg_box.exec_()
            self.parent.setCurrentWidget(self.parent.welcome_screen)
        else:
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setText(msg)
            msg_box.exec_()

    def back_clicked(self):
        self.parent.setCurrentWidget(self.parent.welcome_screen)