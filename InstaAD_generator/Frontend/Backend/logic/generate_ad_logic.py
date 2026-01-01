import requests
import re
import os

GOOGLE_AI_API_KEY = os.getenv("AIzaSyAMevFDxpW1sQ1DBFTxaeDglAAJ_-dbmb4")

def generate_video_with_google_ai(prompt: str):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    headers = {
        "Content-Type": "application/json"
    }

    params = {
        "key": GOOGLE_AI_API_KEY
    }

    body = {
        "contents": [{
            "parts": [{
                "text": f"Generate a short advertisement video idea for: {prompt}"
            }]
        }]
    }

    response = requests.post(url, headers=headers, params=params, json=body)
    response.raise_for_status()
    data = response.json()

    text = data["candidates"][0]["content"]["parts"][0]["text"]

    return {
        "title": "AI Generated Ad Concept",
        "description": text,
        "video_url": None  # Veo → async / future
    }

def extract_keywords(prompt: str):
    # Lowercase
    text = prompt.lower()

    # Remove punctuation
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Split into words
    words = text.split()

    # English stop words
    stop_words = {
        "the", "and", "is", "in", "on", "at", "to", "for", "a", "an", "of", "make", "ad",
        "create", "generate", "with", "image", "video", "text", "advertisement", "advert", "promotion",
        "this", "that", "these", "those", "it", "its", "by", "as", "want", "from", "or", "be", "are",
        "was", "were", "has", "have", "had", "about", "not", "but", "if", "then", "so", "we", "you", "he", "she", "they",
        "i", "my", "me", "your", "yourself", "himself", "herself", "ourselves", "themselves", "all", "any", "both", "each",
        "few", "more", "most", "other", "some", "such", "no", "nor", "only", "own", "same", "too", "very", "s", "t", "can", "will", "just",
        "with", "this", "that", "these", "those", "it", "its", "by", "as", "want",
        "from", "or", "be", "are", "was", "were", "has", "have", "had", "about", 
        "not", "but", "if", "then", "so", "we", "you", "he", "she", "they", "i", "my", "me", "your"
    }

    keywords = [w for w in words if w not in stop_words]

    # Remove duplicates while keeping order
    seen = set()
    unique = []
    for w in keywords:
        if w not in seen:
            unique.append(w)
            seen.add(w)

    return unique


def handle_generate(prompt, user_id):
    if len(prompt) < 5:
        return {"success": False, "message": "Prompt is too short."}

    keywords = extract_keywords(prompt)

    requests.post(
        "http://127.0.0.1:8000/save_keywords",
        json={"user_id": user_id, "keywords": keywords}
    )

    ai_video = generate_video_with_google_ai(prompt)

    return {
        "success": True,
        "message": "AI video concept generated",
        "data": {
            "keywords": keywords,
            "video": ai_video
        }
    }