from fastapi import APIRouter, Path, Query, status, HTTPException
from database.connection import SessionFactory
from user.models import User
from user.request import UserCreateRequest, UserUpdateRequest
from user.response import UserResponse

# user 핸들러 함수들을 관리하는 객체
router = APIRouter(tags=["User"]) # @app을 @router로 변경

# 임시 데이터베이스
users = [
    {"id": 1, "name": "alex", "job": "student"},
    {"id": 2, "name": "bob", "job": "sw engineer"},
    {"id": 3, "name": "chris", "job": "barista"},
]

# 전체 사용자 목록 조회 API
# GET /users
@router.get("/users", status_code=status.HTTP_200_OK)
def get_users_handler():
    return users

@router.get("/users/search")
def search_user_handler(
    name: str | None = Query(None),
    job: str | None = Query(None),
):
    # 예외의 경우:
    # 1) name과 job 둘 다 안 보내는 경우
    if name is None and job is None:
        return {"msg": "조회에 사용할 QueryParam이 필요합니다."}
    return {"name": name, "job": job}


@router.get("/users/{user_id}")
def get_user_handler(
    # ge: 이상(= Greater than or Equal to)
    user_id: int = Path(..., ge=1), # user_id에 필수값 + 조건 설정
):
    for user in users:
        if user["id"] == user_id:
            return user
    
    # user_id=100처럼 사용자가 없는 경우 null로 써 있는 화면이 나옴
    # 이때 상태코드는 200으로 작동하는데 지정을 안 해줬기 때문
    # 데이터가 없는데 200으로 작동하면 안되기 때문에 404로 다뤄야 하며, 이를 해결하는 방법은 예외처리를 하는 것
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User Not Found", # 상태에 대한 설명
    )

# 회원 추가 API
# POST /users
@router.post(
    "/users", 
    status_code=status.HTTP_201_CREATED, # 추가하는 것이기 때문에 201로 설정하는 것이 좋다. (조회의 경우 200이 일반적)
    response_model=UserResponse # 아래 2번에서 실수로 민감 정보를 넣어도 이 UserResponse만 잘 작성되어있으면 문제 없음. 사용하는걸 권장.
)
def create_user_handler(
    body: UserCreateRequest
):
    # context manager를 벗어나는 순간 자동으로 close() 호출
    with SessionFactory() as session:
         # new_user = {"id": len(users) + 1, "name": body.name, "job": body.job}
        new_user = User(name=body.name, job=body.job)
        session.add(new_user)
        session.commit() # 변경사항 저장
        session.refresh(new_user) # id, created_at 읽어옴
        return new_user

# 회원 정보 수정 API
# PATCH /users/{user_id}
@router.patch(
    "/users/{user_id}",
    response_model=UserResponse,
)
def update_user_handler(
    # 1) 입력값 정의
    user_id: int,
    body: UserUpdateRequest,
):
    # 2) 실제 함수 동작 처리
    # user_id로 사용자를 조회
    for user in users:
        if user["id"] == user_id:
            # 데이터 수정
            user["job"] = body.job
            # 3) 반환
            return user # 반환 처리는 여기서 해야한다
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User Not Found",
    )

# 회원 삭제 API
# DELETE /users/{user_id}
@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_handler(user_id: int):
    for user in users:
        if user["id"] == user_id:
            users.remove(user)
            return {"msg": "user deleted..."}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User Not Found",
    )
