from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum


class Gender(str, Enum):
    male = "male"
    female = "female"

class Role(str, Enum):
    admin = "admin"
    user = "user"
    student = "student"

class User(BaseModel):
    id: Optional[UUID] = None 
    first_name: str
    last_name: str
    middle_name: Optional[str] = None 
    gender: Optional[Gender] = None    
    roles: List[Role]

class UserUpdateRequest(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str] 
    middle_name: Optional[str] 
    roles: Optional[List[Role]]
    