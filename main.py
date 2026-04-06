# 결과 확인할 때는 `python 파일명`으로 터미널에 입력
from fastapi import FastAPI

app = FastAPI()

# @ -> Python 데코레이터 문법
# 데코레이터 : 파이썬 함수에 추가적인 기능을 부여하는 문법
@app.get("/") # GET / 요청이 들어오면, root_handler라는 함수를 실행하라
def root_handler():
    return {"ping": "pong"}

@app.get("/hello")
def hello_handler():
    return {"message": "Hello from FastAPI!"}

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

# 더미 데이터
users = [
        {"id": 1, "name": "alex", "job": "student"},
        {"id": 2, "name": "bob", "job": "sw engineer"},
        {"id": 3, "name": "chris", "job": "barista"},
    ]

@app.get("/users")
def get_users_handler():
    return users

# 아래 이 코드는 {user_id}보다 나중에 나오면 int 파싱 관련 에러?가 나온다.
# users/다음에 user_id같은 뭔가가 온다고 생각해서 int로 파싱할라는데
# search는 숫자가 아니므로 해당 오류에 걸리는 것
# 이러한 코드는 위에서부터 순서대로 진행되므로 제일 윗부분은 무조건 상위걸로,
# 그 다음부터는 하위로 이동하는 느낌에 {}로 변수처리로 관리하는 것은 제일 하단으로 배치
@app.get("/users/search")
def search_user_handler():
    return {"msg": "searching..."}

@app.get("/users/{user_id}")
def get_user_handler(user_id: int): # GET /users/1 에서 1은 사실 문자열 "1" 이기 때문에 타입 변환 필요
    for user in users:
        if user["id"] == user_id:
            return user
    # return None이 숨어있음 -> 데이터에 없는(예: id=4)걸 시도하면 null로 나옴
