from src.eth.init import init


def test_inits_right():
    provider, contract = init()
    assert provider.isConnected()
    assert contract.functions.name().call() == "SMPLverse"
