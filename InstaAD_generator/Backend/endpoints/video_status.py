import os
import time
import requests
import replicate
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

USE_MOCK = True  # for debug purposes
KIE_API_KEY = os.getenv("KIE_API_KEY")
KIE_STATUS_URL = "https://api.kie.ai/api/v1/jobs/recordInfo"

class StatusRequest(BaseModel):
    task_id: str

@router.post("/check-video-status")
def check_video_status(req: StatusRequest):
    # ---------- MOCK ----------
    if USE_MOCK and req.task_id.startswith("mock-"):
        print("MOCK MODE: returning local video")

        return {
            "status": "SUCCESS",
            "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"
        }

    # ---------- REAL KIE ----------
    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}"
    }

    params = {
        "taskId": req.task_id
    }

    response = requests.get(
        "https://api.kie.ai/api/v1/jobs/recordInfo",
        headers=headers,
        params=params,
        timeout=15
    )
    response.raise_for_status()

    data = response.json()
    print("KIE recordInfo response:", data)

    state = data.get("data", {}).get("state")

    if state == "success":
        import json
        result_json = json.loads(data["data"]["resultJson"])
        video_url = result_json["resultUrls"][0]

        return {
            "status": "SUCCESS",
            "video_url": video_url
        }

    if state == "failed":
        return {"status": "FAILED"}

    return {"status": "PROCESSING"}