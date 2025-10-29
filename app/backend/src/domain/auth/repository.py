"""認証情報リポジトリインターフェース。

認証情報の永続化を抽象化する。
"""

from abc import ABC, abstractmethod

from src.domain.auth.credential import Credential
from src.domain.user.id import UserId


class CredentialRepository(ABC):
    """認証情報リポジトリインターフェース。

    認証情報の保存・取得を定義する。
    """

    @abstractmethod
    async def save(self, credential: Credential) -> Credential:
        """認証情報を保存する。

        Args:
            credential: 保存する認証情報

        Returns:
            保存された認証情報

        Raises:
            ExpectedBusinessError: 認証情報が既に存在する場合
            ExpectedTechnicalError: DB接続エラーなどの技術的エラー

        """

    @abstractmethod
    async def find_by_user_id(self, user_id: UserId) -> Credential:
        """ユーザーIDで認証情報を検索する。

        Args:
            user_id: 検索するユーザーID

        Returns:
            見つかった認証情報

        Raises:
            ExpectedBusinessError: 認証情報が見つからない場合
            ExpectedTechnicalError: DB接続エラーなどの技術的エラー

        """

    @abstractmethod
    async def delete_by_user_id(self, user_id: UserId) -> None:
        """ユーザーIDで認証情報を削除する。

        Args:
            user_id: 削除するユーザーID

        Raises:
            ExpectedBusinessError: 認証情報が見つからない場合
            ExpectedTechnicalError: DB接続エラーなどの技術的エラー

        """
