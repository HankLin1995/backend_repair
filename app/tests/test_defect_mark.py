import pytest
from fastapi import status
from app.defect_mark import crud
from app.defect_mark.schemas import DefectMarkCreate, DefectMarkUpdate

# CRUD Tests
def test_create_defect_mark(db, test_defect, test_base_map):
    # Create test data
    mark_data = DefectMarkCreate(
        defect_id=test_defect.defect_id,
        base_map_id=test_base_map.base_map_id,
        coordinate_x=100.5,
        coordinate_y=200.5,
        scale=1.5
    )
    
    # Create defect mark
    defect_mark = crud.create_defect_mark(db, mark_data)
    
    # Check defect mark was created correctly
    assert defect_mark.defect_id == test_defect.defect_id
    assert defect_mark.base_map_id == test_base_map.base_map_id
    assert defect_mark.coordinate_x == 100.5
    assert defect_mark.coordinate_y == 200.5
    assert defect_mark.scale == 1.5
    assert defect_mark.defect_mark_id is not None

def test_get_defect_mark(db, test_defect_mark):
    # Get defect mark
    retrieved_mark = crud.get_defect_mark(db, test_defect_mark.defect_mark_id)
    
    # Check defect mark was retrieved correctly
    assert retrieved_mark is not None
    assert retrieved_mark.defect_mark_id == test_defect_mark.defect_mark_id
    assert retrieved_mark.defect_id == test_defect_mark.defect_id
    assert retrieved_mark.base_map_id == test_defect_mark.base_map_id
    assert retrieved_mark.coordinate_x == test_defect_mark.coordinate_x
    assert retrieved_mark.coordinate_y == test_defect_mark.coordinate_y
    assert retrieved_mark.scale == test_defect_mark.scale

def test_get_defect_marks_by_defect(db, test_defect_mark, test_defect):
    # Get defect marks by defect
    defect_marks = crud.get_defect_marks_by_defect(db, test_defect.defect_id)
    
    # Check defect marks were retrieved correctly
    assert len(defect_marks) >= 1
    assert any(m.defect_mark_id == test_defect_mark.defect_mark_id for m in defect_marks)

def test_update_defect_mark(db, test_defect_mark):
    # Create update data
    update_data = DefectMarkUpdate(
        coordinate_x=150.0,
        coordinate_y=250.0,
        scale=2.0
    )
    
    # Update defect mark
    updated_defect_mark = crud.update_defect_mark(db, test_defect_mark.defect_mark_id, update_data)
    
    # Check defect mark was updated correctly
    assert updated_defect_mark is not None
    assert updated_defect_mark.defect_mark_id == test_defect_mark.defect_mark_id
    assert updated_defect_mark.coordinate_x == 150.0
    assert updated_defect_mark.coordinate_y == 250.0
    assert updated_defect_mark.scale == 2.0

def test_delete_defect_mark(db, test_defect_mark):
    # Delete defect mark
    result = crud.delete_defect_mark(db, test_defect_mark.defect_mark_id)
    
    # Check defect mark was deleted correctly
    assert result is True
    
    # Check defect mark no longer exists
    deleted_defect_mark = crud.get_defect_mark(db, test_defect_mark.defect_mark_id)
    assert deleted_defect_mark is None

# API Tests
def test_api_create_defect_mark(client, test_defect, test_base_map):
    # Create test data
    mark_data = {
        "defect_id": test_defect.defect_id,
        "base_map_id": test_base_map.base_map_id,
        "coordinate_x": 200.0,
        "coordinate_y": 300.0,
        "scale": 1.0
    }
    
    # Send request
    response = client.post("/defect-marks/", json=mark_data)
    
    # Check response
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["defect_id"] == test_defect.defect_id
    assert data["base_map_id"] == test_base_map.base_map_id
    assert data["coordinate_x"] == 200.0
    assert data["coordinate_y"] == 300.0
    assert data["scale"] == 1.0
    assert "defect_mark_id" in data

def test_api_read_defect_marks(client, test_defect_mark, test_defect):
    # Send request
    response = client.get(f"/defect-marks/?defect_id={test_defect.defect_id}")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(m["defect_mark_id"] == test_defect_mark.defect_mark_id for m in data)

def test_api_read_defect_mark(client, test_defect_mark):
    # Send request
    response = client.get(f"/defect-marks/{test_defect_mark.defect_mark_id}")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["defect_mark_id"] == test_defect_mark.defect_mark_id
    assert data["defect_id"] == test_defect_mark.defect_id
    assert data["base_map_id"] == test_defect_mark.base_map_id
    assert data["coordinate_x"] == test_defect_mark.coordinate_x
    assert data["coordinate_y"] == test_defect_mark.coordinate_y
    assert data["scale"] == test_defect_mark.scale

def test_api_read_defect_mark_not_found(client):
    # Send request with non-existent ID
    response = client.get("/defect-marks/9999")
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_update_defect_mark(client, test_defect_mark):
    # Create update data
    update_data = {
        "coordinate_x": 350.5,
        "coordinate_y": 450.5,
        "scale": 2.5
    }
    
    # Send request
    response = client.put(f"/defect-marks/{test_defect_mark.defect_mark_id}", json=update_data)
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["defect_mark_id"] == test_defect_mark.defect_mark_id
    assert data["coordinate_x"] == 350.5
    assert data["coordinate_y"] == 450.5
    assert data["scale"] == 2.5

def test_api_update_defect_mark_not_found(client):
    # Create update data
    update_data = {
        "coordinate_x": 350.5,
    }
    
    # Send request with non-existent ID
    response = client.put("/defect-marks/9999", json=update_data)
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_defect_mark(client, test_defect_mark):
    # Send request
    response = client.delete(f"/defect-marks/{test_defect_mark.defect_mark_id}")
    
    # Check response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Check defect mark no longer exists
    response = client.get(f"/defect-marks/{test_defect_mark.defect_mark_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_defect_mark_not_found(client):
    # Send request with non-existent ID
    response = client.delete("/defect-marks/9999")
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND