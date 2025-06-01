from pydantic import BaseModel
from typing import Optional, List

class PermissionBase(BaseModel):
    project_id: int
    user_email: str
    user_role: str

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    user_role: str

class PermissionOut(PermissionBase):
    permission_id: int
    
    model_config = {"from_attributes": True}

class PermissionWithDetailsOut(PermissionOut):
    project_name: str
    user_name: str
    
    model_config = {"from_attributes": True}
