from pydantic import BaseModel
from typing import Optional, List

class BaseMapBase(BaseModel):
    project_id: int
    map_name: str
    file_path: str

class BaseMapCreate(BaseMapBase):
    pass

class BaseMapUpdate(BaseModel):
    map_name: Optional[str] = None
    file_path: Optional[str] = None

class BaseMapOut(BaseMapBase):
    base_map_id: int
    
    model_config = {"from_attributes": True}

class BaseMapWithDefectCountOut(BaseMapOut):
    defect_count: int
