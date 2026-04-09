from fastapi import APIRouter, Path, Query, status, HTTPException, Depends
from sqlalchemy import select, delete
from database.connection import get_session
from user.models import User
from user.request import UserCreateRequest, UserUpdateRequest
from user.response import UserResponse

# user 핸들러 함수들을 관리하는 객체
router = APIRouter(tags=["User"]) # @app을 @router로 변경

# 임시 데이터베이스 -> 모든 API DB 연동 완료로 인한 주석처리 (더 이상 필요없음)
# users = [
#     {"id": 1, "name": "alex", "job": "student"},
#     {"id": 2, "name": "bob", "job": "sw engineer"},
#     {"id": 3, "name": "chris", "job": "barista"},
# ]


@router.get(
    "/users",
    summary="전체 사용자 목록 조회 API",
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponse],
)
def get_users_handler(
    # Depends: FastAPI에서 의존성(get_session)을 자동으로 실행/주입/정리
    session = Depends(get_session),
):
    # stmt = statement = 구문(명령문)
    stmt = select(User) # SELECT * FROM user
    result = session.execute(stmt)
    users = result.scalars().all() # [user1, user2, user3, ...]
    return users

@router.get(
    "/users/search",
    summary="사용자 정보 검색 API",
    response_model=list[UserResponse], # name과 job은 중복이 발생할 수 있는 데이터이므로 list로 반환해야 함
)
def search_user_handler(
    name: str | None = Query(None),
    job: str | None = Query(None),
    session = Depends(get_session),
):
    if not name and not job:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="검색 조건이 없습니다."
        )
    
    # 1) name O / job X
    # 2) name X / job O
    # 3) name X / job X
    # 4) name O / job O
    # 위와 같은 경우의 수를 다루는데 조건문(if/elif/else)은 비효율적이기 때문에 "체이닝"이라는 기법을 사용한다

    stmt = select(User)

    if name:
        stmt = stmt.where(User.name == name)
        # stmt = select(User).where(User.name == name)

    if job:
        stmt = stmt.where(User.job == job)

        # 이때 statement 문구는 두 가지 경우로 나뉨

        # 1) name을 거쳐온 경우
        # stmt = select(User).where(User.name == name).where(User.job == job)

        # 2) name을 거치지 않은 경우
        # stmt = select(User).where(User.job == job)

    result = session.execute(stmt)
    users = result.scalars().all()
    return users


@router.get(
    "/users/{user_id}",
    summary="단일 사용자 데이터 조회 API", # 주석으로 설명했던 걸 summary에 넣어 표현 가능
    response_model=UserResponse,
)
def get_user_handler(
    user_id: int = Path(..., ge=1),
    session = Depends(get_session),
):
    # 예) SELECT * FROM user WHERE id = 10;
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user = result.scalar() # 존재하면 user 객체, 존재하지 않으면 None

    # scalars() -> 첫 번째 열의 첫 번째 데이터만 가져온다
    # all() -> 리스트로 변환한다

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
        )
    return user


@router.post(
    "/users", 
    summary="회원 추가 API",
    status_code=status.HTTP_201_CREATED, # 추가하는 것이기 때문에 201로 설정하는 것이 좋다. (조회의 경우 200이 일반적)
    response_model=UserResponse # 아래 2번에서 실수로 민감 정보를 넣어도 이 UserResponse만 잘 작성되어있으면 문제 없음. 사용하는걸 권장.
)
def create_user_handler(
    body: UserCreateRequest,
    session = Depends(get_session),
):
    # new_user = {"id": len(users) + 1, "name": body.name, "job": body.job}
    new_user = User(name=body.name, job=body.job)
    session.add(new_user)
    session.commit() # 변경사항 저장
    session.refresh(new_user) # id, created_at 읽어옴
    return new_user


@router.patch(
    "/users/{user_id}",
    summary="회원 정보 수정 API",
    response_model=UserResponse,
)
def update_user_handler(
    user_id: int,
    body: UserUpdateRequest,
    session = Depends(get_session),
):
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user = result.scalar()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
        )

    user.job = body.job
    # 여기서 session.add()는 필요 없음 -> 위 result.scalar()에서 SQLAlchemy가 이미 user객체를 기억하고 있기 때문
    session.commit() # 현재 user 상태(job 변경)를 DB 반영
    # e.g. UPDATE user SET job = '  ' WHERE user.id = 1;
    return user


@router.delete(
    "/users/{user_id}",
    summary="회원 삭제 API",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user_handler(
    user_id: int,
    session = Depends(get_session),
):
    # # 1) get + delete 방법 -> user를 먼저 조회해서 있으면 제거, 없으면 에러 반환
    # with SessionFactory() as session:
    #     stmt = select(User).where(User.id == user_id)
    #     result = session.execute(stmt)
    #     user = result.scalar()

    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail="User Not Found",
    #         )

    #     session.delete(user) # 객체를 삭제
    #     # session.expunge(user) -> 세션의 추적 대상에서 제거
    #     session.commit()

    # # 2) 바로 delete 하는 방법 -> 그냥 삭제 쿼리문 날리기 (있으면 제거, 없으면 무시됨)
    # with SessionFactory() as session:
    #     stmt = delete(User).where(User.id == user_id)
    #     session.execute(stmt)
    #     session.commit()

    # ---------------------------------

    # Depends 사용
    # 1) get + delete 방법 -> user를 먼저 조회해서 있으면 제거, 없으면 에러 반환
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user = result.scalar()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
        )

    session.delete(user)
    session.commit()

    # 2) 바로 delete 하는 방법 -> 그냥 삭제 쿼리문 날리기 (있으면 제거, 없으면 무시됨)
    # stmt = delete(User).where(User.id == user_id)
    # session.execute(stmt)
    # session.commit()

