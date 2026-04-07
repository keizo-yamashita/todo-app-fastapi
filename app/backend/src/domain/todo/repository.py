"""Todoリポジトリのインターフェース。

Todoの永続化操作を定義する。
"""

from abc import ABC, abstractmethod

from src.domain.todo.id import TodoId
from src.domain.todo.todo import Todo


class TodoRepository(ABC):
    """Todoリポジトリのインターフェース。"""

    @abstractmethod
    async def find_by_id(self, todo_id: TodoId) -> Todo:
        """IDでTodoを検索する。

        Args:
            todo_id: 検索するTodoID

        Returns:
            見つかったTodo

        Raises:
            ExpectedBusinessError: Todoが見つからない場合

        """

    @abstractmethod
    async def save(self, todo: Todo) -> Todo:
        """Todoを保存(更新)する。

        Args:
            todo: 保存するTodo

        Returns:
            保存されたTodo

        """
