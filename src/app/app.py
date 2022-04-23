from flask import Flask, abort, jsonify, request
from werkzeug.sansio.response import Response

from src.app.encode import b64_to_numpy, numpy_to_b64
from src.inference_package.matcher import Matcher

app = Flask(__name__)

matcher = Matcher()


def bad_request(msg: str):
    return Response(response=jsonify({"error": msg}), status=400)


@app.route("/detect-face", methods=["POST"])
def detect_face():
    if not request.json:
        bad_request("No JSON data provided")
    if "image" not in request.json:
        bad_request("No image provided")
    img_b64 = request.json["image"]
    img = b64_to_numpy(img_b64)
    img_with_landmarks = matcher.detector.face_mesh(img)
    if img_with_landmarks is None:
        return jsonify({"image": None, "error": "could not detect face"})
    b64 = numpy_to_b64(img_with_landmarks)
    return jsonify({"image": b64, "error": None})


@app.route("/get-smpl", methods=["POST"])
def assign_smpl():
    if not request.json:
        bad_request("No JSON data provided")
    if "image" not in request.json:
        bad_request("No image provided")
    if "address" not in request.json:
        bad_request("No address provided")
    if "tokenId" not in request.json:
        bad_request("No tokenId provided")
    return jsonify({"error": None})
