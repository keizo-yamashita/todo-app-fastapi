"""テスト用の共通設定。

SQLAlchemyを使用したデータベースのセットアップとクリーンアップを行う。
"""

import os
from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.infrastructure.config.database import Base

# anyioのバックエンドを設定
pytest_plugins = ("anyio",)


@pytest.fixture
def anyio_backend() -> str:
    """anyioのバックエンドをasyncioに固定する。

    anyioはデフォルトでasyncioとtrioの両方でテストを実行するが、
    SQLAlchemyのgreenletがtrioと互換性がないため、asyncioのみで実行する。

    Returns:
        str: 使用するバックエンド名('asyncio')

    """
    return "asyncio"


# テスト用のデータベースURL
TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost:5432/template",
)

# テスト用エンジンとセッションファクトリー
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,  # コネクションの健全性チェック
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession]:
    """テスト用のデータベースセッションを提供する。

    各テスト前にテーブルを再作成してクリーンな状態を保つ。
    リポジトリのcommit()/rollback()をそのまま使用できる一般的な実装パターン。

    Note:
        anyioは各テストごとに新しいイベントループを作成するため、
        コネクションプールを使いまわすとイベントループの不整合が発生します。
        そのため、各テスト前にengineを破棄し、テーブルを再作成します。

    Yields:
        AsyncSession: データベースセッション

    """
    # anyioの新しいイベントループに対応するため、コネクションプールをクリア
    await test_engine.dispose()

    # テーブルを再作成
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # セッションを作成して提供
    async with TestSessionLocal() as session:
        yield session
