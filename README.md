# FastAPI Practice

## Run
pip install -r requirements.txt

fastapi dev main.py

## Features

### Day 2
- Get all users
- Get user by ID (Path Parameter)
- Search users (Query Parameter)
- Create user (POST)
- Data validation using Pydantic
- Response filtering using response_model

### Day 3 (In Progress)
- Project structure refactoring (router, models, schemas separation)
- Database setup using SQLAlchemy
- User creation API connected to database
- Update/Delete APIs (currently using in-memory data, will be migrated to DB)
- HTTP status code handling (200, 201, 204, 404)
- Error handling using HTTPException

## Dependencies
- fastapi: Main web framework for building APIs
- uvicorn: ASGI server used to run FastAPI (also used internally by `fastapi dev`)
- pydantic: Data validation and schema management for request/response models
- sqlalchemy: ORM for database interaction

## Notes
- SQLite database (`local.db`) is automatically created when running the application.
- Currently, only the user creation API is connected to the database.
- Other APIs are still using in-memory data and will be refactored to use the database.
