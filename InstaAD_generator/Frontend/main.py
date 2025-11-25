import sys
import os
import threading
import uvicorn
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from guis.welcome_screen import WelcomeScreen 
from guis.login_screen import LoginScreen
from guis.register_screen import RegisterScreen
from guis.userHome_screen import UserHomeScreen
from guis.generate_screen import GenerateScreen
from PyQt5.QtWidgets import QApplication, QStackedWidget
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
#from Backend.api import app as auth_app
from Backend.endpoints.auth_login import router as login_router
from Backend.endpoints.auth_register import router as register_router
from Backend.endpoints.db_init import customers_collection

# FastAPI app instance (required for Uvicorn)
app = FastAPI()

app.include_router(login_router)
app.include_router(register_router)

# Start FastAPI server in a separate thread
def start_fastapi():
    uvicorn.run("main:app", host="127.0.0.1", port=8000)  # removed reload=True

# Main PyQt application
class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.welcome_screen = WelcomeScreen(self)
        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self) 
        self.user_home_screen = UserHomeScreen(self, username="")  # username דיפולטיבי
        self.generate_screen = GenerateScreen(self)

        self.addWidget(self.user_home_screen)
        self.addWidget(self.generate_screen)
        self.addWidget(self.welcome_screen)  # stacking it to index 0
        self.addWidget(self.login_screen)    # stacking it to index 1
        self.addWidget(self.register_screen)
    

        self.setCurrentWidget(self.welcome_screen)  # default screen

if __name__ == "__main__":
    # Start FastAPI server in the background
    fastapi_thread = threading.Thread(target=start_fastapi, daemon=True)
    fastapi_thread.start()

    # Start the PyQt5 application
    qt_app = QApplication(sys.argv)

    # Load QSS for styling
    qss_path = os.path.join(os.path.dirname(__file__), "styles", "style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r") as file:
            qt_app.setStyleSheet(file.read())

    window = MainApp()
    window.setGeometry(400, 400, 800, 400)
    window.setWindowTitle("InstaAD")
    #windows.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "assets", "icon.png")))  # Ensure the icon path is correct
    window.show()

    sys.exit(qt_app.exec_())
