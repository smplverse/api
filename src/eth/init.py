import json
import os
from typing import Tuple

from web3 import HTTPProvider, Web3
from web3.contract import Contract

CHAIN = "rinkeby"
INFURA_KEY = os.environ.get("INFURA_KEY")


def init() -> Tuple[Web3, Contract]:
    provider_url = f"https://{CHAIN}.infura.io/v3/" + INFURA_KEY
    w3 = Web3(HTTPProvider(provider_url))
    with open("artifacts/SMPLverse.json", "r") as f:
        artifact = json.loads(f.read())
    contract = w3.eth.contract(
        os.environ.get(f"CONTRACT_ADDRESS_{CHAIN.upper()}"),
        abi=artifact['abi'],
    )
    return w3, contract
