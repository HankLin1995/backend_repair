from sqlalchemy.orm import Session
from typing import List, Optional

from app.photo.models import Photo
from app.photo.schemas import PhotoCreate, PhotoUpdate

def get_photo(db: Session, photo_id: int) -> Optional[Photo]:
    """Get a single photo by ID"""
    return db.query(Photo).filter(Photo.photo_id == photo_id).first()

def get_photos(db: Session, skip: int = 0, limit: int = 100) -> List[Photo]:
    """Get a list of photos with pagination"""
    return db.query(Photo).offset(skip).limit(limit).all()

def get_photos_by_related(db: Session, related_type: str, related_id: int) -> List[Photo]:
    """Get all photos for a specific related item"""
    return db.query(Photo).filter(
        Photo.related_type == related_type,
        Photo.related_id == related_id
    ).all()

def create_photo(db: Session, photo: PhotoCreate) -> Photo:
    """Create a new photo"""
    db_photo = Photo(
        related_type=photo.related_type,
        related_id=photo.related_id,
        description=photo.description,
        image_url=photo.image_url
    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo

def update_photo(db: Session, photo_id: int, photo: PhotoUpdate) -> Optional[Photo]:
    """Update an existing photo"""
    db_photo = get_photo(db, photo_id)
    if not db_photo:
        return None
    
    update_data = photo.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_photo, key, value)
    
    db.commit()
    db.refresh(db_photo)
    return db_photo

def delete_photo(db: Session, photo_id: int) -> bool:
    """Delete a photo"""
    db_photo = get_photo(db, photo_id)
    if not db_photo:
        return False
    
    db.delete(db_photo)
    db.commit()
    return True
