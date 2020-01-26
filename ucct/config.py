from starlette.config import Config

config = Config(".env")
DEBUG = config("DEBUG", cast=bool, default=False)
PORT = config("PORT", cast=int, default=1808)
HOST = config("HOST", default="localhost")
LOAD_BASE = config("LOAD_BASE", cast=bool, default=True)
# maximum upload file size in bytes, default 157286400 (15MiB)
MAX_FILE_SIZE = config("MAX_FILE_SIZE", cast=int, default=157286400)
