from fastapi import HTTPException, status


class NotFoundError(HTTPException):
    def __init__(self, detail: str = "Not Found", **kwargs):
        """Returns HTTP 404"""
        super().__init__(status.HTTP_404_NOT_FOUND, detail=detail, **kwargs)


class UnauthenticatedRequest(HTTPException):
    def __init__(self, detail: str = "Forbidden", **kwargs):
        """Returns HTTP 403"""
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail, **kwargs)


class UnauthorizedRequest(HTTPException):
    def __init__(self, detail: str = "Unauthorized", **kwargs):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=detail, **kwargs
        )


class InternalError(HTTPException):
    def __init__(self, detail: str = "Internal Server Error", **kwargs):
        """Returns HTTP 500"""
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail, **kwargs)
