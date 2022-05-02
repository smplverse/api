from src.app import app


def test_hello():
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert response.text is not None
