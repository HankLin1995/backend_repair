# Test Plan

This document outlines the testing strategy and process for the Backend Defect Management System.

## 1. Testing Framework

The project uses `pytest` as the primary framework for writing and running tests. It is used for both unit and integration testing of the application's components.

## 2. Test Environment

Tests are executed in a controlled environment that mirrors the production setup as closely as possible. This includes:

- **Test Database**: A separate, in-memory SQLite database is used for testing to ensure that tests are isolated and do not affect the development or production databases.
- **Test Client**: FastAPI's `TestClient` is used to make requests to the API endpoints, simulating real-world client interactions.
- **Fixtures**: `pytest` fixtures are used extensively to provide a consistent and reusable setup for tests. This includes creating test data such as users, projects, defects, etc., which are required for many of the tests.

## 3. Test Coverage

The testing process is divided into two main categories for each module: **CRUD Tests** and **API Tests**.

### 3.1. CRUD Tests

These tests focus on the data access layer, specifically the `crud.py` file in each module. The goal is to ensure that the functions for creating, reading, updating, and deleting records in the database are working correctly.

For each model, the following operations are tested:

- **Create**: Verify that a new record can be created with valid data.
- **Read**: Verify that existing records can be retrieved, both individually and as a list. This also includes testing any filtering capabilities.
- **Update**: Verify that an existing record can be updated with new data.
- **Delete**: Verify that a record can be successfully deleted from the database.

### 3.2. API Tests

These tests focus on the API endpoints defined in the `routers.py` file of each module. The goal is to ensure that the API is functioning as expected, including request handling, data validation, and response generation.

For each endpoint, the following aspects are tested:

- **Successful Requests**: Verify that the endpoint returns the correct status code (e.g., `200 OK`, `201 Created`) and response body for valid requests.
- **Error Handling**: Verify that the endpoint returns the appropriate error status code (e.g., `404 Not Found`, `422 Unprocessable Entity`) for invalid or malformed requests.
- **Authentication and Authorization**: For endpoints that require it, verify that access is correctly restricted based on user roles and permissions.

### 3.3. Module-Specific Test Plans

- **User Management (`test_user*.py`)**:
    - CRUD tests for the `User` model.
    - API tests for user creation, retrieval, update, and deletion.
    - Tests for retrieving a user's associated projects.
    - Tests for avatar uploads and path management.
    - Validation tests for user data (e.g., email format, required fields).
    - Edge case tests for user updates (e.g., empty data, partial updates).

- **Project Management (`test_project.py`)**:
    - CRUD tests for the `Project` model.
    - API tests for project creation, retrieval, update, and deletion.
    - Tests for project image uploads.

- **Permission Management (`test_permission.py`)**:
    - CRUD tests for the `Permission` model.
    - API tests for creating, retrieving, updating, and deleting permissions.
    - Tests for retrieving permissions by project and by user.

- **Defect Management (`test_defect.py`)**:
    - CRUD tests for the `Defect` model.
    - API tests for defect creation, retrieval, update, and deletion.
    - Tests for filtering defects based on various criteria.
    - Tests for retrieving defect statistics.
    - Tests for status transitions and relationships with other models (e.g., improvements).

- **Defect Category Management (`test_defect_category.py`)**:
    - CRUD tests for the `DefectCategory` model.
    - API tests for category creation, retrieval, update, and deletion.
    - Tests for retrieving categories with defect counts.

- **Vendor Management (`test_vendor.py`)**:
    - CRUD tests for the `Vendor` model.
    - API tests for vendor creation, retrieval, update, and deletion.
    - Tests for retrieving vendors with defect counts.

- **Photo Management (`test_photo.py`)**:
    - CRUD tests for the `Photo` model.
    - API tests for photo retrieval, update, and deletion.
    - Tests for photo uploads and association with other models (e.g., defects).

- **Improvement and Confirmation (`test_improvement.py`, `test_confirmation.py`)**:
    - CRUD and API tests for the `Improvement` and `Confirmation` models.
    - Tests for the relationship between defects, improvements, and confirmations.

- **Base Map Management (`test_base_map.py`)**:
    - CRUD and API tests for the `BaseMap` model.
    - Tests for retrieving base maps with defect counts.

## 4. How to Run Tests

To run the entire test suite, execute the following command from the root directory of the project:

```bash
pytest
```

## TODOLIST

### Redundant Tests (To Be Removed or Consolidated)

- **`test_defect.py`**: 
    - `test_get_defect_with_marks_and_photos`: This test is deprecated and its functionality is covered by `test_get_defect_details`. It should be removed.
- **`test_permission.py`**: 
    - `test_api_create_permission_invalid_user`: This test is commented out and should be reviewed. If the logic is still relevant, it should be re-enabled; otherwise, it should be removed.
- **`test_photo.py`**: 
    - `test_create_photo` and `test_api_create_photo`: These tests are commented out and their functionality is likely covered by the file upload tests. They should be removed.
- **`test_project.py`**: 
    - `test_api_upload_project_image_crop_size`: This test is commented out and should be reviewed. If the cropping functionality is still desired, the test should be re-enabled; otherwise, it should be removed.
- **`test_user_project_relation.py`**: 
    - `test_permission_with_non_existent_user`: This test is commented out and should be reviewed and either re-enabled or removed.
- **User Test Files**: 
    - The user-related tests are split across multiple files (`test_user.py`, `test_user_avatar.py`, `test_user_project_relation.py`, `test_user_update_edge_cases.py`, `test_user_validation.py`). These should be consolidated into a single `test_user.py` file for better organization.

### Missing Tests (To Be Added)

- **Authentication and Authorization**:
    - While some tests implicitly handle authorization (e.g., `test_api_update_improvement_unauthorized`), there is no systematic testing of role-based access control. Tests should be added to verify that users with different roles (admin, editor, viewer) have the correct permissions for various actions.
- **Data Validation**:
    - More comprehensive data validation tests are needed. For example, testing the maximum length of string fields, valid ranges for numerical fields, and other constraints.
- **Concurrency and Race Conditions**:
    - There are no tests for handling concurrent requests or potential race conditions, which could be important in a multi-user environment.
- **Performance and Scalability**:
    - No performance or load tests are currently in place. While not always necessary for all projects, adding some basic performance benchmarks could be beneficial.
- **Defect Mark Module (`defect_mark`)**:
    - There are no tests for the `defect_mark` module. Tests for its CRUD operations and API endpoints should be created.