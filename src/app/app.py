import os
from typing import Tuple
from flask import Flask, abort, jsonify, request
from werkzeug.sansio.response import Response

from src.app.encode import b64_to_numpy, numpy_to_b64
from src.inference_package.matcher import Matcher
from web3 import Web3, HTTPProvider
from web3.contract import Contract

app = Flask(__name__)


def init() -> Tuple[Matcher, Web3, Contract]:
    key = os.environ.get("INFURA_KEY")
    provider_url = "https://rinkeby.infura.io/v3/" + key
    w3 = Web3(HTTPProvider(provider_url))
    contract = Contract(os.environ.get("CONTRACT_ADDRESS_RINKEBY"))
    return matcher, w3, contract


def bad_request(msg: str):
    return Response(response=jsonify({"error": msg}), status=400)


matcher, provider, contract = init()


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

    # verify that address is the owner of a given smpl

    # verify that the hash of image sent is the same as the one in the smart contract
    return jsonify({"error": None})
