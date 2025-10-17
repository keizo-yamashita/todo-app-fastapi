"""ユーザーマッパーの実装。

ドメインモデルとデータベースモデルの変換を行う。
"""

from __future__ import annotations

from typing import Any

from src.domain.user.email_address import EmailAddress
from src.domain.user.id import UserId
from src.domain.user.name import UserName
from src.domain.user.role import Role, RoleEnum
from src.domain.user.user import User


class UserMapper:
    """ユーザーのドメインモデルとデータベースモデルの変換を行うマッパー。"""

    @staticmethod
    def to_domain(record: dict[str, Any]) -> User:
        """データベースレコードをドメインモデルに変換する。

        Args:
            record: データベースレコード

        Returns:
            ドメインモデル

        """
        return User(
            id=UserId(value=record["id"]),
            email=EmailAddress(value=record["email"]),
            role=Role(value=RoleEnum(record["role"])),
            name=UserName(value=record["name"]),
            created_at=record["created_at"],
        )

    @staticmethod
    def to_db(entity: User) -> dict[str, Any]:
        """ドメインモデルをデータベース用辞書に変換する。

        Args:
            entity: ドメインモデル

        Returns:
            データベース用辞書

        """
        return {
            "id": entity.id.value,
            "email": entity.email.value,
            "role": entity.role.value.value,
            "name": entity.name.value,
            "created_at": entity.created_at,
        }

    @staticmethod
    def to_domain_list(records: list[dict[str, Any]]) -> list[User]:
        """データベースレコードリストをドメインモデルリストに変換する。

        Args:
            records: データベースレコードリスト

        Returns:
            ドメインモデルリスト

        """
        return [UserMapper.to_domain(record) for record in records]
