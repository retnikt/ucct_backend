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

from starlette.config import Config

config = Config(".env")
DEBUG = config("DEBUG", cast=bool, default=False)
PORT = config("PORT", cast=int, default=1808)
HOST = config("HOST", default="localhost")
LOAD_BASE = config("LOAD_BASE", cast=bool, default=True)
# maximum upload file size in bytes, default 157286400 (15MiB)
MAX_FILE_SIZE = config("MAX_FILE_SIZE", cast=int, default=157286400)
