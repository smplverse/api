from .encode import b64_to_numpy, numpy_to_b64
from .serialize import deserialize, serialize
from .json import load_json, save_json


def format_address(address):
    return address[:3] + "..." + address[-3:]
