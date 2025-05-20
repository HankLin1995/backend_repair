from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

def check_exists(db: Session, model, id_value: int, id_field_name: str = "id"):
    """
    Check if an entity with the given ID exists in the database.
    Raises an HTTPException with 404 status if not found.
    """
    entity = db.query(model).filter(getattr(model, id_field_name) == id_value).first()
    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} with ID {id_value} not found"
        )
    return entity

def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    """Format datetime to ISO format string or return None"""
    if dt:
        return dt.isoformat()
    return None

def get_current_time() -> datetime:
    """Get current UTC time"""
    return datetime.utcnow()

def paginate_query(query, page: int = 1, page_size: int = 10):
    """
    Paginate a SQLAlchemy query
    """
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10
    
    # Calculate skip and limit
    skip = (page - 1) * page_size
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    items = query.offset(skip).limit(page_size).all()
    
    # Calculate total pages
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }
