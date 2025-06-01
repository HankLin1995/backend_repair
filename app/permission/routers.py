from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.permission import crud, schemas
from app.utils import check_exists
from app.project.models import Project
from app.user.models import User

router = APIRouter()

@router.post("/", response_model=schemas.PermissionOut, status_code=status.HTTP_201_CREATED)
def create_permission(permission: schemas.PermissionCreate, db: Session = Depends(get_db)):
    """Create a new permission"""
    # Check if project exists
    check_exists(db, Project, permission.project_id, "project_id")
    
    # Check if user exists
    user = db.query(User).filter(User.email == permission.user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with email {permission.user_email} not found")
    
    return crud.create_permission(db=db, permission=permission)

@router.get("/", response_model=List[schemas.PermissionWithDetailsOut])
def read_permissions(
    project_id: Optional[int] = None,
    user_email: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get a list of permissions with pagination and optional filtering"""
    if project_id:
        # Check if project exists
        check_exists(db, Project, project_id, "project_id")
    
    if user_email:
        # Check if user exists
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"User with email {user_email} not found")
    
    permissions = crud.get_permissions_with_details(
        db, project_id=project_id, user_email=user_email
    )
    
    # Apply pagination manually since we're using a custom query
    start = skip
    end = skip + limit
    return permissions[start:end]

@router.get("/{permission_id}", response_model=schemas.PermissionOut)
def read_permission(permission_id: int, db: Session = Depends(get_db)):
    """Get a specific permission by ID"""
    db_permission = crud.get_permission(db, permission_id=permission_id)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission

@router.put("/{permission_id}", response_model=schemas.PermissionOut)
def update_permission(
    permission_id: int, permission: schemas.PermissionUpdate, db: Session = Depends(get_db)
):
    """Update a permission"""
    db_permission = crud.update_permission(db, permission_id=permission_id, permission=permission)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission

@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    """Delete a permission"""
    success = crud.delete_permission(db, permission_id=permission_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permission not found")
    return None
