import pytest
from fastapi import status
from app.base_map import crud
from app.base_map.schemas import BaseMapCreate, BaseMapUpdate

# CRUD Tests
def test_create_base_map(db, test_project):
    # Create test data
    base_map_data = BaseMapCreate(
        project_id=test_project.project_id,
        map_name="Test Base Map",
        file_path="/path/to/test_map.jpg"
    )
    
    # Create base map
    base_map = crud.create_base_map(db, base_map_data)
    
    # Check base map was created correctly
    assert base_map.project_id == test_project.project_id
    assert base_map.map_name == "Test Base Map"
    assert base_map.file_path == "/path/to/test_map.jpg"
    assert base_map.base_map_id is not None

def test_get_base_map(db, test_base_map):
    # Get base map
    base_map = crud.get_base_map(db, test_base_map.base_map_id)
    
    # Check base map was retrieved correctly
    assert base_map is not None
    assert base_map.base_map_id == test_base_map.base_map_id
    assert base_map.project_id == test_base_map.project_id
    assert base_map.map_name == test_base_map.map_name
    assert base_map.file_path == test_base_map.file_path

def test_get_base_maps(db, test_base_map):
    # Create another base map
    base_map_data = BaseMapCreate(
        project_id=test_base_map.project_id,
        map_name="Another Test Base Map",
        file_path="/path/to/another_map.jpg"
    )
    crud.create_base_map(db, base_map_data)
    
    # Get base maps
    base_maps = crud.get_base_maps(db)
    
    # Check base maps were retrieved correctly
    assert len(base_maps) >= 2
    assert any(m.map_name == "Test Base Map" for m in base_maps)
    assert any(m.map_name == "Another Test Base Map" for m in base_maps)

def test_get_base_maps_by_project(db, test_base_map, test_project):
    # Get base maps by project
    base_maps = crud.get_base_maps_by_project(db, test_project.project_id)
    
    # Check base maps were retrieved correctly
    assert len(base_maps) >= 1
    assert any(m.base_map_id == test_base_map.base_map_id for m in base_maps)
    assert all(m.project_id == test_project.project_id for m in base_maps)

def test_update_base_map(db, test_base_map):
    # Create update data
    base_map_data = BaseMapUpdate(
        map_name="Updated Test Base Map",
        file_path="/path/to/updated_map.jpg"
    )
    
    # Update base map
    updated_base_map = crud.update_base_map(db, test_base_map.base_map_id, base_map_data)
    
    # Check base map was updated correctly
    assert updated_base_map is not None
    assert updated_base_map.base_map_id == test_base_map.base_map_id
    assert updated_base_map.project_id == test_base_map.project_id
    assert updated_base_map.map_name == "Updated Test Base Map"
    assert updated_base_map.file_path == "/path/to/updated_map.jpg"

def test_delete_base_map(db, test_base_map):
    # Delete base map
    result = crud.delete_base_map(db, test_base_map.base_map_id)
    
    # Check base map was deleted correctly
    assert result is True
    
    # Check base map no longer exists
    base_map = crud.get_base_map(db, test_base_map.base_map_id)
    assert base_map is None

def test_get_base_maps_with_defect_counts(db, test_base_map, test_project, test_defect, test_defect_mark):
    # Get base maps with defect counts
    base_maps_data = crud.get_base_maps_with_defect_counts(db, test_project.project_id)
    
    # Check base maps data was retrieved correctly
    assert len(base_maps_data) >= 1
    base_map_data = next((m for m in base_maps_data if m["base_map_id"] == test_base_map.base_map_id), None)
    assert base_map_data is not None
    assert base_map_data["project_id"] == test_project.project_id
    assert base_map_data["map_name"] == test_base_map.map_name
    assert base_map_data["file_path"] == test_base_map.file_path
    assert base_map_data["defect_count"] >= 1

# API Tests
def test_api_create_base_map(client, test_project):
    # Create test data
    base_map_data = {
        "project_id": test_project.project_id,
        "map_name": "API Test Base Map",
        "file_path": "/path/to/api_test_map.jpg"
    }
    
    # Send request
    response = client.post("/base-maps/", json=base_map_data)
    
    # Check response
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["project_id"] == test_project.project_id
    assert data["map_name"] == "API Test Base Map"
    assert data["file_path"] == "/path/to/api_test_map.jpg"
    assert "base_map_id" in data

def test_api_create_base_map_invalid_project(client):
    # Create test data with invalid project ID
    base_map_data = {
        "project_id": 999,
        "map_name": "Invalid Project Base Map",
        "file_path": "/path/to/invalid_project_map.jpg"
    }
    
    # Send request
    response = client.post("/base-maps/", json=base_map_data)
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_read_base_maps(client, test_base_map):
    # Send request
    response = client.get("/base-maps/")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(m["base_map_id"] == test_base_map.base_map_id for m in data)

def test_api_read_base_maps_by_project(client, test_base_map, test_project):
    # Send request
    response = client.get(f"/base-maps/?project_id={test_project.project_id}")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(m["base_map_id"] == test_base_map.base_map_id for m in data)
    assert all(m["project_id"] == test_project.project_id for m in data)

def test_api_read_base_maps_with_defect_counts(client, test_base_map, test_project, test_defect, test_defect_mark):
    # Send request
    response = client.get(f"/base-maps/project/{test_project.project_id}/with-counts")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    base_map_data = next((m for m in data if m["base_map_id"] == test_base_map.base_map_id), None)
    assert base_map_data is not None
    assert "defect_count" in base_map_data
    assert base_map_data["defect_count"] >= 1

def test_api_read_base_map(client, test_base_map):
    # Send request
    response = client.get(f"/base-maps/{test_base_map.base_map_id}")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["base_map_id"] == test_base_map.base_map_id
    assert data["project_id"] == test_base_map.project_id
    assert data["map_name"] == test_base_map.map_name
    assert data["file_path"] == test_base_map.file_path

def test_api_read_base_map_not_found(client):
    # Send request with non-existent ID
    response = client.get("/base-maps/999")
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_update_base_map(client, test_base_map):
    # Create update data
    base_map_data = {
        "map_name": "Updated API Test Base Map",
        "file_path": "/path/to/updated_api_map.jpg"
    }
    
    # Send request
    response = client.put(f"/base-maps/{test_base_map.base_map_id}", json=base_map_data)
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["base_map_id"] == test_base_map.base_map_id
    assert data["project_id"] == test_base_map.project_id
    assert data["map_name"] == "Updated API Test Base Map"
    assert data["file_path"] == "/path/to/updated_api_map.jpg"

def test_api_update_base_map_not_found(client):
    # Create update data
    base_map_data = {
        "map_name": "Updated API Test Base Map"
    }
    
    # Send request with non-existent ID
    response = client.put("/base-maps/999", json=base_map_data)
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_base_map(client, test_base_map):
    # Send request
    response = client.delete(f"/base-maps/{test_base_map.base_map_id}")
    
    # Check response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Check base map no longer exists
    response = client.get(f"/base-maps/{test_base_map.base_map_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_base_map_not_found(client):
    # Send request with non-existent ID
    response = client.delete("/base-maps/999")
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND
