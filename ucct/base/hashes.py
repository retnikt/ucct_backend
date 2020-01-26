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
