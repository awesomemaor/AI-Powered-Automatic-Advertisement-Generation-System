import os
import time
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

KIE_API_KEY = os.getenv("KIE_API_KEY")
KIE_STATUS_URL = "https://api.kie.ai/api/v1/jobs/queryTask"

# ======================
# MOCK storage
# ======================
MOCK_TASKS = {}

class StatusRequest(BaseModel):
    task_id: str


@router.post("/check-video-status")
def check_video_status(req: StatusRequest):

    # ==================================================
    # MOCK MODE – אם זה task מזויף
    # ==================================================
    if req.task_id.startswith("mock-task"):
        now = time.time()
        created = MOCK_TASKS.setdefault(req.task_id, now)

        # מדמים עיבוד של כמה שניות
        if time.time() - created < 6:
            return {"status": "PROCESSING"}

        return {
            "status": "SUCCESS",
            "video_url": "https://filesamples.com/samples/video/mp4/sample_640x360.mp4"
        }

    # ==================================================
    # KIE אמיתי – רק אם זה לא mock
    # ==================================================
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
        raise HTTPException(
            status_code=500,
            detail=f"Error connecting to KIE API: {str(e)}"
        )

    data = response.json()

    # לוגים
    print("Checking status for task_id:", req.task_id)
    print("Response from KIE API:", data)

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
