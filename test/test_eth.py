from src.eth import init


def test_inits_right():
    provider, contract = init()
    assert provider.isConnected()
    assert contract.functions.name().call() == "SMPLverse"


def test_checks_ownership():
    _, contract = init()
    owner_of_first, _, _ = contract.functions.explicitOwnershipOf(0).call()
    assert owner_of_first == contract.functions.owner().call()


def test_checks_hash_uploaded():
    _, contract = init()
    upload_hash: bytes = contract.functions.uploads(880).call()
    hash_hex = "0x" + upload_hash.hex()
    zero = "0x0000000000000000000000000000000000000000000000000000000000000000"
    assert hash_hex == zero
