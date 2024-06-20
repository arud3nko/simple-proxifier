from __future__ import annotations

from abc import ABC, abstractmethod

from typing import TYPE_CHECKING, TypeVar, Callable

if TYPE_CHECKING:
    T = TypeVar("T")


class ProxifierMiddleware(ABC):
    """Base proxifier middleware class"""

    @abstractmethod
    def __call__(self, request: T, call_next: Callable):
        """Abstract __call__ method

        :param request: `Request` instance
        :param call_next: Instance of type `Callable`"""
        pass
