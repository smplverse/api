import cv2
import numpy as np
import base64
from flask import Flask, request, abort, jsonify

from src.inference_package.matcher import Matcher

app = Flask(__name__)

matcher = Matcher()


def b64_to_numpy(b64_string: str) -> np.ndarray:
    img = cv2.imdecode(
        np.frombuffer(base64.b64decode(b64_string), np.uint8),
        cv2.IMREAD_UNCHANGED,
    )
    return img


def numpy_to_b64(img: np.ndarray) -> str:
    _, buffer = cv2.imencode('.png', img)
    return base64.b64encode(buffer).decode('utf-8')


@app.route("/detect-face", methods=["POST"])
def detect_face():
    if not request.json or 'image' not in request.json:
        abort(400)
    img_b64 = request.json['image']
    img = b64_to_numpy(img_b64)
    b64 = numpy_to_b64(img)
    return jsonify({"image": b64})
