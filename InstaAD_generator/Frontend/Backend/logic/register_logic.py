class RegisterLogic:
    def __init__(self, db=None):
        self.db = db

    def validate_inputs(self, username, password, birthdate, business_type, business_field):
        # בדיקה ששום שדה לא ריק
        if not username or not password or not business_field:
            return False, "Please fill all fields."

        # בדיקה בסיסית על אורך סיסמה
        if len(password) < 4:
            return False, "Password must be at least 4 characters."

        # בדיקה על תחום העסק
        if len(business_field) < 2:
            return False, "Business field too short."

        return True, "Valid"

    def register_user(self, username, password, birthdate, business_type, business_field):
        """
        פונקציה מרכזית של ההרשמה.
        כרגע מחזירה הצלחה בלבד,
        מאוחר יותר נוסיף שמירה למאגר.
        """

        valid, msg = self.validate_inputs(username, password, birthdate, business_type, business_field)
        if not valid:
            return False, msg

        # כאן בעתיד: שמירה אמיתית למאגר
        print("Saving user:")
        print({
            "username": username,
            "password": password,
            "birthdate": birthdate,
            "business_type": business_type,
            "business_field": business_field
        })

        return True, "Registration successful!"