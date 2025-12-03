import requests
#from keybert import KeyBERT
#import spacy

#nlp = spacy.load("en_core_web_sm")
#kw_model = KeyBERT(model=nlp)

import re

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

        return {
            "success": True,
            "message": "Keywords saved!",
            "data": {"keywords": keywords}
        }

    except Exception as e:
        return {
            "success": False,
            "message": f"Server error: {e}"
        }
