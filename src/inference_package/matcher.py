from typing import List, Tuple

import numpy as np
import random

from .detector import Detector
from .distance import Distance
from .model import Model
from ..smpls import get_smpls_object


class Matcher:

    model: Model
    detector: Detector
    scores: List[float] = []

    def __init__(self):
        self.model = Model(path="artifacts/resnet100.onnx")
        self.distance = Distance()
        self.detector = Detector()
        self.failed_detections = 0
        self.smpls = get_smpls_object()

    def match(self, img: np.ndarray):
        """
        matches face from image against embeddings of smpls
        """
        face = self.detector.detect_face(img)
        if face is None:
            raise Exception("No face detected")
        face_repr = self.model(face)
        scores = []
        skipped = []
        for fpath, smpl_repr in self.smpls._smpls.items():
            if smpl_repr is None:
                skipped.append(fpath)
                continue
            assert face_repr.shape == smpl_repr.shape
            scores.append(self.distance.euclidean_l2(smpl_repr, face_repr))
        fnames = list(self.smpls.available().keys())
        best_match = fnames[np.argmin(scores)]
        self.smpls.claim(best_match)
        distance = np.min(scores)
        return best_match, distance

    def get_random(self) -> Tuple[str, float]:
        """
        returns a random smpl
        """
        random_smpl = np.random.choice(self.smpls.available().keys())
        self.smpls.claim(random_smpl)
        return random_smpl, random.uniform(0, 0.7)
