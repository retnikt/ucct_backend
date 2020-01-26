import hashlib
from typing import TYPE_CHECKING

from ucct.category import Category

if TYPE_CHECKING:
    from ucct.app import App

NAMES = {"whirlpool": "Whirlpool"}


def load(app: "App"):
    for algorithm in sorted(hashlib.algorithms_available):

        @app.tool(
            slug=f"hash_{algorithm}",
            name=NAMES.get(algorithm) or algorithm.replace("_", " ").upper(),
            version=(1, 0, 0),
            author="retnikt",
            description="Hashes",
            category=Category.Hash,
        )
        async def do(data: bytes):
            h = hashlib.new(algorithm)
            h.update(data)
            return h.digest()
