import requests

def login_user(username, password):
    try:
        print(f"Sending login request with: {username} / {password}")
        response = requests.post(
            "http://127.0.0.1:8000/login",
            json={"username": username, "password": password}
        )
        print(f"Received response: {response.status_code} - {response.text}")
        response.raise_for_status()
        return {"success": True, "message": response.json()["message"]}
    except requests.HTTPError as e:
        try:
            error_message = e.response.json().get("detail", "Unknown error")
            print(f"Login failed: {error_message}")
            return {"success": False, "message": error_message}
        except Exception as ex:
            print("Unexpected error:", ex)
            return {"success": False, "message": "Server error"}
