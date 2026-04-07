"""Todoマッパーの実装。

ドメインモデルとデータベースモデルの変換を行う。
"""

from __future__ import annotations

from typing import Any

from src.domain.todo.id import TodoId
from src.domain.todo.todo import Todo


class TodoMapper:
    """Todoのドメインモデルとデータベースモデルの変換を行うマッパー。"""

    @staticmethod
    def to_domain(record: dict[str, Any]) -> Todo:
        """データベースレコードをドメインモデルに変換する。"""
        return Todo(
            id=TodoId(value=record["id"]),
            title=record["title"],
            completed=record["completed"],
            created_at=record["created_at"],
            updated_at=record["updated_at"],
        )

    @staticmethod
    def to_db(entity: Todo) -> dict[str, Any]:
        """ドメインモデルをデータベース用辞書に変換する。"""
        return {
            "id": entity.id.value,
            "title": entity.title,
            "completed": entity.completed,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }

    @staticmethod
    def to_domain_list(records: list[dict[str, Any]]) -> list[Todo]:
        """データベースレコードリストをドメインモデルリストに変換する。"""
        return [TodoMapper.to_domain(record) for record in records]
