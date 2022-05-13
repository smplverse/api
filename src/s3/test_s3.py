import numpy as np
import pytest

from . import S3


@pytest.fixture()
def s3() -> S3:
    s3 = S3()
    yield s3


def test_client_works(s3: S3):
    assert len([bucket.name for bucket in s3.resource.buckets.all()])


def test_upload_file(s3: S3):
    s3.upload('artifacts/sample_face.png')
