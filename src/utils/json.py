import json

from typing import Any


def load_json(fpath: str) -> Any:
    with open(fpath, "r") as f:
        obj = json.load(f)
    return obj


def save_json(obj: Any, fpath: str):
    with open(fpath, "w") as f:
        obj = json.dump(obj, f)
    return obj
