from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PhotoBase(BaseModel):
    defect_form_id: int
    description: Optional[str] = None
    photo_type: str
    image_url: str

class PhotoCreate(PhotoBase):
    pass

class PhotoUpdate(BaseModel):
    description: Optional[str] = None
    photo_type: Optional[str] = None
    image_url: Optional[str] = None

class PhotoOut(PhotoBase):
    photo_id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}
