# schemas.py
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class Computer(BaseModel):
    name: str
    dnsname: Optional[str]
    location: Optional[str]
    cpu: Optional[str]
    ram: Optional[str]
    ipv4: Optional[str]
    mac: Optional[str]


class CreateComputer(Computer):
    created_at: Optional[datetime]
    pass


class UpdateComputer(CreateComputer):
    updated_at: Optional[datetime]
    
    class Config:
        orm_mode = True


class CreateLog(BaseModel):
    message: str
    id_logflag: Optional[int] = 0
    id_computer: Optional[int] = 0
    created_at: Optional[str]


class RespondLog(BaseModel):
    message: str
    created_at: str

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    email: EmailStr
    password: str
    created_at: Optional[datetime]


class RespondUser(BaseModel):
    email: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]


class CreateOwner(BaseModel):
    firstname: str
    lastname: str
    department: Optional[str]
    created_at: Optional[datetime]


class UpdateOwner(CreateOwner):
    new_firstname: str
    new_lastname: str
    updated_at: Optional[datetime]


class RespondOwner(BaseModel):
    firstname: str
    lastname: str
    department: str
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class RespondLogToComp(BaseModel):
    message: Optional[str]
    id_logflag: Optional[int]

    class Config:
        orm_mode = True


class RespondOwnerToComp(CreateOwner):
    id: int

    class Config:
        orm_mode = True


class RespondComputer(Computer):
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    owner: RespondOwnerToComp

    class Config:
        orm_mode = True
