import pytest
from fastapi import HTTPException
from Backend.endpoints.generate_ad import save_keywords, KeywordRequest

@pytest.mark.asyncio
async def test_save_keywords_new_user(mock_db):
    # Mocking success
    mock_db.bulk_write.return_value.matched_count = 1
    mock_db.bulk_write.return_value.modified_count = 1

    req = KeywordRequest(user_id="daniel", keywords=["tech", "ai"])
    result = await save_keywords(req)

    mock_db.bulk_write.assert_called_once()

    assert result["message"] == "Keywords saved"
    assert result["keywords_added"] == ["tech", "ai"]

@pytest.mark.asyncio
async def test_save_keywords_user_not_found(mock_db):
    """
    Test scenario where user does not exist in DB.
    Expects 400 Bad Request.
    """
    # 1. Mock setup: matched_count = 0
    mock_db.bulk_write.return_value.matched_count = 0
    
    # 2. Prepare request
    req = KeywordRequest(user_id="unknown", keywords=["tech", "ai"])
    
    # 3. Assert exception
    with pytest.raises(HTTPException) as e_info:
        await save_keywords(req)

    mock_db.bulk_write.assert_called_once()
    assert e_info.value.status_code == 400
    assert e_info.value.detail == "User not found"

@pytest.mark.asyncio
async def test_save_keywords_duplicate(mock_db):
    """
    Test scenario where keywords already exist.
    Expects a message indicating duplication without error.
    """
    # 1. Mock setup: User found (matched=1) but no changes made (modified=0)
    mock_db.bulk_write.return_value.matched_count = 1 
    mock_db.bulk_write.return_value.modified_count = 0 
    
    # 2. Prepare request
    req = KeywordRequest(user_id="daniel", keywords=["tech"])
    
    # 3. Run function
    result = await save_keywords(req)

    # 4. Assert response
    assert result["message"] == "Keywords already exist"
    assert result["keywords_added"] == []