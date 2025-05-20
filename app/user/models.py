from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    line_id = Column(String)
    name = Column(String, nullable=False)
    email = Column(String)
    company_name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    permissions = relationship("Permission", back_populates="user")
    submitted_defects = relationship("Defect", foreign_keys="Defect.submitted_id", back_populates="submitter")
    confirmed_defects = relationship("Defect", foreign_keys="Defect.confirmer_id", back_populates="confirmer")
