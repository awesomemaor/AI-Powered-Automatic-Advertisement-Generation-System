import requests

def validate_inputs(username, password, birthdate, business_type, business_field):
    # בדיקה ששום שדה לא ריק
    if not username or not password or not business_field:
        return {"success": False, "message": "Please fill all fields."}

    # בדיקה בסיסית על אורך סיסמה
    if len(password) < 4:
        return {"success": False, "message": "Password must be at least 4 characters."}

    # בדיקה על תחום העסק
    if len(business_field) < 2:
        return {"success": False, "message": "Business field too short."}

    return {"success": True, "message": "Valid"}


def register_user(username, password, birthdate, business_type, business_field):
    validation = validate_inputs(username, password, birthdate, business_type, business_field)
    if not validation["success"]:
        return {"success": False, "message": validation["message"]}

    try:
        print("Sending register request...")
        response = requests.post(
            "http://127.0.0.1:8000/register",
            json={
                "username": username,
                "password": password,
                "birthdate": birthdate,
                "business_type": business_type,
                "business_field": business_field,
                "connected": False,
                "searched_keywords": []
            }
        )

        print(f"Received response: {response.status_code} - {response.text}")

        response.raise_for_status()

        data = response.json()

        return {"success": True, "message": data.get("message", "Registration successful!")}

    except requests.HTTPError as e:
        try:
            error_message = e.response.json().get("detail", "Unknown error")
            print(f"Registration failed: {error_message}")
            return {"success": False, "message": error_message}
        except:
            return {"success": False, "message": "Server error"}

    except Exception as ex:
        print("Unexpected error:", ex)
        return {"success": False, "message": "Could not connect to server"}
