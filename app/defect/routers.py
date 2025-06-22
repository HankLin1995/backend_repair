from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Union

from app.database import get_db
from app.defect import crud, schemas
from app.defect.models import Defect
from app.utils import check_exists
from app.project.models import Project
from app.user.models import User
from app.defect_category.models import DefectCategory
from app.vendor.models import Vendor

router = APIRouter()

@router.post("/", response_model=schemas.DefectOut, status_code=status.HTTP_201_CREATED)
def create_defect(defect: schemas.DefectCreate, db: Session = Depends(get_db)):
    """Create a new defect"""
    # Check if project exists
    check_exists(db, Project, defect.project_id, "project_id")
    
    # Check if submitter exists
    check_exists(db, User, defect.submitted_id, "user_id")
    
    # Check if category exists if provided
    if defect.defect_category_id:
        check_exists(db, DefectCategory, defect.defect_category_id, "defect_category_id")
    
    # Check if vendor exists if provided
    if defect.assigned_vendor_id:
        check_exists(db, Vendor, defect.assigned_vendor_id, "vendor_id")
    
    # Check if confirmer exists if provided
    # if defect.confirmer_id:
    #     check_exists(db, User, defect.confirmer_id, "user_id")
    
    return crud.create_defect(db=db, defect=defect)

@router.get("/", response_model=List[schemas.DefectDetailOut])
def read_defects(
    project_id: Optional[int] = None,
    submitted_id: Optional[int] = None,
    defect_category_id: Optional[int] = None,
    assigned_vendor_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(1000),
    db: Session = Depends(get_db)
):
    """Get a list of defects with pagination and optional filtering"""
    defects = crud.get_defects_with_details(
        db, 
        skip=skip, 
        limit=limit,
        project_id=project_id,
        submitted_id=submitted_id,
        defect_category_id=defect_category_id,
        assigned_vendor_id=assigned_vendor_id,
        status=status
    )
    return defects

@router.get("/stats", response_model=dict)
def read_defect_stats(
    project_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get defect statistics"""
    if project_id:
        # Check if project exists
        check_exists(db, Project, project_id, "project_id")
    
    return crud.get_defect_stats(db, project_id=project_id)

@router.get("/unique_code/{unique_code}", response_model=schemas.DefectOut)
def read_defect_by_unique_code(
    unique_code: str,
    db: Session = Depends(get_db)
):
    """Get a specific defect by unique code"""
    return crud.get_defect_by_unique_code(db, unique_code=unique_code)


@router.get("/{defect_id}", response_model=Union[schemas.DefectDetailOut, schemas.DefectWithMarksAndPhotosOut, schemas.DefectFullDetailOut])
def read_defect(
    defect_id: int, 
    with_marks: bool = False,
    with_photos: bool = False,
    with_improvements: bool = False,
    with_full_related: bool = False,
    db: Session = Depends(get_db)
):
    """Get a specific defect by ID with details
    
    - with_marks: 是否包含標記資料
    - with_photos: 是否包含照片資料
    - with_improvements: 是否包含改善資料
    - with_full_related: 是否包含完整關聯實體資料
    """
    # 確保布林參數正確轉換
    with_marks = with_marks in [True, "True", "true", "1", "yes", "on"]
    with_photos = with_photos in [True, "True", "true", "1", "yes", "on"]
    with_improvements = with_improvements in [True, "True", "true", "1", "yes", "on"]
    with_full_related = with_full_related in [True, "True", "true", "1", "yes", "on"]
    
    defect_data = crud.get_defect_details(
        db, 
        defect_id=defect_id,
        with_marks=with_marks,
        with_photos=with_photos,
        with_improvements=with_improvements,
        with_full_related=with_full_related
    )
    if defect_data is None:
        raise HTTPException(status_code=404, detail="Defect not found")
    return defect_data

# 保留舊端點以向後相容，但標記為棄用
@router.get("/{defect_id}/full", response_model=schemas.DefectFullDetailOut, deprecated=True)
def read_defect_full(defect_id: int, db: Session = Depends(get_db)):
    """[已棄用] 請改用 /{defect_id}?with_full_related=true 端點"""
    defect_data = crud.get_defect_details(db, defect_id=defect_id, with_marks=True, with_photos=True, with_improvements=True, with_full_related=True)
    if defect_data is None:
        raise HTTPException(status_code=404, detail="Defect not found")
    return defect_data

@router.put("/{defect_id}", response_model=schemas.DefectOut)
def update_defect(
    defect_id: int, defect: schemas.DefectUpdate, db: Session = Depends(get_db)
):
    """Update a defect"""
    # Check if defect exists
    check_exists(db, Defect, defect_id, "defect_id")
    
    # Check if category exists if provided
    if defect.defect_category_id:
        check_exists(db, DefectCategory, defect.defect_category_id, "defect_category_id")
    
    # Check if vendor exists if provided
    if defect.assigned_vendor_id:
        check_exists(db, Vendor, defect.assigned_vendor_id, "vendor_id")
    
    # Check if confirmer exists if provided
    # if defect.confirmer_id:
    #     check_exists(db, User, defect.confirmer_id, "user_id")
    
    db_defect = crud.update_defect(db, defect_id=defect_id, defect=defect)
    if db_defect is None:
        raise HTTPException(status_code=404, detail="Defect not found")
    return db_defect

@router.delete("/{defect_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_defect(defect_id: int, db: Session = Depends(get_db)):
    """Delete a defect"""
    success = crud.delete_defect(db, defect_id=defect_id)
    if not success:
        raise HTTPException(status_code=404, detail="Defect not found")
    return None
