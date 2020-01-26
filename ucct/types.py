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
