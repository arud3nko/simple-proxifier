from __future__ import annotations

from abc import ABC, abstractmethod

from typing import Callable

from ..types.generic import Request_T


class ProxifierMiddleware(ABC):
    """Base proxifier middleware class"""

    @abstractmethod
    def __call__(self, request: Request_T, call_next: Callable):
        """Abstract __call__ method

        :param request: `Request` instance
        :param call_next: Instance of type `Callable`"""
        pass
