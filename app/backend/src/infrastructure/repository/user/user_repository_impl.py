"""PostgreSQLを使用したユーザーリポジトリの実装。

SQLAlchemy 2.0を使用してユーザーの永続化を行う。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.domain.user.email_address import EmailAddress
    from src.domain.user.user import User

from src.domain.user.id import UserId
from src.domain.user.repository import UserRepository
from src.infrastructure.mapper.user_mapper import UserMapper
from src.infrastructure.models.user_model import UserModel
from src.shared.errors.codes import TechnicalErrorCode, UserErrorCode
from src.shared.errors.errors import ExpectedBusinessError, ExpectedTechnicalError


class UserRepositoryImpl(UserRepository):
    """PostgreSQLを使用したユーザーリポジトリの実装。

    SQLAlchemy 2.0を使用してユーザーの永続化操作を行う。
    """

    def __init__(self, session: AsyncSession) -> None:
        """リポジトリを初期化する。

        Args:
            session: データベースセッション

        """
        self.session = session

    async def filter(self) -> list[User]:
        """すべてのユーザーを取得する。

        Returns:
            ユーザーのリスト

        """
        # SQLAlchemy 2.0の型安全なクエリ
        stmt = select(UserModel)
        result = await self.session.execute(stmt)
        users = result.scalars().all()

        # UserModelをdict形式に変換してMapperに渡す
        return UserMapper.to_domain_list(
            [
                {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "role": user.role,
                    "created_at": user.created_at,
                }
                for user in users
            ]
        )

    async def find_by_id(self, user_id: UserId) -> User:
        """IDでユーザーを検索する。

        Args:
            user_id: 検索するユーザーID

        Returns:
            見つかったユーザー

        Raises:
            ExpectedBusinessError: ユーザーが見つからない場合

        """
        stmt = select(UserModel).where(UserModel.id == user_id.value)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            raise ExpectedBusinessError(
                code=UserErrorCode.NotFound,
                details={"user_id": user_id.value},
            )

        return UserMapper.to_domain(
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "created_at": user.created_at,
            }
        )

    async def find_by_email(self, email: EmailAddress) -> User:
        """メールアドレスでユーザーを検索する。

        Args:
            email: 検索するメールアドレス

        Returns:
            見つかったユーザー

        Raises:
            ExpectedBusinessError: ユーザーが見つからない場合

        """
        stmt = select(UserModel).where(UserModel.email == email.value)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            raise ExpectedBusinessError(
                code=UserErrorCode.NotFound,
                details={"email": email.value},
            )

        return UserMapper.to_domain(
            {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "created_at": user.created_at,
            }
        )

    async def save(self, user: User) -> User:
        """ユーザーを保存する。

        Args:
            user: 保存するユーザー

        Returns:
            保存されたユーザー

        Raises:
            ExpectedBusinessError: メールアドレスが重複している場合
            ExpectedTechnicalError: データベース操作に失敗した場合

        """
        try:
            db_data = UserMapper.to_db(user)
            user_model = UserModel(
                id=db_data["id"],
                email=db_data["email"],
                role=db_data["role"],
                name=db_data["name"],
                created_at=db_data["created_at"],
            )
            self.session.add(user_model)
            await self.session.commit()
            await self.session.refresh(user_model)
        except IntegrityError as e:
            await self.session.rollback()
            # メールアドレスの一意制約違反をチェック
            if "email" in str(e).lower() or "unique" in str(e).lower():
                raise ExpectedBusinessError(
                    code=UserErrorCode.EmailAlreadyExists,
                    details={"email": user.email.value},
                ) from e
            raise ExpectedTechnicalError(
                code=TechnicalErrorCode.DatabaseOperationFailed,
                details={"message": str(e)},
            ) from e
        except Exception as e:
            await self.session.rollback()
            raise ExpectedTechnicalError(
                code=TechnicalErrorCode.DatabaseOperationFailed,
                details={"message": str(e)},
            ) from e

        return user

    async def delete(self, user_id: UserId) -> UserId:
        """ユーザーを削除する。

        Args:
            user_id: 削除するユーザーID

        Returns:
            削除されたユーザーID

        Raises:
            ExpectedBusinessError: ユーザーが見つからない場合

        """
        stmt = select(UserModel).where(UserModel.id == user_id.value)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            raise ExpectedBusinessError(
                code=UserErrorCode.NotFound,
                details={"user_id": user_id.value},
            )

        await self.session.delete(user)
        await self.session.commit()

        return UserId(value=user_id.value)
