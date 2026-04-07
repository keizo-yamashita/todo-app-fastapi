"""Todoリポジトリのインターフェース。

Todoの永続化操作を定義する。
"""

from abc import ABC, abstractmethod

from src.domain.todo.id import TodoId
from src.domain.todo.todo import Todo


class TodoRepository(ABC):
    """Todoリポジトリのインターフェース。"""

    @abstractmethod
    async def search(self, query: str) -> list[Todo]:
        """タイトルでTodoを検索する。"""

    @abstractmethod
    async def find_by_id(self, todo_id: TodoId) -> Todo:
        """IDでTodoを検索する。"""

    @abstractmethod
    async def save(self, todo: Todo) -> Todo:
        """Todoを保存(更新)する。"""
