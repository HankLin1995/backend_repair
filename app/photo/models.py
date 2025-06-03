from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Photo(Base):
    __tablename__ = "photos"
    
    photo_id = Column(Integer, primary_key=True, index=True)
    related_type = Column(String, nullable=False)  # '缺失單', '改善單', '確認單'
    related_id = Column(Integer, nullable=False)
    description = Column(Text)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
