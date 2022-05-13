import cv2
import os
import logging

import boto3
import numpy as np

from botocore.exceptions import ClientError


class S3:
    resource = boto3.resource('s3')
    bucket = 'smplverse'

    def upload_image(self, name: str, img: np.ndarray):
        assert name
        assert img is not None and all(i for i in img.shape)
        file_name = f'{name}.png'
        cv2.imwrite(file_name, img)
        try:
            self.resource.Bucket('smplverse').put_object(
                Key=file_name,
                Body=open(file_name, 'rb'),
                ExtraArgs={'ACL': 'public-read'},
            )
        except ClientError as e:
            logging.error(e)
        finally:
            os.remove(file_name)
