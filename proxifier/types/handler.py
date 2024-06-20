from abc import ABC, abstractmethod

from ..types.generic import Request_T, Session_T


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
