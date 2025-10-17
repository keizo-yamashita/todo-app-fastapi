"""ユーザーIDを表現する値オブジェクト。

UUID形式の文字列でユーザーを一意に識別する。
"""

import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class UserId:
    """ユーザーIDを表現する値オブジェクト。

    UUID形式の文字列でユーザーを一意に識別する。
    """

    value: str = field(default_factory=lambda: str(uuid.uuid4()))
