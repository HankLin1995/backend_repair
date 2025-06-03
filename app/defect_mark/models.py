from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class DefectMark(Base):
    __tablename__ = "defect_marks"
    
    defect_mark_id = Column(Integer, primary_key=True, index=True)
    defect_id = Column(Integer, ForeignKey("defects.defect_id", ondelete="CASCADE"))
    base_map_id = Column(Integer, ForeignKey("base_maps.base_map_id", ondelete="CASCADE"))
    coordinate_x = Column(Float, nullable=False)
    coordinate_y = Column(Float, nullable=False)
    scale = Column(Float, nullable=False)
    
    # Relationships
    defect = relationship("Defect", back_populates="defect_marks")
    base_map = relationship("BaseMap", back_populates="defect_marks")
