from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.base_map import crud, schemas
from app.utils import check_exists
from app.project.models import Project

router = APIRouter()

@router.post("/", response_model=schemas.BaseMapOut, status_code=status.HTTP_201_CREATED)
def create_base_map(base_map: schemas.BaseMapCreate, db: Session = Depends(get_db)):
    """Create a new base map"""
    # Check if project exists
    check_exists(db, Project, base_map.project_id, "project_id")
    
    return crud.create_base_map(db=db, base_map=base_map)

@router.get("/", response_model=List[schemas.BaseMapOut])
def read_base_maps(
    project_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get a list of base maps with pagination and optional filtering by project"""
    if project_id:
        # Check if project exists
        check_exists(db, Project, project_id, "project_id")
        return crud.get_base_maps_by_project(db, project_id=project_id)
    else:
        return crud.get_base_maps(db, skip=skip, limit=limit)

@router.get("/project/{project_id}/with-counts", response_model=List[schemas.BaseMapWithDefectCountOut])
def read_base_maps_with_defect_counts(project_id: int, db: Session = Depends(get_db)):
    """Get base maps with defect counts for a project"""
    # Check if project exists
    check_exists(db, Project, project_id, "project_id")
    
    return crud.get_base_maps_with_defect_counts(db, project_id=project_id)

@router.get("/{base_map_id}", response_model=schemas.BaseMapOut)
def read_base_map(base_map_id: int, db: Session = Depends(get_db)):
    """Get a specific base map by ID"""
    db_base_map = crud.get_base_map(db, base_map_id=base_map_id)
    if db_base_map is None:
        raise HTTPException(status_code=404, detail="Base map not found")
    return db_base_map

@router.put("/{base_map_id}", response_model=schemas.BaseMapOut)
def update_base_map(
    base_map_id: int, base_map: schemas.BaseMapUpdate, db: Session = Depends(get_db)
):
    """Update a base map"""
    db_base_map = crud.update_base_map(db, base_map_id=base_map_id, base_map=base_map)
    if db_base_map is None:
        raise HTTPException(status_code=404, detail="Base map not found")
    return db_base_map

@router.delete("/{base_map_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_base_map(base_map_id: int, db: Session = Depends(get_db)):
    """Delete a base map"""
    success = crud.delete_base_map(db, base_map_id=base_map_id)
    if not success:
        raise HTTPException(status_code=404, detail="Base map not found")
    return None
