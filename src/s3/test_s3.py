import pytest
import numpy as np

from . import S3


@pytest.fixture()
def s3() -> S3:
    s3 = S3()
    yield s3


def test_client_works(s3: S3):
    assert len([bucket.name for bucket in s3.resource.buckets.all()])


def test_upload_file_public(s3: S3):
    s3.upload_public('artifacts/sample_face.png')


def test_upload_file(s3: S3):
    s3.upload('artifacts/sample_face.png')


def test_get_img(s3: S3):
    img = s3.get_img('artifacts/sample_face.png')
    assert isinstance(img, np.ndarray)
    assert all(i for i in img.shape)


def test_make_img_public(s3: S3):
    res = s3.make_public('artifacts/sample_face.png')
    assert 'ResponseMetadata' in res
    assert res['ResponseMetadata']['HTTPStatusCode'] == 200
