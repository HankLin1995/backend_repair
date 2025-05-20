from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.defect_category import crud, schemas

router = APIRouter()

@router.post("/", response_model=schemas.DefectCategoryOut, status_code=status.HTTP_201_CREATED)
def create_defect_category(defect_category: schemas.DefectCategoryCreate, db: Session = Depends(get_db)):
    """Create a new defect category"""
    return crud.create_defect_category(db=db, defect_category=defect_category)

@router.get("/", response_model=List[schemas.DefectCategoryOut])
def read_defect_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get a list of defect categories with pagination"""
    defect_categories = crud.get_defect_categories(db, skip=skip, limit=limit)
    return defect_categories

@router.get("/with-counts", response_model=List[schemas.DefectCategoryWithCountOut])
def read_defect_categories_with_counts(db: Session = Depends(get_db)):
    """Get defect categories with defect counts"""
    return crud.get_defect_categories_with_counts(db)

@router.get("/{defect_category_id}", response_model=schemas.DefectCategoryOut)
def read_defect_category(defect_category_id: int, db: Session = Depends(get_db)):
    """Get a specific defect category by ID"""
    db_defect_category = crud.get_defect_category(db, defect_category_id=defect_category_id)
    if db_defect_category is None:
        raise HTTPException(status_code=404, detail="Defect category not found")
    return db_defect_category

@router.put("/{defect_category_id}", response_model=schemas.DefectCategoryOut)
def update_defect_category(
    defect_category_id: int, defect_category: schemas.DefectCategoryUpdate, db: Session = Depends(get_db)
):
    """Update a defect category"""
    db_defect_category = crud.update_defect_category(db, defect_category_id=defect_category_id, defect_category=defect_category)
    if db_defect_category is None:
        raise HTTPException(status_code=404, detail="Defect category not found")
    return db_defect_category

@router.delete("/{defect_category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_defect_category(defect_category_id: int, db: Session = Depends(get_db)):
    """Delete a defect category"""
    success = crud.delete_defect_category(db, defect_category_id=defect_category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Defect category not found")
    return None
