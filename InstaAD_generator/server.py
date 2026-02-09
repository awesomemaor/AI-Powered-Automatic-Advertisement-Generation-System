import uvicorn
import os
from fastapi import FastAPI

# Inside Docker, we are already in the correct path thanks to the PYTHONPATH we defined.
# There is no need to write 'InstaAD_generator' nor 'Frontend'.
# We can simply access 'Backend' directly:
from Backend.endpoints import generate_ad, save_ad, auth_login, auth_register, video_status

# Create the application
app = FastAPI(title="InstaAD Backend")

# Include routers
app.include_router(generate_ad.router)
app.include_router(save_ad.router)
app.include_router(auth_login.router)
app.include_router(auth_register.router)
app.include_router(video_status.router)

@app.get("/")
def root():
    return {"message": "InstaAD Docker Server is Running!"}

if __name__ == "__main__":
    # The server will run on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)