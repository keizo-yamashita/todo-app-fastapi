"""メールアドレスを表現する値オブジェクト。

RFC 5322に準拠したメールアドレスの構文検証を行う。
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

from email_validator import validate_email


@dataclass(frozen=True, slots=True)
class EmailAddress:
    """メールアドレスを表現する値オブジェクト。

    メールアドレスの構文検証を行い、有効なメールアドレスのみを許可する。
    """

    value: str

    def __post_init__(self) -> None:
        """メールアドレスの構文検証を行う。

        Raises:
            ValueError: メールアドレスの構文が無効な場合

        """
        try:
            validate_email(self.value, check_deliverability=False)
        except Exception as e:
            raise ValueError(f"invalid email address, email: {self.value}") from e

    @staticmethod
    def random() -> EmailAddress:
        """テスト用のランダムなメールアドレスを生成する。

        Returns:
            ランダムなメールアドレス

        """
        return EmailAddress(f"test{uuid.uuid4()}@galirage.com")
