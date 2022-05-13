import cv2
import os
import logging

import boto3
import numpy as np

from botocore.exceptions import ClientError


class S3:
    resource = boto3.resource('s3')
    bucket = 'smplverse'

    def upload(self, fname: str):
        assert fname
        try:
            self.resource.Bucket('smplverse').put_object(
                Key=fname.split('/')[-1] if "/" in fname else fname,
                Body=open(fname, 'rb'),
                ACL='public-read',
            )
        except ClientError as e:
            logging.error(e)
