import pytest
from fastapi import status
from datetime import datetime
from app.project import crud
from app.project.schemas import ProjectCreate, ProjectUpdate

# CRUD Tests
def test_create_project(db):
    # Create test data
    project_data = ProjectCreate(project_name="Test Project")
    
    # Create project
    project = crud.create_project(db, project_data)
    
    # Check project was created correctly
    assert project.project_name == "Test Project"
    assert project.project_id is not None
    assert project.created_at is not None

def test_get_project(db, test_project):
    # Get project
    project = crud.get_project(db, test_project.project_id)
    
    # Check project was retrieved correctly
    assert project is not None
    assert project.project_id == test_project.project_id
    assert project.project_name == test_project.project_name

def test_get_projects(db, test_project):
    # Create another project
    project_data = ProjectCreate(project_name="Another Test Project")
    crud.create_project(db, project_data)
    
    # Get projects
    projects = crud.get_projects(db)
    
    # Check projects were retrieved correctly
    assert len(projects) >= 2
    assert any(p.project_name == "Test Project" for p in projects)
    assert any(p.project_name == "Another Test Project" for p in projects)

def test_update_project(db, test_project):
    # Create update data
    project_data = ProjectUpdate(project_name="Updated Test Project")
    
    # Update project
    updated_project = crud.update_project(db, test_project.project_id, project_data)
    
    # Check project was updated correctly
    assert updated_project is not None
    assert updated_project.project_id == test_project.project_id
    assert updated_project.project_name == "Updated Test Project"

def test_delete_project(db, test_project):
    # Delete project
    result = crud.delete_project(db, test_project.project_id)
    
    # Check project was deleted correctly
    assert result is True
    
    # Check project no longer exists
    project = crud.get_project(db, test_project.project_id)
    assert project is None

# API Tests
def test_api_create_project(client):
    # Create test data
    project_data = {
        "project_name": "API Test Project"
    }
    
    # Send request
    response = client.post("/projects/", json=project_data)
    
    # Check response
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["project_name"] == "API Test Project"
    assert "project_id" in data
    assert "created_at" in data

def test_api_read_projects(client, test_project):
    # Send request
    response = client.get("/projects/")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(p["project_name"] == "Test Project" for p in data)

def test_api_read_project(client, test_project):
    # Send request
    response = client.get(f"/projects/{test_project.project_id}")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["project_id"] == test_project.project_id
    assert data["project_name"] == test_project.project_name

def test_api_update_project(client, test_project):
    # Create update data
    project_data = {
        "project_name": "Updated API Test Project"
    }
    
    # Send request
    response = client.put(f"/projects/{test_project.project_id}", json=project_data)
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["project_id"] == test_project.project_id
    assert data["project_name"] == "Updated API Test Project"

def test_api_delete_project(client, test_project):
    # Send request
    response = client.delete(f"/projects/{test_project.project_id}")
    
    # Check response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Check project no longer exists
    response = client.get(f"/projects/{test_project.project_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
