import numpy as np


class Distance:

    def __init__(self, source: np.ndarray, test: np.ndarray):
        self.source = source
        self.test = test

    def cosine(self) -> float:
        a = np.matmul(np.transpose(self.source), self.test)
        b = np.sum(np.multiply(self.source, self.source))
        c = np.sum(np.multiply(self.test, self.test))
        return 1 - (a / (np.sqrt(b) * np.sqrt(c)))

    def euclidean(self) -> float:
        return self._euclidean(self.source, self.test)

    def euclidean_l2(self) -> float:
        source = self._l2_normalize(self.source)
        test = self._l2_normalize(self.test)
        return self._euclidean(source, test)

    @staticmethod
    def _euclidean(source: np.ndarray, test: np.ndarray) -> float:
        distance = source - test
        distance = np.sum(np.multiply(distance, distance))
        distance = np.sqrt(distance)
        return distance

    @staticmethod
    def _l2_normalize(x: np.ndarray):
        _x = x.copy()
        return _x / np.sqrt(np.sum(np.multiply(_x, _x)))
