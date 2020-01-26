import asyncio
import base64
import types
import warnings
from typing import Tuple, Optional, Type, Union, Callable, TypeVar

import pydantic
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import UJSONResponse

from ucct import config
from ucct.category import Category


class _Tool(dict):
    def __init__(self, func, *args, **kwargs):
        self._func = func
        super(_Tool, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)


class App(Starlette):
    def __init__(self, *args, **kwargs):
        super(App, self).__init__(*args, **kwargs)
        self.tools = {}

        self.add_middleware(CORSMiddleware, allow_origins=["*"])

        @self.route("/:tools")
        async def tools(_):
            await asyncio.sleep(2)
            return UJSONResponse(self.tools)

        if config.LOAD_BASE:
            from ucct import base
            base.load(self)

    tool_decorator_argument = TypeVar(
        "tool_decorator_argument", types.FunctionType, Type[pydantic.BaseModel]
    )

    def tool(
            self,
            *,
            slug: str,
            name: str,
            version: Tuple[int, int, int],
            author: Optional[str] = None,
            description: Optional[str] = None,
            category: Category = Category.Other,
            website: Optional[str] = None,
    ) -> Callable[[tool_decorator_argument], tool_decorator_argument]:
        """
        @decorator to register and convert a callable class or function as a Tool
        :param slug: url-safe identifier for the tool - if it contains whitespace or colon, there may be strange behaviour
        :param name: name of the tool
        :param version: version of the tool as a semver tuple (major, minor, patch)
        :param author: author to credit
        :param description: description of the tool
        :param category: Category enum value of the tool
        :param website: URL for the tool e.g. github, documentation, etc.

        """

        def decorator(obj: Union[types.FunctionType, Type[pydantic.BaseModel]]):
            if isinstance(obj, types.FunctionType):
                # not a class, but a real function
                # so create callable pydantic class from function
                cls = type(
                    slug,
                    (pydantic.BaseModel,),
                    {"__annotations__": obj.__annotations__,
                     "__call__": lambda bound: obj(**bound.dict())},
                )
            else:
                cls = obj

            @self.route(f"/{slug}", methods=["POST"])
            async def do(request: Request):
                form = await request.form()
                try:
                    if hasattr(obj, "context_hook"):
                        with obj.context_hook(request):
                            bound = cls.parse_obj(form)
                    else:
                        bound = cls.parse_obj(form)
                except pydantic.ValidationError as e:
                    raise HTTPException(400, e.json()) from e

                value = await bound()
                if isinstance(value, bytes):
                    value = base64.b64encode(value)

                return UJSONResponse(value)

            if slug in self.tools:
                warnings.warn(
                    f"a tool with the slug '{slug}' is already registered",
                    UserWarning)

            self.tools[slug] = {
                "slug": slug,
                "name": name,
                "version": version,
                "author": author,
                "description": description,
                "website": website,
                "category": category,
                "schema": cls.schema()
            }

            obj.__ucct__ = True
            return obj

        return decorator


app = App(debug=config.DEBUG)
