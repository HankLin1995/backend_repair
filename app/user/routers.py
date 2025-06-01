from fastapi import APIRouter, Depends, HTTPException, status, Query, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
from pathlib import Path

from app.database import get_db
from app.user import crud, schemas
from app.utils import paginate_query

router = APIRouter()

@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if user with the same LINE ID already exists
    if user.line_id:
        db_user = crud.get_user_by_line_id(db, line_id=user.line_id)
        if db_user:
            raise HTTPException(
                status_code=400,
                detail="User with this LINE ID already exists"
            )
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.UserOut])
def read_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get a list of users with pagination"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=schemas.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/line/{line_id}", response_model=schemas.UserOut)
def read_user_by_line_id(line_id: str, db: Session = Depends(get_db)):
    """Get a specific user by LINE ID"""
    db_user = crud.get_user_by_line_id(db, line_id=line_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/{user_id}/projects", response_model=schemas.UserWithProjectsOut)
def read_user_with_projects(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user with their projects and roles"""
    user_data = crud.get_user_with_projects(db, user_id=user_id)
    if user_data is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data

@router.put("/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)
):
    """Update a user"""
    db_user = crud.update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user"""
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None

@router.post("/{user_id}/avatar", response_model=schemas.UserOut)
def upload_avatar(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a user avatar"""
    # 檢查使用者是否存在
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 確保目錄存在
    avatar_dir = Path("static/avatar")
    avatar_dir.mkdir(parents=True, exist_ok=True)
    
    # 建立檔案名稱 (使用使用者 ID)
    file_extension = os.path.splitext(file.filename)[1] if file.filename else ".png"
    avatar_filename = f"user_{user_id}{file_extension}"
    avatar_path = f"static/avatar/{avatar_filename}"
    
    # 儲存檔案
    with open(avatar_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 更新使用者的頭像路徑
    user_update = schemas.UserUpdate(avatar_path=avatar_path)
    updated_user = crud.update_user(db, user_id=user_id, user=user_update)
    
    return updated_user
