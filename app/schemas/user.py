from dataclasses import Field
from datetime import datetime
from typing import List

from pydantic import BaseModel,EmailStr
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone_number: str
    class Config:
        orm_mode = True
class UserOut(BaseModel):
    email: EmailStr
    name: str
    class Config:
        orm_mode = True
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    class Config:
        orm_mode = True
class UserRoles(BaseModel):
    id: int
    id_role:int

