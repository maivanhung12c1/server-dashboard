class BaseAppError(Exception):
    """Base class for all application-level errors."""
    http_status: int = 500
    code: int = 500
    
    def __init__(self, msg: str = "Internal server error") -> None:
        self.msg = msg
        super().__init__(msg)
        
class NotFoundError(BaseAppError):
    http_status = 404
    code = 404
    
    def __init__(self, msg: str = "Resource not found") -> None:
        super().__init__(msg)

class ConflictError(BaseAppError):
    http_status = 409
    code = 409
    
    def __init__(self, msg: str = "Resource already exists") -> None:
        super().__init__(msg)
        
class BadRequestError(BaseAppError):
    http_status = 400
    code = 400
    
    def __init__(self, msg: str = "Bad request") -> None:
        super().__init__(msg)


class UnauthorizedError(BaseAppError):
    http_status = 401
    code = 401

    def __init__(self, msg: str = "Unauthorized") -> None:
        super().__init__(msg)
