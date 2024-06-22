# simple-proxifier

A package, used to recieve user's request, add some pre- & post-middlewares, handle this request with `aiohttp` and return response.

Depends only on `aiohttp`.

Currently middlewares are able to change `Request` instance, but not `Response` instance.


## Usage example

```python
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

```

## Installation

- Clone git repository
```bash
git clone https://github.com/arud3nko/simple-proxifier.git
```
- Install dependencies
```bash
pip install -r requirements.txt
```

## Running tests
- Install dependencies
```bash
pip install -r tests/requirements.txt
```
- Run pytest
```bash
pytest tests
```

## Adding middlewares

You can simply inherit class from `ProxifierMiddleware` and add it to `Proxifier` using `add_pre_middleware()` and `add_post_middleware()`.

```python
class ProxifierMiddleware(ABC):
    """Base proxifier middleware class"""

    @abstractmethod
    async def __call__(self, request: Request_T, call_next: Callable[[], Coroutine[..., Request_T, ...]]):
        """Abstract __call__ method

        :param request: `Request` instance
        :param call_next: Instance of type `Callable`"""
        pass
```

## Adding handler

You can setup your own inherited from `RequestHandler` handler into `Proxifier`.`handler` property.

```python
class RequestHandler(ABC):
    """Base request handler"""
    @abstractmethod
    async def __call__(self, request: Request_T, *args, **kwargs):
        """Handle request"""
        pass

    @property
    @abstractmethod
    def session(self) -> Session_T:
        pass

    @session.setter
    @abstractmethod
    def session(self, v: Session_T):
        pass

```

## Authors

- [@arud3nko](https://www.github.com/arud3nko)


## License

[MIT](https://opensource.org/license/mit/)
