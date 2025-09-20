# Article DB API

FastAPIを使用した記事データベース管理APIです。記事の追加・更新機能を提供します。

## 機能

- 記事の追加
- 同じURLが存在する場合の記事更新
- URLでの記事取得

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -e .
```

### 2. データベース設定

MySQLデータベースを作成し、`db/init.sql`でテーブルを作成してください。

### 3. 環境変数

以下の環境変数を設定してください（オプション）：

```bash
export DB_HOST=localhost
export DB_NAME=article_db
export DB_USER=root
export DB_PASSWORD=password
export DB_PORT=3306
```

### 4. アプリケーションの起動

```bash
python main.py
```

または

```bash
uvicorn api:app --reload
```

## API エンドポイント

### POST /articles

記事を追加または更新します。

**リクエストボディ:**
```json
{
    "title": "記事のタイトル",
    "summary": "記事の要約（オプション）",
    "keywords": "キーワード（オプション）",
    "published_date": "2023-09-20",
    "url": "https://example.com/article"
}
```

**レスポンス:**
```json
{
    "success": true,
    "message": "記事が正常に作成されました",
    "article_id": 1,
    "is_update": false,
    "article": {
        "id": 1,
        "title": "記事のタイトル",
        "summary": "記事の要約",
        "keywords": "キーワード",
        "published_date": "2023-09-20",
        "url": "https://example.com/article"
    }
}
```

### GET /articles/by-url?url={url}

指定されたURLの記事を取得します。

**レスポンス:**
```json
{
    "id": 1,
    "title": "記事のタイトル",
    "summary": "記事の要約",
    "keywords": "キーワード",
    "published_date": "2023-09-20",
    "url": "https://example.com/article"
}
```

## プロジェクト構造

```
article-db-api/
├── main.py              # アプリケーションエントリーポイント
├── api.py               # FastAPI アプリケーション
├── models.py            # Pydantic モデル
├── database.py          # データベース操作
├── pyproject.toml       # プロジェクト設定
├── README.md            # このファイル
└── db/
    └── init.sql         # データベース初期化スクリプト
```
