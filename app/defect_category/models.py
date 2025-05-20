from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base

class DefectCategory(Base):
    __tablename__ = "defect_categories"
    
    defect_category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, nullable=False)
    description = Column(Text)
    
    # Relationships
    defects = relationship("Defect", back_populates="category")
