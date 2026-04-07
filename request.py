# 요청 본문의 데이터 형식 관리
from pydantic import BaseModel, Field

# 사용자 추가할 때, 클라이언트가 서버로 보내는 데이터의 형식
class UserCreateRequest(BaseModel):
    # id는 제거. 자동 생성을 위해
    name: str = Field(..., min_length=2, max_length=10)
    job: str


request_body: UserCreateRequest = UserCreateRequest(name="david", job="teacher")