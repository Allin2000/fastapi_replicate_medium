from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

# 配置数据库连接 URL
SQLALCHEMY_DATABASE_URI = "postgres://myuser:mypassword@localhost:5432/fastapi-median-db"

# 创建 SQLAlchemy 引擎
engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
)

# 创建会话类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 创建一个 DatabaseService 类，用于管理数据库会话
class DatabaseService:
    def __init__(self, db_session: sessionmaker = SessionLocal):
        """构造函数注入数据库会话工厂"""
        self.db_session = db_session

    def get_db(self) -> Generator[Session, None, None]:
        """生成数据库会话"""
        db = self.db_session()
        try:
            yield db
        finally:
            db.close()

    def get_session(self) -> sessionmaker:
        """返回数据库会话工厂"""
        return self.db_session

# database_service = DatabaseService()

# class Service_SQL:
#     @staticmethod
#     def get_db() -> Generator[Session, None, None]:
#         """生成数据库会话"""
#         db = SessionLocal()
#         try:
#             yield db
#         finally:
#             db.close()

#     @staticmethod
#     def get_session() -> sessionmaker:
#         """返回数据库会话工厂"""
#         return SessionLocal