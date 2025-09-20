import uvicorn
from api import app


def main():
    """FastAPI アプリケーションを起動する"""
    print("Starting Article DB API...")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    main()
