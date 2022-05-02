from . import app


def test_metadata_works():
    response = app.test_client().get(
        "/metadata/1",
    )
    print(response.json)
    assert response.status_code == 200
    assert "image" in response.json
    assert "description" in response.json
    assert "token_id" in response.json
    assert response.json["token_id"] == "1"


def test_metadata_doesnt_work_for_not_minted():
    response = app.test_client().get(
        "/metadata/7000",
    )
    assert response.status_code == 404
