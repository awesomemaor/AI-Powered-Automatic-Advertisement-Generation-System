import requests
import replicate
import threading
import uuid
import time
import re
import os
from Backend.logic.gemini_helper import enhance_prompt_with_gemini

USE_MOCK = True  # for debug purposes
KIE_API_KEY = os.getenv("KIE_API_KEY")  
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
# Create Seedance Task (KIE)
# ======================
def create_seedance_video_task(prompt: str):
    if USE_MOCK:
        mock_task_id = f"mock-{uuid.uuid4().hex[:8]}"
        print("MOCK MODE: returning fake task_id:", mock_task_id)
        return mock_task_id
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {KIE_API_KEY}"
    }

    body = {
        "model": "bytedance/seedance-1.5-pro",
        "input": {
            "prompt": prompt,
            "aspect_ratio": "16:9",
            "resolution": "480p",
            "duration": "4"
        }
    }

    response = requests.post(
        KIE_CREATE_TASK_URL,
        headers=headers,
        json=body,
        timeout=20
    )

    data = response.json()

    if response.status_code != 200 or not data.get("data", {}).get("taskId"):
        raise RuntimeError(f"KIE createTask failed: {data}")

    task_id = data["data"]["taskId"]
    print("Created KIE task:", task_id)
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
    
    print("Asking Gemini to enhance the prompt...")
    final_prompt = enhance_prompt_with_gemini(prompt) # enhancing the user prompt (hashuv!!)
    print("Final Prompt:", final_prompt)

    # 1. keywords
    keywords = extract_keywords(final_prompt)

    # 2. save keywords
    requests.post(
        "http://127.0.0.1:8000/save_keywords",
        json={"user_id": user_id, "keywords": keywords},
        timeout=5
    )

    # 3. create video task
    task_id = create_seedance_video_task(final_prompt)

    # 4. return to frontend
    return {
        "success": True,
        "message": "Video generation started",
        "data": {
            "task_id": task_id,
            "keywords": keywords,
            "provider": "bytedance/seedance-1.5-pro (KIE)"
        }
    }
