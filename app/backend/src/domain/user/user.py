"""ユーザーエンティティ。

ユーザーの基本情報とビジネスロジックを表現する。
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from src.domain.user.email_address import EmailAddress
from src.domain.user.id import UserId
from src.domain.user.name import UserName
from src.domain.user.role import Role


@dataclass(eq=False, slots=True)
class User:
    """ユーザーエンティティ。

    ユーザーの基本情報(メールアドレス、名前、ロール)を管理する。
    """

    email: EmailAddress
    name: UserName
    id: UserId = field(default_factory=lambda: UserId(value=str(uuid.uuid4())))
    role: Role = field(default_factory=lambda: Role())
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __eq__(self, other: object) -> bool:
        """ユーザーの同一性を比較する。"""
        if self is other:
            return True
        if not isinstance(other, User):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        """ユーザーのハッシュ値を返す。"""
        return hash(self.id)

    @staticmethod
    def random(
        role: Role | None = None,
        name: UserName | None = None,
    ) -> User:
        """テスト用のランダムなユーザーを生成する。

        Args:
            role: 指定するロール(Noneの場合はデフォルトロール)
            name: 指定するユーザー名(Noneの場合はランダムな名前)

        Returns:
            ランダムなユーザー

        """
        email = EmailAddress.random()
        return User(
            email=email,
            role=role or Role(),
            name=name or UserName(value="test_name"),
        )
