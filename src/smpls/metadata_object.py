from dataclasses import dataclass


@dataclass
class Metadata:

    # the only problem I can think of is that if there are two workers, if they
    # both get a request at the same time they might read in the same set of
    # smpls both assign a different smpl, one writes first, second later, this
    # way there is only one smpl popped from the smpls object
    pass


def get_metadata_object():
    return Metadata()
