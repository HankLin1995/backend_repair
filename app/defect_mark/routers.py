from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.defect_mark import crud, schemas
from app.utils import check_exists
from app.defect.models import Defect
from app.base_map.models import BaseMap

router = APIRouter()

@router.post("/", response_model=schemas.DefectMarkOut, status_code=status.HTTP_201_CREATED)
def create_defect_mark(defect_mark: schemas.DefectMarkCreate, db: Session = Depends(get_db)):
    """Create a new defect mark"""
    # Check if defect exists
    check_exists(db, Defect, defect_mark.defect_form_id, "defect_id")
    
    # Check if base map exists
    check_exists(db, BaseMap, defect_mark.base_map_id, "base_map_id")
    
    return crud.create_defect_mark(db=db, defect_mark=defect_mark)

@router.get("/", response_model=List[schemas.DefectMarkOut])
def read_defect_marks(
    defect_id: Optional[int] = None,
    base_map_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get a list of defect marks with pagination and optional filtering"""
    if defect_id:
        # Check if defect exists
        check_exists(db, Defect, defect_id, "defect_id")
        return crud.get_defect_marks_by_defect(db, defect_id=defect_id)
    elif base_map_id:
        # Check if base map exists
        check_exists(db, BaseMap, base_map_id, "base_map_id")
        return crud.get_defect_marks_by_base_map(db, base_map_id=base_map_id)
    else:
        return crud.get_defect_marks(db, skip=skip, limit=limit)

@router.get("/with-details", response_model=List[schemas.DefectMarkWithDetailsOut])
def read_defect_marks_with_details(
    base_map_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get defect marks with defect and base map details"""
    if base_map_id:
        # Check if base map exists
        check_exists(db, BaseMap, base_map_id, "base_map_id")
    
    return crud.get_defect_marks_with_details(db, base_map_id=base_map_id)

@router.get("/{defect_mark_id}", response_model=schemas.DefectMarkOut)
def read_defect_mark(defect_mark_id: int, db: Session = Depends(get_db)):
    """Get a specific defect mark by ID"""
    db_defect_mark = crud.get_defect_mark(db, defect_mark_id=defect_mark_id)
    if db_defect_mark is None:
        raise HTTPException(status_code=404, detail="Defect mark not found")
    return db_defect_mark

@router.put("/{defect_mark_id}", response_model=schemas.DefectMarkOut)
def update_defect_mark(
    defect_mark_id: int, defect_mark: schemas.DefectMarkUpdate, db: Session = Depends(get_db)
):
    """Update a defect mark"""
    db_defect_mark = crud.update_defect_mark(db, defect_mark_id=defect_mark_id, defect_mark=defect_mark)
    if db_defect_mark is None:
        raise HTTPException(status_code=404, detail="Defect mark not found")
    return db_defect_mark

@router.delete("/{defect_mark_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_defect_mark(defect_mark_id: int, db: Session = Depends(get_db)):
    """Delete a defect mark"""
    success = crud.delete_defect_mark(db, defect_mark_id=defect_mark_id)
    if not success:
        raise HTTPException(status_code=404, detail="Defect mark not found")
    return None
