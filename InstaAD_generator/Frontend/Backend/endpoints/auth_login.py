from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from .db_init import customers_collection  # Import your MongoDB collection

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login(req: LoginRequest):
    print(f"Received login request: username={req.username}, password={req.password}")
    
    user = customers_collection.find_one({"username": req.username})
    print(f"MongoDB query result: {user}")
    
    if user:
        if user["password"] == req.password:
            print("Password matched")
            return {"success": True, "message": "Login successful!", "username": req.username}
        else:
            print("Incorrect password")
            raise HTTPException(status_code=401, detail="Incorrect password")
    else:
        print("User not found")
        raise HTTPException(status_code=401, detail="User not found")

