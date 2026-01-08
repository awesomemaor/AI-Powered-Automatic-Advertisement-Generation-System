import os
import requests
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

    try:
        response = requests.get(
            KIE_STATUS_URL,
            headers=headers,
            params=params,
            timeout=15
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail=f"Task with ID {req.task_id} not found"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"KIE API returned HTTP error: {str(e)}"
            )
    except requests.exceptions.RequestException as e:
        # כל שגיאה אחרת ברשת
        raise HTTPException(
            status_code=500,
            detail=f"Error connecting to KIE API: {str(e)}"
        )

    data = response.json()

    # ✅ הדפסות לוגים
    print("Checking status for task_id:", req.task_id)
    print("Response from KIE API:", data)
    
    # ⚠️ משתנה לפי API – זה מבוסס על KIE docs
    status = data.get("data", {}).get("status")

    if status == "SUCCESS":
        video_url = data.get("data", {}).get("output", {}).get("video_url")
        return {
            "status": "SUCCESS",
            "video_url": video_url
        }

    if status == "FAILED":
        return {"status": "FAILED"}

    return {"status": "PROCESSING"}
