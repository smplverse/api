import pytest
from src.ipfs import IPFS


@pytest.fixture()
def ipfs():
    ipfs = IPFS()
    ipfs._init_auth()
    return ipfs


def test_uploads_image_right(ipfs: IPFS):
    response = ipfs.upload("artifacts/sample_face.png")
    print(response)
    assert response["Name"] == "sample_face.png"
    assert response["Hash"]
    assert int(response["Size"]) > 25000
