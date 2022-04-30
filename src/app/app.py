from hashlib import sha256

from flask import Flask, jsonify, request

from ..eth.init import init
from ..inference_package.matcher import Matcher
from .encode import b64_to_numpy, numpy_to_b64

app = Flask(__name__)

matcher = Matcher()

_, contract = init()

# below has to be backed up in some way,
# ideally stored on ipfs, but pickling should work too
metadata = {}


@app.route("/", methods=["GET"])
def root():
    return "OK", 200


@app.route("/detect-face", methods=["POST"])
def detect_face():
    if "image" not in request.json:
        return "No image provided", 400
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
        return "No JSON data provided", 400
    if "image" not in request.json:
        return "No image provided", 400
    if "address" not in request.json:
        return "No address provided", 400
    if "tokenId" not in request.json:
        return "No tokenId provided", 400

    tokenId = request.json["tokenId"]
    sender_address = request.json["address"]
    image = request.json["image"]
    _, img_b64 = ",".split(image)

    img_hash = sha256(img_b64.encode()).hexdigest()

    owner, _, _ = contract.functions.explicitOwnershipOf(tokenId).call()
    if owner != sender_address:
        return "address is not the owner of the smpl", 400

    hash_in_contract: bytes = contract.functions.uploads(tokenId).call()
    if img_hash != hash_in_contract.hex():
        return "image hash does not match one in contract", 400

    best_match, distance = matcher.match(b64_to_numpy(img_b64))
    best_match_fname = best_match.split("/")[-1].split(".")[0]
    desc = "SMPLverse is a collection of synthetic face data from the computational infrastructure of the metaverse, assigned to minters using facial recognition."
    clustered_ones = [
        "037544",
        "069701",
        "099370",
        "093321",
        "051039",
        "046594",
        "059759",
        "074727",
        "083824",
        "037661",
        "059324",
    ]

    metadata_to_add = {
        "tokenId": tokenId,
        "name": f"SMPL {best_match_fname}",
        "description": desc,
        # add rev proxy to aws
        "external_url": "https://pieces.smplverse.xyz/token/#",
        "image": "ipfs://...",
        "attributes": [
            {
                "trait_type": "confidence",
                "value": f"{1 - distance:%}",  # TODO: make this a percentage with 3 decimals
            },
            {
                "trait_type": "user image hash",
                "value": img_hash,
            },
        ],
    }

    if best_match_fname in clustered_ones:
        metadata_to_add["attributes"].append(
            {
                "trait_type": "Head Pose",
                "value": "cluster_182",
            }
        )

    # TODO upload on a rolling basis, show the ipfs cid on the frontend and hyperlink it
    # replace the user image with the smpl
    # stop displaying face mesh on hover

    metadata[metadata_to_add] = metadata_to_add
    return jsonify(metadata_to_add)


@app.route("/metadata/<tokenId>", methods=["POST", "GET"])
def metadata(tokenId):
    if tokenId in metadata:
        return metadata[tokenId]
    return f"metadata for {tokenId} could not be found", 404
