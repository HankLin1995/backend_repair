from pydantic import BaseModel
from typing import Optional, List

class DefectCategoryBase(BaseModel):
    category_name: str
    description: Optional[str] = None

class DefectCategoryCreate(DefectCategoryBase):
    pass

class DefectCategoryUpdate(BaseModel):
    category_name: Optional[str] = None
    description: Optional[str] = None

class DefectCategoryOut(DefectCategoryBase):
    defect_category_id: int
    
    model_config = {"from_attributes": True}

class DefectCategoryWithCountOut(DefectCategoryOut):
    defect_count: int
