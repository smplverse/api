import pickle
from typing import Any


def serialize(obj: Any, fpath):
    with open(fpath, "wb") as f:
        pickle.dump(obj, f)


def deserialize(fpath: str) -> Any:
    with open(fpath, "rb") as f:
        obj = pickle.load(f)
    return obj
