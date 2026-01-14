import requests

# ===============================
# save ad
# ===============================
def handle_save_ad(
    username: str,
    task_id: str,
    video_url: str,
) -> dict:
    """
    Sends ad data to backend and returns result dict:
    { success: bool, message: str }
    """

    payload = {
        "username": username,
        "task_id": task_id,
        "video_url": video_url,
    }

    try:
        response = requests.post(
            f"{"http://127.0.0.1:8000"}/save-ad",
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            return {
                "success": True,
                "message": "Ad saved successfully"
            }

        return {
            "success": False,
            "message": f"Save failed ({response.status_code})"
        }

    except requests.RequestException as e:
        return {
            "success": False,
            "message": str(e)
        }

# ===============================
# GET saved ads
# ===============================
def handle_get_ad(username: str) -> list:
    try:
        response = requests.get(
            f"{"http://127.0.0.1:8000"}/get-ads/{username}",
            timeout=10
        )

        if response.status_code == 200:
            return response.json().get("ads", [])

        return []

    except requests.RequestException:
        return []
    
# ===============================
# DELETE ad
# ===============================
def handle_delete_ad(ad_id: str) -> bool:
    try:
        response = requests.delete(
            f"{"http://127.0.0.1:8000"}/delete-ad/{ad_id}",
            timeout=10
        )

        return response.status_code == 200

    except requests.RequestException:
        return False
