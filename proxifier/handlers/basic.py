from __future__ import annotations

from typing import Type

from aiohttp import ClientSession
from aiohttp.web import Request, Response

from proxifier.types.handler import RequestHandler


class BasicAsyncHandler(RequestHandler):
    """Basic `aiohttp` request handler, just sends request and returns response"""

    def __init__(self):
        self._session: Type[ClientSession] = ClientSession

    @property
    def session(self) -> Type[ClientSession]:
        return self._session

    @session.setter
    def session(self, v: Type[ClientSession]):
        self._session = v

    async def __call__(self, request: Request, *args, **kwargs) -> Response:
        async with self._session() as session:
            _data = await request.read()
            _get_data = request.rel_url.query
            async with session.request(url=request.url,
                                       method=request.method,
                                       headers=request.headers,
                                       params=_get_data,
                                       data=_data,
                                       **kwargs) as _response:
                raw = await _response.read()

        return Response(body=raw,
                        status=_response.status,
                        headers=_response.headers)
