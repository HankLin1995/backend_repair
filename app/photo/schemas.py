from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PhotoBase(BaseModel):
    related_type: str  # 'defect', 'improvement', 'confirmation'
    related_id: int
    description: Optional[str] = None
    image_url: str

class PhotoCreate(PhotoBase):
    pass

class PhotoUpload(BaseModel):
    related_type: str = Field(description="Type of related form ('defect', 'improvement', 'confirmation')")
    related_id: int
    description: Optional[str] = None

class PhotoUpdate(BaseModel):
    description: Optional[str] = None
    image_url: Optional[str] = None

class PhotoOut(PhotoBase):
    photo_id: int
    created_at: datetime
    
    model_config = {"from_attributes": True}
    
class PhotoResponse(PhotoOut):
    """Response model with full URL for frontend display"""
    full_url: str = Field(description="Full URL to access the photo")
    
    model_config = {"from_attributes": True}
