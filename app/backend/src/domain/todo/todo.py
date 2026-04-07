"""Todoエンティティ。

Todoの基本情報とビジネスロジックを表現する。
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from src.domain.todo.id import TodoId


@dataclass(eq=False, slots=True)
class Todo:
    """Todoエンティティ。"""

    title: str
    id: TodoId = field(default_factory=lambda: TodoId(value=str(uuid.uuid4())))
    completed: bool = field(default=False)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def toggle(self) -> None:
        """completedフラグをトグルする。"""
        self.completed = not self.completed
        self.updated_at = datetime.now(UTC)

    def __eq__(self, other: object) -> bool:
        """Todoの同一性を比較する。"""
        if self is other:
            return True
        if not isinstance(other, Todo):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        """Todoのハッシュ値を返す。"""
        return hash(self.id)
