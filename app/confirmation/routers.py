from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.confirmation import crud, schemas

router = APIRouter()

@router.post("/", response_model=schemas.ConfirmationOut, status_code=status.HTTP_201_CREATED)
def create_confirmation(
    confirmation: schemas.ConfirmationCreate,
    db: Session = Depends(get_db),
    x_current_user_id: str = Header(None)
):
    """Create a new confirmation record"""
    if x_current_user_id:
        confirmation.confirmer_id = int(x_current_user_id)
    return crud.create_confirmation(db=db, confirmation=confirmation)

@router.get("/{confirmation_id}", response_model=schemas.ConfirmationOut)
def read_confirmation(
    confirmation_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific confirmation by ID"""
    db_confirmation = crud.get_confirmation(db, confirmation_id=confirmation_id)
    if db_confirmation is None:
        raise HTTPException(status_code=404, detail="Confirmation not found")
    return db_confirmation

@router.get("/", response_model=List[schemas.ConfirmationOut])
def read_confirmations(
    skip: int = 0,
    limit: int = 100,
    improvement_id: Optional[int] = None,
    confirmer_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get a list of confirmations with optional filtering"""
    confirmations = crud.get_confirmations(
        db, 
        skip=skip, 
        limit=limit, 
        improvement_id=improvement_id,
        confirmer_id=confirmer_id,
        status=status
    )
    return confirmations

@router.put("/{confirmation_id}", response_model=schemas.ConfirmationOut)
def update_confirmation(
    confirmation_id: int,
    confirmation: schemas.ConfirmationUpdate,
    db: Session = Depends(get_db),
    x_current_user_id: str = Header(None)
):
    """Update a confirmation"""
    db_confirmation = crud.get_confirmation(db, confirmation_id=confirmation_id)
    if db_confirmation is None:
        raise HTTPException(status_code=404, detail="Confirmation not found")
    
    # Only allow the confirmer to update their own confirmation
    if x_current_user_id and db_confirmation.confirmer_id != int(x_current_user_id):
        raise HTTPException(status_code=403, detail="Not authorized to update this confirmation")
    
    return crud.update_confirmation(db=db, confirmation_id=confirmation_id, confirmation=confirmation)

@router.delete("/{confirmation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_confirmation(
    confirmation_id: int,
    db: Session = Depends(get_db),
    x_current_user_id: str = Header(None)
):
    """Delete a confirmation"""
    db_confirmation = crud.get_confirmation(db, confirmation_id=confirmation_id)
    if db_confirmation is None:
        raise HTTPException(status_code=404, detail="Confirmation not found")
    
    # Only allow the confirmer to delete their own confirmation
    if x_current_user_id and db_confirmation.confirmer_id != int(x_current_user_id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this confirmation")
    
    crud.delete_confirmation(db=db, confirmation_id=confirmation_id)
    return None

@router.get("/{confirmation_id}/details")
def read_confirmation_with_details(
    confirmation_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific confirmation with detailed information"""
    confirmation_details = crud.get_confirmation_with_details(db, confirmation_id=confirmation_id)
    if confirmation_details is None:
        raise HTTPException(status_code=404, detail="Confirmation not found")
    
    # Add related objects to the response
    result = confirmation_details.copy()
    
    # Add confirmer details
    result["confirmer"] = {
        "user_id": confirmation_details["confirmer_id"],
        "name": confirmation_details["confirmer_name"]
    }
    
    # Add improvement details
    result["improvement"] = {
        "improvement_id": confirmation_details["improvement_id"],
        "content": confirmation_details["improvement_content"]
    }
    
    # Add defect details
    result["defect"] = {
        "description": confirmation_details["defect_description"]
    }
    
    return result
