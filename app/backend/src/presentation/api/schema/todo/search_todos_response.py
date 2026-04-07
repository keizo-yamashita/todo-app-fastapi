"""Todo検索レスポンスのスキーマ。"""

from pydantic import BaseModel

from src.presentation.api.schema.todo.todo import Todo


class SearchTodosResponse(BaseModel):
    """Todo検索レスポンスのスキーマ。"""

    todos: list[Todo]
