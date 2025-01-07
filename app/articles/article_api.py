from fastapi import APIRouter,Depends,HTTPException
from typing import List
from app.articles.article_servers import ArticlesService
from app.sqlmodel.alembic_model import Article
from app.articles.dto.aritcle_dto_model import CreateArticleDto, UpdateArticleDto, ArticleDTO # 导入 Pydantic 模型


router = APIRouter()

# 实例化 ArticlesService
# articles_service = ArticlesService()


@router.post("/articles/", response_model=ArticleDTO)
def create_article(article: CreateArticleDto, articles_service: ArticlesService = Depends()):
    return articles_service.create(article=article)

@router.get("/articles/", response_model=List[ArticleDTO])
def get_articles(articles_service: ArticlesService = Depends()):
    return articles_service.find_all()

@router.get("/articles/drafts/", response_model=List[ArticleDTO])
def get_drafts(articles_service: ArticlesService = Depends()):
    return articles_service.find_drafts()

@router.get("/articles/{article_id}", response_model=ArticleDTO)
def get_article(article_id: int, articles_service: ArticlesService = Depends()):
    article = articles_service.find_one(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.put("/articles/{article_id}", response_model=ArticleDTO)
def update_article(article_id: int, article: UpdateArticleDto, articles_service: ArticlesService = Depends()):
    updated_article = articles_service.update(article_id, article)
    if not updated_article:
        raise HTTPException(status_code=404, detail="Article not found")
    return updated_article

@router.delete("/articles/{article_id}", response_model=ArticleDTO)
def delete_article(article_id: int, articles_service: ArticlesService = Depends()):
    article = articles_service.remove(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article