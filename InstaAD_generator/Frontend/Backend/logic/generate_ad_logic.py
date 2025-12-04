import requests
import re

YOUTUBE_API_KEY = "AIzaSyDi6skFKvs4RdvA-A56dubZ6FmMMG800Mw"

def search_youtube_videos(query: str):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "type": "video",
        "maxResults": 5,
        "safeSearch": "strict"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    videos = []
    for item in data.get("items", []):
        videos.append({
            "title": item["snippet"]["title"],
            "videoId": item["id"]["videoId"],
            "thumbnail": item["snippet"]["thumbnails"]["high"]["url"]
        })

    return videos

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
        return {
            "success": False,
            "message": "Prompt is too short."
        }

    # 1. Extract keywords
    keywords = extract_keywords(prompt)
    print("Extracted keywords:", keywords)

    # 2. Send to backend
    try:
        response = requests.post(
            "http://127.0.0.1:8000/save_keywords",
            json={
                "user_id": user_id,
                "keywords": keywords
            }
        )

        response.raise_for_status()

    except Exception as e:
        return {
            "success": False,
            "message": f"Server error: {e}"
        }

    # 3. Search YouTube videos
    search_query = " ".join(keywords) if keywords else prompt
    videos = search_youtube_videos(search_query)

    if not videos:
        return {
            "success": True,
            "message": "Keywords saved, but no videos found.",
            "videos": []
        }

    return {
        "success": True,
        "message": "Keywords saved and videos found!",
        "data": {
            "keywords": keywords,
            "videos": videos
        }
    }