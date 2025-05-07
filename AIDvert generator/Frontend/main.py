from guis.welcome_screen import WelcomeScreen 
from guis.login_screen import LoginScreen
from PyQt5.QtWidgets import QApplication, QStackedWidget
import sys
import os

class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.welcome_screen = WelcomeScreen(self)
        self.login_screen = LoginScreen(self)

        self.addWidget(self.welcome_screen) # stacking it to index 0
        self.addWidget(self.login_screen) # stacking it to index 1

        self.setCurrentWidget(self.welcome_screen) # setting the welcome screen as the default screen

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # loading the QSS file for styling
    qss_path = os.path.join(os.path.dirname(__file__), "styles", "style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r") as file:
            app.setStyleSheet(file.read())

    window = MainApp()
    window.show()

    sys.exit(app.exec_())
