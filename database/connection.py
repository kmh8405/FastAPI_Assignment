# SQLAlchemy를 이용해서 DB와 연결하는 코드
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 데이터베이스 접속
DATABASE_URL = "sqlite:///./local.db" # `/./local.db` -> "현재 프로젝트 루트 기준으로 local.db 파일 생성"

# Engine: DB와 접속을 관리하는 객체
engine = create_engine(DATABASE_URL, echo=True) # echo=True는 엔진을 사용하는 동안 중간에 DB의 SQL문 실행로그들이 출력됨

# Session: 한 번의 DB 요청-응답
SessionFactory = sessionmaker(
    bind=engine,
    # 데이터를 어떻게 다룰지를 조정하는 옵션
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
