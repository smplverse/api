import base64
import os
from typing import TypedDict

import numpy as np
import requests

IpfsResponse = TypedDict(
    "IpfsResponse",
    {
        "Hash": str,
        "Name": str,
        "Size": str,
    },
)


class IPFS:

    s: requests.Session
    endpoint = os.environ.get("IPFS_ENDPOINT")
    project_id = os.environ.get("IPFS_PROJECT_ID")
    project_secret = os.environ.get("IPFS_PROJECT_SECRET")

    def __init__(self):
        self.s = requests.Session()
        self._init_auth()
        assert self.endpoint is not None
        assert self.project_id is not None
        assert self.project_secret is not None

    def upload(self, path: str) -> IpfsResponse:
        response = self.s.post(
            f"{self.endpoint}/api/v0/add",
            params={"pin": "false"},
            files={path: open(path, "rb")},
        )
        return response.json()

    def upload_numpy(self, fname: str, img: np.ndarray) -> IpfsResponse:
        response = self.s.post(
            f"{self.endpoint}/api/v0/add",
            params={"pin": "false"},
            files={fname: img.tobytes()},
        )
        return response.json()

    def _init_auth(self):
        credentials = "%s:%s" % (self.project_id, self.project_secret)
        bs = base64.b64encode(credentials.encode("utf-8"))
        self.s.headers["Authorization"] = "Basic %s" % bs.decode("utf-8")
