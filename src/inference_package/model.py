import onnxruntime as ort
import numpy as np
import cv2

from typing import List


class Model:

    session: ort.InferenceSession
    output_shape: List[int]
    input_shape: List[int]
    input_name: str
    providers = [
        ('CUDAExecutionProvider', {
            'device_id': 0,
            'arena_extend_strategy': 'kNextPowerOfTwo',
            'gpu_mem_limit': 2 * 1024 * 1024 * 1024,
            'cudnn_conv_algo_search': 'EXHAUSTIVE',
            'do_copy_in_default_stream': True,
        }),
        ('CPUExecutionProvider', {
            'use_arena': True,
            'arena_extend_strategy': 'kNextPowerOfTwo',
            'cpu_fast_math_mode': True,
        }),
    ]

    def __init__(self, path: str = "models/resnet100.onnx"):
        self.session = ort.InferenceSession(path, providers=self.providers)
        self.input_shape = self.session.get_inputs()[0].shape
        self.output_shape = self.session.get_outputs()[0].shape
        if "vgg" in path:
            self.input_name = "input_1"
        else:
            self.input_name = "input.1"
        print("%s session started" % path)

    def __call__(self, img: np.ndarray):
        if any(i <= 1 for i in img.shape):
            return np.zeros(512)
        inp = self.preprocess(img)
        out = self.feed(inp)
        return self.postprocess(out)

    def preprocess(self, img: np.ndarray) -> np.ndarray:
        """
        :param img: the face to be fed into the vgg model

        this is assuming that the face has been detected,
        preprocessing is model specific here and is mostly
        around getting the input size right
        """
        _img = img.copy()
        _img = self.apply_padding(_img)
        _img = np.transpose(_img, (2, 1, 0))
        _img = np.expand_dims(_img, axis=0)
        _img = _img / 255
        _img = _img.astype(np.float32)
        return _img

    def feed(self, inp: np.ndarray):
        out = self.session.run(None, {self.input_name: inp})
        return out

    def postprocess(self, out: List):
        [[embedding]] = out
        return embedding

    def apply_padding(self, img: np.ndarray) -> np.ndarray:
        _img = img.copy()
        _, _, h, w = self.input_shape
        factor_0 = h / _img.shape[0]
        factor_1 = w / _img.shape[1]
        factor = min(factor_0, factor_1)

        dsize = (int(_img.shape[1] * factor), int(_img.shape[0] * factor))
        _img = cv2.resize(_img, dsize)

        # Then pad the other side to the target size by adding black pixels
        diff_0 = h - _img.shape[0]
        diff_1 = w - _img.shape[1]
        _img = np.pad(
            _img,
            (
                (diff_0 // 2, diff_0 - diff_0 // 2),
                (diff_1 // 2, diff_1 - diff_1 // 2),
                (0, 0),
            ),
            'constant',
        )
        return _img
