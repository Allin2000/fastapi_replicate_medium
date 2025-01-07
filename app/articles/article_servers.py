from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from app.sqlmodel.alembic_model import Article  # 导入你的 Article 模型
from app.sqlmodel.sql_service import DatabaseService  # 导入你的 DatabaseService
from app.articles.dto.aritcle_dto_model import CreateArticleDto, UpdateArticleDto, ArticleDTO # 导入 Pydantic 模型

class ArticlesService:
    def __init__(self, db: Session = Depends(DatabaseService.get_db)):
        self.db = db

    def create(self, article: CreateArticleDto) -> ArticleDTO:
        # 将 CreateArticleDto 转换为 SQLAlchemy Article
        db_article = Article(
            title=article.title,
            description=article.description,
            body=article.body,
            published=article.published
        )
        self.db.add(db_article)
        self.db.commit()
        self.db.refresh(db_article)
        
        # 直接返回 ArticleDTO
        return ArticleDTO(
            title=db_article.title,
            description=db_article.description,
            body=db_article.body,
            published=db_article.published
        )

    def find_all(self) -> List[ArticleDTO]:
        # 查找所有已发布的文章
        articles = self.db.query(Article).filter(Article.published == True).all()
        # 直接返回 ArticleDTO 列表
        return [
            ArticleDTO(
                title=article.title,
                description=article.description,
                body=article.body,
                published=article.published
            ) for article in articles
        ]

    def find_drafts(self) -> List[ArticleDTO]:
        # 查找所有草稿文章
        articles = self.db.query(Article).filter(Article.published == False).all()
        # 直接返回 ArticleDTO 列表
        return [
            ArticleDTO(
                title=article.title,
                description=article.description,
                body=article.body,
                published=article.published
            ) for article in articles
        ]

    def find_one(self, article_id: int) -> ArticleDTO:
        # 查找指定 ID 的文章
        db_article = self.db.query(Article).filter(Article.id == article_id).first()
        if not db_article:
            return None  # 如果没有找到文章
        # 直接返回 ArticleDTO
        return ArticleDTO(
            title=db_article.title,
            description=db_article.description,
            body=db_article.body,
            published=db_article.published
        )

    def update(self, article_id: int, article: UpdateArticleDto) -> ArticleDTO:
        # 更新指定 ID 的文章
        db_article = self.db.query(Article).filter(Article.id == article_id).first()
        if not db_article:
            return None  # 如果找不到文章
        
        # 根据 UpdateArticleDto 更新字段
        if article.title is not None:
            db_article.title = article.title
        if article.description is not None:
            db_article.description = article.description
        if article.body is not None:
            db_article.body = article.body
        if article.published is not None:
            db_article.published = article.published
        
        self.db.commit()
        self.db.refresh(db_article)
        
        # 直接返回更新后的 ArticleDTO
        return ArticleDTO(
            title=db_article.title,
            description=db_article.description,
            body=db_article.body,
            published=db_article.published
        )

    def remove(self, article_id: int) -> ArticleDTO:
        # 删除指定 ID 的文章
        db_article = self.db.query(Article).filter(Article.id == article_id).first()
        if db_article:
            self.db.delete(db_article)
            self.db.commit()
        
        # 返回删除后的空文章，或者 None
        if db_article:
            return ArticleDTO(
                title=db_article.title,
                description=db_article.description,
                body=db_article.body,
                published=db_article.published
            )
        return None
    

