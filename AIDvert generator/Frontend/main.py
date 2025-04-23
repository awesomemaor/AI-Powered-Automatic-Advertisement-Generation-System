import sys
import os
from guis.welcome_screen import WelcomeScreen  # Correct import
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Optional: load external stylesheet
    qss_path = os.path.join(os.path.dirname(__file__), "styles", "style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r") as file:
            app.setStyleSheet(file.read())

    window = WelcomeScreen()
    window.show()

    sys.exit(app.exec_())
