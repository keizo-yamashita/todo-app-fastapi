"""データベース接続の設定。

SQLAlchemy 2.0を使用した非同期データベース接続を管理する。
"""

import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

# 環境変数からデータベースURLを取得
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@db:5432/template",
)

# SQLAlchemyのBaseクラスを作成
Base = declarative_base()

# 非同期エンジンの作成
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=False,  # SQLログを出力する場合はTrue
    future=True,
    pool_pre_ping=True,  # 接続の健全性チェック
    pool_size=5,  # コネクションプールのサイズ
    max_overflow=10,  # プールサイズを超えた際の最大接続数
)

# 非同期セッションファクトリーの作成
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    """データベースセッションを取得する。

    FastAPIの依存性注入で使用するセッション提供関数。

    Yields:
        AsyncSession: データベースセッション

    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """データベースの初期化。

    全てのテーブルを作成する。
    本番環境ではAlembicを使用するため、この関数は開発・テスト環境でのみ使用する。

    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """データベース接続を閉じる。

    アプリケーション終了時にコネクションプールを閉じる。

    """
    await engine.dispose()
