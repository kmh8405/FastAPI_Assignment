# FastAPI Practice

## Run
pip install -r requirements.txt

fastapi dev main.py

## Features (2일차 기준)
- Get all users
- Get user by ID (Path Parameter)
- Search users (Query Parameter)
- Create user (POST)
- Data validation using Pydantic
- Response filtering using response_model

## Dependencies
- fastapi: Main web framework for building APIs
- uvicorn: ASGI server used to run FastAPI (also used internally by `fastapi dev`)
- pydantic: Data validation and schema management for request/response models