from src.smpls import get_smpls_object


def test_after_claiming_smpl_becomes_unavailable():
    smpls = get_smpls_object()
    available_smpls_before = smpls.available()
    matched = list(available_smpls_before.keys())[5]
    smpls.claim(matched)
    available_smpls_after = smpls.available()
    assert matched not in list(available_smpls_after.keys())
