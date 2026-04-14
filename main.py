import anyio
from contextlib import asynccontextmanager
from starlette.concurrency import run_in_threadpool

from fastapi import FastAPI
from user.router import router

# 스레드풀 크기 조정
@asynccontextmanager
async def lifespan(_):
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 200
    yield



app = FastAPI(lifespan=lifespan)
app.include_router(router)


def aws_sync():
    # AWS 서버랑 통신(예: 2초)
    return


@app.get("/async")
async def async_handler():
    # 비동기 라이브러리를 지원하지 않는 경우가 존재
    # aws_sync() # time.sleep(2)
    # return {"msg": "ok"}

    # 동기 함수를 비동기 방식으로 실행할 수 있게 해 주는 유틸리티 함수
    await run_in_threadpool(aws_sync) # 여기서 양보(yield) 발생
    return {"msg": "ok"}

# @ -> Python 데코레이터 문법
# 데코레이터 : 파이썬 함수에 추가적인 기능을 부여하는 문법
# @app.get("/") # GET / 요청이 들어오면, root_handler라는 함수를 실행하라
# def root_handler():
#     return {"ping": "pong"}

# @app.get("/hello", status_code=status.HTTP_200_OK)
# def hello_handler():
#     return {"message": "Hello from FastAPI!"}

# REST API
# 전체 사용자 목록 조회 API (GET /users)
# @app.get("/users")
# def get_users_handler():
#     return [
#         {"id": 1, "name": "alex", "job": "student"},
#         {"id": 2, "name": "bob", "job": "sw engineer"},
#         {"id": 3, "name": "chris", "job": "barista"},
#     ]

# 단일 사용자 데이터 조회 API => id를 사용하면 됨
# 예시: GET /users/1 -> 1번 사용자 데이터 조회
# 이 규칙대로 만들어보면
# @app.get("/users/1")
# def get_user_one_handler():
#     return {"id": 1, "name": "alex", "job": "student"}

# 위 방식대로 하면 함수를 사용자 수만큼 계속 만들어야 하므로 비효율적이기 떄문에
# 다음과 같이 수정해줘야 함
# GET /users/{user_id} -> {user_id}번 사용자 조회

# # 더미 데이터
# users = [
#         {"id": 1, "name": "alex", "job": "student"},
#         {"id": 2, "name": "bob", "job": "sw engineer"},
#         {"id": 3, "name": "chris", "job": "barista"},
#     ]

# @app.get("/users", status_code=status.HTTP_200_OK)
# def get_users_handler():
#     return users

# 아래 이 코드는 {user_id}보다 나중에 나오면 int 파싱 관련 에러?가 나온다.
# users/다음에 user_id같은 뭔가가 온다고 생각해서 int로 파싱할라는데
# search는 숫자가 아니므로 해당 오류에 걸리는 것
# 이러한 코드는 위에서부터 순서대로 진행되므로 제일 윗부분은 무조건 상위걸로,
# 그 다음부터는 하위로 이동하는 느낌에 {}로 변수처리로 관리하는 것은 제일 하단으로 배치
# @app.get("/users/search")
# def search_user_handler():
#     return {"msg": "searching..."}

# @app.get("/users/{user_id}")
# def get_user_handler(user_id: int): # GET /users/1 에서 1은 사실 문자열 "1" 이기 때문에 타입 변환 필요
#     for user in users:
#         if user["id"] == user_id:
#             return user
#     # return None이 숨어있음 -> 데이터에 없는(예: id=4)걸 시도하면 null로 나옴

# ------------------------------------------------------

# GET /users/search?name=alex
# GET /users/search?job=student
# @app.get("/users/search")
# def search_user_handler(
#     name: str | None = Query(None),
#     job: str | None = Query(None),
# ):
#     # 예외의 경우:
#     # 1) name과 job 둘 다 안 보내는 경우
#     if name is None and job is None:
#         return {"msg": "조회에 사용할 QueryParam이 필요합니다."}
#     return {"name": name, "job": job}
    
    # 위 return 값에 대한 세부적인 조건 방식
    # for user in users:
    #     if name and job:
    #         if user["name"] == name and user["job"] == job:
    #             return user
    #         else:
    #             return None
    #     else:
    #         if user["name"] == name:
    #             return user
    #         if user["job"] == job:
    #             return user
    # http://127.0.0.1:8000/users/search?job=student 만 입력하면 에러가 뜨는데 이유는 name도 같이 명시해줘야 함
    # 둘 다 필수로 써야한다면 (name:str, job: str) 이렇게 둘 다 쓰면 되지만, 둘 중 하나만으로도 동작하게 하려면 선택적으로 해야 함
    # 둘 중 하나만으로도 한다면 name: str | None = Query(None) 이런식으로 하면 됨. (= None은 기본값 세팅)

    # name과 job 둘 다 써서 검색한다면 url에 이렇게 작성: http://127.0.0.1:8000/users/search?name=alex&job=student



# GET /users/{user_id} -> {user_id}번 사용자 데이터 조회
# @app.get("/users/{user_id}")
# def get_user_handler(
#     # ge: 이상(= Greater than or Equal to)
#     user_id: int = Path(..., ge=1), # user_id에 필수값 + 조건 설정
# ):
#     for user in users:
#         if user["id"] == user_id:
#             return user
    
#     # user_id=100처럼 사용자가 없는 경우 null로 써 있는 화면이 나옴
#     # 이때 상태코드는 200으로 작동하는데 지정을 안 해줬기 때문
#     # 데이터가 없는데 200으로 작동하면 안되기 때문에 404로 다뤄야 하며, 이를 해결하는 방법은 예외처리를 하는 것
#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND,
#         detail="User Not Found", # 상태에 대한 설명
#     )

# # 회원 추가 API
# # POST /users
# @app.post(
#         "/users", 
#         status_code=status.HTTP_201_CREATED, # 추가하는 것이기 때문에 201로 설정하는 것이 좋다. (조회의 경우 200이 일반적)
#         response_model=UserResponse # 아래 2번에서 실수로 민감 정보를 넣어도 이 UserResponse만 잘 작성되어있으면 문제 없음. 사용하는걸 권장.
# )
# def create_user_handler(
#     # 1) 사용자 데이터를 넘겨 받는다 -> 데이터 유효성 검사
#     body: UserCreateRequest
# ):
#     # 2) 사용자 데이터를 저장한다
#     new_user = {
#         "id": len(users) + 1, # 원래는 DB에서 할당해준다
#         "name": body.name,
#         "job": body.job,
#     }
#     users.append(new_user)

#     # 3) 응답을 반환한다
#     return new_user