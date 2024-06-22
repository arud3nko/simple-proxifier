from typing import List

import pytest

from yarl import URL
from aiohttp.web import Application, Response, Request
from pytest_aiohttp.plugin import TestClient

from proxifier.types import RequestHandler

from proxifier.handlers import BasicAsyncHandler

SUCCESS = "success"


async def mock_response(request: Request):
    """Mock route"""
    assert request
    return Response(text=SUCCESS)


class MockRelURL:
    """Mock query params"""
    query: str = ""


class MockRequest:
    """Mocked request clss"""
    def __init__(self, url: URL, method: str, data: str = ""):
        self.url = url
        self.method = method
        self.data = data

        self.headers = {}
        self.rel_url = MockRelURL()

    async def read(self):
        return self.data


def requests(url: URL) -> List[MockRequest]:
    """Provides collection of `ClientRequest` with different methods"""
    return [
        MockRequest(
            url=url,
            method=method,
            data=SUCCESS,
        ) for method in ["GET", "POST"]
    ]


class TestProxifierRequestHandlers:
    """Test class to check proxifier request handlers"""

    @pytest.fixture()
    def app(self):
        """Provides sample aiohttp app (mock)"""
        _app = Application()
        _app.router.add_get("/", mock_response)
        _app.router.add_post("/", mock_response)
        return _app

    @pytest.fixture
    def basic_async_request_handler(self) -> RequestHandler:
        """Provides `BasicAsyncHandler` instance"""
        return BasicAsyncHandler()

    @pytest.mark.asyncio
    async def test_basic_async_request_handler(self,
                                               aiohttp_client,
                                               app,
                                               basic_async_request_handler):
        """
        Check `BasicAsyncHandler` features.

        I replaced handler's session to `TestClient` session to provide `app` fixture's GET & POST routes
        """
        client: TestClient = await aiohttp_client(app)

        url = client.server.make_url("/")
        _requests = requests(url)

        basic_async_request_handler.session = client.session.__class__

        for _request in _requests:
            _resp: Response = await basic_async_request_handler(_request)
            _text = _resp.text

            assert _resp.status == 200
            assert SUCCESS in _text
