from typing import Union, List
from ..utils import load_json, save_json
from ..eth import init
from typing import TypedDict, List

Attribute = TypedDict("Attribute", {"trait_type": str, "value": str})

MetadataEntry = TypedDict(
    "MetadataEntry",
    {
        "token_id": Union[int, str],
        "name": str,
        "description": str,
        "external_url": str,
        "image": str,
        "attributes": List[Attribute],
    },
)


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
        if self._metadata == {}:
            self._prepopulate()

    def _load(self):
        metadata = load_json("artifacts/metadata.json")
        if metadata is not None:
            self._metadata = metadata
        else:
            self._metadata = {}

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
        metadata_entry: MetadataEntry = {
            "token_id": token_id,
            "name": f"SMPL #{best_match_fname}",
            "description": self._description,
            "external_url": f"https://pieces.smplverse.xyz/token/{token_id}",
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

    def _blank(self, token_id: str):
        return {
            "token_id": token_id,
            "name": "UNCLAIMED SMPL",
            "description": self._description,
            "external_url": "",
            "image": "ipfs://QmYypT49WH7rYTL2jXpfoNH2DAMHe9VM7pwwEjUVr45XK1",
            "attributes": [],
        }

    def add(
        self,
        token_id: str,
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

    def get(self, token_id: str):
        if token_id in self._metadata:
            return self._metadata[token_id]
        else:
            return self._blank(token_id)

    # metadtata should be backed up under IPFS or somewhere it never gets lost
    # something like that
    def check(self, name):
        for i in self._metadata:
            if self._metadata[i]["name"] == name:
                return True
            else:
                return False


def get_metadata_object():
    return Metadata()
