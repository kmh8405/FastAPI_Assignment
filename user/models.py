from datetime import datetime
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from database.orm import Base

class User(Base):
    __tablename__ = "user" # 참고: 실무에서는 보통 "users"처럼 복수형을 쓴다고 한다.

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    ) # 기본키 지정
    name: Mapped[str] = mapped_column(String(32)) # String(최대글자수)
    job: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(
        # 레코드가 생성된 시각이 DB에 의해서 자동 저장
        DateTime, server_default=func.now()
    )