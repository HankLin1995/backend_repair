from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class DefectCategory(Base):
    __tablename__ = "defect_categories"
    
    defect_category_id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    category_name = Column(String, nullable=False)
    description = Column(Text)
    
    # Relationships
    project = relationship("Project", back_populates="defect_categories")
    defects = relationship("Defect", back_populates="category")
