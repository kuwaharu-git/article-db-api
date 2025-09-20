from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from datetime import date


class ArticleCreate(BaseModel):
    """記事作成用のリクエストモデル"""

    title: str = Field(..., max_length=255, description="記事のタイトル")
    summary: Optional[str] = Field(None, description="記事の要約")
    keywords: Optional[str] = Field(
        None, max_length=255, description="記事のキーワード"
    )
    published_date: Optional[date] = Field(None, description="記事の公開日")
    url: HttpUrl = Field(..., description="記事のURL")


class ArticleResponse(BaseModel):
    """記事レスポンス用のモデル"""

    id: int
    title: str
    summary: Optional[str]
    keywords: Optional[str]
    published_date: Optional[date]
    url: str

    class Config:
        from_attributes = True


class ArticleUpsertResponse(BaseModel):
    """記事の追加・更新レスポンス用のモデル"""

    success: bool
    message: str
    article_id: Optional[int] = None
    is_update: bool
    article: Optional[ArticleResponse] = None
