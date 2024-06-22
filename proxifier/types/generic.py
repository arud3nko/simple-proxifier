from typing import Type, TypeVar, Callable, Coroutine, Any

Request_T = TypeVar("Request_T")
"""Generic request type to avoid concrete libraries dependencies"""
Response_T = TypeVar("Response_T")
"""Generic response type to avoid concrete libraries dependencies"""
Session_T = TypeVar("Session_T")
"""Generic session type to avoid concrete libraries dependencies"""
CallNext_T: Type = Callable[[Request_T], Coroutine[Any, Request_T, Request_T]]
