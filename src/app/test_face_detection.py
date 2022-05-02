import cv2
import numpy as np

from src.utils import numpy_to_b64, b64_to_numpy
from src.app import app


def test_face_detection():
    face_img = cv2.imread("artifacts/sample_face.png")
    face_img_b64 = numpy_to_b64(face_img)
    response = app.test_client().post(
        "/detect-face",
        json={"image": face_img_b64},
    )
    assert response.status_code == 200
    assert response.json is not None
    assert "image" in response.json
    assert "error" in response.json
    img = b64_to_numpy(response.json["image"])
    assert img.shape == face_img.shape


def test_bad_requests():
    response = app.test_client().post(
        "/detect-face",
        json={"not_image": "not_image"},
    )
    assert response.status_code == 400

    response = app.test_client().post("/detect-face", data={"image": "asdf"})
    assert response.status_code == 400


def test_if_detection_fails():
    no_face_img = numpy_to_b64(np.zeros((100, 100, 3), dtype=np.uint8))
    response = app.test_client().post(
        "/detect-face",
        json={"image": no_face_img},
    )
    assert response.status_code == 200
    assert response.json is not None
    assert response.json["image"] is None
    assert response.json["error"] == "could not detect face"
