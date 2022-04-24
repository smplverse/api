import cv2
import pytest

from src.app.encode import numpy_to_b64, b64_to_numpy
from src.app.app import app
from src.smpls import get_smpls_object

face_img = cv2.imread("artifacts/sample_face.png")


@pytest.fixture()
def smpls_object():
    return get_smpls_object()


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


def test_after_claiming_smpl_becomes_unavailable(smpls_object):
    # TODO ensure that once claimed is out of the data
    ...


def test_only_the_same_hash_can_be_used_to_claim():
    ...
