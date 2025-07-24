# app/schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_verified: bool

    class Config:
        from_attributes = True  # for Pydantic v2

        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        from_attributes = True 
