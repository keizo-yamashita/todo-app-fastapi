"""ユーザー名を表現する値オブジェクト。

1文字以上100文字以下の文字列を許可する。
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

# ユーザー名の長さ制限定数
MIN_USER_NAME_LENGTH = 1
MAX_USER_NAME_LENGTH = 100


@dataclass(frozen=True, slots=True)
class UserName:
    """ユーザー名を表現する値オブジェクト。

    ユーザー名の長さ制限(1-100文字)を検証する。
    """

    value: str

    def __post_init__(self) -> None:
        """ユーザー名の長さと有効性を検証する。

        Raises:
            ValueError: ユーザー名が1文字未満、100文字を超える、またはnull文字を含む場合

        """
        # null文字を含む場合はエラー
        if "\x00" in self.value:
            raise ValueError(f"user name contains null character, name: {self.value!r}")
        if len(self.value) < MIN_USER_NAME_LENGTH:
            raise ValueError(
                f"user name is less than {MIN_USER_NAME_LENGTH} character, name: {self.value}"
            )
        if len(self.value) > MAX_USER_NAME_LENGTH:
            raise ValueError(
                f"user name is more than {MAX_USER_NAME_LENGTH} characters, name: {self.value}",
            )

    @staticmethod
    def random() -> UserName:
        """テスト用のランダムなユーザー名を生成する。

        Returns:
            ランダムなユーザー名

        """
        return UserName(value=str(uuid.uuid4()))
