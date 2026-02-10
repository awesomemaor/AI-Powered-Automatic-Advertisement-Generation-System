def test_check_video_status_mock_flow(client):
    # משתמשים ב-task_id שמתחיל ב-"mock-" כדי להפעיל את ה-MOCK
    task_id = "mock-12345678"

    response = client.post(
        "/check-video-status",
        json={"task_id": task_id}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "SUCCESS"
    assert "video_url" in data
    assert data["video_url"].endswith(".mp4")

def test_check_video_status_real_failed(monkeypatch, client):
    # מדמה תשובה של KIE עם state=failed
    class FakeResponse:
        status_code = 200

        def json(self):
            return {
                "data": {
                    "state": "failed"
                }
            }

        def raise_for_status(self):
            pass

    # מחליפים את requests.get האמיתי
    monkeypatch.setattr(
        "Backend.endpoints.video_status.requests.get",
        lambda *args, **kwargs: FakeResponse()
    )

    response = client.post(
        "/check-video-status",
        json={"task_id": "real-task-id-123"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "FAILED"

def test_check_video_status_real_success(monkeypatch, client):
    # מכבים MOCK
    monkeypatch.setattr(
        "Backend.endpoints.video_status.USE_MOCK",
        False
    )

    # מדמים תשובת KIE אמיתית
    class FakeGetResponse:
        status_code = 200

        def json(self):
            return {
                "data": {
                    "state": "success",
                    "resultJson": '{"resultUrls": ["https://video.real.mp4"]}'
                }
            }

        def raise_for_status(self):
            pass

    monkeypatch.setattr(
        "Backend.endpoints.video_status.requests.get",
        lambda *args, **kwargs: FakeGetResponse()
    )

    response = client.post(
        "/check-video-status",
        json={"task_id": "real-task-999"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "SUCCESS"
    assert data["video_url"] == "https://video.real.mp4"
