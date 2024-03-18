from pathlib import Path

from toml import loads

from .bot import Bot

__version__ = loads(open(Path(__name__).resolve().parents[0] / "pyproject.toml").read())["tool"]["poetry"]["version"]