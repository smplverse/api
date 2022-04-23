import cv2
import base64
import numpy as np


def b64_to_numpy(b64_string: str) -> np.ndarray:
    img = cv2.imdecode(
        np.frombuffer(base64.b64decode(b64_string), np.uint8),
        cv2.IMREAD_UNCHANGED,
    )
    return img


def numpy_to_b64(img: np.ndarray) -> str:
    _, buffer = cv2.imencode('.jpeg', img)
    return base64.b64encode(buffer).decode('utf-8')
