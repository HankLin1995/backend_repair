import pytest
from fastapi import status
from app.vendor import crud
from app.vendor.schemas import VendorCreate, VendorUpdate

# CRUD Tests
def test_create_vendor(db, test_project):
    # Create test data
    vendor_data = VendorCreate(
        vendor_name="Test Vendor",
        project_id=test_project.project_id,
        contact_person="Test Contact",
        phone="123-456-7890",
        responsibilities="Test responsibilities",
        email="test_vendor@example.com",
        line_id="lineid_vendor"
    )
    
    # Create vendor
    vendor = crud.create_vendor(db, vendor_data)
    
    # Check vendor was created correctly
    assert vendor.vendor_name == "Test Vendor"
    assert vendor.contact_person == "Test Contact"
    assert vendor.phone == "123-456-7890"
    assert vendor.responsibilities == "Test responsibilities"
    assert vendor.email == "test_vendor@example.com"
    assert vendor.line_id == "lineid_vendor"
    assert vendor.vendor_id is not None
    assert vendor.unique_code is not None
    assert len(vendor.unique_code) > 0

def test_get_vendor(db, test_vendor):
    # Get vendor
    vendor = crud.get_vendor(db, test_vendor.vendor_id)
    
    # Check vendor was retrieved correctly
    assert vendor is not None
    assert vendor.vendor_id == test_vendor.vendor_id
    assert vendor.project_id == test_vendor.project_id
    assert vendor.vendor_name == test_vendor.vendor_name
    assert vendor.contact_person == test_vendor.contact_person
    assert vendor.phone == test_vendor.phone
    assert vendor.responsibilities == test_vendor.responsibilities
    assert vendor.email == test_vendor.email
    assert vendor.line_id == test_vendor.line_id
    assert vendor.unique_code == test_vendor.unique_code

def test_update_vendor(db, test_vendor):
    update_data = VendorUpdate(
        vendor_name="Updated Vendor",
        contact_person="Updated Contact",
        phone="987-654-3210",
        responsibilities="Updated responsibilities",
        email="updated_vendor@example.com",
        line_id="updated_lineid_vendor"
    )
    updated_vendor = crud.update_vendor(db, test_vendor.vendor_id, update_data)
    assert updated_vendor.vendor_name == "Updated Vendor"
    assert updated_vendor.contact_person == "Updated Contact"
    assert updated_vendor.phone == "987-654-3210"
    assert updated_vendor.responsibilities == "Updated responsibilities"
    assert updated_vendor.email == "updated_vendor@example.com"
    assert updated_vendor.line_id == "updated_lineid_vendor"

def test_api_create_vendor(client, test_project):
    vendor_data = {
        "vendor_name": "API Vendor",
        "project_id": test_project.project_id,
        "contact_person": "API Contact",
        "phone": "000-111-2222",
        "responsibilities": "API responsibilities",
        "email": "api_vendor@example.com",
        "line_id": "api_lineid_vendor"
    }
    response = client.post("/vendors/", json=vendor_data)
    assert response.status_code == 201
    data = response.json()
    assert data["vendor_name"] == "API Vendor"
    assert data["email"] == "api_vendor@example.com"
    assert data["line_id"] == "api_lineid_vendor"
    assert "unique_code" in data
    assert len(data["unique_code"]) > 0

def test_api_update_vendor(client, test_vendor):
    update_data = {
        "vendor_name": "API Updated Vendor",
        "contact_person": "API Updated Contact",
        "phone": "222-333-4444",
        "responsibilities": "API updated responsibilities",
        "email": "api_updated_vendor@example.com",
        "line_id": "api_updated_lineid_vendor"
    }
    response = client.put(f"/vendors/{test_vendor.vendor_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["vendor_name"] == "API Updated Vendor"
    assert data["email"] == "api_updated_vendor@example.com"
    assert data["line_id"] == "api_updated_lineid_vendor"

def test_api_get_vendor(client, test_vendor):
    response = client.get(f"/vendors/{test_vendor.vendor_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["vendor_id"] == test_vendor.vendor_id
    assert "email" in data
    assert "line_id" in data
    assert "unique_code" in data
    assert data["unique_code"] == test_vendor.unique_code

def test_get_vendors(db, test_vendor, test_project):
    # Create another vendor
    vendor_data = VendorCreate(
        vendor_name="Another Test Vendor",
        project_id=test_project.project_id,
        contact_person="Another Contact",
        phone="987-654-3210",
        responsibilities="Another responsibilities"
    )
    crud.create_vendor(db, vendor_data)
    
    # Get vendors
    vendors = crud.get_vendors(db)
    
    # Check vendors were retrieved correctly
    assert len(vendors) >= 2
    assert any(v.vendor_name == "Test Vendor" for v in vendors)
    assert any(v.vendor_name == "Another Test Vendor" for v in vendors)

def test_update_vendor(db, test_vendor):
    # Create update data
    vendor_data = VendorUpdate(
        vendor_name="Updated Test Vendor",
        contact_person="Updated Contact",
        phone="555-555-5555"
    )
    
    # Update vendor
    updated_vendor = crud.update_vendor(db, test_vendor.vendor_id, vendor_data)
    
    # Check vendor was updated correctly
    assert updated_vendor is not None
    assert updated_vendor.vendor_id == test_vendor.vendor_id
    assert updated_vendor.vendor_name == "Updated Test Vendor"
    assert updated_vendor.contact_person == "Updated Contact"
    assert updated_vendor.phone == "555-555-5555"
    assert updated_vendor.responsibilities == test_vendor.responsibilities  # Unchanged

def test_delete_vendor(db, test_vendor):
    # Delete vendor
    result = crud.delete_vendor(db, test_vendor.vendor_id)
    
    # Check vendor was deleted correctly
    assert result is True
    
    # Check vendor no longer exists
    vendor = crud.get_vendor(db, test_vendor.vendor_id)
    assert vendor is None

def test_get_vendors_with_defect_counts(db, test_vendor, test_defect):
    # Get vendors with defect counts
    vendors_data = crud.get_vendors_with_defect_counts(db)
    
    # Check vendors data was retrieved correctly
    assert len(vendors_data) >= 1
    vendor_data = next((v for v in vendors_data if v["vendor_id"] == test_vendor.vendor_id), None)
    assert vendor_data is not None
    assert vendor_data["vendor_name"] == test_vendor.vendor_name
    assert vendor_data["contact_person"] == test_vendor.contact_person
    assert vendor_data["phone"] == test_vendor.phone
    assert vendor_data["responsibilities"] == test_vendor.responsibilities
    assert "defect_count" in vendor_data
    assert vendor_data["defect_count"] >= 1

# API Tests
def test_api_create_vendor(client, test_project):
    # Create test data
    vendor_data = {
        "vendor_name": "API Test Vendor",
        "project_id": test_project.project_id,
        "contact_person": "API Contact",
        "phone": "111-222-3333",
        "responsibilities": "API responsibilities"
    }
    
    # Send request
    response = client.post("/vendors/", json=vendor_data)
    
    # Check response
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["vendor_name"] == "API Test Vendor"
    assert data["contact_person"] == "API Contact"
    assert data["phone"] == "111-222-3333"
    assert data["responsibilities"] == "API responsibilities"
    assert "vendor_id" in data

def test_api_read_vendors(client, test_vendor):
    # Send request
    response = client.get("/vendors/")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(v["vendor_id"] == test_vendor.vendor_id for v in data)

def test_api_read_vendors_with_defect_counts(client, test_vendor, test_defect):
    # Send request
    response = client.get("/vendors/with-counts")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    vendor_data = next((v for v in data if v["vendor_id"] == test_vendor.vendor_id), None)
    assert vendor_data is not None
    assert "defect_count" in vendor_data
    assert vendor_data["defect_count"] >= 1

def test_api_read_vendor(client, test_vendor):
    # Send request
    response = client.get(f"/vendors/{test_vendor.vendor_id}")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["vendor_id"] == test_vendor.vendor_id
    assert data["vendor_name"] == test_vendor.vendor_name
    assert data["contact_person"] == test_vendor.contact_person
    assert data["phone"] == test_vendor.phone
    assert data["responsibilities"] == test_vendor.responsibilities

def test_api_read_vendor_not_found(client):
    # Send request with non-existent ID
    response = client.get("/vendors/999")
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_update_vendor(client, test_vendor):
    # Create update data
    vendor_data = {
        "vendor_name": "Updated API Test Vendor",
        "contact_person": "Updated API Contact",
        "phone": "999-888-7777"
    }
    
    # Send request
    response = client.put(f"/vendors/{test_vendor.vendor_id}", json=vendor_data)
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["vendor_id"] == test_vendor.vendor_id
    assert data["vendor_name"] == "Updated API Test Vendor"
    assert data["contact_person"] == "Updated API Contact"
    assert data["phone"] == "999-888-7777"
    assert data["responsibilities"] == test_vendor.responsibilities  # Unchanged

def test_api_update_vendor_not_found(client):
    # Create update data
    vendor_data = {
        "vendor_name": "Updated API Test Vendor"
    }
    
    # Send request with non-existent ID
    response = client.put("/vendors/999", json=vendor_data)
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_vendor(client, test_vendor):
    # Send request
    response = client.delete(f"/vendors/{test_vendor.vendor_id}")
    
    # Check response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Check vendor no longer exists
    response = client.get(f"/vendors/{test_vendor.vendor_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_vendor_not_found(client):
    # Send request with non-existent ID
    response = client.delete("/vendors/999")
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND
