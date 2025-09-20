from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from models import ArticleCreate, ArticleUpsertResponse, ArticleResponse
from database import (
    create_article,
    update_article_by_url,
    get_article_by_url,
    article_exists_by_url,
)

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Article DB API",
    description="記事データベースへの追加・更新を行うAPI",
    version="1.0.0",
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """ルートエンドポイント"""
    return {"message": "Article DB API is running"}


@app.post("/articles", response_model=ArticleUpsertResponse)
async def upsert_article(article: ArticleCreate):
    """
    記事を追加または更新する

    - 同じURLが存在する場合は更新
    - 存在しない場合は新規作成
    """
    try:
        # URLを文字列に変換
        url_str = str(article.url)

        # 記事データを辞書形式に変換
        article_data = {
            "title": article.title,
            "summary": article.summary,
            "keywords": article.keywords,
            "published_date": article.published_date,
            "url": url_str,
        }

        # 既存の記事をチェック
        if article_exists_by_url(url_str):
            # 更新処理
            success = update_article_by_url(url_str, article_data)
            if success:
                updated_article = get_article_by_url(url_str)
                return ArticleUpsertResponse(
                    success=True,
                    message="記事が正常に更新されました",
                    article_id=updated_article["id"],
                    is_update=True,
                    article=ArticleResponse(**updated_article),
                )
            else:
                raise HTTPException(
                    status_code=500, detail="記事の更新に失敗しました"
                )
        else:
            # 新規作成処理
            article_id = create_article(article_data)
            created_article = get_article_by_url(url_str)
            return ArticleUpsertResponse(
                success=True,
                message="記事が正常に作成されました",
                article_id=article_id,
                is_update=False,
                article=ArticleResponse(**created_article),
            )

    except Exception as e:
        logger.error(f"記事の処理中にエラーが発生しました: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"記事の処理中にエラーが発生しました: {str(e)}",
        )


@app.get("/articles/by-url")
async def get_article_by_url_endpoint(url: str):
    """URLで記事を取得する"""
    try:
        article = get_article_by_url(url)
        if article:
            return ArticleResponse(**article)
        else:
            raise HTTPException(
                status_code=404, detail="指定されたURLの記事が見つかりません"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"記事の取得中にエラーが発生しました: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"記事の取得中にエラーが発生しました: {str(e)}",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
