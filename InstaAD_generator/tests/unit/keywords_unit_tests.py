import pytest
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
    mock_db.update_one.return_value.modified_count = 0

    req = KeywordRequest(user_id="unknown", keywords=["tech", "ai"])
    
    import pytest
    from fastapi import HTTPException

    with pytest.raises(HTTPException) as e_info:
        await save_keywords(req)

    mock_db.update_one.assert_called_once()
    assert e_info.value.detail == "User not found"

@pytest.mark.asyncio
async def test_save_keywords_duplicate(mock_db):
    # נגדיר סט שמכיל כבר את 'tech'
    existing_keywords = {"tech"}

    def fake_update_one(filter, update):
        # נבדוק מה רוצים להוסיף
        keywords_to_add = update["$addToSet"]["searched_keywords"]["$each"]
        added = [kw for kw in keywords_to_add if kw not in existing_keywords]
        existing_keywords.update(added)
        # מחזירים ModifiedCount לפי אם הוספנו משהו חדש
        class Result:
            modified_count = 1 if added else 0
        return Result()

    mock_db.update_one.side_effect = fake_update_one

    req = KeywordRequest(user_id="daniel", keywords=["tech"])
    
    # אם המילה כבר קיימת, modified_count=0 -> צריך לטפל בזה
    from fastapi import HTTPException
    try:
        result = await save_keywords(req)
    except HTTPException as e:
        # ציפינו לזריקה בגלל שאין שינוי
        assert e.status_code == 400
        assert e.detail == "User not found"

