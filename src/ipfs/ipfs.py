import base64
import os
from typing import TypedDict

import requests


class Response(TypedDict):
    Name: str
    Hash: str
    Size: str


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

    def upload(self, content: str) -> Response:
        files = {
            "file": (content),
        }

        response = self.s.post(
            self.endpoint + "/api/v0/add",
            files=files,
        )
        return response.json()

    def get(self, loc: str):
        params = [
            ("arg", loc),
        ]
        res = self.s.post(
            self.endpoint + "/api/v0/block/get",
            params=params,
        )
        print(res.text)
        print(res.headers)

    def _init_auth(self):
        credentials = "%s:%s" % (self.project_id, self.project_secret)
        bs = base64.b64encode(credentials.encode("utf-8"))
        self.s.headers["Authorization"] = "Basic %s" % bs.decode("utf-8")
