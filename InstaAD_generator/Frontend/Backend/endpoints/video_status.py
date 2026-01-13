import os
import time
import requests
import replicate
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

KIE_API_KEY = os.getenv("KIE_API_KEY")
KIE_STATUS_URL = "https://api.kie.ai/api/v1/jobs/queryTask"

class StatusRequest(BaseModel):
    task_id: str

@router.post("/check-video-status")
def check_video_status(req: StatusRequest):
    headers = {
        "Authorization": f"Bearer {KIE_API_KEY}"
    }

    params = {
        "taskId": req.task_id
    }

    response = requests.get(
        KIE_STATUS_URL,
        headers=headers,
        params=params,
        timeout=15
    )

    data = response.json()
    print("KIE status response:", data)

    status = data.get("data", {}).get("status")

    if status == "SUCCESS":
        return {
            "status": "SUCCESS",
            "video_url": data["data"]["output"]["video_url"]
        }

    if status == "FAILED":
        return {"status": "FAILED"}

    return {"status": "PROCESSING"}