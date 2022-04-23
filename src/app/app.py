from flask import Flask, abort, jsonify, request

from src.app.encode import b64_to_numpy, numpy_to_b64
from src.inference_package.matcher import Matcher

app = Flask(__name__)

matcher = Matcher()


@app.route("/detect-face", methods=["POST"])
def detect_face():
    if not request.json or 'image' not in request.json:
        abort(400)
    img_b64 = request.json['image']
    img = b64_to_numpy(img_b64)
    # TODO return None if doesnt work and also enforce detection in frontend
    img_with_landmarks = matcher.detector.face_mesh(img)
    if img_with_landmarks is None:
        return jsonify({"image": None, "error": "could not detect face"})
    b64 = numpy_to_b64(img_with_landmarks)
    return jsonify({"image": b64, "error": None})
