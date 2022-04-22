import numpy as np

from src.inference_package.distance import Distance
from typing import List, Union
from mediapipe.python.solutions.face_detection import FaceDetection


class Detector:

    def __init__(self):
        self.face_detector = FaceDetection(min_detection_confidence=0.7)

    @staticmethod
    def align(
        img: np.ndarray,
        left_eye: List[int],
        right_eye: List[int],
    ):
        left_eye_x, left_eye_y = left_eye
        right_eye_x, right_eye_y = right_eye

        if left_eye_y > right_eye_y:
            point_3rd = np.array([right_eye_x, left_eye_y])
            direction = -1
        else:
            point_3rd = np.array([left_eye_x, right_eye_y])
            direction = 1

        a = Distance(left_eye, point_3rd).euclidean()
        b = Distance(right_eye, point_3rd).euclidean()
        c = Distance(right_eye, left_eye).euclidean()
        if b != 0 and c != 0:
            cos_a = (b * b + c * c - a * a) / (2 * b * c)
            angle = np.arccos(cos_a)
            angle = (angle * 180) / np.pi
            if direction == -1:
                angle = 90 - angle
            img = img.rotate(direction * angle)
        return img

    def detect_face(self, img: np.ndarray) -> Union[np.ndarray, None]:
        results = self.face_detector.process(img)
        if not results.detections:
            return None
        [det, *_] = results.detections
        bbox = det.location_data.relative_bounding_box
        img_height, img_width, _ = img.shape
        x = int(bbox.xmin * img_width)
        w = int(bbox.width * img_width)
        y = int(bbox.ymin * img_height)
        h = int(bbox.height * img_height)
        # landmarks = det.location_data.relative_keypoints
        # right_eye = np.array([
        #     landmarks[0].x * img_width,
        #     landmarks[0].y * img_height,
        # ]).astype(int)
        # left_eye = np.array([
        #     landmarks[1].x * img_width,
        #     landmarks[1].y * img_height,
        # ]).astype(int)
        face = img[y:y + h, x:x + w]
        # face = self.align(face, left_eye, right_eye)
        return face
