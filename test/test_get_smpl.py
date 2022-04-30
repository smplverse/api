import cv2

from src.app.encode import numpy_to_b64
from src.app.app import app
from src.smpls import get_smpls_object

face_img = cv2.imread("artifacts/sample_face.png")


def test_fails_with_invalid_address():
    face_img_b64 = numpy_to_b64(face_img)
    json = {
        "address": "0x0000000000000000000000000000000000000000",
        "image": face_img_b64,
        "tokenId": 1,
    }
    response = app.test_client().post("/get-smpl", json=json)
    # TODO the response will include the smpl cid, so that the user can view their art
    print(response.json)


def test_after_claiming_smpl_becomes_unavailable():
    smpls = get_smpls_object()
    available_smpls_before = smpls.available()
    matched = list(available_smpls_before.keys())[5]
    smpls.claim(matched)
    available_smpls_after = smpls.available()
    assert matched not in list(available_smpls_after.keys())


def test_bad_requests():
    response = app.test_client().post(
        "/get-smpl",
        json={"not_image": "data,asdf"},
    )
    assert response.status_code == 400

    response = app.test_client().post(
        "/get-smpl",
        json={
            "image": "data,asdf",
            "not_address": "not_address",
        },
    )
    assert response.status_code == 400

    response = app.test_client().post(
        "/get-smpl",
        json={
            "image": "data,asdf",
            "address": "0x123123123..",
            "not_tokenId": "not_tokenId",
        },
    )
    assert response.status_code == 400


def test_valid_address():
    response = app.test_client().post(
        "/get-smpl",
        json={
            "image": "data,asdf",
            "address": "0x123123123",
            "tokenId": "123",
        },
    )
    assert response.status_code == 400

    response = app.test_client().post(
        "/get-smpl",
        json={
            "image": "data,asdf",
            "address": "0xF9c4F532074676a1EA27b3b81A0F6c4Ad511AC34",
            "tokenId": "1",
        },
    )
    assert response.status_code == 401
