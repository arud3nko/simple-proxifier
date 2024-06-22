from __future__ import annotations

from abc import ABC, abstractmethod

from ..types.generic import Request_T, CallNext_T


class ProxifierMiddleware(ABC):
    """Base proxifier middleware class"""

    @abstractmethod
    async def __call__(self,
                       request: Request_T, call_next: CallNext_T) -> Request_T:
        """Abstract __call__ method

        :param request: `Request` instance
        :param call_next: Instance of type `Callable`"""
        pass
