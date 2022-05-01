from dataclasses import dataclass


# TODO add typing for metadata values struct


@dataclass
class Metadata:

    _metadata = {}

    # the only problem I can think of is that if there are two workers, if they
    # both get a request at the same time they might read in the same set of
    # smpls both assign a different smpl, one writes first, second later, this
    # way there is only one smpl popped from the smpls object
    # maybe there is a way for them to share the object?
    # or share metadata object? and call the check method?
    def add(self, tokenId, metadata_to_add):
        if tokenId in self._metadata:
            return
        self._metadata[tokenId] = metadata_to_add

    def get(self, tokenId):
        if tokenId in self._metadata:
            return self._metadata[tokenId]
        else:
            return None

    # something like that
    def check(self, name):
        for i in self._metadata:
            if self._metadata[i]["name"] == name:
                return True
            else:
                return False


def get_metadata_object():
    return Metadata()
