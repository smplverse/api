import json
import os
from typing import Tuple

from web3 import HTTPProvider, Web3
from web3.contract import Contract


def init() -> Tuple[Web3, Contract]:
    key = os.environ.get("INFURA_KEY")
    provider_url = "https://rinkeby.infura.io/v3/" + key
    w3 = Web3(HTTPProvider(provider_url))
    with open("artifacts/SMPLverse.json", "r") as f:
        artifact = json.loads(f.read())
    contract = w3.eth.contract(
        os.environ.get("CONTRACT_ADDRESS_RINKEBY"),
        abi=artifact['abi'],
    )
    return w3, contract
