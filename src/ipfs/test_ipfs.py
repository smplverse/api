import pytest
import numpy as np
from src.ipfs import IPFS


@pytest.fixture()
def ipfs():
    ipfs = IPFS()
    ipfs._init_auth()
    return ipfs


def test_uploads_image_right(ipfs: IPFS):
    response = ipfs.upload("artifacts/sample_face.png")
    assert response["Name"] == "sample_face.png"
    assert response["Hash"]
    assert int(response["Size"]) > 25000


def test_uploads_from_numpy(ipfs: IPFS):
    response = ipfs.upload_numpy(
        fname='zeros.png',
        img=np.zeros((100, 100, 3), dtype=np.uint8),
    )
    assert response["Name"] == "zeros.png"
    assert response["Hash"]
    assert int(response["Size"]) != 25000
