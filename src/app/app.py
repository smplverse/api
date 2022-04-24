from flask import Flask, jsonify, request
from werkzeug.sansio.response import Response

from src.app.encode import b64_to_numpy, numpy_to_b64
from src.inference_package.matcher import Matcher
from src.eth.init import init
from hashlib import sha256

app = Flask(__name__)

matcher = Matcher()

_, contract = init()


def bad_request(msg: str):
    return Response(response=jsonify({"error": msg}), status=400)


@app.route("/", methods=["GET"])
def root():
    return jsonify({"welcoming mesange": "helo dis smplverse"})


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

    tokenId = request.json["tokenId"]
    sender_address = request.json["address"]
    image = request.json["image"]
    _, img_b64 = ",".split(image)

    # TODO check hashlib_img_hash == javascript_img_hash
    img_hash = sha256(img_b64.encode()).hexdigest()

    # verify that address is the owner of a given smpl
    owner, _, _ = contract.functions.explicitOwnershipOf(tokenId).call()
    if owner != sender_address:
        bad_request("address is not the owner of the smpl")

    # verify that the hash of image sent is the same as the one in the smart contract
    hash_in_contract: bytes = contract.functions.uploads(tokenId).call()
    if img_hash != hash_in_contract.hex():
        bad_request("image hash does not match one in contract")

    # perform the match

    # disclude the smpl from future runs
    # for the run I think another api of smpls should be up
    # and running synchronously so that it is nicely FIFO

    # TODO upload the smpl to ipfs here or beforehand? (save time)

    # { CID, confidence, random_three_words?, ...}
    return jsonify({"something": "fancy"})
