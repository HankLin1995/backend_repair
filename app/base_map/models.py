from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class BaseMap(Base):
    __tablename__ = "base_maps"
    
    base_map_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.project_id", ondelete="CASCADE"))
    map_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    
    # Relationships
    project = relationship("Project", back_populates="base_maps")
    defect_marks = relationship("DefectMark", back_populates="base_map")
