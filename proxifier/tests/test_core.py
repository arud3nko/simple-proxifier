from typing import Callable, Type

import pytest

from proxifier.types import ProxifierMiddleware, RequestHandler
from proxifier.core import Proxifier


class MockRequest:
    """`Request` mock - contains execute() and calls counter"""
    def __init__(self):
        self.calls = 0

    def execute(self):
        self.calls += 1


class MockRequestHandler(RequestHandler):
    """`RequestHandler` mock - executes `MockRequest`"""
    @property
    def session(self):
        return

    async def __call__(self, request: MockRequest, *args, **kwargs):
        return request.execute()


class MockMiddleware(ProxifierMiddleware):
    """`ProxifierMiddleware` mock - contains .cls calls counter & __call__()"""
    calls = 0

    @classmethod
    def __call__(cls, request, call_next: Callable):
        cls.calls += 1


class TestProxifierMiddlewaresHandler:
    """Test class used to check common proxifier features"""
    @pytest.fixture(scope="function")
    def middleware(self) -> Type[ProxifierMiddleware]:
        """Provides middleware mock"""
        return MockMiddleware

    @pytest.fixture(scope="function")
    def mock_request(self) -> MockRequest:
        """Provides request mock"""
        return MockRequest()

    @pytest.fixture()
    def request_handler(self) -> MockRequestHandler:
        """Provides request handler mock"""
        return MockRequestHandler()

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

        _proxifier.add_pre_middleware(middleware())

        _proxifier.add_post_middleware(middleware())

        await _proxifier.handle(mock_request)

        assert mock_request.calls == 1
        assert middleware.calls == 2
