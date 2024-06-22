from aiohttp import web

from proxifier import Proxifier, ProxifierMiddleware
from proxifier.types.generic import Request_T, CallNext_T

REDIRECT_URL = "/"


class LogPreMiddleware(ProxifierMiddleware):
    """Simple logging middleware"""
    async def __call__(self, request: web.Request, call_next: CallNext_T) -> Request_T:
        print(f"Handling {request.method} request to {request.url} from {request.remote}")
        return await call_next(request)


class ChangeUserRelURL(ProxifierMiddleware):
    """Changes `Request` instance `rel_url` parameter"""
    def __init__(self, rel_url: str):
        self.rel_url = rel_url
        """Final `rel_url`"""

    async def __call__(self, request: web.Request, call_next: CallNext_T) -> Request_T:
        request = request.clone(rel_url=self.rel_url)
        return await call_next(request)


async def init_app() -> web.Application:
    """Initialize the aiohttp application."""
    app = web.Application()

    _proxifier = Proxifier()  # `Proxifier` initializes with default `BasicAsyncHandler` handler
    _proxifier.add_pre_middleware(LogPreMiddleware())
    _proxifier.add_pre_middleware(ChangeUserRelURL(rel_url=REDIRECT_URL))
    _proxifier.add_pre_middleware(LogPreMiddleware())

    app['proxifier'] = _proxifier

    app.router.add_route('*', '/{tail:.*}', app['proxifier'].handle)

    return app

if __name__ == '__main__':
    web.run_app(init_app(), host='127.0.0.1', port=8080)
