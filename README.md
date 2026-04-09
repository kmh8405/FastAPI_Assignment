# FastAPI Practice

## Run
pip install -r requirements.txt

fastapi dev main.py

## Features

### Day 1
- Basic FastAPI application setup
- Define API endpoins using decorators (`@app.get`)
- Implement simple GET APIs (`/`. `/hello`)
- Handle static in-memory data (list of users)
- Implement REST-style endpoints for user retrieval
- Use Path Parameter (`/users/{user_id}`)
- Understand route matching order and its importance

### Day 2
- Get all users
- Get user by ID (Path Parameter)
- Search users (Query Parameter)
- Create user (POST)
- Data validation using Pydantic
- Response filtering using response_model

### Day 3
- Project structure refactoring (router, models, schemas separation)
- Database setup using SQLAlchemy
- User creation API connected to database
- Update/Delete APIs (currently using in-memory data, will be migrated to DB)
- HTTP status code handling (200, 201, 204, 404)
- Error handling using HTTPException

### Day 4
- Complete CRUD operations with SQLAlchemy
- Apply dependency injection using Depends for DB session management
- Refactor session handling (remove `with` pattern)
- Implement dynamic query building using SQLAlchemy (select, where chaining)
- Handle validation and errors with proper HTTP status codes (400, 404)
- Understand ORM behavior (no need for add() on update, delete vs expunge)


## Dependencies
- fastapi: Main web framework for building APIs
- uvicorn: ASGI server used to run FastAPI (also used internally by `fastapi dev`)
- pydantic: Data validation and schema management for request/response models
- sqlalchemy: ORM for database interaction

## Database & Session Management
- Uses SQLAlchemy ORM with SQLite (`local.db`)
- Database session is managed using FastAPI dependency injection (`Depends`)
- `get_session()` creates a session per request and ensures proper cleanup
- CRUD operations are fully integrated with the database

## Notes
- SQLite database (`local.db`) is automatically created when running the application.
- All APIs are now connected to the database (no longer using in-memory data)
- Dependency Injection (`Depends`) is used for managing DB sessions across all endpoints
