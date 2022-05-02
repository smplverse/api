from typing import Dict, Union, List
from ..utils import load_json, save_json

Attribute = Dict[str, str]
MetadataEntry = Dict[str, Union[str, List[Attribute]]]


class Metadata:
    _metadata = {}

    _description = "SMPLverse is a collection of synthetic face data from the computational infrastructure of the metaverse, assigned to minters using facial recognition."

    _clustered_ones = [
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

    def __init__(self):
        self._load()

    def _load(self):
        self._metadata = load_json("artifacts/metadata.json")

    def _save(self):
        save_json(self._metadata, "artifacts/metadata.json")

    def _make_metadata_entry(
        self,
        token_id: Union[int, str],
        best_match_fname: str,
        ipfs_hash: str,
        distance: float,
        user_img_hash: str,
    ) -> MetadataEntry:
        metadata_entry = {
            "token_id": token_id,
            "name": f"SMPL #{best_match_fname}",
            "description": self._description,
            # add rev proxy to aws but only upload the images once all minted
            "external_url": f"https://pieces.smplverse.xyz/token/{token_id}",
            # placeholder image for now
            "image": f"ipfs://{ipfs_hash}",
            "attributes": [
                {
                    "trait_type": "confidence",
                    "value": "%.3f" % (1 - distance),
                },
                {
                    "trait_type": "user image hash",
                    "value": user_img_hash,
                },
            ],
        }
        if best_match_fname in self._clustered_ones:
            metadata_entry["attributes"].append(
                {
                    "trait_type": "Head Pose",
                    "value": "cluster_182",
                }
            )
        return metadata_entry

    def add(
        self,
        token_id: int,
        best_match_fname: str,
        ipfs_hash: str,
        distance: float,
        user_img_hash: str,
    ):
        self._load()
        if token_id in self._metadata:
            return
        self._metadata[token_id] = self._make_metadata_entry(
            token_id,
            best_match_fname,
            ipfs_hash,
            distance,
            user_img_hash,
        )
        self._save()

    def get(self, token_id):
        if token_id in self._metadata:
            return self._metadata[token_id]
        else:
            return None

    # something like that
    def check(self, name):
        for i in self._metadata:
            if self._metadata[i]["name"] == name:
                return True
            else:
                return False


def get_metadata_object():
    return Metadata()
