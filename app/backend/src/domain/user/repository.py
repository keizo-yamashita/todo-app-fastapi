"""ユーザーリポジトリのインターフェース。

ユーザーの永続化操作を定義する。
"""

from abc import ABC, abstractmethod

from src.domain.user.email_address import EmailAddress
from src.domain.user.id import UserId
from src.domain.user.user import User


class UserRepository(ABC):
    """ユーザーリポジトリのインターフェース。

    ユーザーの永続化操作(CRUD)を定義する。
    """

    @abstractmethod
    async def filter(self) -> list[User]:
        """すべてのユーザーを取得する。

        Returns:
            ユーザーのリスト

        """

    @abstractmethod
    async def find_by_id(self, user_id: UserId) -> User:
        """IDでユーザーを検索する。

        Args:
            user_id: 検索するユーザーID

        Returns:
            見つかったユーザー

        Raises:
            ExpectedBusinessError: ユーザーが見つからない場合

        """

    @abstractmethod
    async def find_by_email(self, email: EmailAddress) -> User:
        """メールアドレスでユーザーを検索する。

        Args:
            email: 検索するメールアドレス

        Returns:
            見つかったユーザー

        Raises:
            ExpectedBusinessError: ユーザーが見つからない場合

        """

    @abstractmethod
    async def save(self, user: User) -> User:
        """ユーザーを保存する。

        Args:
            user: 保存するユーザー

        Returns:
            保存されたユーザー

        Raises:
            ExpectedBusinessError: メールアドレスが重複している場合

        """

    @abstractmethod
    async def delete(self, user_id: UserId) -> UserId:
        """ユーザーを削除する。

        Args:
            user_id: 削除するユーザーID

        Returns:
            削除されたユーザーID

        Raises:
            ExpectedBusinessError: ユーザーが見つからない場合

        """
