import sys
import os
import threading
import uvicorn
import requests  # Required for the connection check
import time

# Define paths (as previously configured)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from guis.welcome_screen import WelcomeScreen 
from guis.login_screen import LoginScreen
from guis.register_screen import RegisterScreen
from guis.userHome_screen import UserHomeScreen
from guis.generate_screen import GenerateScreen
from guis.ad_history_screen import AdHistoryScreen
from PyQt5.QtWidgets import QApplication, QStackedWidget

# Backend imports (in case we need to run a local server fallback)
from fastapi import FastAPI
from Backend.endpoints.auth_login import router as login_router
from Backend.endpoints.auth_register import router as register_router
from Backend.endpoints.generate_ad import router as generate_ad_router
from Backend.endpoints.video_status import router as video_status_router
from Backend.endpoints.save_ad import router as save_ad_router

# ==========================================
# Local Server Setup (Fallback if Docker is missing)
# ==========================================
app = FastAPI()
app.include_router(login_router)
app.include_router(register_router)
app.include_router(generate_ad_router)
app.include_router(video_status_router)
app.include_router(save_ad_router)

def start_local_fastapi():
    # Runs a local server if Docker is not detected
    print("Docker not detected. Starting local server...")
    # Passed the app object directly instead of a string string for safety here
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

def check_if_server_is_running():
    # Checks if port 8000 is already in use (by Docker or another instance)
    try:
        # Sends a quick ping request to the server root
        response = requests.get("http://127.0.0.1:8000/", timeout=1)
        return True
    except requests.ConnectionError:
        return False
    except Exception:
        return False

# ==========================================

# Main Application (GUI)
# ==========================================
class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.welcome_screen = WelcomeScreen(self)
        self.login_screen = LoginScreen(self)
        self.register_screen = RegisterScreen(self) 
        self.user_home_screen = UserHomeScreen(self, username="") 
        self.generate_screen = GenerateScreen(self, username="")
        self.ad_history_screen = AdHistoryScreen(self, username="")

        self.addWidget(self.user_home_screen)
        self.addWidget(self.generate_screen)
        self.addWidget(self.welcome_screen)
        self.addWidget(self.login_screen)
        self.addWidget(self.register_screen)
        self.addWidget(self.ad_history_screen)
    
        self.setCurrentWidget(self.welcome_screen)

if __name__ == "__main__":
    app_qt = QApplication(sys.argv)

    # If the server is not running (Docker is down), start a local server in a separate thread
    if not check_if_server_is_running():
        fastapi_thread = threading.Thread(target=start_local_fastapi, daemon=True)
        fastapi_thread.start()
        # Wait a second for the local server to initialize before showing the window
        time.sleep(1) 
    else:
        print("Docker/Server detected! Connecting to existing server.")

    # Load QSS
    qss_path = os.path.join(os.path.dirname(__file__), "styles", "style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r") as file:
            app_qt.setStyleSheet(file.read())

    window = MainApp()
    window.setGeometry(400, 400, 800, 400)
    window.setWindowTitle("InstaAD")
    window.show()

    sys.exit(app_qt.exec_())