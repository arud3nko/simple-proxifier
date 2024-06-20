from __future__ import annotations

from typing import List, Optional, Union, Literal

from ..types import ProxifierMiddleware, RequestHandler
from ..types.generic import Request_T, Response_T

from ..handlers import BasicAsyncHandler


class Proxifier:
    """Handles request"""

    def __init__(self,
                 pre: Optional[List[ProxifierMiddleware]] = None,
                 post: Optional[List[ProxifierMiddleware]] = None,
                 handler: Optional[RequestHandler] = BasicAsyncHandler()):
        self._pre = pre if pre else []
        self._post = post if post else []
        self._handler = handler

    async def handle(self, request: Request_T) -> Response_T:
        """Handles request: runs `pre-middlewares` -> yields `request` -> runs `post-middlewares`"""
        await self._run_middlewares("pre_", request, self._pre)

        _response = await self._handler(request)

        await self._run_middlewares("post_", request, self._post)

        return _response

    @property
    def handler(self) -> RequestHandler:
        """Returns `RequestHandler` instance"""
        return self._handler

    @handler.setter
    def handler(self, v: RequestHandler):
        """Set `RequestHandler` instance"""
        self._handler = v

    def add_pre_middleware(self,
                           middleware: Union[ProxifierMiddleware, List[ProxifierMiddleware]]):
        """Appends middleware to handler's pre-middlewares list"""
        if isinstance(middleware, List):
            return self._pre.extend(middleware)
        elif isinstance(middleware, ProxifierMiddleware):
            return self._pre.append(middleware)

    def add_post_middleware(self,
                            middleware: Union[ProxifierMiddleware, List[ProxifierMiddleware]]):
        """Appends middleware to handler's post-middlewares list"""
        if isinstance(middleware, list):
            return self._post.extend(middleware)
        elif isinstance(middleware, ProxifierMiddleware):
            return self._post.append(middleware)

    async def _run_middlewares(self,
                               type_: Literal["pre_", "post_"],
                               request: Request_T,
                               middlewares: List[ProxifierMiddleware],
                               index: int = 0):
        """Runs middleware chain"""
        if index < len(middlewares):
            middleware = middlewares[index]
            return await middleware(request=request,
                                    call_next=lambda: self._run_middlewares(
                                        type_=type_,
                                        request=request,
                                        index=index + 1,
                                        middlewares=middlewares))
        else:
            return

    @property
    def pre_middlewares(self) -> List[ProxifierMiddleware]:
        """Returns handler's pre-middlewares list"""
        return self._pre

    @property
    def post_middlewares(self) -> List[ProxifierMiddleware]:
        """Returns handler's post-middlewares list"""
        return self._post
