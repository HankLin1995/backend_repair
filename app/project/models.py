from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid

class Project(Base):
    __tablename__ = "projects"
    
    project_id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    image_path = Column(String, default="static/project/default.png")
    unique_code = Column(String, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    
    # Relationships
    permissions = relationship("Permission", back_populates="project")
    base_maps = relationship("BaseMap", back_populates="project")
    defects = relationship("Defect", back_populates="project")
    vendors = relationship("Vendor", back_populates="project", cascade="all, delete-orphan")
    defect_categories = relationship("DefectCategory", back_populates="project", cascade="all, delete-orphan")
