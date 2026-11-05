from pydantic import BaseModel


class CustomResponse(BaseModel):
    message: str
    error: str | None = None
