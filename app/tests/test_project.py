import pytest
from fastapi import status
from datetime import datetime
from app.project import crud
from app.project.schemas import ProjectCreate, ProjectUpdate

# CRUD Tests
def test_create_project(db):
    # Create test data
    project_data = ProjectCreate(project_name="Test Project", image_path="static/project/custom.png")
    
    # Create project
    project = crud.create_project(db, project_data)
    
    # Check project was created correctly
    assert project.project_name == "Test Project"
    assert project.project_id is not None
    assert project.created_at is not None
    assert project.image_path == "static/project/custom.png"
    assert project.unique_code is not None
    assert len(project.unique_code) > 0

def test_get_project(db, test_project):
    # Get project
    project = crud.get_project(db, test_project.project_id)
    
    # Check project was retrieved correctly
    assert project is not None
    assert project.project_id == test_project.project_id
    assert project.project_name == test_project.project_name
    assert project.image_path == test_project.image_path
    assert project.unique_code == test_project.unique_code

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
    project_data = ProjectUpdate(project_name="Updated Test Project", image_path="static/project/updated.png")
    
    # Update project
    updated_project = crud.update_project(db, test_project.project_id, project_data)
    
    # Check project was updated correctly
    assert updated_project is not None
    assert updated_project.project_id == test_project.project_id
    assert updated_project.project_name == "Updated Test Project"
    assert updated_project.image_path == "static/project/updated.png"

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
        "project_name": "API Test Project",
        "image_path": "static/project/api.png"
    }
    
    # Send request
    response = client.post("/projects/", json=project_data)
    
    # Check response
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["project_name"] == "API Test Project"
    assert "project_id" in data
    assert "created_at" in data
    assert data["image_path"] == "static/project/api.png"
    assert "unique_code" in data
    assert len(data["unique_code"]) > 0

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
    assert data["image_path"] == test_project.image_path
    assert data["unique_code"] == test_project.unique_code

def test_api_update_project(client, test_project):
    # Create update data
    project_data = {
        "project_name": "Updated API Test Project",
        "image_path": "static/project/api_updated.png"
    }
    
    # Send request
    response = client.put(f"/projects/{test_project.project_id}", json=project_data)
    
    # Check response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["project_id"] == test_project.project_id
    assert data["project_name"] == "Updated API Test Project"
    assert data["image_path"] == "static/project/api_updated.png"

import io
from fastapi import status

def test_api_upload_project_image(client, test_project):
    # 建立一個有效的 PNG 圖片內容
    from PIL import Image
    import io
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    files = {"file": ("test.png", img_bytes, "image/png")}
    response = client.post(f"/projects/{test_project.project_id}/image", files=files)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["image_path"].startswith("static/project/project_")
    assert data["image_path"].endswith(".png")


# def test_api_upload_project_image_crop_size(client, test_project):
#     # 上傳一張圖片並指定裁切尺寸
#     from PIL import Image
#     import io, os
#     width, height = 256, 128
#     img = Image.new("RGB", (400, 400), color=(0, 255, 0))
#     img_bytes = io.BytesIO()
#     img.save(img_bytes, format="PNG")
#     img_bytes.seek(0)
#     files = {"file": ("test.png", img_bytes, "image/png")}
#     response = client.post(
#         f"/projects/{test_project.project_id}/image?width={width}&height={height}", files=files
#     )
#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     image_path = data["image_path"]
#     # 驗證圖片尺寸
#     with Image.open(image_path) as cropped_img:
#         assert cropped_img.size == (width, height)


def test_api_delete_project_also_remove_image(client, db):
    # 建立一個 project 並上傳圖片
    from PIL import Image
    import io, os
    from app.project import crud
    from app.project.schemas import ProjectCreate
    project = crud.create_project(db, ProjectCreate(project_name="del-img-test"))
    img = Image.new("RGB", (100, 100), color=(0, 0, 255))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    files = {"file": ("test.png", img_bytes, "image/png")}
    upload_resp = client.post(f"/projects/{project.project_id}/image", files=files)
    assert upload_resp.status_code == 200
    image_path = upload_resp.json()["image_path"]
    assert os.path.exists(image_path)
    # 刪除 project
    del_resp = client.delete(f"/projects/{project.project_id}")
    assert del_resp.status_code == status.HTTP_204_NO_CONTENT
    # 圖片檔案也應該被刪除
    assert not os.path.exists(image_path)

def test_api_delete_project(client, test_project):
    # Send request
    response = client.delete(f"/projects/{test_project.project_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    # Check project no longer exists
    get_response = client.get(f"/projects/{test_project.project_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
