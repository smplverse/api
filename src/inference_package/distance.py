import numpy as np


class Distance:

    def cosine(self, source: np.ndarray, test: np.ndarray) -> float:
        a = np.matmul(np.transpose(source), test)
        b = np.sum(np.multiply(source, source))
        c = np.sum(np.multiply(test, test))
        return 1 - (a / (np.sqrt(b) * np.sqrt(c)))

    def euclidean(self, source: np.ndarray, test: np.ndarray) -> float:
        return self._euclidean(source, test)

    def euclidean_l2(self, source: np.ndarray, test: np.ndarray) -> float:
        _source = self._l2_normalize(source)
        _test = self._l2_normalize(test)
        return self._euclidean(_source, _test)

    @staticmethod
    def _euclidean(source: np.ndarray, test: np.ndarray) -> float:
        distance = np.subtract(source, test)
        distance = np.sum(np.multiply(distance, distance))
        distance = np.sqrt(distance)
        return distance

    @staticmethod
    def _l2_normalize(x: np.ndarray):
        _x = x.copy()
        return _x / np.sqrt(np.sum(np.multiply(_x, _x)))
