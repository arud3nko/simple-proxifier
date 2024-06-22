from typing import Type

import pytest

from proxifier.types import ProxifierMiddleware, RequestHandler
from proxifier.core import Proxifier
from proxifier.types.generic import Request_T


SUCCESS = "success"


class MockRequest:
    """`Request` mock - contains execute() and calls counter"""
    def __init__(self, calls: int = 0, headers: dict = None):
        self.calls = calls
        self.headers = headers

    def execute(self):
        self.calls += 1
        return self

    def clone(self, calls: int = None, headers: dict = None):
        return self.__class__(calls=calls if calls else self.calls,
                              headers=headers if headers else self.headers)


class MockRequestHandler(RequestHandler):
    """`RequestHandler` mock - executes `MockRequest`"""
    @property
    def session(self):
        return

    async def __call__(self, request: MockRequest, *args, **kwargs):
        return request.execute()


class MockMiddleware(ProxifierMiddleware):
    """`ProxifierMiddleware` mock - contains calls counter & __call__()"""
    def __init__(self):
        self.calls = 0

    async def __call__(self, request, call_next) -> Request_T:
        self.calls += 1
        return await call_next(request)


class ChangeRequestHeaderMiddleware(ProxifierMiddleware):
    """This middleware changes incoming request headers"""
    async def __call__(self, request: Request_T, call_next):
        _request = request.clone(headers={SUCCESS: True})
        return await call_next(_request)


class TestProxifierMiddlewaresHandler:
    """Test class used to check common proxifier features"""
    @pytest.fixture(scope="function")
    def middleware(self) -> Type[ProxifierMiddleware]:
        """Provides middleware mock"""
        return MockMiddleware

    @pytest.fixture(scope="function")
    def headers_middleware(self) -> Type[ProxifierMiddleware]:
        """Provides `ChangeRequestHeaderMiddleware` instance"""
        return ChangeRequestHeaderMiddleware

    @pytest.fixture(scope="function")
    def mock_request(self) -> MockRequest:
        """Provides request mock"""
        return MockRequest()

    @pytest.fixture(scope="function")
    def request_handler(self) -> MockRequestHandler:
        """Provides request handler mock"""
        return MockRequestHandler()

    @pytest.fixture(scope="function")
    def proxifier(self) -> Proxifier:
        """Provides `Proxifier` instance"""
        return Proxifier()

    @pytest.mark.asyncio()
    async def test_proxifier(self,
                             mock_request: MockRequest,
                             request_handler: MockRequestHandler):
        """Check if request was handled"""
        _proxifier = Proxifier()
        _proxifier.handler = request_handler

        await _proxifier.handle(mock_request)

        assert mock_request.calls == 1

    @pytest.mark.asyncio
    async def test_proxifier_middlewares_handler(self,
                                                 middleware: Type[MockMiddleware],
                                                 mock_request: MockRequest,
                                                 request_handler: MockRequestHandler):
        """Check if request was handled and middlewares were handled too"""
        _proxifier = Proxifier()

        _proxifier.handler = request_handler

        m1, m2 = middleware(), middleware()

        _proxifier.add_pre_middleware(m1)

        _proxifier.add_post_middleware(m2)

        await _proxifier.handle(mock_request)

        assert mock_request.calls == 1
        assert m1.calls == 1

    @pytest.mark.asyncio
    async def test_middleware_changes_request_instance(self,
                                                       headers_middleware: Type[MockMiddleware],
                                                       mock_request: MockRequest,
                                                       request_handler: MockRequestHandler,
                                                       proxifier: Proxifier):
        """Test if middleware changes `Request` instance correctly"""
        proxifier.handler = request_handler

        m1 = headers_middleware()

        proxifier.add_pre_middleware(m1)

        assert mock_request.headers is None and mock_request.calls == 0

        request = await proxifier.handle(mock_request)

        assert id(mock_request) != id(request)

        assert request.headers == {SUCCESS: True} and request.calls == 1
