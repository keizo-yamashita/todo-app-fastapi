"""TodoIDを表現する値オブジェクト。

UUID形式の文字列でTodoを一意に識別する。
"""

import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class TodoId:
    """TodoIDを表現する値オブジェクト。"""

    value: str = field(default_factory=lambda: str(uuid.uuid4()))
