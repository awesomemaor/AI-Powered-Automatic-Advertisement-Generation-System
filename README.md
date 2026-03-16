# 🎬 InstaAD - AI-Powered Automatic Advertisement Generation

## 📖 Overview
Creating high-quality video ads is typically a time-consuming process that requires marketing, design, and creative expertise. Businesses often struggle to produce content quickly, consistently, and cost-effectively. 

**InstaAD** solves this by using advanced AI to **automatically generate personalized video advertisements**. Our platform streamlines the entire marketing workflow, significantly reduces manual effort, and allows users to quickly produce stunning, tailored video content for different target audiences in a matter of seconds.

## ✨ Features
- 👤 **User Management:** Secure registration and personal account dashboard.
- 🎥 **Text-to-Video Generation:** Create full video ads simply from text prompts.
- 🤖 **Smart AI Recommendations:** Automatic video creation based on user preferences and past interactions.
- 💾 **Ad History & Library:** Save, manage, and playback previously generated advertisements.
- 📝 **Feedback Loop:** User feedback collection to continuously improve ad quality.
- ⚙️ **Customization:** Tailored ad recommendations and keyword tracking for targeted campaigns.

## 🏗 Architecture & Workflow
We built InstaAD on a modern, decoupled Client-Server architecture, utilizing containerization and continuous integration for deployment.<br>
<img width="600" alt="InstaAD Architecture" src="https://github.com/user-attachments/assets/9c2032ab-b133-4307-9ac8-f7a361ab3373" />


* **Frontend (Client):** A standalone desktop application built with PyQt5, providing a rich, responsive user interface.
* **Backend (Server):** A FastAPI service running inside a Docker container, handling API requests, user authentication, and AI model orchestration.
* **Database:** MongoDB handles all persistent data (users, ad history), connected via a dedicated Docker volume.
* **CI/CD Pipeline:** GitHub Actions automatically tests and builds the backend code upon every push, publishing the latest Docker Image directly to our Docker Hub's personal repo.

## 🛠 Tech Stack
* **Frontend GUI:** Python, PyQt5, QSS (Styling)
* **Backend API:** Python, FastAPI, Uvicorn
* **Database:** MongoDB, PyMongo
* **AI / ML Models:** Google Gemini 2.5 Flash Lite (Text Generation LLM), KIE.ai + Seedance 1.5 Pro (Text-to-Video Generation)
* **Security:** Argon2 (Password hashing), JWT (Authentication)
* **DevOps & Deployment:** Docker, Docker Compose, GitHub Actions (CI/CD), Docker Hub

---

## 🚀 Installation & Setup Guide

Welcome to our InstaAD project! This document provides step-by-step instructions on how to initialize, configure, and run the application on your local machine.

### Step 1: Obtain the Source Code
First, pull the latest version of the project repository to your local machine. Open your terminal and run:

```bash
git clone [https://github.com/awesomemaor/AI-Powered-Automatic-Advertisement-Generation-System.git](https://github.com/awesomemaor/AI-Powered-Automatic-Advertisement-Generation-System.git)
cd InstaAD_generator
```

### Step 2: Configure the .env File (Mandatory)
The InstaAD system relies on strictly separated environment variables to securely manage external API keys (Google Gemini, KIE.ai) and the MongoDB connection URI.

> ⚠️ **IMPORTANT INSTRUCTION:** Inside the ZIP archive we provided/sent to you privately, there is a file named `.env`. You must extract this `.env` file and place it directly into the root directory of the cloned project (`InstaAD_generator/`). The system will not operate in terms of connections to API's and the database without this file in the correct location.

### Step 3: Choose Your Execution Method
You can run the system using either a completely Local Server setup or via Docker (Recommended). Please choose one of the following methods:

#### Option A: Local Server Execution (Without Docker)
This method runs the entire application—both backend and frontend—directly on your local Python environment.

1. Open your terminal and ensure you are in the project's root directory.
2. Install the dedicated project dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application (You can also run this directly from your IDE through main.py file):

```bash
python Frontend/main.py
```

*(Note: The system will detect that Docker is not running and will automatically spin up a local FastAPI server in the background before launching the GUI).*

#### Option B: Docker Execution (Recommended & Modern Approach)
This method isolates the backend services and the database using containerization. Thanks to our CI/CD pipeline, you do not need to build the backend locally. The latest stable version is always pulled directly from our docker hub repo in the cloud.

1. **Prerequisite:** Ensure **Docker Desktop** is open and running on your machine.
2. Open your terminal in the project's root directory and pull the latest images from our Docker Hub registry:

```bash
docker compose pull
```

3. Start the backend server and database in "detached" mode (this frees up your terminal):

```bash
docker compose up -d
```

4. Once the Docker containers are successfully running in the background, launch the PyQt5 Desktop application (Frontend) from your terminal:

```bash
python Frontend/main.py
```

---

## 👥 Core Development Team
* **Daniel Ayash** – System Architecture, Backend & Frontend Logic, DevOps
* **Maor Siboni** – UI/UX Design, Frontend Implementation & Styling

> ✅ *Stable Release — InstaAD is fully operational and ready to generate your next campaign.*
