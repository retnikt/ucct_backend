"""
Copyright 2020 retnikt

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import base64
import binascii
from typing import TYPE_CHECKING

from starlette.datastructures import UploadFile
from starlette.exceptions import HTTPException


class Bytes:
    """
    represent raw binary data in transport using uploaded files or base-64
    """

    @classmethod
    def validate(cls, obj) -> bytes:
        if isinstance(obj, UploadFile):
            # uploaded as a file
            return obj.file.read()

        elif isinstance(obj, str):
            # uploaded in base64
            try:
                return base64.b64decode(obj.encode())
            except binascii.Error:
                raise HTTPException(400, "invalid base64 data")

    @classmethod
    def __get_validators__(cls):
        yield cls.validate


# for type-checker simplification:
if TYPE_CHECKING:
    Bytes = bytes
