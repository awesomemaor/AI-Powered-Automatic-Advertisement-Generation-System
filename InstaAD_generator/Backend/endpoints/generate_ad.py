from fastapi import APIRouter, HTTPException
from Backend.endpoints.db_init import customers_collection
from pydantic import BaseModel
from pymongo import UpdateOne
from bson import ObjectId

router = APIRouter()

class KeywordRequest(BaseModel):
    user_id: str
    keywords: list[str]

class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str

# Endpoint to save user searched keywords limited to last 50 entries
@router.post("/save_keywords")
async def save_keywords(req: KeywordRequest):
    user_id = req.user_id
    keywords = req.keywords

    # Use bulk_write to remove duplicates and push new entries atomically
    operations = [
        # 1. Pull: Remove keywords if they already exist (prevents duplicates)
        UpdateOne(
            {"username": user_id},
            {"$pull": {"searched_keywords": {"$in": keywords}}}
        ),
        # 2. Push: Add keywords to the end, keeping only the last 50
        UpdateOne(
            {"username": user_id},
            {
                "$push": {
                    "searched_keywords": {
                        "$each": keywords,
                        "$slice": -50
                    }
                }
            }
        )
    ]

    result = customers_collection.bulk_write(operations)

    # Check if user exists (sum of matches from both operations)
    if result.matched_count == 0:
        raise HTTPException(status_code=400, detail="User not found")

    # Check if any change occurred
    if result.modified_count == 0:
        return {"message": "Keywords already exist", "keywords_added": []}

    return {"message": "Keywords saved", "keywords_added": keywords}


@router.post("/save_feedback")
async def save_feedback(req: FeedbackRequest):
    operations = [
        # 1. Pull: Remove feedback if it already exists
        UpdateOne(
            {"username": req.user_id},
            {"$pull": {"feedback_notes": req.feedback}}
        ),
        # 2. Push: Add feedback to the end, keeping only the last 25
        UpdateOne(
            {"username": req.user_id},
            {
                "$push": {
                    "feedback_notes": {
                        "$each": [req.feedback],
                        "$slice": -25
                    }
                }
            }
        )
    ]

    result = customers_collection.bulk_write(operations)

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Feedback saved"}

# Endpoint to retrieve user preferences (keywords and feedback)
@router.get("/get_user_preferences/{user_id}")
async def get_user_preferences(user_id: str):
    user = customers_collection.find_one(
        {"username": user_id},
        {"_id": 0, "searched_keywords": 1, "feedback_notes": 1}
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "searched_keywords": user.get("searched_keywords", []),
        "feedback_notes": user.get("feedback_notes", [])
    }
