import pytest
from fastapi import status
from app.user import crud
from app.user.schemas import UserCreate, UserUpdate

# CRUD Tests
def test_create_user(db):
    # Create test data
    user_data = UserCreate(
        name="New Test User",
        line_id="new_line_id",
        email="new_test@example.com",
        company_name="New Test Company"
    )
    
    # Create user
    user = crud.create_user(db, user_data)
    
    # Check user was created correctly
    assert user.name == "New Test User"
    assert user.line_id == "new_line_id"
    assert user.email == "new_test@example.com"
    assert user.company_name == "New Test Company"
    assert user.user_id is not None
    assert user.created_at is not None

def test_get_user(db, test_user):
    # Get user
    user = crud.get_user(db, test_user.user_id)
    
    # Check user was retrieved correctly
    assert user is not None
    assert user.user_id == test_user.user_id
    assert user.name == test_user.name
    assert user.line_id == test_user.line_id
    assert user.email == test_user.email
    assert user.company_name == test_user.company_name

def test_get_user_by_line_id(db, test_user):
    # Get user by LINE ID
    user = crud.get_user_by_line_id(db, test_user.line_id)
    
    # Check user was retrieved correctly
    assert user is not None
    assert user.user_id == test_user.user_id
    assert user.line_id == test_user.line_id

def test_get_users(db, test_user):
    # Create another user
    user_data = UserCreate(
        name="Another Test User",
        line_id="another_line_id",
        email="another_test@example.com",
        company_name="Another Test Company"
    )
    crud.create_user(db, user_data)
    
    # Get users
    users = crud.get_users(db)
    
    # Check users were retrieved correctly
    assert len(users) == 2
    assert any(u.name == "Test User" for u in users)
    assert any(u.name == "Another Test User" for u in users)

def test_update_user(db, test_user):
    # Create update data
    user_data = UserUpdate(
        name="Updated Test User",
        email="updated_test@example.com"
    )
    
    # Update user
    updated_user = crud.update_user(db, test_user.user_id, user_data)
    
    # Check user was updated correctly
    assert updated_user is not None
    assert updated_user.user_id == test_user.user_id
    assert updated_user.name == "Updated Test User"
    assert updated_user.email == "updated_test@example.com"
    assert updated_user.line_id == test_user.line_id  # Unchanged
    assert updated_user.company_name == test_user.company_name  # Unchanged

def test_delete_user(db, test_user):
    # Delete user
    result = crud.delete_user(db, test_user.user_id)
    
    # Check user was deleted correctly
    assert result is True
    
    # Check user no longer exists
    user = crud.get_user(db, test_user.user_id)
    assert user is None

def test_get_user_with_projects(db, test_user, test_project, test_permission):
    # Get user with projects
    user_data = crud.get_user_with_projects(db, test_user.user_id)
    
    # Check user data was retrieved correctly
    assert user_data is not None
    assert user_data["user_id"] == test_user.user_id
    assert user_data["name"] == test_user.name
    assert user_data["email"] == test_user.email
    assert user_data["company_name"] == test_user.company_name
    assert user_data["line_id"] == test_user.line_id
    
    # Check projects data
    assert len(user_data["projects"]) == 1
    project = user_data["projects"][0]
    assert project["project_id"] == test_project.project_id
    assert project["project_name"] == test_project.project_name
    assert project["role"] == "admin"

# API Tests
def test_api_create_user(client):
    # Create test data
    user_data = {
        "name": "API Test User",
        "line_id": "api_line_id",
        "email": "api_test@example.com",
        "company_name": "API Test Company"
    }
    
    # Send request
    response = client.post("/users/", json=user_data)
    
    # Check response
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "API Test User"
    assert data["line_id"] == "api_line_id"
    assert data["email"] == "api_test@example.com"
    assert data["company_name"] == "API Test Company"
    assert "user_id" in data
    assert "created_at" in data

def test_api_create_user_duplicate_line_id(client, test_user):
    # Create test data with existing LINE ID
    user_data = {
        "name": "Duplicate LINE ID User",
        "line_id": test_user.line_id,  # Use existing LINE ID
        "email": "duplicate@example.com",
        "company_name": "Duplicate Company"
    }
    
    # Send request
    response = client.post("/users/", json=user_data)
    
    # Check response
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_api_read_users(client, test_user):
    # Send request
    response = client.get("/users/")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(u["name"] == "Test User" for u in data)

def test_api_read_user(client, test_user):
    # Send request
    response = client.get(f"/users/{test_user.user_id}")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["user_id"] == test_user.user_id
    assert data["name"] == test_user.name
    assert data["line_id"] == test_user.line_id
    assert data["email"] == test_user.email
    assert data["company_name"] == test_user.company_name

def test_api_read_user_by_line_id(client, test_user):
    # Send request
    response = client.get(f"/users/line/{test_user.line_id}")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["user_id"] == test_user.user_id
    assert data["line_id"] == test_user.line_id

def test_api_read_user_not_found(client):
    # Send request with non-existent ID
    response = client.get("/users/999")
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_read_user_with_projects(client, test_user, test_project, test_permission):
    # Send request
    response = client.get(f"/users/{test_user.user_id}/projects")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["user_id"] == test_user.user_id
    assert data["name"] == test_user.name
    assert len(data["projects"]) == 1
    project = data["projects"][0]
    assert project["project_id"] == test_project.project_id
    assert project["project_name"] == test_project.project_name
    assert project["role"] == "admin"

def test_api_update_user(client, test_user):
    # Create update data
    user_data = {
        "name": "Updated API Test User",
        "email": "updated_api@example.com"
    }
    
    # Send request
    response = client.put(f"/users/{test_user.user_id}", json=user_data)
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["user_id"] == test_user.user_id
    assert data["name"] == "Updated API Test User"
    assert data["email"] == "updated_api@example.com"
    assert data["line_id"] == test_user.line_id  # Unchanged

def test_api_update_user_not_found(client):
    # Create update data
    user_data = {
        "name": "Updated API Test User"
    }
    
    # Send request with non-existent ID
    response = client.put("/users/999", json=user_data)
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_user(client, test_user):
    # Send request
    response = client.delete(f"/users/{test_user.user_id}")
    
    # Check response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Check user no longer exists
    response = client.get(f"/users/{test_user.user_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_user_not_found(client):
    # Send request with non-existent ID
    response = client.delete("/users/999")
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND
