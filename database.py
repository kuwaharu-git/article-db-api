import mysql.connector
from mysql.connector import Error
from typing import Optional, Dict, Any
import os
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

# データベース接続設定
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "article_db"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "password"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "charset": "utf8mb4",
    "autocommit": True,
}


def get_db_connection():
    """データベース接続を取得する"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise


def create_article(article_data: Dict[str, Any]) -> int:
    """記事を作成する"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        query = """
        INSERT INTO articles (title, summary, keywords, published_date, url)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                article_data["title"],
                article_data["summary"],
                article_data["keywords"],
                article_data["published_date"],
                article_data["url"],
            ),
        )
        article_id = cursor.lastrowid
        return article_id
    except Error as e:
        print(f"Error creating article: {e}")
        raise
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def update_article_by_url(url: str, article_data: Dict[str, Any]) -> bool:
    """URLで記事を更新する"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        query = """
        UPDATE articles 
        SET title = %s, summary = %s, keywords = %s, published_date = %s
        WHERE url = %s
        """
        cursor.execute(
            query,
            (
                article_data["title"],
                article_data["summary"],
                article_data["keywords"],
                article_data["published_date"],
                url,
            ),
        )
        return cursor.rowcount > 0
    except Error as e:
        print(f"Error updating article: {e}")
        raise
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def get_article_by_url(url: str) -> Optional[Dict[str, Any]]:
    """URLで記事を取得する"""
    connection = get_db_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM articles WHERE url = %s"
        cursor.execute(query, (url,))
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"Error getting article: {e}")
        raise
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def article_exists_by_url(url: str) -> bool:
    """URLで記事が存在するかチェックする"""
    article = get_article_by_url(url)
    return article is not None
