from hashlib import sha256

from flask import Flask, jsonify, request

from ..eth import init
from ..inference_package.matcher import Matcher
from ..utils import b64_to_numpy, numpy_to_b64, format_address, b64_from_file
from ..smpls import Metadata
from ..ipfs import IPFS
from ..s3 import S3

app = Flask(__name__)

matcher = Matcher()

_, contract = init()

ipfs = IPFS()

metadata_object = Metadata()

s3 = S3()


@app.route("/", methods=["GET"])
def root():
    return "OK", 200


@app.route("/detect-face", methods=["POST"])
def detect_face():
    if not request.json:
        return 400
    if "image" not in request.json:
        return "No image provided", 400
    if not "data:image/jpeg;base64," in request.json["image"]:
        return "Invalid image", 400
    _, img_b64 = request.json["image"].split(",")
    img = b64_to_numpy(img_b64)
    img_with_landmarks = matcher.detector.face_mesh(img)
    if img_with_landmarks is None:
        return jsonify({"image": None, "error": "could not detect face"})
    b64 = numpy_to_b64(img_with_landmarks)
    return jsonify({"image": b64, "error": None})


@app.route("/get-smpl", methods=["POST"])
def get_smpl():
    if not request.json:
        return 400
    if "image" not in request.json:
        return "No image provided", 400
    if "address" not in request.json:
        return "No address provided", 400
    if "tokenId" not in request.json:
        return "No token_id provided", 400

    try:
        assert 7667 > int(request.json["tokenId"]) >= 0
    except (ValueError, AssertionError):
        return "Invalid token_id", 400

    token_id = int(request.json["tokenId"])
    sender_address = request.json["address"]
    image = request.json["image"]

    if not contract.web3.isAddress(sender_address):
        return "Invalid address", 400

    if not "data:image/jpeg;base64," in image:
        return "Invalid image", 400

    user_img_hash = "0x" + sha256(image.encode()).hexdigest()
    hash_in_contract = "0x" + contract.functions.uploads(token_id).call().hex()
    
    existing_metadata = metadata_object.get(token_id)
    if 'name' in existing_metadata:
        if existing_metadata["name"] != "UNCLAIMED SMPL":
            return f"SMPL already assigned for token_id {token_id}", 400

    owner, _, _ = contract.functions.explicitOwnershipOf(token_id).call()
    if owner != sender_address:
        return (
            "Address {} is not the owner of the token {} ({})".format(
                format_address(sender_address),
                format_address(owner),
                token_id,
            ),
            401,
        )

    if eval(hash_in_contract) == 0:
        return f"SMPL not uploaded for {token_id} yet", 400

    if user_img_hash != hash_in_contract:
        return "Image hash does not match one in contract", 401

    _, img_b64 = image.split(",")
    img_numpy = b64_to_numpy(img_b64)
    best_match, distance = matcher.match(img_numpy)
    best_match_fname = best_match.split("/")[-1].split(".")[0]

    print(best_match)
    ipfs_response = ipfs.upload(best_match)

    # convert back to string (easier with dicts)
    token_id = str(token_id)
    s3.upload_image(best_match_fname, img_numpy)

    metadata_object.add(
        token_id,
        best_match_fname,
        ipfs_response["Hash"],
        distance,
        user_img_hash,
    )

    smpl_image = f"data:image/png;base64,{b64_from_file(best_match)}"

    return jsonify({
        **metadata_object.get(token_id),
        "smpl_image": smpl_image,
    })


@app.route("/metadata/<token_id>", methods=["GET"])
def get_metadata(token_id: str):
    try:
        assert 7667 > int(token_id) >= 0
    except (ValueError, AssertionError):
        return "Invalid token_id", 400
    total_supply = contract.functions.totalSupply().call()
    if int(token_id) + 1 > total_supply:
        return "Token not minted yet", 404
    return metadata_object.get(token_id)
