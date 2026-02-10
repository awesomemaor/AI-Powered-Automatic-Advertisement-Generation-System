from Backend.logic.register_logic import validate_inputs

def test_validate_inputs_missing_username():
    res = validate_inputs("", "1234", "2000-01-01", "Self-employed", "Food")
    assert res["success"] is False
    assert res["message"] == "Please fill all fields."

def test_validate_inputs_short_password():
    res = validate_inputs("user", "123", "2000-01-01", "Self-employed", "Food")
    assert res["success"] is False
    assert res["message"] == "Password must be at least 4 characters."

def test_validate_inputs_short_business_field():
    res = validate_inputs("user", "1234", "2000-01-01", "Self-employed", "F")
    assert res["success"] is False
    assert res["message"] == "Business field too short."

def test_validate_inputs_success():
    res = validate_inputs("user", "1234", "2000-01-01", "Self-employed", "Food")
    assert res["success"] is True

def test_validate_inputs_business_field_min_length():
    res = validate_inputs("user", "1234", "2000-01-01", "Self-employed", "IT")
    assert res["success"] is True

def test_validate_inputs_password_min_length():
    res = validate_inputs("user", "1234", "2000-01-01", "Self-employed", "Food")
    assert res["success"] is True
