"""認証情報エンティティ。

ユーザーの認証に必要な情報を管理する。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.auth.password_hash import PasswordHash
    from src.domain.user.id import UserId


@dataclass(eq=False, slots=True)
class Credential:
    """認証情報エンティティ。

    ユーザーIDとパスワードハッシュを管理する。
    パスワードの検証機能は提供せず、純粋にデータを保持する。
    """

    user_id: UserId
    password_hash: PasswordHash
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __eq__(self, other: object) -> bool:
        """認証情報の同一性を比較する。

        Args:
            other: 比較対象

        Returns:
            同一の場合True

        """
        if self is other:
            return True
        if not isinstance(other, Credential):
            return NotImplemented
        return self.user_id == other.user_id

    def __hash__(self) -> int:
        """認証情報のハッシュ値を返す。

        Returns:
            ハッシュ値

        """
        return hash(self.user_id)
