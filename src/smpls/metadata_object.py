from typing import Union, List
from ..utils import load_json, save_json
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

    _description = "SMPLverse NFTs use facial recognition to retrieve synthetic training data from the computational infrastructure of the metaverse."

    _clustered_ones = [
        "078131",
        "017289",
        "085461",
        "001785",
        "012285",
        "086697",
        "012364",
    ]

    _base_s3_url = "https://smplverse.s3.us-east-2.amazonaws.com"

    def __init__(self):
        self._load()

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
            "token_id":
            token_id,
            "name":
            f"SMPL #{best_match_fname}",
            "description":
            self._description,
            "image":
            f"{self._base_s3_url}/smpls/{best_match_fname}.png",
            "external_url":
            f"{self._base_s3_url}/smpls/{best_match_fname}.png",
            "ipfs_url":
            "ipfs://%s" % ipfs_hash,
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
            metadata_entry["attributes"].append({
                "trait_type": "Head Pose",
                "value": "cluster_747",
            })
        return metadata_entry

    def _blank(self, token_id: str):
        return {
            "token_id": token_id,
            "name": "UNCLAIMED SMPL",
            "description": self._description,
            "external_url": "",
            "image": "ipfs://QmcbP1QmrEmTcumRbufYnmad95tH5ix7HD84PszQxJK1R2",
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

    def check(self, name):
        for i in self._metadata:
            if self._metadata[i]["name"] == name:
                return True
            else:
                return False


def get_metadata_object():
    return Metadata()
