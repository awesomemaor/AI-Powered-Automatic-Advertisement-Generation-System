import requests
import uuid
import time
import re
import os

USE_MOCK = True
KIE_API_KEY = os.getenv("KIE_API_KEY")  # אל תשים מפתח בקוד!
KIE_CREATE_TASK_URL = "https://api.kie.ai/api/v1/jobs/createTask"
print("KIE_API_KEY =", os.getenv("KIE_API_KEY"))

# ======================
# Keywords
# ======================
def extract_keywords(prompt: str):
    text = prompt.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    words = text.split()

    stop_words = {
        "the", "and", "is", "in", "on", "at", "to", "for", "a", "an", "of",
        "create", "generate", "video", "advertisement", "ad", "promotion",
        "with", "this", "that", "it", "by", "as", "from", "or", "be"
    }

    seen = set()
    unique = []
    for w in words:
        if w not in stop_words and w not in seen:
            unique.append(w)
            seen.add(w)

    return unique


# ======================
# Seedance – create task
# ======================
def create_seedance_video_task(prompt: str):
    if USE_MOCK:
        print("MOCK MODE: creating fake task")
        return f"mock-task-{uuid.uuid4()}"
    
    url = "https://api.kie.ai/api/v1/jobs/createTask"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {KIE_API_KEY}"
    }

    body = {
        "model": "bytedance/seedance-1.5-pro",
        "input": {
            "prompt": prompt,
            "aspect_ratio": "1:1",
            "resolution": "480p",
            "duration": "4"
        }
    }

    response = requests.post(url, headers=headers, json=body, timeout=20)

    try:
        data = response.json()
    except ValueError:
        raise RuntimeError(f"Seedance API did not return JSON: {response.text}")

    if response.status_code != 200:
        raise RuntimeError(f"Seedance API error {response.status_code}: {data}")

    # בדיקה אם data["data"] קיים
    if not data.get("data") or not data["data"].get("taskId"):
        raise RuntimeError(f"taskId missing in API response: {data}")

    task_id = data["data"]["taskId"]
    print(f"Created task with ID: {task_id}")  # הדפסה ללוג
    return task_id


# ======================
# Main entry
# ======================
def handle_generate(prompt: str, user_id: str):
    if len(prompt) < 5:
        return {
            "success": False,
            "message": "Prompt is too short"
        }

    # 1. keywords
    keywords = extract_keywords(prompt)

    # 2. save keywords
    requests.post(
        "http://127.0.0.1:8000/save_keywords",
        json={"user_id": user_id, "keywords": keywords},
        timeout=5
    )

    # 3. create video task
    task_id = create_seedance_video_task(prompt)

    # 4. return to frontend
    return {
        "success": True,
        "message": "Video generation started",
        "data": {
            "task_id": task_id,
            "keywords": keywords,
            "provider": "seedance-1.5-pro"
        }
    }
