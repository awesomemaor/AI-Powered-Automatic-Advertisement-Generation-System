import pytest
from fastapi import HTTPException
from Backend.endpoints.generate_ad import save_keywords, KeywordRequest

@pytest.mark.asyncio
async def test_save_keywords_new_user(mock_db):
    mock_db.update_one.return_value.modified_count = 1

    req = KeywordRequest(user_id="daniel", keywords=["tech", "ai"])
    result = await save_keywords(req)

    mock_db.update_one.assert_called_once_with(
        {"username": "daniel"},
        {"$addToSet": {"searched_keywords": {"$each": ["tech", "ai"]}}}
    )

    assert result["message"] == "Keywords saved"
    assert result["keywords_added"] == ["tech", "ai"]

@pytest.mark.asyncio
async def test_save_keywords_user_not_found(mock_db):
    """
    בודק מקרה שבו המשתמש בכלל לא קיים במסד הנתונים.
    הציפייה: הקוד יזרוק שגיאה 400 עם ההודעה User not found.
    """
    # 1. הכנת ה-Mock
    mock_db.matched_count = 0   # <--- זה התיקון הקריטי! (0 אומר לא נמצא)
    
    mock_db.update_one.return_value = mock_db

    # 2. הכנת הבקשה
    req = KeywordRequest(user_id="unknown", keywords=["tech", "ai"])
    
    # 3. בדיקה שהשגיאה נזרקת
    with pytest.raises(HTTPException) as e_info:
        await save_keywords(req)

    # 4. וידוא פרטי השגיאה
    mock_db.update_one.assert_called_once()
    assert e_info.value.status_code == 400
    assert e_info.value.detail == "User not found"

@pytest.mark.asyncio
async def test_save_keywords_duplicate(mock_db):
    """
    בודק מקרה שבו המשתמש קיים, אבל המילים כבר נמצאות ברשימה.
    הציפייה: הקוד לא יזרוק שגיאה, אלא יחזיר הודעה שהמילים כבר קיימות.
    """
    # 1. הכנת ה-Mock
    mock_db.matched_count = 1   # המשתמש נמצא
    mock_db.modified_count = 0  # אבל שום דבר לא השתנה (כי המילים כפולות)
    
    mock_db.update_one.return_value = mock_db

    # 2. הכנת הבקשה
    req = KeywordRequest(user_id="daniel", keywords=["tech"])
    
    # 3. הרצת הפונקציה
    result = await save_keywords(req)

    # 4. בדיקה (עכשיו זה תואם לקוד האמיתי שמחזיר הודעה ולא שגיאה)
    assert result["message"] == "Keywords already exist"
    assert result["keywords_added"] == []

