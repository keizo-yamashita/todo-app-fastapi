"""ユーザーのロールを表現する値オブジェクト。

ユーザーの権限レベルを定義する。
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar


class RoleEnum(str, Enum):
    """ユーザーのロールを定義する列挙型。

    Attributes:
        SUPERADMIN: スーパー管理者
        ADMIN: 管理者
        MEMBER: 一般メンバー

    """

    SUPERADMIN = "superadmin"
    ADMIN = "admin"
    MEMBER = "member"


@dataclass(frozen=True, slots=True)
class Role:
    """ユーザーのロールを表現する値オブジェクト。

    ユーザーの権限レベルを定義し、デフォルトはMEMBERロール。
    """

    DEFAULT_ROLE: ClassVar[RoleEnum] = RoleEnum.MEMBER

    value: RoleEnum = field(default=DEFAULT_ROLE)

    def __post_init__(self) -> None:
        """ロールの型を検証する。

        Raises:
            TypeError: ロールがRoleEnum型でない場合

        """
        if not isinstance(self.value, RoleEnum):
            raise TypeError(
                f"invalid role type: {type(self.value)}, expected: RoleEnum",
            )
