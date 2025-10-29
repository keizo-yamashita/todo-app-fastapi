"""パスワードハッシュ値オブジェクト。

ハッシュ化されたパスワードを表現する。
"""

from __future__ import annotations

from dataclasses import dataclass

MIN_PASSWORD_HASH_LENGTH = 10

@dataclass(frozen=True, slots=True)
class PasswordHash:
    """パスワードハッシュ値オブジェクト。

    bcryptでハッシュ化されたパスワードを保持する。
    """

    value: str

    def __post_init__(self) -> None:
        """バリデーションを実行する。

        Raises:
            ValueError: ハッシュ値が空の場合

        """
        if not self.value:
            raise ValueError("password hash is empty")
        if len(self.value) < MIN_PASSWORD_HASH_LENGTH:
            raise ValueError(f"password hash is too short, hash: {self.value}")
