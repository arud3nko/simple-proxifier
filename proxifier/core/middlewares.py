from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, Literal, TypeVar, AsyncIterator

if TYPE_CHECKING:
    from ..types import ProxifierMiddleware
    T = TypeVar("T")


class ProxifierMiddlewaresHandler:
    """Handles middlewares"""

    def __init__(self,
                 pre: Optional[List[ProxifierMiddleware]],
                 post: Optional[List[ProxifierMiddleware]]):
        self._pre = pre if pre else []
        self._post = post if post else []

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
        if isinstance(middleware, List):
            return self._post.extend(middleware)
        elif isinstance(middleware, ProxifierMiddleware):
            return self._post.append(middleware)

    async def handle(self, request: T) -> AsyncIterator:
        """Handles request: runs `pre-middlewares` -> yields `request` -> runs `post-middlewares`"""
        await self._run_middlewares("pre_", request, self._pre)
        yield request
        await self._run_middlewares("post_", request, self._post)

    async def _run_middlewares(self,
                               type_: Literal["pre_", "post_"],
                               request: T,
                               middlewares: List[ProxifierMiddleware],
                               index: int = 0):
        """Runs middleware chain"""
        if index < len(middlewares):
            middleware = middlewares[index]
            return middleware(request=request,
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
