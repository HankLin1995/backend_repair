from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.vendor import crud, schemas

router = APIRouter()

@router.post("/", response_model=schemas.VendorOut, status_code=status.HTTP_201_CREATED)
def create_vendor(vendor: schemas.VendorCreate, db: Session = Depends(get_db)):
    """Create a new vendor"""
    return crud.create_vendor(db=db, vendor=vendor)

@router.get("/", response_model=List[schemas.VendorOut])
def read_vendors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get a list of vendors with pagination"""
    vendors = crud.get_vendors(db, skip=skip, limit=limit)
    return vendors

@router.get("/with-counts", response_model=List[schemas.VendorWithDefectCountOut])
def read_vendors_with_defect_counts(db: Session = Depends(get_db)):
    """Get vendors with defect counts"""
    return crud.get_vendors_with_defect_counts(db)

@router.get("/{vendor_id}", response_model=schemas.VendorOut)
def read_vendor(vendor_id: int, db: Session = Depends(get_db)):
    """Get a specific vendor by ID"""
    db_vendor = crud.get_vendor(db, vendor_id=vendor_id)
    if db_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db_vendor

@router.put("/{vendor_id}", response_model=schemas.VendorOut)
def update_vendor(
    vendor_id: int, vendor: schemas.VendorUpdate, db: Session = Depends(get_db)
):
    """Update a vendor"""
    db_vendor = crud.update_vendor(db, vendor_id=vendor_id, vendor=vendor)
    if db_vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return db_vendor

@router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)):
    """Delete a vendor"""
    success = crud.delete_vendor(db, vendor_id=vendor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return None
