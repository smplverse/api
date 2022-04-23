import cv2

from src.app.encode import numpy_to_b64, b64_to_numpy
from src.app.app import app


class TestGetSmpl:

    face_img = cv2.imread("artifacts/sample_face.png")

    def fails_with_invalid_address(self):
        face_img_b64 = numpy_to_b64(self.face_img)
        json = {
            "address": "0x0000000000000000000000000000000000000000",
            "image": face_img_b64,
            "tokenId": 1,
        }
        response = app.test_client().post("/get-smpl", json=json)
        # TODO the response will include the smpl cid, so that the user can view their art
        print(response.json)

    def after_claiming_smpl_becomes_unavailable():
        ...
        # TODO ensure that once claimed is out of the data
