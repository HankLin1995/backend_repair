from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Union
from app.improvement.schemas import ImprovementOut
from app.vendor.schemas import VendorOut
from app.defect_category.schemas import DefectCategoryOut
from app.user.schemas import UserOut
from app.project.schemas import ProjectOut

class DefectBase(BaseModel):
    project_id: int
    submitted_id: int
    defect_category_id: Optional[int] = None
    defect_description: str
    assigned_vendor_id: Optional[int] = None
    repair_description: Optional[str] = None
    expected_completion_day: Optional[date] = None
    # responsible_vendor_id: Optional[int] = None
    previous_defect_id: Optional[int] = None
    status: Optional[str] = None  # 等待中、改善中、待確認、已完成、退件

class DefectCreate(DefectBase):
    pass
    # confirmer_id: Optional[int] = None

class DefectUpdate(BaseModel):
    defect_category_id: Optional[int] = None
    defect_description: Optional[str] = None
    assigned_vendor_id: Optional[int] = None
    repair_description: Optional[str] = None
    expected_completion_day: Optional[date] = None
    responsible_vendor_id: Optional[int] = None
    status: Optional[str] = None
    confirmer_id: Optional[int] = None

class DefectOut(DefectBase):
    defect_id: int
    confirmer_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}

class DefectDetailOut(DefectOut):
    project_name: str
    submitter_name: str
    category_name: Optional[str] = None
    assigned_vendor_name: Optional[str] = None
    responsible_vendor_name: Optional[str] = None
    
    model_config = {"from_attributes": True}

class DefectWithMarksAndPhotosOut(DefectDetailOut):
    defect_marks: List["DefectMarkOut"] = []
    photos: List["PhotoOut"] = []
    improvements: List[ImprovementOut] = []

# Forward references for nested schemas
class DefectMarkBase(BaseModel):
    defect_id: int  # Changed from defect_form_id to defect_id
    base_map_id: int
    coordinate_x: float
    coordinate_y: float
    scale: float

class DefectMarkOut(DefectMarkBase):
    defect_mark_id: int
    
    model_config = {"from_attributes": True}

class PhotoBase(BaseModel):
    related_type: str  # '缺失單', '改善單', '確認單'
    related_id: int
    description: Optional[str] = None
    image_url: str

class PhotoOut(PhotoBase):
    photo_id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}

class DefectFullDetailOut(DefectWithMarksAndPhotosOut):
    """完整的缺失詳細資訊，包含所有相關實體的完整資料"""
    defect_category: Optional[Dict[str, Any]] = None
    assigned_vendor: Optional[Dict[str, Any]] = None
    responsible_vendor: Optional[Dict[str, Any]] = None
    submitter: Optional[Dict[str, Any]] = None
    # confirmer: Optional[Dict[str, Any]] = None
    project: Optional[Dict[str, Any]] = None
    
    model_config = {"from_attributes": True}

# Update forward references
DefectWithMarksAndPhotosOut.model_rebuild()
