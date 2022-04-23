import cv2

from src.app.encode import numpy_to_b64, b64_to_numpy
from src.app.app import app


def test_face_detection():
    face_img = cv2.imread("artifacts/sample_face.png")
    face_img_b64 = numpy_to_b64(face_img)
    response = app.test_client().post(
        '/detect-face',
        json={"image": face_img_b64},
    )
    assert response.status_code == 200
    assert response.json is not None
    assert "image" in response.json
    assert "error" in response.json
    img = b64_to_numpy(response.json["image"])
    assert img.shape == face_img.shape
