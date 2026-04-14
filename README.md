# FastAPI & Asyncio Practice

FastAPI를 활용한 백엔드 API 개발과 Python 비동기 프로그래밍(asyncio)을 함께 학습한 레포지토리

---

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

### Day 5 - Asynchronous Programming
- Introduction to asyncio and asynchronous programming
- Define coroutine functions using `async def`
- Understand that calling a coroutine returns a coroutine object (not executed immediately)
- Execute coroutines using `asyncio.run`
- Understand that `await` pauses execution and yields control to the event loop
- Run multiple coroutines concurrently with `asyncio.gather`
- Compare execution time between sync (`time.sleep`) and async (`asyncio.sleep`)
- Understand blocking vs non-blocking behavior
- Learn that `await` can only be used inside async functions and with awaitable objects

### Day 6 - Async FastAPI & Database Integration
- Refactor all API handlers to async (`async def`)
- Apply asynchronous SQLAlchemy (`create_async_engine`, `async_sessionmaker`)
- Use `await session.execute()` for non-blocking DB queries
- Integrate `aiosqlite` for async SQLite driver
- Maintain dependency injection with async session (`Depends`)
- Understand difference between sync and async DB execution
- Apply proper async transaction handling (`await commit`, `await refresh`)
- Handle blocking code using `run_in_threadpool`
- Control thread pool size using FastAPI lifespan and `anyio`
- Improve API performance by enabling non-blocking request handling

## Dependencies
- fastapi: Main web framework for building APIs
- uvicorn: ASGI server used to run FastAPI (also used internally by `fastapi dev`)
- pydantic: Data validation and schema management for request/response models
- sqlalchemy: ORM for database interaction
- aiosqlite: Async SQLite driver for SQLAlchemy
- greenlet: Required for SQLAlchemy async operations
- anyio: Async concurrency support (used in threadpool control)

## Database & Session Management
- Uses SQLAlchemy ORM with SQLite (`local.db`)
- Supports both synchronous and asynchronous DB sessions
- Async session is managed using FastAPI dependency injection (`Depends`)
- `get_async_session()` ensures session lifecycle (create → yield → close)
- CRUD operations are fully integrated with async DB handling

## Notes
- SQLite database (`local.db`) is automatically created when running the application.
- All APIs are fully migrated to async-based database handling
- Blocking operations are safely handled using threadpool (`run_in_threadpool`)
- Async architecture allows better scalability and performance under concurrent requests