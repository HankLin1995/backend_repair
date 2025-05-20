from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    company_name: Optional[str] = None
    line_id: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    company_name: Optional[str] = None
    line_id: Optional[str] = None

class UserOut(UserBase):
    user_id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}

class UserWithProjectsOut(UserOut):
    projects: List["ProjectInfo"] = []

class ProjectInfo(BaseModel):
    project_id: int
    project_name: str
    role: str
    
    model_config = {"from_attributes": True}

# Update forward references
UserWithProjectsOut.model_rebuild()
