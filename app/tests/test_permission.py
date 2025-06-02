import pytest
from fastapi import status
from app.permission import crud
from app.permission.schemas import PermissionCreate, PermissionUpdate

# CRUD Tests
def test_create_permission(db, test_project, test_user):
    # Create test data
    permission_data = PermissionCreate(
        project_id=test_project.project_id,
        user_email=test_user.email,
        user_role="editor"
    )
    
    # Create permission
    permission = crud.create_permission(db, permission_data)
    
    # Check permission was created correctly
    assert permission.project_id == test_project.project_id
    assert permission.user_email == test_user.email
    assert permission.user_role == "editor"
    assert permission.permission_id is not None

def test_get_permission(db, test_permission):
    # Get permission
    permission = crud.get_permission(db, test_permission.permission_id)
    
    # Check permission was retrieved correctly
    assert permission is not None
    assert permission.permission_id == test_permission.permission_id
    assert permission.project_id == test_permission.project_id
    assert permission.user_email == test_permission.user_email
    assert permission.user_role == test_permission.user_role

def test_get_permissions(db, test_permission):
    # Create another permission with a new user
    from app.user.models import User
    new_user = User(
        name="Another Test User",
        line_id="another_line_id",
        email="another_test@example.com",
        company_name="Another Test Company"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    permission_data = PermissionCreate(
        project_id=test_permission.project_id,
        user_email=new_user.email,
        user_role="viewer"
    )
    crud.create_permission(db, permission_data)
    
    # Get permissions
    permissions = crud.get_permissions(db)
    
    # Check permissions were retrieved correctly
    assert len(permissions) == 2
    assert any(p.user_role == "admin" for p in permissions)
    assert any(p.user_role == "viewer" for p in permissions)

def test_get_permissions_by_project(db, test_permission):
    # Get permissions by project
    permissions = crud.get_permissions_by_project(db, test_permission.project_id)
    
    # Check permissions were retrieved correctly
    assert len(permissions) == 1
    assert permissions[0].permission_id == test_permission.permission_id
    assert permissions[0].project_id == test_permission.project_id
    assert permissions[0].user_email == test_permission.user_email
    assert permissions[0].user_role == test_permission.user_role

def test_get_permissions_by_user(db, test_permission):
    # Get permissions by user
    permissions = crud.get_permissions_by_user(db, test_permission.user_email)
    
    # Check permissions were retrieved correctly
    assert len(permissions) == 1
    assert permissions[0].permission_id == test_permission.permission_id
    assert permissions[0].project_id == test_permission.project_id
    assert permissions[0].user_email == test_permission.user_email
    assert permissions[0].user_role == test_permission.user_role

def test_update_permission(db, test_permission):
    # Create update data
    permission_data = PermissionUpdate(
        project_id=test_permission.project_id,
        user_email=test_permission.user_email,
        user_role="viewer"
    )
    
    # Update permission
    updated_permission = crud.update_permission(db, test_permission.permission_id, permission_data)
    
    # Check permission was updated correctly
    assert updated_permission is not None
    assert updated_permission.permission_id == test_permission.permission_id
    assert updated_permission.project_id == test_permission.project_id
    assert updated_permission.user_email == test_permission.user_email
    assert updated_permission.user_role == "viewer"

def test_delete_permission(db, test_permission):
    # Delete permission
    result = crud.delete_permission(db, test_permission.permission_id)
    
    # Check permission was deleted correctly
    assert result is True
    
    # Check permission no longer exists
    permission = crud.get_permission(db, test_permission.permission_id)
    assert permission is None

def test_get_permissions_with_details(db, test_permission, test_project, test_user):
    # Get permissions with details
    permissions_data = crud.get_permissions_with_details(db)
    
    # Check permissions data was retrieved correctly
    assert len(permissions_data) == 1
    permission_data = permissions_data[0]
    assert permission_data["permission_id"] == test_permission.permission_id
    assert permission_data["project_id"] == test_permission.project_id
    assert permission_data["user_email"] == test_permission.user_email
    assert permission_data["user_role"] == test_permission.user_role
    assert permission_data["project_name"] == test_project.project_name
    assert permission_data["user_name"] == test_user.name

# API Tests
def test_api_create_permission(client, test_project, test_user):
    # Create test data
    permission_data = {
        "project_id": test_project.project_id,
        "user_email": test_user.email,
        "user_role": "editor"
    }
    
    # Send request
    response = client.post("/permissions/", json=permission_data)
    
    # Check response
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["project_id"] == test_project.project_id
    assert data["user_email"] == test_user.email
    assert data["user_role"] == "editor"
    assert "permission_id" in data

def test_api_create_permission_invalid_project(client, test_user):
    # Create test data with invalid project ID
    permission_data = {
        "project_id": 999,  # Non-existent project ID
        "user_email": test_user.email,
        "user_role": "editor"
    }
    
    # Send request
    response = client.post("/permissions/", json=permission_data)
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

# def test_api_create_permission_invalid_user(client, test_project):
#     # Create test data with invalid user email
#     permission_data = {
#         "project_id": test_project.project_id,
#         "user_email": "nonexistent@example.com",  # Non-existent user email
#         "user_role": "editor"
#     }
    
#     # Send request
#     response = client.post("/permissions/", json=permission_data)
    
#     # Check response
#     assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_read_permissions(client, test_permission):
    # Send request
    response = client.get("/permissions/")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(p["permission_id"] == test_permission.permission_id for p in data)
    assert any(p["user_role"] == test_permission.user_role for p in data)
    assert any(p["user_email"] == test_permission.user_email for p in data)

def test_api_read_permissions_by_project(client, test_permission, test_project, test_user):
    # Send request
    response = client.get(f"/permissions/?project_id={test_project.project_id}")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["permission_id"] == test_permission.permission_id
    assert data[0]["project_id"] == test_project.project_id
    assert data[0]["user_email"] == test_permission.user_email
    assert data[0]["project_name"] == test_project.project_name
    assert data[0]["user_name"] == test_user.name

def test_api_read_permissions_by_user(client, test_permission, test_user):
    # Send request
    response = client.get(f"/permissions/?user_email={test_user.email}")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["permission_id"] == test_permission.permission_id
    assert data[0]["project_id"] == test_permission.project_id
    assert data[0]["user_email"] == test_user.email
    assert data[0]["user_role"] == test_permission.user_role

def test_api_read_permission(client, test_permission):
    # Send request
    response = client.get(f"/permissions/{test_permission.permission_id}")
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["permission_id"] == test_permission.permission_id
    assert data["project_id"] == test_permission.project_id
    assert data["user_email"] == test_permission.user_email
    assert data["user_role"] == test_permission.user_role

def test_api_read_permission_not_found(client):
    # Send request with non-existent ID
    response = client.get("/permissions/999")
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_update_permission(client, test_permission):
    # Create update data
    permission_data = {
        "user_email": test_permission.user_email,
        "project_id": test_permission.project_id,
        "user_role": "viewer"
    }
    
    # Send request
    response = client.put(f"/permissions/{test_permission.permission_id}", json=permission_data)
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["permission_id"] == test_permission.permission_id
    assert data["project_id"] == test_permission.project_id
    assert data["user_email"] == test_permission.user_email
    assert data["user_role"] == "viewer"

def test_api_update_permission_not_found(client):
    # Create update data
    permission_data = {
        "user_email": "test@example.com",
        "project_id": 1,
        "user_role": "viewer"
    }
    
    # Send request with non-existent ID
    response = client.put("/permissions/999", json=permission_data)
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_permission(client, test_permission):
    # Send request
    response = client.delete(f"/permissions/{test_permission.permission_id}")
    
    # Check response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Check permission no longer exists
    response = client.get(f"/permissions/{test_permission.permission_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_api_delete_permission_not_found(client):
    # Send request with non-existent ID
    response = client.delete("/permissions/999")
    
    # Check response
    assert response.status_code == status.HTTP_404_NOT_FOUND
