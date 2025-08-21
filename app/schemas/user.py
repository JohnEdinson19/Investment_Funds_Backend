from typing import Optional, Literal
from pydantic import BaseModel, EmailStr

Role = Literal["admin", "user"]

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    notification: Literal["email", "sms"] = "email"
    role: Role = "user"
    balance: float = 500_000

class UserPublic(BaseModel):
    id: str
    username: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    notification: Literal["email", "sms"]
    role: Role
    balance: float

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
