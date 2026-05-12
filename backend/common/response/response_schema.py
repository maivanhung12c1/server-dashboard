from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseModel(BaseModel, Generic[T]):
    """Standard API response envelope: {code, msg, data}."""
    code: int = 200
    msg: str = "OK"
    data: T | None = None
    
class ResponseBase:
    @staticmethod
    def success(data=None, msg: str = "OK") -> ResponseModel:
        return ResponseModel(code=200, msg=msg, data=data)
    
    @staticmethod
    def fail(code: int = 400, msg: str = "Bad Request") -> ResponseModel:
        return ResponseModel(code=code, msg=msg, data=None)
    
response_base = ResponseBase()