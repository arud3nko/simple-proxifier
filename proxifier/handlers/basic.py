from __future__ import annotations

from aiohttp import ClientSession
from aiohttp.web import Request, Response

from proxifier.types.handler import RequestHandler


class BasicAsyncHandler(RequestHandler):
    """Basic `aiohttp` request handler, just sends request and returns response"""

    def __init__(self):
        self._session: ClientSession = ClientSession()

    @property
    def session(self) -> ClientSession:
        return self._session

    @session.setter
    def session(self, v: ClientSession):
        self._session = v

    async def __call__(self, request: Request, *args, **kwargs) -> Response:
        async with self._session.request(method=request.method,
                                         url=request.url,
                                         **kwargs) as _response:
            _text = await _response.text()

        return Response(status=_response.status,
                        reason=_response.reason,
                        text=_text)