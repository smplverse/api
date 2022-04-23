import numpy as np

from typing import Union
from mediapipe.python.solutions.face_detection import FaceDetection
from mediapipe.python.solutions.face_mesh import (
    FaceMesh,
    FACEMESH_TESSELATION,
    FACEMESH_CONTOURS,
    FACEMESH_IRISES,
)
from mediapipe.python.solutions.drawing_utils import draw_landmarks
from mediapipe.python.solutions import drawing_styles


class Detector:

    def __init__(self):
        self.face_detector = FaceDetection(min_detection_confidence=0.7)
        self.face_mesh_detector = FaceMesh(
            min_detection_confidence=0.7,
            max_num_faces=1,
            refine_landmarks=True,
        )

    def face_mesh(self, img: np.ndarray) -> Union[np.ndarray, None]:
        results = self.face_mesh_detector.process(img)
        if results.multi_face_landmarks:
            _img = img.copy()
            for face_landmarks in results.multi_face_landmarks:
                draw_landmarks(
                    image=_img,
                    landmark_list=face_landmarks,
                    connections=FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=drawing_styles.
                    get_default_face_mesh_tesselation_style(),
                )
                draw_landmarks(
                    image=_img,
                    landmark_list=face_landmarks,
                    connections=FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=drawing_styles.
                    get_default_face_mesh_contours_style(),
                )
                draw_landmarks(
                    image=_img,
                    landmark_list=face_landmarks,
                    connections=FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=drawing_styles.
                    get_default_face_mesh_iris_connections_style(),
                )
        else:
            return None
        return _img

    def detect_face(
        self,
        img: np.ndarray,
    ) -> Union[np.ndarray, None]:
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
        face = img[y:y + h, x:x + w]
        return face
