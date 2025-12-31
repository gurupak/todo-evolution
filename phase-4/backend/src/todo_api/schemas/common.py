"""Common schemas used across the API."""

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Individual field error detail."""

    field: str
    message: str
    code: str = "validation_error"


class ErrorResponse(BaseModel):
    """Standard error response format."""

    detail: str
    errors: list[ErrorDetail] | None = None


class DeleteResponse(BaseModel):
    """Response for successful deletion."""

    message: str
    id: str
