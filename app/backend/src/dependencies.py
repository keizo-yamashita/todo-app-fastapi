"""依存性注入の設定。

アプリケーションで使用する依存性を定義する。
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user.repository import UserRepository
from src.infrastructure.config.database import AsyncSessionLocal
from src.infrastructure.repository.user.user_repository_impl import UserRepositoryImpl


async def get_db_session() -> AsyncGenerator[AsyncSession]:
    """データベースセッションを取得する。

    FastAPIの依存性注入で使用するセッション提供関数。
    リクエスト成功時は自動的にコミットし、エラー発生時はロールバックする。

    Yields:
        AsyncSession: データベースセッション

    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_user_repository(
    session: AsyncSession,
) -> UserRepository:
    """ユーザーリポジトリの依存性を提供する。

    Args:
        session: データベースセッション

    Returns:
        SQLAlchemy実装のユーザーリポジトリ

    """
    return UserRepositoryImpl(session=session)
