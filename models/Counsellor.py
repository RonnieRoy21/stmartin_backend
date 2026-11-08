from pydantic import BaseModel


class CounsellorModel(BaseModel):
    id: str
    name: str
    phone_number: str
    email: str
    role: str

class CounsellorProfile(BaseModel):
    name: str
    phone_number: str
    email: str
    role: str

class LoginModel(BaseModel):
    email:str
    password:str

    