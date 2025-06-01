from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ProjectBase(BaseModel):
    project_name: str

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    project_name: Optional[str] = None

class ProjectOut(ProjectBase):
    project_id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}

class ProjectWithCountsOut(ProjectOut):
    base_map_count: int
    defect_count: int
    user_count: int

class UserRoleOut(BaseModel):
    email: str
    role: str
    
    model_config = {"from_attributes": True}

class ProjectWithUsersOut(BaseModel):
    project_id: int
    project_name: str
    user_roles: List[UserRoleOut]
    
    model_config = {"from_attributes": True}

