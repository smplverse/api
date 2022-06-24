import json
import os
from typing import Tuple

from web3 import HTTPProvider, Web3
from web3.contract import Contract

CHAIN = os.environ.get("CHAIN")
INFURA_KEY = os.environ.get("INFURA_KEY")
CONTRACT_ADDRESS = os.environ.get(f"CONTRACT_ADDRESS_{CHAIN.upper()}")


def init() -> Tuple[Web3, Contract]:
    if not INFURA_KEY:
        raise ValueError("INFURA_KEY is not set")
    if not CONTRACT_ADDRESS:
        raise ValueError(f"CONTRACT_ADDRESS_{CHAIN.upper()} is not set")
    provider_url = f"https://{CHAIN}.infura.io/v3/{INFURA_KEY}"
    w3 = Web3(HTTPProvider(provider_url))
    with open("artifacts/SMPLverse.json", "r") as f:
        artifact = json.loads(f.read())
    contract = w3.eth.contract(
        w3.toChecksumAddress(CONTRACT_ADDRESS),
        abi=artifact["abi"],
    )
    print(f"using contract at {CONTRACT_ADDRESS} on {CHAIN}")
    return w3, contract
