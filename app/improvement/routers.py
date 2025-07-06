from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.improvement import crud, schemas

router = APIRouter()

@router.post("/", response_model=schemas.ImprovementOut, status_code=status.HTTP_201_CREATED)
def create_improvement(
    improvement: schemas.ImprovementCreate,
    db: Session = Depends(get_db),
    x_current_user_id: str = Header(None)
):
    """Create a new improvement record"""
    if x_current_user_id:
        improvement.submitter_id = int(x_current_user_id)
    return crud.create_improvement(db=db, improvement=improvement)

@router.post("/by-unique-code/{unique_code}", response_model=schemas.ImprovementOut, status_code=status.HTTP_201_CREATED)
def create_improvement_by_unique_code(
    unique_code: str,
    improvement_data: schemas.ImprovementCreateByUniqueCode,
    db: Session = Depends(get_db)
):
    """Create a new improvement record using defect unique code
    
    This endpoint allows vendors to submit improvements without authentication,
    using only the defect's unique code.
    """
    # 根據唯一碼查找缺失
    from app.defect.models import Defect
    defect = db.query(Defect).filter(Defect.unique_code == unique_code).first()
    if not defect:
        raise HTTPException(status_code=404, detail="Defect not found with this unique code")
    
    # 創建完整的 ImprovementCreate 物件
    complete_improvement_data = schemas.ImprovementCreate(
        defect_id=defect.defect_id,
        content=improvement_data.content,
        submitter_id=improvement_data.submitter_id,
        improvement_date=improvement_data.improvement_date
    )
    
    # 如果有指定負責廠商，可以將其設為提交者
    if defect.responsible_vendor_id and not complete_improvement_data.submitter_id:
        from app.vendor.models import Vendor
        vendor = db.query(Vendor).filter(Vendor.vendor_id == defect.responsible_vendor_id).first()
        if vendor and hasattr(vendor, 'user_id') and vendor.user_id:
            complete_improvement_data.submitter_id = vendor.user_id
    
    return crud.create_improvement(db=db, improvement=complete_improvement_data)

@router.get("/{improvement_id}", response_model=schemas.ImprovementOut)
def read_improvement(
    improvement_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific improvement by ID"""
    db_improvement = crud.get_improvement(db, improvement_id=improvement_id)
    if db_improvement is None:
        raise HTTPException(status_code=404, detail="Improvement not found")
    return db_improvement

@router.get("/", response_model=List[schemas.ImprovementOut])
def read_improvements(
    skip: int = 0,
    limit: int = 100,
    defect_id: Optional[int] = None,
    submitter_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get a list of improvements with optional filtering"""
    improvements = crud.get_improvements(
        db, 
        skip=skip, 
        limit=limit, 
        defect_id=defect_id,
        submitter_id=submitter_id
    )
    return improvements

@router.put("/{improvement_id}", response_model=schemas.ImprovementOut)
def update_improvement(
    improvement_id: int,
    improvement: schemas.ImprovementUpdate,
    db: Session = Depends(get_db),
    x_current_user_id: str = Header(None)
):
    """Update an improvement"""
    db_improvement = crud.get_improvement(db, improvement_id=improvement_id)
    if db_improvement is None:
        raise HTTPException(status_code=404, detail="Improvement not found")
    
    # Only allow the submitter to update their own improvement
    if x_current_user_id and db_improvement.submitter_id != int(x_current_user_id):
        raise HTTPException(status_code=403, detail="Not authorized to update this improvement")
    
    return crud.update_improvement(db=db, improvement_id=improvement_id, improvement=improvement)

@router.delete("/{improvement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_improvement(
    improvement_id: int,
    db: Session = Depends(get_db),
    x_current_user_id: str = Header(None)
):
    """Delete an improvement"""
    db_improvement = crud.get_improvement(db, improvement_id=improvement_id)
    if db_improvement is None:
        raise HTTPException(status_code=404, detail="Improvement not found")
    
    # Only allow the submitter to delete their own improvement
    if x_current_user_id and db_improvement.submitter_id != int(x_current_user_id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this improvement")
    
    crud.delete_improvement(db=db, improvement_id=improvement_id)
    return None

@router.get("/{improvement_id}/details", response_model=dict)
def read_improvement_with_details(
    improvement_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific improvement with detailed information"""
    improvement_details = crud.get_improvement_with_details(db, improvement_id=improvement_id)
    if improvement_details is None:
        raise HTTPException(status_code=404, detail="Improvement not found")
    return improvement_details
