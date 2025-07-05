# Backend Defect Management System

This is the backend for a comprehensive defect management system, built with FastAPI. It provides a robust API for managing projects, users, defects, vendors, and related data, making it suitable for industries like construction, manufacturing, and quality assurance.

## Features

- **Project Management**: CRUD operations for projects, including project image uploads.
- **User Management**: User registration, profile updates, and avatar management.
- **Role-Based Access Control**: Assign roles (e.g., admin, editor, viewer) to users on a per-project basis.
- **Defect Tracking**: Detailed defect records, including location, description, status tracking, and photo attachments.
- **Vendor Management**: Manage vendor information and assign them to specific defects.
- **Improvement & Confirmation Cycle**: Track improvement suggestions and their confirmation status.
- **File Uploads**: Handles image uploads for project visuals, user avatars, and defect photos.
- **Data Relationships**: Well-defined relationships between projects, users, defects, and vendors.
- **Statistical Analysis**: Endpoints to get statistics on defect distribution and status.

## Technologies Used

- **Backend**: Python, FastAPI
- **Database**: SQLAlchemy ORM (compatible with PostgreSQL, SQLite, etc.)
- **Testing**: Pytest
- **Containerization**: Docker, Docker Compose

## Project Structure

The project follows a modular structure, with each major feature area separated into its own directory under `app/`.

```
app/
├───base_map/         # Base map management
├───confirmation/     # Confirmation records for improvements
├───defect/           # Core defect tracking logic
├───defect_category/  # Defect categorization
├───defect_mark/      # Markings on defect photos/maps
├───improvement/      # Improvement suggestions
├───permission/       # User-project permissions
├───photo/            # Photo handling
├───project/          # Project management
├───user/             # User management
├───vendor/           # Vendor management
├───database.py       # Database session setup
├───main.py           # FastAPI application entrypoint
└───tests/            # Pytest test suite
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd backend_defect
    ```

2.  **Create and activate a virtual environment:**
    - On Windows:
      ```bash
      python -m venv venv
      .\venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the development server, use `uvicorn`:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`, and interactive API documentation (Swagger UI) can be accessed at `http://127.0.0.1:8000/docs`.

## Running Tests

The project uses `pytest` for testing. To run the entire test suite:

```bash
pytest
```

## Database

The database schema is defined using DBML in the `database.dbml` file. SQLAlchemy models corresponding to this schema are located in the `models.py` file within each feature module (e.g., `app/user/models.py`).
