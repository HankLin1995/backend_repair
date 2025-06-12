import pytest
from fastapi import status
from app.defect_category import crud
from app.defect_category.schemas import DefectCategoryCreate, DefectCategoryUpdate

# CRUD Tests
def test_create_defect_category(db, test_project):
    # Create test data
    category_data = DefectCategoryCreate(
        category_name="Test Category",
        project_id=test_project.project_id,
        description="Test description"
    )
    
    # Create defect category
    category = crud.create_defect_category(db, category_data)
    
    # Check defect category was created correctly
    assert category.category_name == "Test Category"
    assert category.description == "Test description"
    assert category.defect_category_id is not None

def test_get_defect_category(db, test_defect_category):
    # Get defect category
    category = crud.get_defect_category(db, test_defect_category.defect_category_id)
    
    # Check defect category was retrieved correctly
    assert category is not None
    assert category.defect_category_id == test_defect_category.defect_category_id
    assert category.project_id == test_defect_category.project_id
    assert category.category_name == test_defect_category.category_name
    assert category.description == test_defect_category.description

def test_get_defect_categories(db, test_defect_category, test_project):
    # Create another defect category
    category_data = DefectCategoryCreate(
        category_name="Another Test Category",
        project_id=test_project.project_id,
        description="Another test description"
    )
    crud.create_defect_category(db, category_data)
    
    # Get defect categories
    categories = crud.get_defect_categories(db)
    
    # Check defect categories were retrieved correctly
    assert len(categories) >= 2
    assert any(c.category_name == "Test Category" for c in categories)
    assert any(c.category_name == "Another Test Category" for c in categories)

def test_update_defect_category(db, test_defect_category):
    # Create update data
    category_data = DefectCategoryUpdate(
        category_name="Updated Test Category",
        description="Updated test description"
    )
    
    # Update defect category
    updated_category = crud.update_defect_category(db, test_defect_category.defect_category_id, category_data)
    
    # Check defect category was updated correctly
    assert updated_category is not None
    assert updated_category.defect_category_id == test_defect_category.defect_category_id
    assert updated_category.category_name == "Updated Test Category"
    assert updated_category.description == "Updated test description"

def test_delete_defect_category(db, test_defect_category):
    # Delete defect category
    result = crud.delete_defect_category(db, test_defect_category.defect_category_id)
    
    # Check defect category was deleted correctly
    assert result is True
    
    # Check defect category no longer exists
    category = crud.get_defect_category(db, test_defect_category.defect_category_id)
    assert category is None

def test_get_defect_categories_with_counts(db, test_defect_category, test_defect):
    # Get defect categories with counts
    categories_data = crud.get_defect_categories_with_counts(db)
    
    # Check defect categories data was retrieved correctly
    assert len(categories_data) >= 1
    category_data = next((c for c in categories_data if c["defect_category_id"] == test_defect_category.defect_category_id), None)
    assert category_data is not None
    assert category_data["category_name"] == test_defect_category.category_name
    assert category_data["description"] == test_defect_category.description
    assert "defect_count" in category_data
    assert category_data["defect_count"] >= 1

# API Tests
def test_api_create_defect_category(client, test_project):
    # Create test data
    category_data = {
        "category_name": "API Test Category",
        "project_id": test_project.project_id,
        "description": "API test description"
    }
    
    # Send request
    response = client.post("/defect-categories/", json=category_data)
    
    # Check response
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["category_name"] == "API Test Category"
    assert data["description"] == "API test description"
    assert "defect_category_id" in data

def test_api_read_defect_categories(client, test_defect_category):
    # Send request
    response = client.get("/defect-categories/")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(c["defect_category_id"] == test_defect_category.defect_category_id for c in data)

def test_api_read_defect_categories_with_counts(client, test_defect_category, test_defect):
    # Send request
    response = client.get("/defect-categories/with-counts")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    category_data = next((c for c in data if c["defect_category_id"] == test_defect_category.defect_category_id), None)
    assert category_data is not None
    assert "defect_count" in category_data
    assert category_data["defect_count"] >= 1

def test_api_read_defect_category(client, test_defect_category):
    # Send request
    response = client.get(f"/defect-categories/{test_defect_category.defect_category_id}")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["defect_category_id"] == test_defect_category.defect_category_id
    assert data["category_name"] == test_defect_category.category_name
    assert data["description"] == test_defect_category.description

def test_api_read_defect_category_not_found(client):
    # Send request with non-existent ID
    response = client.get("/defect-categories/999")
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_update_defect_category(client, test_defect_category):
    # Create update data
    category_data = {
        "category_name": "Updated API Test Category",
        "project_id": test_defect_category.project_id,
        "description": "Updated API test description"
    }
    
    # Send request
    response = client.put(f"/defect-categories/{test_defect_category.defect_category_id}", json=category_data)
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["defect_category_id"] == test_defect_category.defect_category_id
    assert data["category_name"] == "Updated API Test Category"
    assert data["description"] == "Updated API test description"

def test_api_update_defect_category_not_found(client):
    # Create update data
    category_data = {
        "category_name": "Updated API Test Category"
    }
    
    # Send request with non-existent ID
    response = client.put("/defect-categories/999", json=category_data)
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_defect_category(client, test_defect_category):
    # Send request
    response = client.delete(f"/defect-categories/{test_defect_category.defect_category_id}")
    
    # Check response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Check defect category no longer exists
    response = client.get(f"/defect-categories/{test_defect_category.defect_category_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_defect_category_not_found(client):
    # Send request with non-existent ID
    response = client.delete("/defect-categories/999")
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND
