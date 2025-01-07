from pydantic import BaseModel
from typing import Optional
from pydantic.networks import EmailStr
from app.sqlmodel.alembic_model import Article  # 导入 Article 模型以便用作关联

class ArticleDTO(BaseModel):
    title: str
    description: Optional[str] = None
    body: str
    published: bool = False


class CreateArticleDto(BaseModel):
    title: str
    description: Optional[str] = None  # description 可选
    body: str
    published: Optional[bool] = False  # 默认值为 False

    class Config:
        orm_mode = True  # 使 Pydantic 模型支持 ORM 实例


class UpdateArticleDto(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None
    published: Optional[bool] = None

    class Config:
        orm_mode = True