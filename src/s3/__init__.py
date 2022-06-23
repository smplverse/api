import logging
import tempfile

import boto3
from botocore.exceptions import ClientError
import numpy as np
from PIL import Image
from typing import Any


class S3:
    resource = boto3.resource('s3')
    bucket = 'smplverse'
    s3 = boto3.client('s3')

    def upload(self, fname: str):
        assert fname
        self.s3.upload_file(fname, self.bucket, fname)

    def upload_public(self, fname: str):
        assert fname
        try:
            self.resource.Bucket(self.bucket).put_object(
                Key=fname,
                Body=open(fname, 'rb'),
                ACL='public-read',
            )
        except ClientError as e:
            logging.error(e)

    def get_img(self, fname: str):
        assert fname
        with tempfile.TemporaryFile() as f:
            self.s3.download_fileobj(self.bucket, fname, f)
            f.seek(0)
            return np.array(Image.open(f))

    def make_public(self, fname: str) -> Any:
        object_acl = self.resource.ObjectAcl(self.bucket, fname)
        return object_acl.put(ACL='public-read')
