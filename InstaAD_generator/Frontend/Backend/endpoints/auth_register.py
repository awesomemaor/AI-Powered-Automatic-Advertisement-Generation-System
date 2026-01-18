from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from Backend.endpoints.db_init import customers_collection
from utils.security import hash_password
from bson import ObjectId

router = APIRouter()

class RegisterRequest(BaseModel):
    username: str
    password: str
    birthdate: str
    business_type: str
    business_field: str
    connected : bool 
    searched_keywords: list
    feedback_notes: list

@router.post("/register")
def register_user(data: RegisterRequest):

    # Check if user already exists
    if customers_collection.find_one({"username": data.username}):
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    hashed_password = hash_password(data.password) # hashing the password before storing

    new_user = {
        "username": data.username,
        "password": hashed_password, # hashed password storage
        "birthdate": data.birthdate,
        "business_type": data.business_type,
        "business_field": data.business_field,
        "connected": False,
        "searched_keywords": [data.business_field.lower()], # saving user searched keywords
        "feedback_notes": [] # saving user feedback notes
    }

    result = customers_collection.insert_one(new_user)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id)
    }