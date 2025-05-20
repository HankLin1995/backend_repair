from pydantic import BaseModel
from typing import Optional

class DefectMarkBase(BaseModel):
    defect_form_id: int
    base_map_id: int
    coordinate_x: float
    coordinate_y: float
    scale: float

class DefectMarkCreate(DefectMarkBase):
    pass

class DefectMarkUpdate(BaseModel):
    coordinate_x: Optional[float] = None
    coordinate_y: Optional[float] = None
    scale: Optional[float] = None

class DefectMarkOut(DefectMarkBase):
    defect_mark_id: int
    
    model_config = {"from_attributes": True}

class DefectMarkWithDetailsOut(DefectMarkOut):
    defect_description: str
    map_name: str
    
    model_config = {"from_attributes": True}
