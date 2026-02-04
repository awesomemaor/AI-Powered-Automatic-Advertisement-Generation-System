import requests
import replicate
import threading
import uuid
import time
import re
import os
from Backend.logic.gemini_helper import enhance_prompt_with_gemini

USE_MOCK = True  # for debug purposes to not wast KIE tokens
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
# Submit feedback
# ====================== 
def handle_submit_feedback(user_id: str, feedback: str):
    if not feedback or len(feedback) < 3:
        return {
            "success": False,
            "message": "Feedback is too short"
        }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/save_feedback",
            json={
                "user_id": user_id,
                "feedback": feedback
            },
            timeout=5
        )

        if response.status_code != 200:
            return {
                "success": False,
                "message": response.json().get("detail", "Failed to save feedback")
            }

        return {
            "success": True,
            "message": "Feedback saved successfully"
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
    
# ======================
# Fetch user ad preferences
# ======================
def fetch_user_ad_prefernces(user_id: str):
    response = requests.get(
        f"http://127.0.0.1:8000/get_user_preferences/{user_id}",
        timeout=5
    )

    if response.status_code != 200:
        return {}, []

    data = response.json()
    return (
        data.get("searched_keywords", []),
        data.get("feedback_notes", [])
    )

# ======================
# Create Seedance Task (KIE)
# ======================
def create_seedance_video_task(prompt: str):
    # smock section for debug purposes
    if USE_MOCK:
        mock_task_id = f"mock-{uuid.uuid4().hex[:8]}"
        print("MOCK MODE: returning fake task_id:", mock_task_id)
        return mock_task_id
    
    # real section for KIE API
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
def handle_generate(prompt: str | None, user_id: str, mode="manual"):

    searched_keywords, feedback_notes = fetch_user_ad_prefernces(user_id)

    keywords = []

    # -------------------------
    # 1. base prompt
    # -------------------------
    if mode == "manual":
        if not prompt or len(prompt) < 5:
            return {"success": False, "message": "Prompt is too short"}
        base_prompt = prompt

    else:  # recommended
        base_prompt = (
            "Create a short, engaging, professional video advertisement "
            "suitable for social media platforms."
        )

    # -------------------------
    # 2. enrich with user data
    # -------------------------
    if mode == "recommended":
        if searched_keywords:
            base_prompt += (
                "\nFocus on themes and concepts related to: "
                + ", ".join(searched_keywords[-5:])
            )

        if feedback_notes:
            base_prompt += (
                "\nUser preferences and feedback to consider: "
                + " ".join(feedback_notes[-3:])
            )

    elif mode == "manual":
        if feedback_notes:
            base_prompt += (
                "\nUser preferences and feedback to consider: "
                + " ".join(feedback_notes[-3:])
            )

    # -------------------------
    # 3. Gemini enhancement
    # -------------------------
    print("Enhancing prompt with Gemini...")
    final_prompt = enhance_prompt_with_gemini(base_prompt) # enhance with Gemini AI (hashuv!!)
    print("Final prompt:", final_prompt)
    
    # -------------------------
    # 4. keywords + task
    # -------------------------
    if mode == "manual":
        keywords = extract_keywords(final_prompt)
        requests.post(
            "http://127.0.0.1:8000/save_keywords",
            json={"user_id": user_id, "keywords": keywords},
            timeout=5
        )

    task_id = create_seedance_video_task(final_prompt)

    # returns to generate_screen then sends the taskid to Ad_preview_screen and from there to the 
    # הסבר בשבילנו)המשך )- video_status backend get the response of the video url and show it
    return {
        "success": True,
        "message": "Video generation started",
        "data": {
            "task_id": task_id,
            "keywords": keywords,
            "provider": "bytedance/seedance-1.5-pro (KIE)"
        }
    }
