from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from typing import List, Optional, Dict, Any

from app.vendor.models import Vendor
from app.vendor.schemas import VendorCreate, VendorUpdate
from app.defect.models import Defect

def get_vendor(db: Session, vendor_id: int) -> Optional[Vendor]:
    """Get a single vendor by ID"""
    return db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()

def get_vendors(db: Session, skip: int = 0, limit: int = 100) -> List[Vendor]:
    """Get a list of vendors with pagination"""
    return db.query(Vendor).offset(skip).limit(limit).all()

def create_vendor(db: Session, vendor: VendorCreate) -> Vendor:
    """Create a new vendor"""
    db_vendor = Vendor(
        vendor_name=vendor.vendor_name,
        contact_person=vendor.contact_person,
        phone=vendor.phone,
        responsibilities=vendor.responsibilities,
        email=vendor.email,
        line_id=vendor.line_id
    )
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

def update_vendor(db: Session, vendor_id: int, vendor: VendorUpdate) -> Optional[Vendor]:
    """Update an existing vendor"""
    db_vendor = get_vendor(db, vendor_id)
    if not db_vendor:
        return None
    
    update_data = vendor.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_vendor, key, value)
    
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

def delete_vendor(db: Session, vendor_id: int) -> bool:
    """Delete a vendor"""
    db_vendor = get_vendor(db, vendor_id)
    if not db_vendor:
        return False
    
    db.delete(db_vendor)
    db.commit()
    return True

def get_vendors_with_defect_counts(db: Session) -> List[Dict[str, Any]]:
    """Get vendors with defect counts"""
    vendors = get_vendors(db)
    
    result = []
    for vendor in vendors:
        # Count defects assigned to this vendor
        defect_count = db.query(func.count(Defect.defect_id)).filter(
            Defect.assigned_vendor_id == vendor.vendor_id
        ).scalar()
        
        result.append({
            "vendor_id": vendor.vendor_id,
            "vendor_name": vendor.vendor_name,
            "contact_person": vendor.contact_person,
            "phone": vendor.phone,
            "responsibilities": vendor.responsibilities,
            "defect_count": defect_count
        })
    
    return result
