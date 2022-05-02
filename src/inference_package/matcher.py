import pickle
from typing import Dict, List

import numpy as np

from .detector import Detector
from .distance import Distance
from .model import Model


class Matcher:

    model: Model
    detector: Detector
    smpls_embeddings: Dict[str, np.ndarray]
    fnames: List[str]
    scores: List[float] = []

    def __init__(self):
        self.model = Model(path="artifacts/resnet100.onnx")
        self.distance = Distance()
        self.detector = Detector()
        self.failed_detections = 0
        with open("artifacts/embeddings.p", "rb") as f:
            self.smpls_embeddings = pickle.load(f)
        self.fnames = list(self.smpls_embeddings.keys())

    def match(self, img: np.ndarray):
        """
        matches face from image against embeddings of smpls
        """
        face = self.detector.detect_face(img)
        if not face:
            raise Exception("No face detected")
        face_repr = self.model(face)
        scores = []
        skipped = []
        for fpath, smpl_repr in self.smpls_embeddings.items():
            if smpl_repr is None:
                skipped.append(fpath)
                continue
            assert face_repr.shape == smpl_repr.shape
            scores.append(self.distance.euclidean_l2(smpl_repr, face_repr))
        best_match = self.fnames[np.argmin(scores)]
        distance = np.min(scores)
        return best_match, distance
