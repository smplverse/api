from src.utils import deserialize
from dataclasses import dataclass

from src.utils.serialize import serialize


@dataclass
class SMPLs:
    _smpls: dict

    def __init__(self):
        self._smpls = deserialize("artifacts/embeddings.p")

    def available(self):
        return self._smpls

    def claim(self, smpl_path: str):
        self._smpls.pop(smpl_path, None)
        serialize(self._smpls, "artifacts/embeddings.p")


def get_smpls_object() -> SMPLs:
    return SMPLs()
