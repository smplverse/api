import os


def test_data_dir_exists():
    smpls = [f for f in os.listdir("data/smpls") if "png" in f]
    assert len(smpls) == 7667
