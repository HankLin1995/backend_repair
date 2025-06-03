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
