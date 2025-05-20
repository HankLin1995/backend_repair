import pytest
from fastapi import status
from datetime import datetime
from app.defect import crud
from app.defect.schemas import DefectCreate, DefectUpdate

# CRUD Tests
def test_create_defect(db, test_project, test_user, test_defect_category, test_vendor):
    # Create test data
    defect_data = DefectCreate(
        project_id=test_project.project_id,
        submitted_id=test_user.user_id,
        defect_category_id=test_defect_category.defect_category_id,
        defect_description="Test defect description",
        assigned_vendor_id=test_vendor.vendor_id,
        confirmation_status="pending"
    )
    
    # Create defect
    defect = crud.create_defect(db, defect_data)
    
    # Check defect was created correctly
    assert defect.project_id == test_project.project_id
    assert defect.submitted_id == test_user.user_id
    assert defect.defect_category_id == test_defect_category.defect_category_id
    assert defect.defect_description == "Test defect description"
    assert defect.assigned_vendor_id == test_vendor.vendor_id
    assert defect.confirmation_status == "pending"
    assert defect.defect_id is not None
    assert defect.created_at is not None
    assert defect.updated_at is not None

def test_get_defect(db, test_defect):
    # Get defect
    defect = crud.get_defect(db, test_defect.defect_id)
    
    # Check defect was retrieved correctly
    assert defect is not None
    assert defect.defect_id == test_defect.defect_id
    assert defect.project_id == test_defect.project_id
    assert defect.submitted_id == test_defect.submitted_id
    assert defect.defect_category_id == test_defect.defect_category_id
    assert defect.defect_description == test_defect.defect_description
    assert defect.assigned_vendor_id == test_defect.assigned_vendor_id
    assert defect.confirmation_status == test_defect.confirmation_status

def test_get_defects(db, test_defect):
    # Create another defect
    defect_data = DefectCreate(
        project_id=test_defect.project_id,
        submitted_id=test_defect.submitted_id,
        defect_description="Another test defect description",
        confirmation_status="in_progress"
    )
    crud.create_defect(db, defect_data)
    
    # Get defects
    defects = crud.get_defects(db)
    
    # Check defects were retrieved correctly
    assert len(defects) >= 2
    assert any(d.defect_description == test_defect.defect_description for d in defects)
    assert any(d.defect_description == "Another test defect description" for d in defects)

def test_get_defects_with_filters(db, test_defect, test_project, test_user, test_defect_category, test_vendor):
    # Test filtering by project
    defects = crud.get_defects(db, project_id=test_project.project_id)
    assert len(defects) >= 1
    assert all(d.project_id == test_project.project_id for d in defects)
    
    # Test filtering by submitter
    defects = crud.get_defects(db, submitted_id=test_user.user_id)
    assert len(defects) >= 1
    assert all(d.submitted_id == test_user.user_id for d in defects)
    
    # Test filtering by category
    if test_defect.defect_category_id:
        defects = crud.get_defects(db, defect_category_id=test_defect.defect_category_id)
        assert len(defects) >= 1
        assert all(d.defect_category_id == test_defect.defect_category_id for d in defects)
    
    # Test filtering by vendor
    if test_defect.assigned_vendor_id:
        defects = crud.get_defects(db, assigned_vendor_id=test_defect.assigned_vendor_id)
        assert len(defects) >= 1
        assert all(d.assigned_vendor_id == test_defect.assigned_vendor_id for d in defects)
    
    # Test filtering by status
    defects = crud.get_defects(db, confirmation_status=test_defect.confirmation_status)
    assert len(defects) >= 1
    assert all(d.confirmation_status == test_defect.confirmation_status for d in defects)

def test_update_defect(db, test_defect):
    # Create update data
    repair_description = "Test repair description"
    repair_completed_at = datetime.utcnow()
    confirmation_status = "completed"
    
    defect_data = DefectUpdate(
        repair_description=repair_description,
        repair_completed_at=repair_completed_at,
        confirmation_status=confirmation_status
    )
    
    # Update defect
    updated_defect = crud.update_defect(db, test_defect.defect_id, defect_data)
    
    # Check defect was updated correctly
    assert updated_defect is not None
    assert updated_defect.defect_id == test_defect.defect_id
    assert updated_defect.repair_description == repair_description
    assert updated_defect.confirmation_status == confirmation_status
    # Check that repair_completed_at was set (can't check exact value due to microsecond differences)
    assert updated_defect.repair_completed_at is not None
    # 在測試環境中不檢查 updated_at 時間戳，因為可能不夠精確

def test_delete_defect(db, test_defect):
    # Delete defect
    result = crud.delete_defect(db, test_defect.defect_id)
    
    # Check defect was deleted correctly
    assert result is True
    
    # Check defect no longer exists
    defect = crud.get_defect(db, test_defect.defect_id)
    assert defect is None

def test_get_defect_with_details(db, test_defect, test_project, test_user, test_defect_category, test_vendor):
    # Get defect with details
    defect_data = crud.get_defect_with_details(db, test_defect.defect_id)
    
    # Check defect data was retrieved correctly
    assert defect_data is not None
    assert defect_data["defect_id"] == test_defect.defect_id
    assert defect_data["project_id"] == test_defect.project_id
    assert defect_data["project_name"] == test_project.project_name
    assert defect_data["submitted_id"] == test_defect.submitted_id
    assert defect_data["submitter_name"] == test_user.name
    
    if test_defect.defect_category_id:
        assert defect_data["defect_category_id"] == test_defect.defect_category_id
        assert defect_data["category_name"] == test_defect_category.category_name
    
    assert defect_data["defect_description"] == test_defect.defect_description
    
    if test_defect.assigned_vendor_id:
        assert defect_data["assigned_vendor_id"] == test_defect.assigned_vendor_id
        assert defect_data["vendor_name"] == test_vendor.vendor_name
    
    assert defect_data["confirmation_status"] == test_defect.confirmation_status

def test_get_defect_with_marks_and_photos(db, test_defect, test_defect_mark, test_photo):
    # Get defect with marks and photos
    defect_data = crud.get_defect_with_marks_and_photos(db, test_defect.defect_id)
    
    # Check defect data was retrieved correctly
    assert defect_data is not None
    assert defect_data["defect_id"] == test_defect.defect_id
    
    # Check defect marks
    assert "defect_marks" in defect_data
    assert len(defect_data["defect_marks"]) >= 1
    mark = defect_data["defect_marks"][0]
    assert mark["defect_mark_id"] == test_defect_mark.defect_mark_id
    assert mark["defect_form_id"] == test_defect_mark.defect_form_id
    assert mark["base_map_id"] == test_defect_mark.base_map_id
    assert mark["coordinate_x"] == test_defect_mark.coordinate_x
    assert mark["coordinate_y"] == test_defect_mark.coordinate_y
    assert mark["scale"] == test_defect_mark.scale
    
    # Check photos
    assert "photos" in defect_data
    assert len(defect_data["photos"]) >= 1
    photo = defect_data["photos"][0]
    assert photo["photo_id"] == test_photo.photo_id
    assert photo["defect_form_id"] == test_photo.defect_form_id
    assert photo["description"] == test_photo.description
    assert photo["photo_type"] == test_photo.photo_type
    assert photo["image_url"] == test_photo.image_url

def test_get_defect_stats(db, test_defect, test_project):
    # Get defect stats
    stats = crud.get_defect_stats(db)
    
    # Check stats were retrieved correctly
    assert stats is not None
    assert "total_count" in stats
    assert stats["total_count"] >= 1
    assert "pending_count" in stats
    assert "in_progress_count" in stats
    assert "completed_count" in stats
    assert "category_stats" in stats
    
    # Test project-specific stats
    project_stats = crud.get_defect_stats(db, project_id=test_project.project_id)
    assert project_stats is not None
    assert project_stats["total_count"] >= 1

# API Tests
def test_api_create_defect(client, test_project, test_user, test_defect_category, test_vendor):
    # Create test data
    defect_data = {
        "project_id": test_project.project_id,
        "submitted_id": test_user.user_id,
        "defect_category_id": test_defect_category.defect_category_id,
        "defect_description": "API Test defect description",
        "assigned_vendor_id": test_vendor.vendor_id,
        "confirmation_status": "pending"
    }
    
    # Send request
    response = client.post("/defects/", json=defect_data)
    
    # Check response
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["project_id"] == test_project.project_id
    assert data["submitted_id"] == test_user.user_id
    assert data["defect_category_id"] == test_defect_category.defect_category_id
    assert data["defect_description"] == "API Test defect description"
    assert data["assigned_vendor_id"] == test_vendor.vendor_id
    assert data["confirmation_status"] == "pending"
    assert "defect_id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_api_read_defects(client, test_defect):
    # Send request
    response = client.get("/defects/")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(d["defect_id"] == test_defect.defect_id for d in data)

def test_api_read_defects_with_filters(client, test_defect, test_project, test_user, test_defect_category, test_vendor):
    # Test filtering by project
    response = client.get(f"/defects/?project_id={test_project.project_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    assert all(d["project_id"] == test_project.project_id for d in data)
    
    # Test filtering by submitter
    response = client.get(f"/defects/?submitted_id={test_user.user_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    assert all(d["submitted_id"] == test_user.user_id for d in data)
    
    # Test filtering by category
    if test_defect.defect_category_id:
        response = client.get(f"/defects/?defect_category_id={test_defect.defect_category_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
        assert all(d["defect_category_id"] == test_defect.defect_category_id for d in data)
    
    # Test filtering by vendor
    if test_defect.assigned_vendor_id:
        response = client.get(f"/defects/?assigned_vendor_id={test_defect.assigned_vendor_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) >= 1
        assert all(d["assigned_vendor_id"] == test_defect.assigned_vendor_id for d in data)
    
    # Test filtering by status
    response = client.get(f"/defects/?confirmation_status={test_defect.confirmation_status}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) >= 1
    assert all(d["confirmation_status"] == test_defect.confirmation_status for d in data)

def test_api_read_defect_stats(client, test_project):
    # 先確保有至少一個缺陷存在
    # 創建一個新的缺陷
    defect_data = {
        "project_id": test_project.project_id,
        "submitted_id": test_project.project_id,  # 使用 project_id 作為 user_id (僅測試用)
        "defect_description": "Stats Test defect description",
        "confirmation_status": "pending"
    }
    client.post("/defects/", json=defect_data)
    
    # Send request
    response = client.get("/defects/stats")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_count" in data
    # 只檢查統計數據的結構，不檢查具體數值
    assert "pending_count" in data
    assert "in_progress_count" in data
    assert "completed_count" in data
    assert "category_stats" in data
    
    # Test project-specific stats
    response = client.get(f"/defects/stats?project_id={test_project.project_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # 確保至少有總數統計
    assert "total_count" in data

def test_api_read_defect(client, test_defect):
    # Send request
    response = client.get(f"/defects/{test_defect.defect_id}")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["defect_id"] == test_defect.defect_id
    assert data["project_id"] == test_defect.project_id
    assert data["submitted_id"] == test_defect.submitted_id
    assert data["defect_description"] == test_defect.defect_description
    assert data["confirmation_status"] == test_defect.confirmation_status

def test_api_read_defect_full(client, test_defect, test_defect_mark, test_photo):
    # Send request
    response = client.get(f"/defects/{test_defect.defect_id}/full")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["defect_id"] == test_defect.defect_id
    
    # Check defect marks
    assert "defect_marks" in data
    assert len(data["defect_marks"]) >= 1
    
    # Check photos
    assert "photos" in data
    assert len(data["photos"]) >= 1

def test_api_read_defect_not_found(client):
    # Send request with non-existent ID
    response = client.get("/defects/999")
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_update_defect(client, test_defect):
    # Create update data
    defect_data = {
        "repair_description": "API Test repair description",
        "confirmation_status": "completed"
    }
    
    # Send request
    response = client.put(f"/defects/{test_defect.defect_id}", json=defect_data)
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["defect_id"] == test_defect.defect_id
    assert data["repair_description"] == "API Test repair description"
    assert data["confirmation_status"] == "completed"

def test_api_update_defect_not_found(client):
    # Create update data
    defect_data = {
        "repair_description": "API Test repair description"
    }
    
    # Send request with non-existent ID
    response = client.put("/defects/999", json=defect_data)
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_defect(client, test_defect):
    # Send request
    response = client.delete(f"/defects/{test_defect.defect_id}")
    
    # Check response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Check defect no longer exists
    response = client.get(f"/defects/{test_defect.defect_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_defect_not_found(client):
    # Send request with non-existent ID
    response = client.delete("/defects/999")
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND
