from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ucct.app import App

from ucct.base import hashes


def load(app: "App"):
    hashes.load(app)
