"""PostgreSQLを使用した認証情報リポジトリの実装。

SQLAlchemy 2.0を使用して認証情報の永続化を行う。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.auth.credential import Credential
from src.domain.auth.password_hash import PasswordHash
from src.domain.auth.repository import CredentialRepository
from src.domain.user.id import UserId
from src.infrastructure.models.credential_model import CredentialModel
from src.shared.errors.codes import AuthErrorCode
from src.shared.errors.errors import ExpectedBusinessError


class CredentialRepositoryImpl(CredentialRepository):
    """PostgreSQLを使用した認証情報リポジトリの実装。

    SQLAlchemy 2.0を使用して認証情報の永続化操作を行う。
    """

    def __init__(self, session: AsyncSession) -> None:
        """リポジトリを初期化する。

        Args:
            session: データベースセッション

        """
        self.session = session

    async def save(self, credential: Credential) -> Credential:
        """認証情報を保存する。

        Args:
            credential: 保存する認証情報

        Returns:
            保存された認証情報

        Raises:
            ExpectedBusinessError: 認証情報が既に存在する場合

        """
        try:
            credential_model = CredentialModel(
                user_id=credential.user_id.value,
                password_hash=credential.password_hash.value,
                created_at=credential.created_at,
                updated_at=credential.updated_at,
            )
            self.session.add(credential_model)
            await self.session.flush()
        except IntegrityError as e:
            # 一意制約違反の場合、ビジネスエラーに変換
            if "user_id" in str(e).lower():
                raise ExpectedBusinessError(
                    code=AuthErrorCode.CredentialAlreadyExists,
                    details={"user_id": credential.user_id.value},
                ) from e
            raise
        else:
            return credential

    async def find_by_user_id(self, user_id: UserId) -> Credential:
        """ユーザーIDで認証情報を検索する。

        Args:
            user_id: 検索するユーザーID

        Returns:
            見つかった認証情報

        Raises:
            ExpectedBusinessError: 認証情報が見つからない場合

        """
        stmt = select(CredentialModel).where(CredentialModel.user_id == user_id.value)
        result = await self.session.execute(stmt)
        credential_model = result.scalar_one_or_none()

        if credential_model is None:
            raise ExpectedBusinessError(
                code=AuthErrorCode.CredentialNotFound,
                details={"user_id": user_id.value},
            )

        return Credential(
            user_id=UserId(value=credential_model.user_id),
            password_hash=PasswordHash(value=credential_model.password_hash),
            created_at=credential_model.created_at,
            updated_at=credential_model.updated_at,
        )

    async def delete_by_user_id(self, user_id: UserId) -> None:
        """ユーザーIDで認証情報を削除する。

        Args:
            user_id: 削除するユーザーID

        Raises:
            ExpectedBusinessError: 認証情報が見つからない場合

        """
        # 存在確認
        await self.find_by_user_id(user_id)

        # 削除
        stmt = select(CredentialModel).where(CredentialModel.user_id == user_id.value)
        result = await self.session.execute(stmt)
        credential_model = result.scalar_one_or_none()

        if credential_model is not None:
            await self.session.delete(credential_model)
            await self.session.flush()
