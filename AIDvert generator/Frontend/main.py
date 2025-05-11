import sys
import os
import threading
import uvicorn
from guis.welcome_screen import WelcomeScreen 
from guis.login_screen import LoginScreen
from PyQt5.QtWidgets import QApplication, QStackedWidget
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
#from Backend.api import app as auth_app
from Backend.auth_login import router as login_router
from Backend.db_init import customers_collection

# FastAPI app instance (required for Uvicorn)
app = FastAPI()

app.include_router(login_router)

# Start FastAPI server in a separate thread
def start_fastapi():
    uvicorn.run("main:app", host="127.0.0.1", port=8000)  # removed reload=True

# Main PyQt application
class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.welcome_screen = WelcomeScreen(self)
        self.login_screen = LoginScreen(self)

        self.addWidget(self.welcome_screen)  # stacking it to index 0
        self.addWidget(self.login_screen)    # stacking it to index 1

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
    window.show()

    sys.exit(qt_app.exec_())
