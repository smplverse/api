import cv2

from . import app

face_img = cv2.imread("artifacts/sample_face.png")


def test_bad_requests():
    response = app.test_client().post(
        "/get-smpl",
        json={"not_image": "data:image/jpeg;base64,asdf"},
    )
    assert response.status_code == 400

    response = app.test_client().post(
        "/get-smpl",
        json={
            "image": "data:image/jpeg;base64,asdf",
            "not_address": "not_address",
        },
    )
    assert response.status_code == 400

    response = app.test_client().post(
        "/get-smpl",
        json={
            "image": "data:image/jpeg;base64,asdf",
            "address": "0x123123123..",
            "not_tokenId": "not_tokenId",
        },
    )
    assert response.status_code == 400


def test_valid_address():
    response = app.test_client().post(
        "/get-smpl",
        json={
            "image": "data:image/jpeg;base64,asdf",
            "address": "0x123123123",
            "tokenId": "123",
        },
    )
    assert response.status_code == 400

    response = app.test_client().post(
        "/get-smpl",
        json={
            "image": "data:image/jpeg;base64,asdf",
            "address": "0xF9c4F532074676a1EA27b3b81A0F6c4Ad511AC34",
            "tokenId": "1",
        },
    )
    assert response.status_code == 401


def test_valid_token_id():
    response = app.test_client().post(
        "/get-smpl",
        json={
            "image": "data:image/jpeg;base64,asdf",
            "address": "0xF9c4F532074676a1EA27b3b81A0F6c4Ad511AC34",
            "tokenId": "123.5",
        },
    )
    assert response.status_code == 400

    response = app.test_client().post(
        "/get-smpl",
        json={
            "image": "data:image/jpeg;base64,asdf",
            "address": "0xF9c4F532074676a1EA27b3b81A0F6c4Ad511AC34",
            "tokenId": "123123123",
        },
    )
    assert response.status_code == 400

    response = app.test_client().post(
        "/get-smpl",
        json={
            "image": "data:image/jpeg;base64,asdf",
            "address": "0xF9c4F532074676a1EA27b3b81A0F6c4Ad511AC34",
            "tokenId": "5",
        },
    )
    assert response.status_code == 401


def test_valid_image():
    response = app.test_client().post(
        "/get-smpl",
        json={
            "image": "asdf",
            "address": "0xF9c4F532074676a1EA27b3b81A0F6c4Ad511AC34",
            "tokenId": "36",
        },
    )
    assert response.status_code == 400
    assert response.text == "Invalid image"


def test_fails_for_different_image():
    response = app.test_client().post(
        "/get-smpl",
        json={
            "image": "data:image/jpeg;base64,asdf",
            "address": "0xF9c4F532074676a1EA27b3b81A0F6c4Ad511AC34",
            "tokenId": "0",
        },
    )
    print(response.text)
    assert response.status_code == 401
    assert response.text == "Image hash does not match one in contract"
