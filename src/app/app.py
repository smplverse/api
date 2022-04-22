from flask import Flask, request, abort, jsonify

from src.inference_package.matcher import Matcher
from src.app.encode import b64_to_numpy, numpy_to_b64

app = Flask(__name__)

matcher = Matcher()


@app.route("/detect-face", methods=["POST"])
def detect_face():
    if not request.json or 'image' not in request.json:
        abort(400)
    img_b64 = request.json['image']
    img = b64_to_numpy(img_b64)
    b64 = numpy_to_b64(img)
    return jsonify({"image": b64})
