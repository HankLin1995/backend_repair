from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.photo import crud, schemas
from app.utils import check_exists
from app.defect.models import Defect

router = APIRouter()

@router.post("/", response_model=schemas.PhotoOut, status_code=status.HTTP_201_CREATED)
def create_photo(photo: schemas.PhotoCreate, db: Session = Depends(get_db)):
    """Create a new photo"""
    # Check if defect exists
    check_exists(db, Defect, photo.defect_form_id, "defect_id")
    
    return crud.create_photo(db=db, photo=photo)

@router.get("/", response_model=List[schemas.PhotoOut])
def read_photos(
    defect_id: Optional[int] = None,
    photo_type: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get a list of photos with pagination and optional filtering"""
    if defect_id:
        # Check if defect exists
        check_exists(db, Defect, defect_id, "defect_id")
        
        if photo_type:
            return crud.get_photos_by_type(db, defect_id=defect_id, photo_type=photo_type)
        else:
            return crud.get_photos_by_defect(db, defect_id=defect_id)
    else:
        return crud.get_photos(db, skip=skip, limit=limit)

@router.get("/{photo_id}", response_model=schemas.PhotoOut)
def read_photo(photo_id: int, db: Session = Depends(get_db)):
    """Get a specific photo by ID"""
    db_photo = crud.get_photo(db, photo_id=photo_id)
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return db_photo

@router.put("/{photo_id}", response_model=schemas.PhotoOut)
def update_photo(
    photo_id: int, photo: schemas.PhotoUpdate, db: Session = Depends(get_db)
):
    """Update a photo"""
    db_photo = crud.update_photo(db, photo_id=photo_id, photo=photo)
    if db_photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    return db_photo

@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_photo(photo_id: int, db: Session = Depends(get_db)):
    """Delete a photo"""
    success = crud.delete_photo(db, photo_id=photo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Photo not found")
    return None
