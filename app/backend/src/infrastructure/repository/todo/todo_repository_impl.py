"""PostgreSQLを使用したTodoリポジトリの実装。

SQLAlchemy 2.0を使用してTodoの永続化を行う。
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import select

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.domain.todo.id import TodoId
    from src.domain.todo.todo import Todo

from src.domain.todo.repository import TodoRepository
from src.infrastructure.mapper.todo_mapper import TodoMapper
from src.infrastructure.models.todo_model import TodoModel
from src.shared.errors.codes import TodoErrorCode
from src.shared.errors.errors import ExpectedBusinessError


class TodoRepositoryImpl(TodoRepository):
    """PostgreSQLを使用したTodoリポジトリの実装。"""

    def __init__(self, session: AsyncSession) -> None:
        """リポジトリを初期化する。"""
        self.session = session

    async def search(self, query: str) -> list[Todo]:
        """タイトルでTodoを検索する。"""
        if query:
            stmt = select(TodoModel).where(TodoModel.title.ilike(f"%{query}%"))
        else:
            stmt = select(TodoModel)
        result = await self.session.execute(stmt)
        rows = result.scalars().all()
        return TodoMapper.to_domain_list(
            [
                {
                    "id": row.id,
                    "title": row.title,
                    "completed": row.completed,
                    "created_at": row.created_at,
                    "updated_at": row.updated_at,
                }
                for row in rows
            ]
        )

    async def find_by_id(self, todo_id: TodoId) -> Todo:
        """IDでTodoを検索する。"""
        stmt = select(TodoModel).where(TodoModel.id == todo_id.value)
        result = await self.session.execute(stmt)
        todo = result.scalar_one_or_none()

        if todo is None:
            raise ExpectedBusinessError(
                code=TodoErrorCode.NotFound,
                details={"todo_id": todo_id.value},
            )

        return TodoMapper.to_domain(
            {
                "id": todo.id,
                "title": todo.title,
                "completed": todo.completed,
                "created_at": todo.created_at,
                "updated_at": todo.updated_at,
            }
        )

    async def save(self, todo: Todo) -> Todo:
        """Todoを保存(更新)する。"""
        stmt = select(TodoModel).where(TodoModel.id == todo.id.value)
        result = await self.session.execute(stmt)
        todo_model = result.scalar_one_or_none()

        if todo_model is None:
            raise ExpectedBusinessError(
                code=TodoErrorCode.NotFound,
                details={"todo_id": todo.id.value},
            )

        db_data = TodoMapper.to_db(todo)
        todo_model.title = db_data["title"]
        todo_model.completed = db_data["completed"]
        todo_model.updated_at = db_data["updated_at"]

        await self.session.commit()
        await self.session.refresh(todo_model)

        return todo
