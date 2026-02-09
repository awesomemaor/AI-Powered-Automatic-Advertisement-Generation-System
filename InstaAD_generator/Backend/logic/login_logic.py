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
        data = response.json()

        return {"success": data["success"], "message": data["message"]}
    except requests.HTTPError as e:
        try:
            error_message = e.response.json().get("detail", "Unknown error")
            print(f"Login failed: {error_message}")
            return {"success": False, "message": error_message}
        except Exception as ex:
            print("Unexpected error:", ex)
            return {"success": False, "message": "Server error"}

def logout_user_request(username):
    print(f"Sending logout request for: {username}")
    try:
        response = requests.post(
            "http://127.0.0.1:8000/logout",
            json={"username": username}
        )
        print(f"Received response: {response.status_code} - {response.text}")

        response.raise_for_status()
        data = response.json()
        
        return {"success": data["success"], "message": data["message"]}

    except requests.HTTPError as e:
        try:
            error_message = e.response.json().get("detail", "Unknown error")
            print(f"Logout failed: {error_message}")
            return {"success": False, "message": error_message}
        except Exception as ex:
            print("Unexpected error:", ex)
            return {"success": False, "message": "Server error"}

    except Exception as ex:
        print("Unexpected error:", ex)
        return {"success": False, "message": "Could not connect to server"}