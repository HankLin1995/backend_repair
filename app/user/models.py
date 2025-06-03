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
    avatar_path = Column(String, default="static/avatar/default.png")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    # 註解掉與 Permission 的關聯，因為 Permission 模型中對應的關聯已被註解
    # permissions = relationship("Permission", back_populates="user")
    submitted_defects = relationship("Defect", foreign_keys="Defect.submitted_id", back_populates="submitter")
    submitted_improvements = relationship("Improvement", foreign_keys="Improvement.submitter_id", back_populates="submitter")
    confirmations = relationship("Confirmation", foreign_keys="Confirmation.confirmer_id", back_populates="confirmer")
