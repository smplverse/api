import logging
import tempfile

import boto3
from botocore.exceptions import ClientError
import numpy as np
from PIL import Image


class S3:
    resource = boto3.resource('s3')
    bucket = 'smplverse'

    def upload(self, fname: str):
        assert fname
        try:
            self.resource.Bucket('smplverse').put_object(
                Key=fname,
                Body=open(fname, 'rb'),
                ACL='public-read',
            )
        except ClientError as e:
            logging.error(e)

    def get_img(self, fname: str):
        assert fname
        s3 = boto3.client('s3')
        with tempfile.TemporaryFile() as f:
            s3.download_fileobj('smplverse', fname, f)
            f.seek(0)
            return np.array(Image.open(f))
