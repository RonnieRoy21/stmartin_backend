from pydantic import BaseModel


class CounsellorModel(BaseModel):
    id: str
    name: str
    phone_number: str
    email: str
    role: str
