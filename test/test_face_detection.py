import pytest
import cv2

from src.app.encode import numpy_to_b64
from src.app.app import app


@pytest.fixture()
def face_img():
    img = cv2.imread("artifacts/sample_face.png")
    yield numpy_to_b64(img)


def test_face_detection(face_img: str):
    response = app.test_client().post('/detect-face', json={"image": face_img})
    assert response.status_code == 200
    assert response.json['image'] == face_img
