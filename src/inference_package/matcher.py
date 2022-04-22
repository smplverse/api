import pickle
from typing import Dict, List

import numpy as np

from src.inference_package.detector import Detector
from src.inference_package.distance import Distance
from src.inference_package.model import Model


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
        # TODO face has to be pre-detected as well in the frontend
        # so make /detect-face endpoint that will return same image with coords
        # plotted on it, on hover show the base image
        # so that this surely wont fail
        face = self.detector.detect_face(img)
        if face is None or any(i == 0 for i in face.shape):
            print("could not detect face")
            return
        face_repr = self.model(face)
        scores = []
        skipped = []
        for fpath, smpl_repr in self.smpls_embeddings.items():
            if smpl_repr is None:
                skipped.append(fpath)
                continue
            assert face_repr.shape == smpl_repr.shape
            scores.append(self.distance(smpl_repr, face_repr).euclidean_l2())
        best_match = self.fnames[np.argmin(scores)]
        return best_match
