from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.project import crud, schemas
from app.utils import paginate_query

router = APIRouter()

@router.post("/", response_model=schemas.ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    """Create a new project"""
    return crud.create_project(db=db, project=project)

@router.get("/", response_model=List[schemas.ProjectOut])
def read_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get a list of projects with pagination"""
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects

@router.get("/{project_id}", response_model=schemas.ProjectOut)
def read_project(project_id: int, db: Session = Depends(get_db)):
    """Get a specific project by ID"""
    db_project = crud.get_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.get("/{project_id}/with-counts", response_model=schemas.ProjectWithCountsOut)
def read_project_with_counts(project_id: int, db: Session = Depends(get_db)):
    """Get a specific project with counts of related entities"""
    project_data = crud.get_project_with_counts(db, project_id=project_id)
    if project_data is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_data

@router.get("/{project_id}/with-roles", response_model=schemas.ProjectWithUsersOut)
def read_project_roles(project_id: int, db: Session = Depends(get_db)):
    """獲取專案中存在的角色"""
    project_roles = crud.get_project_roles(db, project_id=project_id)
    if project_roles is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_roles

@router.put("/{project_id}", response_model=schemas.ProjectOut)
def update_project(
    project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)
):
    """Update a project"""
    db_project = crud.update_project(db, project_id=project_id, project=project)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete a project"""
    success = crud.delete_project(db, project_id=project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return None
