from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Union

class DefectBase(BaseModel):
    project_id: int
    submitted_id: int
    defect_category_id: Optional[int] = None
    defect_description: str
    assigned_vendor_id: Optional[int] = None
    repair_description: Optional[str] = None
    expected_completion_date: Optional[datetime] = None
    repair_completed_at: Optional[datetime] = None
    confirmation_status: Optional[str] = None
    confirmation_time: Optional[datetime] = None
    confirmer_id: Optional[int] = None

class DefectCreate(DefectBase):
    pass

class DefectUpdate(BaseModel):
    defect_category_id: Optional[int] = None
    defect_description: Optional[str] = None
    assigned_vendor_id: Optional[int] = None
    repair_description: Optional[str] = None
    expected_completion_date: Optional[datetime] = None
    repair_completed_at: Optional[datetime] = None
    confirmation_status: Optional[str] = None
    confirmation_time: Optional[datetime] = None
    confirmer_id: Optional[int] = None

class DefectOut(DefectBase):
    defect_id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}

class DefectDetailOut(DefectOut):
    project_name: str
    submitter_name: str
    category_name: Optional[str] = None
    vendor_name: Optional[str] = None
    confirmer_name: Optional[str] = None
    
    model_config = {"from_attributes": True}

class DefectWithMarksAndPhotosOut(DefectDetailOut):
    defect_marks: List["DefectMarkOut"] = []
    photos: List["PhotoOut"] = []

# Forward references for nested schemas
class DefectMarkBase(BaseModel):
    defect_form_id: int
    base_map_id: int
    coordinate_x: float
    coordinate_y: float
    scale: float

class DefectMarkOut(DefectMarkBase):
    defect_mark_id: int
    
    model_config = {"from_attributes": True}

class PhotoBase(BaseModel):
    defect_form_id: int
    description: Optional[str] = None
    photo_type: str
    image_url: str

class PhotoOut(PhotoBase):
    photo_id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}

# Update forward references
DefectWithMarksAndPhotosOut.model_rebuild()
